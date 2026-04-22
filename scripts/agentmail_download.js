#!/usr/bin/env node
const { AgentMailClient } = require('agentmail');
const fs = require('fs');
const path = require('path');

const API_KEY = 'am_us_14a4a7ccfbff5ed90374fb30577bdb7562cba20cd12f958fed2b68a43e0b6e52';
const INBOX_ID = 'stevieai@agentmail.to';

async function downloadAttachments() {
    const client = new AgentMailClient({ apiKey: API_KEY });

    try {
        const result = await client.inboxes.messages.list(INBOX_ID);
        const messages = result.messages.filter(m =>
            m.subject.includes('RFP') || m.subject.includes('RFQ')
        );

        const outputDir = '/home/rwhitaker/.openclaw/workspace/msp-rfps';

        // Create output directory if needed
        if (!fs.existsSync(outputDir)) {
            fs.mkdirSync(outputDir, { recursive: true });
        }

        console.log(`Processing ${messages.length} RFP messages...\n`);

        for (const msg of messages) {
            console.log(`\nProcessing: ${msg.subject}`);

            if (msg.attachments && msg.attachments.length > 0) {
                for (const att of msg.attachments) {
                    if (att.filename.endsWith('.pdf')) {
                        const outputPath = path.join(outputDir, att.filename);

                        // Download attachment
                        try {
                            await client.inboxes.messages.attachment.download(INBOX_ID, msg.id, att.id, outputPath);
                            console.log(`  ✓ Downloaded: ${att.filename} (${att.size} bytes)`);
                        } catch (err) {
                            console.error(`  ✗ Failed to download ${att.filename}:`, err.message);
                        }
                    }
                }
            }
        }

        console.log(`\n\nAll PDFs saved to: ${outputDir}`);
    } catch (error) {
        console.error('Error:', error.message);
        if (error.body) {
            console.error('Details:', JSON.stringify(error.body, null, 2));
        }
    }
}

downloadAttachments();
