#!/usr/bin/env node
const { AgentMailClient } = require('agentmail');

const API_KEY = 'am_us_14a4a7ccfbff5ed90374fb30577bdb7562cba20cd12f958fed2b68a43e0b6e52';
const INBOX_ID = 'stevieai@agentmail.to';

async function fetchMessage(messageId) {
    const client = new AgentMailClient({ apiKey: API_KEY });

    try {
        const message = await client.inboxes.messages.get(INBOX_ID, messageId);

        console.log('From:', message.from);
        console.log('Subject:', message.subject);
        console.log('Timestamp:', message.timestamp);
        console.log('\n--- BODY ---');
        console.log(message.text || message.html || '(No text content)');
        console.log('\n--- ATTACHMENTS ---');
        if (message.attachments && message.attachments.length > 0) {
            message.attachments.forEach(att => {
                console.log(`- ${att.filename} (${att.contentType})`);
            });
        } else {
            console.log('(None)');
        }
    } catch (error) {
        console.error('Error fetching message:', error.message);
        if (error.body) {
            console.error('Error details:', JSON.stringify(error.body, null, 2));
        }
    }
}

const messageId = process.argv[2];
if (!messageId) {
    console.error('Usage: node agentmail_fetch.js <message-id>');
    process.exit(1);
}

fetchMessage(messageId);
