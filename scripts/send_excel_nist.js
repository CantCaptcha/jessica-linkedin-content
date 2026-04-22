#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { AgentMailClient } = require('agentmail');

const API_KEY = 'am_us_14a4a7ccfbff5ed90374fb30577bdb7562cba20cd12f958fed2b68a43e0b6e52';
const INBOX_ID = 'stevieai@agentmail.to';

async function sendEmail() {
    const client = new AgentMailClient({ apiKey: API_KEY });

    // Read Excel file
    const excelPath = path.join(__dirname, '..', 'NIST-CMMC-Artifacts-by-Level.xlsx');
    const buffer = fs.readFileSync(excelPath);

    const message = {
        to: ['jessica.allen@cybersecgru.com'],
        subject: 'NIST-CMMC Artifacts by Level (Excel)',
        buffer: buffer.toString('base64'),
        filename: 'NIST-CMMC-Artifacts-by-Level.xlsx',
        mimeType: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    };

    try {
        const result = await client.inboxes.messages.send(INBOX_ID, message);
        console.log('✅ Email sent successfully!');
        console.log('Message ID:', result.id);
        console.log('To:', message.to.join(', '));
        console.log('Subject:', message.subject);
        console.log('Filename:', message.filename);
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

sendEmail();
