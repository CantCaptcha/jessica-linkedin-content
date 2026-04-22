#!/usr/bin/env node
const { AgentMailClient } = require('agentmail');
const fs = require('fs');
const path = require('path');

const API_KEY = 'am_us_14a4a7ccfbff5ed90374fb30577bdb7562cba20cd12f958fed2b68a43e0b6e52';
const INBOX_ID = 'stevieai@agentmail.to';

async function getRawMessage() {
    const client = new AgentMailClient({ apiKey: API_KEY });

    try {
        const result = await client.inboxes.messages.list(INBOX_ID);
        const rfpMsg = result.messages.find(m =>
            m.subject.includes('Calyra')
        );

        if (!rfpMsg) {
            console.log('Message not found');
            return;
        }

        console.log('Getting raw message for:', rfpMsg.messageId);

        const raw = await client.inboxes.messages.getRaw(INBOX_ID, rfpMsg.messageId);

        console.log('Raw message type:', typeof raw);
        console.log('Raw message keys:', Object.keys(raw));
        console.log('Raw message download URL:', raw.downloadUrl.substring(0, 80), '...');

        // Download raw message from URL
        const { execSync } = require('child_process');
        const outputDir = '/home/rwhitaker/.openclaw/workspace/msp-rfps';
        if (!fs.existsSync(outputDir)) {
            fs.mkdirSync(outputDir, { recursive: true });
        }

        const rawPath = path.join(outputDir, 'raw_message.eml');
        console.log('Downloading raw EML...');
        execSync(`curl -s -L "${raw.downloadUrl}" -o "${rawPath}"`);
        console.log(`Saved raw message to: ${rawPath}`);
        console.log('File size:', fs.statSync(rawPath).size);
        console.log(`Saved raw message to: ${rawPath}`);
    } catch (error) {
        console.error('Error:', error.message);
        console.error('Stack:', error.stack);
    }
}

getRawMessage();
