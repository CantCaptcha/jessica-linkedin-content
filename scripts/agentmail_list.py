#!/usr/bin/env node
const { AgentMailClient } = require('agentmail');

const API_KEY = 'am_us_14a4a7ccfbff5ed90374fb30577bdb7562cba20cd12f958fed2b68a43e0b6e52';

async function listInboxes() {
    const client = new AgentMailClient({ apiKey: API_KEY });

    try {
        const inboxes = await client.inboxes.list();
        console.log('Inboxes:');
        console.log(JSON.stringify(inboxes, null, 2));
    } catch (error) {
        console.error('Error listing inboxes:', error.message);
        if (error.body) {
            console.error('Error details:', error.body);
        }
    }
}

listInboxes();
