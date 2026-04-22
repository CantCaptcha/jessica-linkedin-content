#!/usr/bin/env node
const { AgentMailClient } = require('agentmail');

const API_KEY = 'am_us_14a4a7ccfbff5ed90374fb30577bdb7562cba20cd12f958fed2b68a43e0b6e52';
const INBOX_ID = 'stevieai@agentmail.to';

async function getTemplateEmail() {
    const client = new AgentMailClient({ apiKey: API_KEY });

    try {
        const result = await client.inboxes.messages.list(INBOX_ID);
        const templateMsg = result.messages.find(m =>
            m.subject.includes('Template for RFP review and analysis') &&
            m.from.includes('jessica.allen@cybersecgru.com')
        );

        if (!templateMsg) {
            console.log('Template message not found');
            return;
        }

        console.log('Getting full message:', templateMsg.messageId);

        const fullMsg = await client.inboxes.messages.get(INBOX_ID, templateMsg.messageId);

        console.log('\n=== MESSAGE INFO ===');
        console.log('Subject:', fullMsg.subject);
        console.log('From:', fullMsg.from);
        console.log('To:', fullMsg.to);
        console.log('Timestamp:', fullMsg.timestamp);
        console.log('Labels:', fullMsg.labels);

        console.log('\n=== BODY TEXT ===');
        if (fullMsg.text) {
            console.log(fullMsg.text);
        } else if (fullMsg.html) {
            console.log('(HTML message - showing first 500 chars)');
            console.log(fullMsg.html.substring(0, 500));
        } else {
            console.log('(No text body)');
        }

        console.log('\n=== ATTACHMENTS ===');
        if (fullMsg.attachments && fullMsg.attachments.length > 0) {
            console.log(`Found ${fullMsg.attachments.length} attachment(s):`);
            for (const att of fullMsg.attachments) {
                console.log(`  - Name: ${att.filename || '(unnamed)'}`);
                console.log(`    ID: ${att.attachmentId}`);
                console.log(`    Size: ${att.size}`);
                console.log(`    Type: ${att.contentType}`);
            }
        } else {
            console.log('No attachments found');
        }

    } catch (error) {
        console.error('Error:', error.message);
        if (error.body) {
            console.error('Error details:', JSON.stringify(error.body, null, 2));
        }
    }
}

getTemplateEmail();
