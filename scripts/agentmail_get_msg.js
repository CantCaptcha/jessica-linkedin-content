#!/usr/bin/env node
const { AgentMailClient } = require('agentmail');
const fs = require('fs');
const path = require('path');

const API_KEY = 'am_us_14a4a7ccfbff5ed90374fb30577bdb7562cba20cd12f958fed2b68a43e0b6e52';
const INBOX_ID = 'stevieai@agentmail.to';

async function downloadMessage() {
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

        console.log('Getting full message:', rfpMsg.messageId);

        const fullMsg = await client.inboxes.messages.get(INBOX_ID, rfpMsg.messageId);

        console.log('Message subject:', fullMsg.subject);
        console.log('Has attachments?', fullMsg.attachments ? fullMsg.attachments.length : 0);
        console.log('Message object keys:', Object.keys(fullMsg));

        if (fullMsg.attachments && fullMsg.attachments.length > 0) {
            const outputDir = '/home/rwhitaker/.openclaw/workspace/msp-rfps';
            if (!fs.existsSync(outputDir)) {
                fs.mkdirSync(outputDir, { recursive: true });
            }

            for (const att of fullMsg.attachments) {
                if (att.filename.endsWith('.pdf')) {
                    console.log(`\nAttachment: ${att.filename}`);
                    console.log('  ID:', att.attachmentId);
                    console.log('  Size:', att.size);
                    console.log('  Type:', att.contentType);

                    // Try to get attachment content
                    try {
                        const attachment = await client.inboxes.messages.getAttachment(
                            INBOX_ID,
                            rfpMsg.messageId,
                            att.attachmentId
                        );
                        console.log('  Got attachment, size:', attachment.length);
                        console.log('  Attachment type:', typeof attachment);
                        console.log('  Attachment keys:', Object.keys(attachment));

                        // Try to get the actual data
                        let data = attachment;
                        if (typeof attachment === 'object' && attachment.data) {
                            data = attachment.data;
                        }

                        // Write to file
                        const outputPath = path.join(outputDir, att.filename);
                        fs.writeFileSync(outputPath, data);
                        console.log(`  ✓ Saved to: ${outputPath}`);
                    } catch (err) {
                        console.error('  ✗ Error:', err.message);
                        console.error('  Stack:', err.stack);
                    }
                }
            }
        }
    } catch (error) {
        console.error('Error:', error.message);
        console.error('Stack:', error.stack);
    }
}

downloadMessage();
