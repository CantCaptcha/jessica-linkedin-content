#!/usr/bin/env node
const { AgentMailClient } = require('agentmail');
const fs = require('fs');
const path = require('path');

const API_KEY = 'am_us_14a4a7ccfbff5ed90374fb30577bdb7562cba20cd12f958fed2b68a43e0b6e52';
const INBOX_ID = 'stevieai@agentmail.to';
const SENT_LOG = '/home/rwhitaker/.openclaw/workspace/logs/agentmail-sent.json';

// Prevent duplicates within 5 minutes
const DUPLICATE_WINDOW_MS = 5 * 60 * 1000;

function loadSentLog() {
    try {
        if (fs.existsSync(SENT_LOG)) {
            const data = fs.readFileSync(SENT_LOG, 'utf8');
            return JSON.parse(data);
        }
    } catch (error) {
        return [];
    }
    return [];
}

function saveSentLog(log) {
    const dir = path.dirname(SENT_LOG);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(SENT_LOG, JSON.stringify(log, null, 2));
}

function isDuplicate(to, subject) {
    const log = loadSentLog();
    const now = Date.now();

    // Remove old entries (older than 1 hour)
    const filteredLog = log.filter(entry => (now - entry.timestamp) < (60 * 60 * 1000));
    saveSentLog(filteredLog);

    // Check for recent match (same to addresses + subject within DUPLICATE_WINDOW_MS)
    const toKey = to.split(',').map(e => e.trim()).sort().join(',');
    const recentEntry = filteredLog.find(entry =>
        entry.to === toKey &&
        entry.subject === subject &&
        (now - entry.timestamp) < DUPLICATE_WINDOW_MS
    );

    return recentEntry !== undefined;
}

function recordSent(to, subject) {
    const log = loadSentLog();
    log.push({
        to: to,
        subject: subject,
        timestamp: Date.now()
    });
    saveSentLog(log);
}

async function sendEmail(to, subject, textFile, cc = null) {
    const client = new AgentMailClient({ apiKey: API_KEY });

    // Check for duplicate
    if (isDuplicate(to, subject)) {
        console.log('⚠️  Duplicate email detected (same recipients + subject within 5 minutes)');
        console.log('   Skipping send to avoid duplicate.');
        return null;
    }

    // Read email text from file
    let text;
    try {
        text = fs.readFileSync(textFile, 'utf8');
    } catch (error) {
        console.error('Error reading file:', error.message);
        throw error;
    }

    // Parse comma-separated emails into array
    const toEmails = to.split(',').map(e => e.trim());
    const ccEmails = cc ? cc.split(',').map(e => e.trim()) : null;

    const message = {
        to: toEmails,
        subject: subject,
        text: text
    };

    if (ccEmails && ccEmails.length > 0) {
        message.cc = ccEmails;
    }

    console.log(`Sending to: ${toEmails.join(', ')}`);

    try {
        const result = await client.inboxes.messages.send(INBOX_ID, message);

        // Record that we sent this
        recordSent(to, subject);

        console.log('✅ Email sent!');
        console.log('   Message ID:', result.messageId);
        return result;
    } catch (error) {
        console.error('Error sending email:', error.message);
        if (error.body) {
            console.error('Error details:', JSON.stringify(error.body, null, 2));
        }
        throw error;
    }
}

// Get command line arguments
const args = process.argv.slice(2);
if (args.length >= 3) {
    const cc = args[3] || null;
    sendEmail(args[0], args[1], args[2], cc);
} else {
    console.log('Usage: node agentmail_send_file_array_dedup.js <to> <subject> <textFile> [cc]');
    console.log('  <to>: Comma-separated email addresses');
}
