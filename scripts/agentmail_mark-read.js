#!/usr/bin/env node
const { AgentMailClient } = require('agentmail');

const API_KEY = 'am_us_14a4a7ccfbff5ed90374fb30577bdb7562cba20cd12f958fed2b68a43e0b6e52';
const INBOX_ID = 'stevieai@agentmail.to';

async function markAllAsRead() {
    const client = new AgentMailClient({ apiKey: API_KEY });

    try {
        const result = await client.inboxes.messages.list(INBOX_ID);
        
        // Filter for unread received messages
        const unreadMessages = result.messages.filter(msg => 
            msg.labels.includes('received') && msg.labels.includes('unread')
        );

        if (unreadMessages.length === 0) {
            console.log('No unread messages to mark as read.');
            return;
        }

        console.log(`Marking ${unreadMessages.length} message(s) as read...`);

        for (const msg of unreadMessages) {
            console.log(`\nMarking as read: ${msg.subject} (${msg.from})`);
            
            await client.inboxes.messages.update(INBOX_ID, msg.messageId, {
                addLabels: ['read'],
                removeLabels: ['unread']
            });
            
            console.log(`✅ Marked as read`);
        }

        console.log(`\n✅ All ${unreadMessages.length} messages marked as read.`);
    } catch (error) {
        console.error('Error marking messages as read:', error.message);
        throw error;
    }
}

markAllAsRead();
