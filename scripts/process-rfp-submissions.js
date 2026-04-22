#!/usr/bin/env node
/**
 * Process Millar RFP submissions from Jessica Allen
 * Workflow:
 * 1. Check for new emails from Jessica with RFP responses
 * 2. Extract MSP name from subject (detect "continued" markers)
 * 3. Download attachments
 * 4. Link continuation files to main submission
 * 5. Track all submissions by MSP company
 */

const { AgentMailClient } = require('agentmail');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const API_KEY = 'am_us_14a4a7ccfbff5ed90374fb30577bdb7562cba20cd12f958fed2b68a43e0b6e52';
const INBOX_ID = 'stevieai@agentmail.to';
const OUTPUT_DIR = '/home/rwhitaker/.openclaw/workspace/msp-rfps';
const TRACKING_FILE = '/home/rwhitaker/.openclaw/workspace/msp-rfps/submissions-tracked.json';
const MSP_FILE = '/home/rwhitaker/.openclaw/workspace/msp-rfps/msp-companies.json';

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// Initialize or load tracking file
let trackedSubmissions = {};
if (fs.existsSync(TRACKING_FILE)) {
    trackedSubmissions = JSON.parse(fs.readFileSync(TRACKING_FILE, 'utf8'));
}

// Track MSP companies by name for continuation linking
let mspCompanies = {};
if (fs.existsSync(MSP_FILE)) {
    mspCompanies = JSON.parse(fs.readFileSync(MSP_FILE, 'utf8'));
}

function saveTracking() {
    fs.writeFileSync(TRACKING_FILE, JSON.stringify(trackedSubmissions, null, 2));
}

function saveMSPCompanies() {
    fs.writeFileSync(MSP_FILE, JSON.stringify(mspCompanies, null, 2));
}

function downloadFile(url, outputPath) {
    return new Promise((resolve, reject) => {
        try {
            execSync(`curl -s -L "${url}" -o "${outputPath}"`, {
                stdio: 'pipe',
                maxBuffer: 10 * 1024 * 1024 // 10MB
            });
            resolve();
        } catch (err) {
            reject(err);
        }
    });
}

function extractMSPInfo(subject) {
    // Try to extract company name from subject
    // Subject format: "[Company Name] - Millar MSP Proposal Submission"
    // Also handle continuation files marked with "continued"
    
    // First, get the company name before the hyphen
    const companyMatch = subject.match(/^([^\-]+)\s*-/);
    let companyName = 'Unknown_MSP';
    
    if (companyMatch) {
        companyName = companyMatch[1].trim();
    }
    
    // Clean up common prefixes
    companyName = companyName
        .replace(/^(FW|Fwd|RE):\s*/i, '')
        .trim();

    // Check if this is a continuation file
    const isContinuation = /continued|continuation|supplemental/i.test(subject);
    
    // If still has content, use it
    if (companyName.length > 2) {
        return {
            name: companyName.substring(0, 50),
            isContinuation: isContinuation,
            cleanName: companyName.replace(/[^a-zA-Z0-9]/g, '_').substring(0, 50)
        };
    }

    // Fallback
    return {
        name: 'Unknown_MSP',
        isContinuation: false,
        cleanName: 'Unknown_MSP'
    };
}

