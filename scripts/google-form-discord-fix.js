// Google Form to Discord - New Client Quote
// ==========================================
// Auto-posts Google Form submissions to #project Discord channel
// For Cleaning Services Quote Request Form
// ==========================================

const DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1489256487883899070/NXyyDk1nV6b4a1vG2TBtcIWR3ycmBW13boSxSzpSRlS4qsG_zLm-4yvLfYpzrmnU-9p2';

function onFormSubmit(e) {
  // Guard: check if event object exists
  if (!e || !e.response) {
    Logger.log('Error: Event object is missing. This function must be triggered by a form submission.');
    return;
  }

  // Get form response directly from event object
  const response = e.response;
  const itemResponses = response.getItemResponses();

  // Build Discord message
  let message = '';

  message += '🏠 **New Client Quote Request**\n';
  message += '━━━━━━━━━━━━━━━━━━━━\n\n';

  // Section 1: The Basics
  message += '📋 **The Basics**\n';
  message += '**Full Name:** ' + getItemValue(itemResponses, 'Full Name') + '\n';
  message += '**Email:** ' + getItemValue(itemResponses, 'Email Address') + '\n';
  message += '**Phone:** ' + getItemValue(itemResponses, 'Phone Number') + '\n';
  message += '**Service Address:**\n> ' + getItemValue(itemResponses, 'Service Address') + '\n';
  message += '**Heard About Us:** ' + getItemValue(itemResponses, 'How did you hear about us?') + '\n\n';

  // Section 2: Property Profile
  message += '🏡 **Property Profile**\n';
  message += '**Home Type:** ' + getItemValue(itemResponses, 'Home Type') + '\n';
  message += '**Sq Ft:** ' + getItemValue(itemResponses, 'Approximate Square Footage') + '\n';
  message += '**Bedrooms:** ' + getItemValue(itemResponses, 'Number of Bedrooms') + '\n';
  message += '**Bathrooms:** ' + getItemValue(itemResponses, 'Number of Bathrooms') + '\n';
  message += '**Floor Types:** ' + getItemValue(itemResponses, 'Floor Types') + '\n\n';

  // Section 3: Level of Effort
  message += '⚡ **Level of Effort**\n';
  message += '**Cleaning Type:** ' + getItemValue(itemResponses, 'Type of Cleaning Requested') + '\n';
  message += '**Occupancy:** ' + getItemValue(itemResponses, 'Occupancy') + '\n';
  message += '**Pets:** ' + getItemValue(itemResponses, 'Are there pets?') + '\n';
  message += '**Significant Shedding:** ' + getItemValue(itemResponses, 'Follow-up: "Does your pet shed significantly?"') + '\n';
  message += '**Current State:** ' + getItemValue(itemResponses, 'Current State of Home') + '\n\n';

  // Section 4: Add-ons & Specifics
  message += '✨ **Add-ons & Specifics**\n';
  message += '**Extra Services:** ' + getItemValue(itemResponses, 'Select "Extra Mile" Services') + '\n';
  message += '**Frequency:** ' + getItemValue(itemResponses, 'Preferred Frequency') + '\n';
  message += '**Access:** ' + getItemValue(itemResponses, 'Access Instructions') + '\n\n';

  // Section 5: Visuals & Notes
  message += '📝 **Visuals & Notes**\n';
  const photos = getItemValue(itemResponses, 'Photo Upload (Optional)');
  if (photos && photos !== 'No response') {
    message += '**📸 Photos Uploaded:** Yes\n';
  } else {
    message += '**📸 Photos:** None\n';
  }
  message += '**Anything else:**\n> ' + getItemValue(itemResponses, 'Anything else we should know?') + '\n';
  message += '━━━━━━━━━━━━━━━━━━━━\n';
  message += '📅 Timestamp: ' + new Date().toLocaleString();

  // Send to Discord
  sendToDiscord(message);
}

// Optional: Test function to manually trigger with the latest form response
function testWithLatestResponse() {
  const form = FormApp.getActiveForm();
  const responses = form.getResponses();

  if (responses.length === 0) {
    Logger.log('No form responses found to test with.');
    return;
  }

  // Use the most recent response
  const latestResponse = responses[responses.length - 1];
  const mockEvent = { response: latestResponse };

  onFormSubmit(mockEvent);
}

function getItemValue(responses, questionTitle) {
  for (let i = 0; i < responses.length; i++) {
    const item = responses[i];
    const title = item.getItem().getTitle();
    if (title === questionTitle) {
      return item.getResponse() || 'Not provided';
    }
  }
  return 'Not provided';
}

function sendToDiscord(message) {
  try {
    const payload = {
      content: message
    };

    const options = {
      method: 'post',
      contentType: 'application/json',
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    };

    UrlFetchApp.fetch(DISCORD_WEBHOOK_URL, options);
    Logger.log('Message sent to Discord successfully');
  } catch (error) {
    Logger.log('Error sending to Discord: ' + error.toString());
  }
}
