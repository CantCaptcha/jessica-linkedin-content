#!/usr/bin/env node
const { AgentMailClient } = require('agentmail');

const API_KEY = 'am_us_14a4a7ccfbff5ed90374fb30577bdb7562cba20cd12f958fed2b68a43e0b6e52';
const INBOX_ID = 'stevieai@agentmail.to';

async function checkUnread() {
    const client = new AgentMailClient({ apiKey: API_KEY });

    try {
        const result = await client.inboxes.messages.list(INBOX_ID);
        
        // Filter for unread received messages
        const unreadMessages = result.messages.filter(msg => 
            msg.labels.includes('received') && msg.labels.includes('unread')
        );

        if (unreadMessages.length === 0) {
            console.log('No new unread messages.');
            return [];
        }

        console.log(`Found ${unreadMessages.length} unread message(s):`);
        unreadMessages.forEach(msg => {
            console.log(`\n---`);
            console.log(`From: ${msg.from}`);
            console.log(`Subject: ${msg.subject}`);
            console.log(`Time: ${new Date(msg.timestamp).toLocaleString()}`);
            console.log(`Message ID: ${msg.messageId}`);
            if (msg.preview) {
                console.log(`Preview: ${msg.preview.substring(0, 200)}...`);
            }
        });

        return unreadMessages;
    } catch (error) {
        console.error('Error checking inbox:', error.message);
        throw error;
    }
}

checkUnread();
