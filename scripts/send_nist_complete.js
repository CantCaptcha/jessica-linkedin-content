#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { AgentMailClient } = require('agentmail');

const API_KEY = 'am_us_14a4a7ccfbff5ed90374fb30577bdb7562cba20cd12f958fed2b68a43e0b6e52';
const INBOX_ID = 'stevieai@agentmail.to';

async function sendEmailWithExcelContent() {
    const client = new AgentMailClient({ apiKey: API_KEY });

    // Read the markdown guide (which has the Excel content)
    const markdownPath = path.join(__dirname, '..', 'NIST-Artifacts-Level-Breakdown.md');
    const text = fs.readFileSync(markdownPath, 'utf8');

    const message = {
        to: ['jessica.allen@cybersecgru.com'],
        subject: 'NIST-CMMC Artifacts by Level (Complete Guide)',
        text: text
    };

    try {
        const result = await client.inboxes.messages.send(INBOX_ID, message);
        console.log('✅ Email sent successfully!');
        console.log('Message ID:', result.id);
        console.log('To:', message.to.join(', '));
        console.log('Subject:', message.subject);
        console.log('Length:', text.length, 'characters');
        console.log('\nNote: This is the complete Level breakdown guide (markdown format).');
        console.log('The Excel file is also available at: /home/rwhitaker/.openclaw/workspace/NIST-CMMC-Artifacts-by-Level.xlsx');
        return result;
    } catch (error) {
        console.error('❌ Error sending email:', error.message);
        if (error.body) {
            console.error('Error details:', JSON.stringify(error.body, null, 2));
        }
        throw error;
    }
}

sendEmailWithExcelContent();
