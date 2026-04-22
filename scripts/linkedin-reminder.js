#!/usr/bin/env node

/**
 * LinkedIn Weekly Reminder Script
 * Runs every Thursday at 8:00 AM EST
 * Suggests LinkedIn topic to Jessica Allen
 */

const axios = require('axios');

// LinkedIn topic rotation (20 topics, won't repeat until all used)
const TOPICS = [
  "Hiring chaos — how to hire smart when you're drowning in candidates",
  "Burnout awareness — recognizing the signs before it's too late",
  "Managing up with investors — how to speak their language",
  "High-performance teams without breaking culture",
  "Metrics vs Art — measurement challenges and art/science tension",
  "Culture Code — maintaining values while growing fast",
  "Scale Stories — companies that scaled well (or failed) based on culture fit",
  "When to say 'no' as a leader",
  "Remote team management in 2026",
  "The art of delegation — letting go of control",
  "Operational visibility without micromanagement",
  "Building trust in distributed teams",
  "Crisis leadership lessons learned",
  "Transitioning from manager to executive",
  "Board readiness — what directors actually look for",
  "Work-life boundaries that actually work",
  "Negotiation strategies for leaders",
  "Building your personal brand as a leader",
  "Mentor vs Sponsor — understanding the difference",
  "The first 90 days in a new COO role"
];

// Track used topics to avoid repeats
const USED_TOPICS_FILE = '/home/rwhitaker/.openclaw/workspace/logs/linkedin-topics-used.json';

// Function to get unused topic
async function getTopic() {
  const fs = require('fs').promises;
  
  // Load used topics
  let usedTopics = [];
  try {
    const data = await fs.readFile(USED_TOPICS_FILE, 'utf8');
    usedTopics = JSON.parse(data);
  } catch (err) {
    // File doesn't exist yet, create it
  }

  // Find first unused topic
  const availableTopics = TOPICS.filter(t => !usedTopics.includes(t));

  // If all used, reset rotation
  if (availableTopics.length === 0) {
    console.log('All topics used! Resetting rotation.');
    usedTopics = [];
  }

  // Select next topic
  const topic = availableTopics[0] || TOPICS[0];

  // Mark as used
  usedTopics.push(topic);
  await fs.writeFile(USED_TOPICS_FILE, JSON.stringify(usedTopics, null, 2));

  return topic;
}

// Function to send Discord message
async function sendDiscordMessage(message) {
  try {
    const botToken = process.env.DISCORD_BOT_TOKEN;
    const channelId = '1488952869603377243'; // #Richard channel

    if (!botToken) {
      console.error('DISCORD_BOT_TOKEN not set');
      return;
    }

    await axios.post(`https://discord.com/api/v10/channels/${channelId}/messages`, {
      content: message
    }, {
      headers: {
        'Authorization': `Bot ${botToken}`,
        'Content-Type': 'application/json'
      }
    });

    console.log('Discord message sent successfully');
  } catch (error) {
    console.error('Failed to send Discord message:', error.message);
  }
}

// Main function
async function main() {
  const topic = await getTopic();
  const message = `🖤 **Thursday LinkedIn Topic Suggestion**

This week's topic: *${topic}*

**Your turn, Queen!** 

Drop a paragraph of your thoughts/learnings on this topic. Keep it raw and unpolished — I'll clean it up and email you a LinkedIn-ready post!

📋 Ready when you are!`;

  await sendDiscordMessage(message);
}

main().catch(console.error);
