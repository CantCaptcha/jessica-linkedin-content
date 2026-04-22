#!/usr/bin/env node
const { AgentMailClient } = require('agentmail');

const API_KEY = 'am_us_14a4a7ccfbff5ed90374fb30577bdb7562cba20cd12f958fed2b68a43e0b6e52';
const INBOX_ID = 'stevieai@agentmail.to';

async function checkAttachments() {
    const client = new AgentMailClient({ apiKey: API_KEY });

    try {
        const result = await client.inboxes.messages.list(INBOX_ID);
        const messages = result.messages.filter(m => m.subject.includes('RFP') || m.subject.includes('RFQ'));

        console.log(`Found ${messages.length} RFP-related messages:\n`);

        for (const msg of messages) {
            console.log('---');
            console.log('From:', msg.from);
            console.log('Subject:', msg.subject);
            console.log('Time:', msg.timestamp);
            if (msg.attachments && msg.attachments.length > 0) {
                console.log('\nAttachments:');
                msg.attachments.forEach((att, i) => {
                    console.log(`  ${i+1}. ${att.filename} (${att.contentType}) - ${att.size} bytes`);
                    console.log(`     ID: ${att.id}`);
                });
            } else {
                console.log('\nNo attachments');
            }
            console.log('');
        }
    } catch (error) {
        console.error('Error:', error.message);
        if (error.body) {
            console.error('Details:', JSON.stringify(error.body, null, 2));
        }
    }
}

checkAttachments();
