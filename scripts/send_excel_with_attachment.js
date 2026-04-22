#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { AgentMailClient } = require('agentmail');

const API_KEY = 'am_us_14a4a7ccfbff5ed90374fb30577bdb7562cba20cd12f958fed2b68a43e0b6e52';
const INBOX_ID = 'stevieai@agentmail.to';

async function sendExcelAttachment() {
    const client = new AgentMailClient({ apiKey: API_KEY });

    const excelPath = path.join(__dirname, '..', 'NIST-CMMC-Artifacts-by-Level.xlsx');
    const buffer = fs.readFileSync(excelPath);

    console.log('File size:', buffer.length, 'bytes');
    console.log('File path:', excelPath);

    const message = {
        to: ['jessica.allen@cybersecgru.com'],
        subject: 'NIST-CMMC Artifacts by Level (Excel Spreadsheet)',
        text: 'Hi Jessica,\n\nAttached is the Excel spreadsheet with CMMC artifacts organized by Level 1 and Level 2.\n\nThis includes:\n\n- Overview sheet with level summaries\n- Domain comparison (controls per domain)\n- Level 1 artifacts (17 controls)\n- Level 2 artifacts (72 controls)\n- Critical documents required at each level\n- Implementation roadmap (11 phases)\n\nLet me know if you have any questions!\n\nBest,\nStevie',
        attachments: [{
            filename: 'NIST-CMMC-Artifacts-by-Level.xlsx',
            contentType: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            content: buffer.toString('base64')
        }]
    };

    try {
        const result = await client.inboxes.messages.send(INBOX_ID, message);
        console.log('✅ Email sent successfully!');
        console.log('Message ID:', result.id);
        console.log('To:', message.to.join(', '));
        console.log('Subject:', message.subject);
        console.log('Attachment:', message.attachments[0].filename);
        console.log('Size:', buffer.length, 'bytes');
        return result;
    } catch (error) {
        console.error('❌ Error sending email:', error.message);
        if (error.body) {
            console.error('Error details:', JSON.stringify(error.body, null, 2));
        }
        throw error;
    }
}

sendExcelAttachment();
