// ==========================================
// Google Form to Discord - New Client Quote
// ==========================================
// Auto-posts Google Form submissions to #project Discord channel
// For Cleaning Services Quote Request Form
// ==========================================

const DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1489256487883899070/NXyyDk1nV6b4a1vG2TBtcIWR3ycmBW13boSxSzpSRlS4qsG_zLm-4yvLfYpzrmnU-9p2';

function onFormSubmit(e) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  const responseRow = sheet.getLastRow();
  const values = sheet.getRange(responseRow, 1, 1, headers.length).getValues()[0];
  
  // Map values to headers
  const data = {};
  headers.forEach((header, index) => {
    data[header] = values[index] || '';
  });
  
  // Build Discord message
  let message = '';
  
  message += '🏠 **New Client Quote Request**\n';
  message += '━━━━━━━━━━━━━━━━━━━━\n\n';
  
  // Section 1: The Basics
  message += '📋 **The Basics**\n';
  message += '**Full Name:** ' + getValue(data, 'Full Name') + '\n';
  message += '**Email:** ' + getValue(data, 'Email Address') + '\n';
  message += '**Phone:** ' + getValue(data, 'phone number') + '\n';
  message += '**Service Address:**\n> ' + getValue(data, 'service address: include unit numbers/gate codes (if applicable)') + '\n';
  message += '**Heard About Us:** ' + getValue(data, 'How did you hear about us?') + '\n\n';
  
  // Section 2: Property Profile
  message += '🏡 **Property Profile**\n';
  message += '**Home Type:** ' + getValue(data, 'Home Type') + '\n';
  message += '**Sq Ft:** ' + getValue(data, 'Approximate Square Footage') + '\n';
  message += '**Bedrooms:** ' + getValue(data, 'Number of BedroomsNumber of Bathrooms') + '\n';
  message += '**Floor Types:** ' + getValue(data, 'Floor Types') + '\n\n';
  
  // Section 3: Level of Effort
  message += '⚡ **Level of Effort**\n';
  message += '**Cleaning Type:** ' + getValue(data, 'Type of Cleaning Requested') + '\n';
  message += '**Occupancy:** ' + getValue(data, 'Occupancy (Multiple choice: 1-2 people, 3-5 people, 6+)') + '\n';
  message += '**Pets:** ' + getValue(data, 'Are there pets? (Checkboxes: No, Dog(s), Cat(s), Other)') + '\n';
  message += '**Significant Shedding:** ' + getValue(data, 'Follow-up: "Does your pet shed significantly?" (Yes/No)') + '\n';
  message += '**Current State:** ' + getValue(data, 'Current State of Home') + '\n\n';
  
  // Section 4: Add-ons & Specifics
  message += '✨ **Add-ons & Specifics**\n';
  message += '**Extra Services:** ' + getValue(data, 'Extra Services') + '\n';
  message += '**Frequency:** ' + getValue(data, 'Preferred Frequency') + '\n';
  message += '**Access:** ' + getValue(data, 'Access Instructions') + '\n\n';
  
  // Section 5: Visuals & Notes
  message += '📝 **Visuals & Notes**\n';
  const photos = getValue(data, 'Photo Upload (Optional)');
  if (photos && photos !== '') {
    message += '**📸 Photos Uploaded:** Yes\n';
  } else {
    message += '**📸 Photos:** None\n';
  }
  message += '**Timestamp:** ' + getValue(data, 'Timestamp') + '\n';
  message += '━━━━━━━━━━━━━━━━━━━━';
  
  // Send to Discord
  sendToDiscord(message);
}

function getValue(data, key) {
  // Try exact match first
  if (data[key] !== undefined && data[key] !== '') {
    return data[key];
  }
  
  // Try partial match (for variations)
  const matchingKey = Object.keys(data).find(k => 
    k.toLowerCase().includes(key.toLowerCase().substring(0, 20))
  );
  
  if (matchingKey) {
    return data[matchingKey];
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