async function checkForSubmissions() {
    const client = new AgentMailClient({ apiKey: API_KEY });

    try {
        const result = await client.inboxes.messages.list(INBOX_ID);

        // Filter for emails from Jessica about RFP submissions
        const submissionEmails = result.messages.filter(m =>
            m.from.includes('jessica.allen@cybersecgru.com') &&
            !m.labels.includes('sent') &&
            m.subject && m.subject.match(/RFP|response|submission/i)
        );

        console.log(`\n=== RFP Submission Checker ===`);
        console.log(`Total messages from Jessica: ${submissionEmails.length}`);
        console.log(`Already tracked: ${Object.keys(trackedSubmissions).length}\n`);

        for (const email of submissionEmails) {
            const msgId = email.messageId;
            
            // Skip if already processed
            if (trackedSubmissions[msgId]) {
                console.log(`⊘ Skipping: ${email.subject || '(no subject)'} (already tracked)`);
                continue;
            }

            // Safety check for subject
            if (!email.subject) {
                console.log(`⚠ Skipping email with no subject (msgId: ${msgId})`);
                continue;
            }

            console.log(`\n✓ New submission: ${email.subject}`);
            console.log(`  From: ${email.from}`);
            console.log(`  Date: ${email.timestamp}`);

            // Get full message to see attachments
            const fullMsg = await client.inboxes.messages.get(INBOX_ID, msgId);

            // Extract MSP info from subject
            const mspInfo = extractMSPInfo(email.subject);
            console.log(`  MSP Name: ${mspInfo.name}`);
            console.log(`  Continuation: ${mspInfo.isContinuation ? 'YES' : 'NO'}`);

            // Download attachments
            if (fullMsg.attachments && fullMsg.attachments.length > 0) {
                console.log(`  Attachments: ${fullMsg.attachments.length}`);

                for (const att of fullMsg.attachments) {
                    console.log(`    - ${att.filename || '(unnamed)'} (${att.size} bytes)`);

                    try {
                        // Try to get attachment metadata via API
                        const attachmentMetadata = await client.inboxes.messages.getAttachment(
                            INBOX_ID,
                            msgId,
                            att.attachmentId
                        );

                        console.log(`    API returned attachment type: ${typeof attachmentMetadata}`);
                        if (typeof attachmentMetadata === 'object' && attachmentMetadata) {
                            console.log(`    Attachment properties: ${Object.keys(attachmentMetadata).join(', ')}`);
                        }

                        let saved = false;
                        let outputPath;

                        // Check if downloadUrl is available
                        if (typeof attachmentMetadata === 'object' && attachmentMetadata && attachmentMetadata.downloadUrl) {
                            // Use download URL from API response
                            console.log(`    ✓ Found downloadUrl in API response!`);
                            
                            const safeName = mspInfo.cleanName.replace(/[^a-zA-Z0-9]/g, '_');
                            const contMarker = mspInfo.isContinuation ? '_continued' : '';
                            const ext = att.filename ? path.extname(att.filename) : '.pdf';
                            const filename = `${safeName}${contMarker}_${Date.now()}${ext}`;
                            outputPath = path.join(OUTPUT_DIR, filename);

                            await downloadFile(attachmentMetadata.downloadUrl, outputPath);
                            saved = true;
                        } else {
                            console.log(`    ⚠ No downloadUrl available, skipping attachment`);
                        }

                        if (saved && outputPath) {
                            const filename = path.basename(outputPath);
                            console.log(`    ✓ Saved to: ${filename}`);

                            // Track this submission
                            trackedSubmissions[msgId] = {
                                mspName: mspInfo.name,
                                isContinuation: mspInfo.isContinuation,
                                filename: filename,
                                subject: email.subject,
                                timestamp: email.timestamp,
                                processed: false,
                                attachmentId: att.attachmentId
                            };

                            // Update MSP company tracking (for linking continuations)
                            if (!mspCompanies[mspInfo.name]) {
                                mspCompanies[mspInfo.name] = {
                                    name: mspInfo.name,
                                    files: [],
                                    continuations: []
                                };
                            }

                            if (mspInfo.isContinuation) {
                                mspCompanies[mspInfo.name].continuations.push(filename);
                                console.log(`    📎 Linked as continuation to: ${mspInfo.name}`);
                            } else {
                                mspCompanies[mspInfo.name].files.push(filename);
                                console.log(`    📄 Main submission file for: ${mspInfo.name}`);
                            }
                        } else {
                            console.log(`    ✗ Could not save attachment`);
                        }

                    } catch (err) {
                        console.error(`    ✗ Error processing attachment: ${err.message}`);
                    }
                }
            } else {
                console.log(`  ⚠ No attachments found`);
            }
        }

        // Save tracking state
        saveTracking();
        saveMSPCompanies();

        // Summary
        const unprocessed = Object.values(trackedSubmissions).filter(s => !s.processed).length;
        const totalMSPs = Object.keys(mspCompanies).length;
        const continuationsCount = Object.values(mspCompanies).reduce((sum, msp) => sum + msp.continuations.length, 0);
        
        console.log(`\n=== Summary ===`);
        console.log(`Total tracked emails: ${Object.keys(trackedSubmissions).length}`);
        console.log(`Unique MSP companies: ${totalMSPs}`);
        console.log(`Continuation files: ${continuationsCount}`);
        console.log(`Awaiting analysis: ${unprocessed}`);
        console.log(`Processed: ${Object.keys(trackedSubmissions).length - unprocessed}`);

        // Show MSP breakdown
        if (totalMSPs > 0) {
            console.log(`\n=== MSP Companies ===`);
            for (const [name, data] of Object.entries(mspCompanies)) {
                console.log(`\n${name}:`);
                console.log(`  Main files: ${data.files.length}`);
                console.log(`  Continuations: ${data.continuations.length}`);
                if (data.files.length > 0) {
                    data.files.forEach(f => console.log(`    - ${f}`));
                }
                if (data.continuations.length > 0) {
                    data.continuations.forEach(f => console.log(`    📎 ${f}`));
                }
            }
        }

        return trackedSubmissions;

    } catch (error) {
        console.error('Error checking for submissions:', error.message);
        if (error.body) {
            console.error('Details:', JSON.stringify(error.body, null, 2));
        }
        throw error;
    }
}

// Run the checker
checkForSubmissions()
    .then(submissions => {
        console.log('\n✓ Check complete');
        process.exit(0);
    })
    .catch(err => {
        console.error('\n✗ Check failed:', err.message);
        process.exit(1);
    });
