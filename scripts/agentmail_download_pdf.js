#!/usr/bin/env node
const { AgentMailClient } = require('agentmail');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const API_KEY = 'am_us_14a4a7ccfbff5ed90374fb30577bdb7562cba20cd12f958fed2b68a43e0b6e52';
const INBOX_ID = 'stevieai@agentmail.to';

function downloadFile(url, outputPath) {
    return new Promise((resolve, reject) => {
        try {
            // Use curl with -L for redirects and -s for silent
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

async function downloadMessage() {
    const client = new AgentMailClient({ apiKey: API_KEY });

    try {
        const result = await client.inboxes.messages.list(INBOX_ID);
        const rfpMsgs = result.messages.filter(m =>
            m.subject.includes('RFP') || m.subject.includes('RFQ')
        );

        const outputDir = '/home/rwhitaker/.openclaw/workspace/msp-rfps';
        if (!fs.existsSync(outputDir)) {
            fs.mkdirSync(outputDir, { recursive: true });
        }

        console.log(`Processing ${rfpMsgs.length} RFP messages...\n`);

        for (const msg of rfpMsgs) {
            console.log(`\nMessage: ${msg.subject}`);

            const fullMsg = await client.inboxes.messages.get(INBOX_ID, msg.messageId);

            if (fullMsg.attachments && fullMsg.attachments.length > 0) {
                for (const att of fullMsg.attachments) {
                    if (att.filename.endsWith('.pdf')) {
                        if (!att.downloadUrl) {
                            console.log(`  Skipping: ${att.filename} (no download URL)`);
                            continue;
                        }
                        
                        const outputPath = path.join(outputDir, att.filename);

                        console.log(`  Downloading: ${att.filename}`);
                        console.log(`  URL: ${att.downloadUrl.substring(0, 80)}...`);

                        try {
                            await downloadFile(att.downloadUrl, outputPath);

                            if (fs.existsSync(outputPath)) {
                                const size = fs.statSync(outputPath).size;
                                console.log(`  ✓ Saved (${size} bytes)`);
                            } else {
                                console.log(`  ✗ File not created`);
                            }
                        } catch (err) {
                            console.error(`  ✗ Failed: ${err.message}`);
                        }
                    }
                }
            }
        }

        console.log(`\n\nDone! PDFs saved to: ${outputDir}`);
    } catch (error) {
        console.error('Error:', error.message);
        console.error('Stack:', error.stack);
    }
}

downloadMessage();
