#!/usr/bin/env node

const { AgentMailClient } = require('agentmail');
const fs = require('fs');
const path = require('path');

// Load environment variables from .env file
require('dotenv').config();

const API_KEY = process.env.AGENTMAIL_API_KEY;
const INBOX_ID = 'stevieai@agentmail.to';

async function sendEmail() {
    if (!API_KEY) {
        throw new Error('AGENTMAIL_API_KEY not found in environment variables. Please create a .env file with your API key.');
    }

    const client = new AgentMailClient({ apiKey: API_KEY });

    // Get post text from drafts folder
    const text = fs.readFileSync(path.join(__dirname, '../drafts/linkedin-post-jessica-2026-03-27-v2.txt'), 'utf8');

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
