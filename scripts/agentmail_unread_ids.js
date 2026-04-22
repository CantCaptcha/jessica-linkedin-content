#!/usr/bin/env node
const { AgentMailClient } = require('agentmail');

const API_KEY = 'am_us_14a4a7ccfbff5ed90374fb30577bdb7562cba20cd12f958fed2b68a43e0b6e52';
const INBOX_ID = 'stevieai@agentmail.to';

async function checkUnread() {
    const client = new AgentMailClient({ apiKey: API_KEY });

    try {
        const result = await client.inboxes.messages.list(INBOX_ID);
        const unread = result.messages.filter(m => !m.labels.includes('read'));

        if (unread.length === 0) {
            console.log('No unread messages');
            return;
        }

        console.log(`Found ${unread.length} unread message(s):\n`);

        unread.forEach(msg => {
            console.log('---');
            console.log('ID:', msg.id);
            console.log('From:', msg.from);
            console.log('Subject:', msg.subject);
            console.log('Time:', msg.timestamp);
            console.log('Preview:', msg.preview);
            console.log('Labels:', msg.labels.join(', '));
            console.log('Has Attachments:', msg.attachments && msg.attachments.length > 0 ? 'Yes' : 'No');
            console.log('');
        });
    } catch (error) {
        console.error('Error checking unread:', error.message);
        if (error.body) {
            console.error('Error details:', JSON.stringify(error.body, null, 2));
        }
    }
}

checkUnread();
