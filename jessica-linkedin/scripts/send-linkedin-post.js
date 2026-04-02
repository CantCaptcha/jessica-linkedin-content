#!/usr/bin/env node

const { AgentMailClient } = require('agentmail');
const fs = require('fs');

const API_KEY = 'am_us_14a4a7ccfbff5ed90374fb30577bdb7562cba20cd12f958fed2b68a43e0b6e52';
const INBOX_ID = 'stevieai@agentmail.to';

async function sendEmail() {
    const client = new AgentMailClient({ apiKey: API_KEY });

    const text = fs.readFileSync('linkedin-post-jessica-2026-03-27-v2.txt', 'utf8');

    const message = {
        to: ["jessica@yea-me.com"],
        subject: "LinkedIn Post - New Version Ready for Tuesday 9 AM",
        text: text
    };

    console.log('Sending to: jessica@yea-me.com');

    try {
        const result = await client.inboxes.messages.send(INBOX_ID, message);
        console.log('✅ Email sent!');
        console.log('   Message ID:', result.messageId);
        return result;
    } catch (error) {
        console.error('Error sending email:', error.message);
        throw error;
    }
}

sendEmail().catch(console.error);
