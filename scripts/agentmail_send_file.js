#!/usr/bin/env node
const { AgentMailClient } = require('agentmail');
const fs = require('fs');

const API_KEY = 'am_us_14a4a7ccfbff5ed90374fb30577bdb7562cba20cd12f958fed2b68a43e0b6e52';
const INBOX_ID = 'stevieai@agentmail.to';

async function sendEmail(to, subject, textFile, cc = null) {
    const client = new AgentMailClient({ apiKey: API_KEY });

    // Read email text from file
    let text;
    try {
        text = fs.readFileSync(textFile, 'utf8');
    } catch (error) {
        console.error('Error reading file:', error.message);
        throw error;
    }

    const message = {
        to: to,
        subject: subject,
        text: text
    };

    if (cc) {
        message.cc = cc;
    }

    try {
        const result = await client.inboxes.messages.send(INBOX_ID, message);
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
    console.log('Usage: node agentmail_send_file.js <to> <subject> <textFile> [cc]');
}
