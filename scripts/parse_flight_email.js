#!/usr/bin/env node

/**
 * Parse flight confirmation emails from AgentMail
 * Detects United Airlines and other airline bookings
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// AgentMail API
const AGENTMAIL_API = 'https://api.agentmail.to/v1';
const INBOX_ID = 'stevieai@agentmail.to';

async function checkInbox() {
  try {
    const response = await fetch(`${AGENTMAIL_API}/mail/inbox?includeBody=true&limit=50`, {
      headers: {
        'User-Agent': 'OpenClaw-FlightParser/1.0'
      }
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.status}`);
    }

    const data = await response.json();

    if (!data.success || !data.messages) {
      return { messages: [], total: 0 };
    }

    return {
      messages: data.messages.filter(m => m.labels.includes('received') && !m.labels.includes('read')),
      total: data.count
    };
  } catch (error) {
    console.error('Error checking inbox:', error.message);
    return { messages: [], total: 0, error: error.message };
  }
}

function detectFlightEmail(message) {
  const subject = message.subject || '';
  const from = message.from || '';
  const body = message.body || '';
  const attachments = message.attachments || [];

  const lowerSubject = subject.toLowerCase();
  const lowerBody = body.toLowerCase();

  // Flight detection patterns
  const flightPatterns = [
    // United Airlines
    { regex: /\b(?:eTicket|Itinerary)\b.*\bConfirmation\b/i, airline: 'United', codePattern: /\b(?:confirmation\s+)([A-Z0-9]{4,6})\b/i },
    { regex: /\bMS[A-Z0-9]{4,6}\b/i, airline: 'United', codePattern: /\bMS([A-Z0-9]{4,6})\b/i },
    { regex: /\bunited\.\s*united\.com\b/i, airline: 'United', codePattern: /(?:ticket|confirmation)\s*[:\s]*\s*([A-Z0-9]{4,6})/i },
    
    // American Airlines
    { regex: /\bAmerican\s*Airlines\b/i, airline: 'American', codePattern: /(?:confirmation|record\s+)([A-Z0-9]{4,6})\b/i },
    { regex: /\bAA[A-Z0-9]{4,6}\b/i, airline: 'American', codePattern: /\bAA([A-Z0-9]{4,6})\b/i },
    
    // Delta
    { regex: /\bDelta\s+Flight\b/i, airline: 'Delta', codePattern: /(?:confirmation|ticket)\s*[:\s]*\s*([A-Z0-9]{4,6})/i },
    { regex: /\bDL[A-Z0-9]{4,6}\b/i, airline: 'Delta', codePattern: /\bDL([A-Z0-9]{4,6})\b/i },
    
    // Generic flight indicators
    { regex: /\bflight\b/i, airline: 'Unknown', codePattern: /(?:confirmation|reservation|booking)(?:\s*[#]*\s*([A-Z0-9]{4,6})/i },
    { regex: /\b(?:boarding\s+pass|e[-]?ticket)\b/i, airline: 'Unknown', codePattern: /(?:ticket#|eticket)(?:\s*[#]*\s*([A-Z0-9]{4,6})/i }
  ];

  for (const pattern of flightPatterns) {
    const match = subject.match(pattern.regex);
    if (match) {
      // Extract confirmation code
      const codeMatch = subject.match(pattern.codePattern);
      const confirmationCode = codeMatch ? codeMatch[1] || codeMatch[0] : null;

      return {
        type: 'flight',
        airline: pattern.airline,
        confirmationCode: confirmationCode,
        confidence: 'high'
      };
    }
  }

  return {
    type: 'unknown',
    airline: null,
    confirmationCode: null,
    confidence: 'low'
  };
}

function extractFlightDetails(message) {
  const { confirmationCode, airline } = detectFlightEmail(message);
  const body = message.body || '';
  const subject = message.subject || '';

  if (!confirmationCode) {
    return null;
  }

  // Extract flight number
  const flightPatterns = [
    { regex: /\bFlight\s*[:#]\s*([A-Z]{2}\s*\d{3,4}\b/gi },
    { regex: /\b(?:Flight|Flight\s+No)[.:]?\s*([A-Z]{2})(?:\s*\d{3,4})?/gi },
    { regex: /\b(?:Flight\s*No)[.:]?\s*([A-Z]{2})(?:\s*\d{3,4})?/gi },
    { regex: /\b(?:United\s+Flight\s*No)[.:]?\s*([A-Z]{2})(?:\s*\d{3,4})?/gi }
  ];

  let flightNumber = null;
  for (const pattern of flightPatterns) {
    const match = body.match(pattern.regex) || subject.match(pattern.regex);
    if (match) {
      flightNumber = match[1];
      break;
    }
  }

  // Extract route (origin/destination)
  const routePatterns = [
    { regex: /\b(?:from|departing?|origin)\s*:?\s*([A-Z]{3,4})\s*(?:to|arriving?|destination)\s*:?\s*([A-Z]{3,4})\b/gi },
    { regex: /\b([A-Z]{3,4})\s*→\s*([A-Z]{3,4})\b/gi },
    { regex: /\b(?:DEN|CVG|DFW|ORD|ATL|SFO|LAX|JFK|BOS|SEA|MSP)\b.*\b(?:to|→)\s*([A-Z]{3,4})\b/gi }
  ];

  let origin = null;
  let destination = null;
  for (const pattern of routePatterns) {
    const match = body.match(pattern.regex);
    if (match) {
      origin = match[1];
      destination = match[2];
      break;
    }
  }

  // Extract date and time
  const dateTimePatterns = [
    { regex: /\b(?:departure|depart|depart)\s*:?\s*(?:on\s*)?(\d{1,2}[/-]\d{1,2}[/-]\d{4})\b/gi },
    { regex: /\b(?:departure|depart)\s*:?\s*(?:on\s*)?(\d{1,2}[/-]\d{1,2}[/-]\d{4})\b/gi },
    { regex: /(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*\d{1,2},?\s*\d{4}/gi }
  ];

  let departureDate = null;
  for (const pattern of dateTimePatterns) {
    const match = body.match(pattern.regex);
    if (match) {
      departureDate = match[1];
      break;
    }
  }

  // Extract passengers
  const passengerPatterns = [
    { regex: /\bpassengers?\s*:?\s*(?:for|:)\s*([^.\n\r]+)/gi },
    { regex: /\btravelers?\s*:?\s*(?:for|:)\s*([^.\n\r]+)/gi }
  ];

  let passengers = null;
  for (const pattern of passengerPatterns) {
    const match = body.match(pattern.regex);
    if (match) {
      passengers = match[1].trim();
      break;
    }
  }

  return {
    confirmationCode,
    airline,
    flightNumber,
    origin,
    destination,
    departureDate,
    passengers: passengers,
    messageId: message.messageId,
    timestamp: message.timestamp
  };
}

function addFlightToMonitor(flightDetails) {
  const flightsFile = path.join(__dirname, '../tasks/flights.md');
  const flightsPath = path.join(__dirname, '../tasks/flights.md');
  
  if (!fs.existsSync(flightsPath)) {
    console.log('Flight monitor file not found. Creating it...');
    return false;
  }

  const flightsContent = fs.readFileSync(flightsPath, 'utf-8');

  // Check if flight already exists in the monitor table
  const flightExists = flightsContent.includes(`| ${flightDetails.confirmationCode} |`);

  if (flightExists) {
    return { exists: true };
  }

  // Add flight to monitor table
  const newFlight = `| ${flightDetails.confirmationCode} | ${flightDetails.flightNumber || 'TBD'} | ${flightDetails.airline} | ${flightDetails.origin || 'TBD'} → ${flightDetails.destination || 'TBD'} | ${flightDetails.departureDate || 'TBD'} | ${flightDetails.passengers || 'TBD'} | ${new Date().toISOString().slice(0, 19)} | | |`;

  fs.appendFileSync(flightsPath, newFlight, 'utf-8');

  console.log(`✅ Flight added to monitor: ${flightDetails.confirmationCode} (${flightDetails.airline})`);
  return { added: true, exists: false };
}

// Main execution
async function main() {
  console.log('🔍 Scanning AgentMail for flight confirmations...\n');

  const { messages, total } = await checkInbox();

  if (messages.length === 0) {
    console.log('📭 No new messages found.');
    return;
  }

  console.log(`📧 Found ${messages.length} unread messages (scanning ${total} total)`);

  const flights = [];
  const hotelBookings = [];

  for (const message of messages) {
    const detection = detectFlightEmail(message);

    if (detection.type === 'flight' && detection.confidence === 'high') {
      const flightDetails = extractFlightDetails(message);
      
      if (flightDetails && flightDetails.confirmationCode) {
        const result = addFlightToMonitor(flightDetails);
        flights.push({
          ...flightDetails,
          monitorResult: result
        });
      }
    } else if (lowerSubject.includes('hotel') || lowerBody.includes('hotel') || lowerSubject.includes('egencia')) {
      hotelBookings.push({
        subject: message.subject,
        messageId: message.messageId
      });
    }
  }

  console.log('\n📊 Results:');
  console.log(`  Flights detected: ${flights.length}`);
  console.log(`  Hotel bookings: ${hotelBookings.length}`);

  if (flights.length > 0) {
    console.log('\n✈️ Flights added to monitor:');
    console.table(flights.map(f => ({
      'Code': f.confirmationCode,
      'Flight': f.flightNumber || 'TBD',
      'Airline': f.airline,
      'Route': `${f.origin || '?'} → ${f.destination || '?'}`,
      'Date': f.departureDate || '?',
      'Status': 'Monitoring'
    })));
  }

  if (hotelBookings.length > 0) {
    console.log('\n🏨 Hotel bookings found:');
    hotelBookings.forEach(h => {
      console.log(`  - ${h.subject}`);
    });
  }

  const summary = {
    timestamp: new Date().toISOString(),
    totalScanned: total,
    flightsFound: flights.length,
    hotelsFound: hotelBookings.length
  };

  console.log('\n📝 Summary:', JSON.stringify(summary, null, 2));
}

main().catch(error => {
  console.error('❌ Error:', error.message);
  process.exit(1);
});
