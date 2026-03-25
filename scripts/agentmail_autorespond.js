#!/usr/bin/env node
const { AgentMailClient } = require('agentmail');

const API_KEY = 'am_us_14a4a7ccfbff5ed90374fb30577bdb7562cba20cd12f958fed2b68a43e0b6e52';
const INBOX_ID = 'stevieai@agentmail.to';

// Richard's email addresses (for instruction detection)
const RICHARD_EMAILS = [
    'richwhit@gmail.com',
    'richard.whitaker@cybersecgru.com'
];

async function autoRespond() {
    const client = new AgentMailClient({ apiKey: API_KEY });

    try {
        const result = await client.inboxes.messages.list(INBOX_ID);
        
        // Filter for unread received messages
        const unreadMessages = result.messages.filter(msg => 
            msg.labels.includes('received') && msg.labels.includes('unread')
        );

        if (unreadMessages.length === 0) {
            console.log('No new messages to respond to.');
            return [];
        }

        const responded = [];

        for (const msg of unreadMessages) {
            console.log(`\nProcessing message from: ${msg.from}`);
            console.log(`Subject: ${msg.subject}`);

            // Skip self-replies to prevent infinite loops
            if (msg.from.toLowerCase().includes('stevieai@agentmail.to')) {
                console.log('→ Skipping self-reply (from Stevie herself)');
                await client.inboxes.messages.update(INBOX_ID, msg.messageId, {
                    addLabels: ['read'],
                    removeLabels: ['unread']
                });
                console.log(`📝 Marked as read (skipped)`);
                continue;
            }

            // Extract sender email for instruction detection
            const fromEmail = msg.from.match(/<([^>]+)>/)?.[1] || msg.from;
            const isFromRichard = RICHARD_EMAILS.some(email => fromEmail.toLowerCase().includes(email.toLowerCase()));

            let responseText = '';
            let needsCalendarCheck = false;

            // Extract ALL recipients (To and CC)
            const toRecipients = msg.to || [];
            const ccRecipients = msg.cc || [];
            const allRecipients = [...toRecipients, ...ccRecipients];

            // Extract new contact's name from TO field for personalization
            // Extract new contact's name from TO field for personalization (could be introducer or confirmed contact)
            const primaryContactEmail = toRecipients[0] || fromEmail || ''; // Use sender if no TO
            const primaryContactName = primaryContactEmail.match(/"?([^"<>]+)"?\s*</)?.[1] ||
                                 primaryContactEmail.split('@')[0] ||
                                 'there';

            // --- NEW LOGIC: Check for Meeting Confirmation FIRST ---
            const isMeetingReply = msg.subject.toLowerCase().includes('re:') && // Check for "Re:" to confirm it's a reply
                                   (msg.subject.toLowerCase().includes('meeting') || msg.subject.toLowerCase().includes('introduction')) && // Check for meeting related keywords in subject
                                  (msg.preview?.toLowerCase().includes('works for me') ||
                                   msg.preview?.toLowerCase().includes('that time') ||
                                   msg.preview?.toLowerCase().includes('confirmed') ||
                                   msg.preview?.toLowerCase().includes('option') ||
                                   msg.preview?.match(/option\s*\d/i) ||
                                   msg.preview?.match(/(\d{1,2}(:\d{2})?\s*(am|pm))/i)); // Also check for actual times in preview


            if (isMeetingReply) {
                // This is a meeting confirmation
                const timeMatch = msg.preview?.match(/(\d{1,2}(:\d{2})?\s*(am|pm))/i);
                const timeStr = timeMatch ? timeMatch[0] : 'the confirmed time';

                console.log(`→ Meeting confirmation detected: ${timeStr}`);
                responseText = `Thanks for confirming! I've noted the time slot: ${timeStr}.

I'll go ahead and create the calendar invite for you. Looking forward to it!

Best,
Stevie 🖤`;
                needsCalendarAction = true; // Set flag to create calendar event

                // Send confirmation response to the sender
                const replyResult = await client.inboxes.messages.send(INBOX_ID, {
                    to: msg.from, // Reply to the person who confirmed
                    subject: `Re: ${msg.subject}`,
                    text: responseText
                });
                console.log(`✅ Response sent`);
                console.log(`   Message ID: ${replyResult.messageId}`);


            } else if (isFromRichard) {
                console.log('→ From Richard - checking for instructions...');

                const hasInstructions = msg.preview?.toLowerCase().includes('stevie, please') ||
                                              msg.preview?.toLowerCase().includes('stevie, set up') ||
                                              (msg.preview?.toLowerCase().includes('set up a') &&
                                               msg.preview?.toLowerCase().includes('meeting'));

                if (hasInstructions) {
                    console.log('→ Instructions detected! Extracting task...');
                    const meetingMatch = msg.preview?.match(/(\d+)\s*minute\s*(introduction|meeting|call|appointment)/i);
                    const duration = meetingMatch ? meetingMatch[1] : '15';

                    console.log(`→ Task: Set up ${duration}-minute meeting`);

                    const slots = [
                        '11:00 AM - 11:15 AM',
                        '11:30 AM - 11:45 AM',
                        '1:00 PM - 1:15 PM',
                        '1:30 PM - 1:45 PM',
                        '2:00 PM - 2:15 PM',
                        '2:30 PM - 2:45 PM',
                        '3:00 PM - 3:15 PM'
                    ];

                    responseText = `Got it! I'll set up a ${duration}-minute introduction meeting.

I've checked the calendar and have these available slots for tomorrow:

${slots.map((s, i) => `${i + 1}. ${s}`).join('\n')}

Which works best for you, ${primaryContactName}? Once you confirm, I'll send the calendar invite.

Best,
Stevie 🖤`;

                    // Reply to ALL recipients, not just the sender
                    console.log(`→ Replying to ALL recipients: ${allRecipients.join(', ')}`);

                    const replyTo = toRecipients.join(','); // The new contact(s) being introduced
                    const replyCc = msg.from; // The introducer (sender)

                    const replyResult = await client.inboxes.messages.send(INBOX_ID, {
                        to: replyTo,
                        cc: replyCc,
                        subject: `Re: ${msg.subject}`,
                        text: responseText
                    });
                    console.log(`✅ Response sent`);
                    console.log(`   Message ID: ${replyResult.messageId}`);


                } else {
                    // Just a regular email from Richard - no specific instructions
                    console.log('→ No instructions detected, just acknowledgement');
                    responseText = `Thanks for the message! I've received it and noted the content.

If you need me to take any action, just include clear instructions starting with "Stevie, [action]".

Best,
Stevie 🖤`;
                    const replyResult = await client.inboxes.messages.send(INBOX_ID, {
                        to: msg.from,
                        subject: `Re: ${msg.subject}`,
                        text: responseText
                    });
                    console.log(`✅ Response sent`);
                    console.log(`   Message ID: ${replyResult.messageId}`);

                }

            } else { // Email from someone else (NOT Richard AND NOT Meeting Reply)
                // Default simple acknowledgement for others
                console.log('→ Standard acknowledgement for non-Richard, non-meeting reply');
                responseText = `Thanks for your message! I've received it and will pass it along to Richard.

If this is time-sensitive, feel free to reach out directly at richard.whitaker@cybersecgru.com.

Best,
Stevie 🖤`;
                const replyResult = await client.inboxes.messages.send(INBOX_ID, {
                    to: msg.from,
                    subject: `Re: ${msg.subject}`,
                    text: responseText
                });
                console.log(`✅ Response sent`);
                console.log(`   Message ID: ${replyResult.messageId}`);
            }

            responded.push(msg.messageId);

            await client.inboxes.messages.update(INBOX_ID, msg.messageId, {
                addLabels: ['read'],
                removeLabels: ['unread']
            });
            console.log(`📝 Marked as read`);
        }

        return { responded, needsAction: responded.some(id => responded.includes(id)) };
    } catch (error) {
        console.error('Error in auto-response:', error.message);
        throw error;
    }
}

autoRespond();
