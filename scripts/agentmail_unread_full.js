#!/usr/bin/env node



async function checkUnread() {
  const response = await fetch('https://api.agentmail.to/v1/messages?limit=20', {
    headers: {
      'Authorization': `Bearer ${process.env.AGENTMAIL_TOKEN}`
    }
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();
  const unread = data.messages.filter(m => !m.labels.includes('read'));

  if (unread.length === 0) {
    console.log('No unread messages');
    return;
  }

  console.log(`Found ${unread.length} unread message(s):\n`);

  unread.forEach(msg => {
    console.log('---');
    console.log('ID:', msg.id);
    console.log('From:', msg.from);
    console.log('Subject:', msg.subject);
    console.log('Time:', msg.timestamp);
    console.log('Preview:', msg.preview);
    console.log('Labels:', msg.labels.join(', '));
    console.log('Has Attachments:', msg.attachments && msg.attachments.length > 0 ? 'Yes' : 'No');
    console.log('');
  });
}

checkUnread().catch(console.error);
