#!/usr/bin/env node

/**
 * Check flight status for monitored flights
 * Uses browser automation to check airline websites
 * Supports: United, American, Delta
 */

const https = require('https');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-extra'); // If available, otherwise use fetch

// Flight monitor file path
const flightsFile = path.join(__dirname, '../tasks/flights.md');
const outputLog = path.join(__dirname, '../logs/flight_status_checks.log');

async function readFlightsMonitor() {
  try {
    const content = fs.readFileSync(flightsFile, 'utf-8');
    const lines = content.split('\n');
    
    const flights = [];
    let currentFlight = null;
    
    for (const line of lines) {
      if (line.includes('Active Flights')) continue;
      if (!line.includes('|')) continue;
      
      const parts = line.split('|').map(p => p.trim());
      if (parts.length < 8) continue;
      
      const [code, flightNum, airline, route, date, passengers, status, start] = parts;
      if (code && flightNum && status.includes('Monitoring')) {
        currentFlight = {
          code: code.trim(),
          flightNumber: flightNum.trim(),
          airline: airline.trim(),
          route: route.trim(),
          date: date.trim(),
          passengers: passengers.trim(),
          status: 'Monitoring'
        };
        flights.push(currentFlight);
      }
    }
    
    return flights;
  } catch (error) {
    console.error('Error reading flights monitor:', error.message);
    return [];
  }
}

async function checkUnitedStatus(flight) {
  console.log(`\n🔍 Checking United flight: ${flight.flightNumber} (${flight.route})`);
  
  try {
    // Try to get status via web fetch first
    const flightSearchUrl = `https://www.united.com/en-us/fly-flight/status?q=${flight.flightNumber}`;
    
    const response = await fetch(flightSearchUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
      }
    });

    if (!response.ok) {
      return {
        status: 'unknown',
        message: 'Could not reach United website',
        url: flightSearchUrl
      };
    }

    const html = await response.text();
    
    // Parse for status indicators
    const statusPatterns = [
      { regex: /\bcancelled\b/i, status: 'cancelled' },
      { regex: /\bdelayed\b/i, status: 'delayed' },
      { regex: /\b(?:on\s*time|in\s*air)\b/i, status: 'on time' },
      { regex: /\b(?:departed|boarding)\b/i, status: 'boarding/departed' },
      { regex: /\b(?:arrived|landed)\b/i, status: 'arrived' }
    ];

    let detectedStatus = 'unknown';
    let delayInfo = null;
    
    for (const pattern of statusPatterns) {
      const match = html.match(pattern.regex);
      if (match) {
        detectedStatus = pattern.status;
        
        // Try to extract delay info
        if (pattern.status === 'delayed') {
          const delayMatch = html.match(/(?:delayed\s*by\s*)(\d+(?:\s*(?:minutes?|hours?|hrs?))?\b/gi);
          if (delayMatch) {
            delayInfo = delayMatch[2];
          }
        }
        break;
      }
    }

    return {
      status: detectedStatus,
      delayInfo: delayInfo,
      source: 'united.com',
      url: flightSearchUrl
    };

  } catch (error) {
    return {
      status: 'error',
      message: `Error checking United: ${error.message}`
    };
  }
}

async function checkAmericanStatus(flight) {
  console.log(`\n🔍 Checking American flight: ${flight.flightNumber} (${flight.route})`);
  
  try {
    const flightSearchUrl = `https://www.aa.com/flight-info/search?q=${flight.flightNumber}`;
    
    const response = await fetch(flightSearchUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
      }
    });

    if (!response.ok) {
      return {
        status: 'unknown',
        message: 'Could not reach American Airlines website',
        url: flightSearchUrl
      };
    }

    const html = await response.text();
    
    // Parse for status indicators
    const statusPatterns = [
      { regex: /\bcancelled\b/i, status: 'cancelled' },
      { regex: /\bdelayed\b/i, status: 'delayed' },
      { regex: /\b(?:on\s*time|in\s*air)\b/i, status: 'on time' },
      { regex: /\b(?:departed|boarding)\b/i, status: 'boarding/departed' },
      { regex: /\b(?:arrived|landed)\b/i, status: 'arrived' }
    ];

    let detectedStatus = 'unknown';
    
    for (const pattern of statusPatterns) {
      const match = html.match(pattern.regex);
      if (match) {
        detectedStatus = pattern.status;
        break;
      }
    }

    return {
      status: detectedStatus,
      source: 'aa.com',
      url: flightSearchUrl
    };

  } catch (error) {
    return {
      status: 'error',
      message: `Error checking American: ${error.message}`
    };
  }
}

async function checkDeltaStatus(flight) {
  console.log(`\n🔍 Checking Delta flight: ${flight.flightNumber} (${flight.route})`);
  
  try {
    const flightSearchUrl = `https://www.delta.com/flight-status/search/${flight.flightNumber}`;
    
    const response = await fetch(flightSearchUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
      }
    });

    if (!response.ok) {
      return {
        status: 'unknown',
        message: 'Could not reach Delta website',
        url: flightSearchUrl
      };
    }

    const html = await response.text();
    
    // Parse for status indicators
    const statusPatterns = [
      { regex: /\bcancelled\b/i, status: 'cancelled' },
      { regex: /\bdelayed\b/i, status: 'delayed' },
      { regex: /\b(?:on\s*time|in\s*air)\b/i, status: 'on time' },
      { regex: /\b(?:departed|boarding)\b/i, status: 'boarding/departed' },
      { regex: /\b(?:arrived|landed)\b/i, status: 'arrived' }
    ];

    let detectedStatus = 'unknown';
    
    for (const pattern of statusPatterns) {
      const match = html.match(pattern.regex);
      if (match) {
        detectedStatus = pattern.status;
        break;
      }
    }

    return {
      status: detectedStatus,
      source: 'delta.com',
      url: flightSearchUrl
    };

  } catch (error) {
    return {
      status: 'error',
      message: `Error checking Delta: ${error.message}`
    };
  }
}

function logStatusCheck(flight, result, newStatus) {
  const timestamp = new Date().toISOString();
  
  let logLine = `| ${timestamp} | ${flight.code} ${flight.flightNumber} | ${result.status} | ${result.source || result.message}`;
  
  if (result.delayInfo) {
    logLine += ` | ${result.delayInfo}`;
  }
  
  if (newStatus !== 'unknown' && newStatus !== result.status) {
    logLine += ` | STATUS CHANGED: ${result.status} → ${newStatus}`;
  }
  
  logLine += '\n';
  
  // Ensure log directory exists
  const logDir = path.dirname(outputLog);
  if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir, { recursive: true });
  }
  
  fs.appendFileSync(outputLog, logLine + '\n', 'utf-8');
  
  console.log(`📝 Logged: ${flight.code} ${flight.flightNumber} - ${result.status}`);
}

async function updateFlightStatus(flight, newStatus) {
  try {
    const content = fs.readFileSync(flightsFile, 'utf-8');
    const lines = content.split('\n');
    
    let updated = false;
    let newContent = '';
    
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      
      // Skip headers and separator
      if (!line.includes('|') || line.includes('---')) continue;
      
      const parts = line.split('|').map(p => p.trim());
      if (parts.length < 8) continue;
      
      const [code, flightNum, airline, route, date, passengers, status, start, end] = parts;
      
      // Check if this is the flight to update
      if (code.trim() === flight.code && flightNum.trim() === flight.flightNumber) {
        // Find the line with status and start times
        const statusIndex = lines.findIndex(l => l.includes(flight.code) && l.includes(flight.flightNumber));
        
        if (statusIndex !== -1) {
          const statusLine = lines[statusIndex];
          const statusParts = statusLine.split('|').map(p => p.trim());
          
          const [sCode, sFlight, sAirline, sRoute, sDate, sPass, sStatus, sStart] = statusParts;
          
          sStatus = newStatus;
          sEnd = new Date().toISOString().slice(0, 19);
          
          const updatedStatusLine = `| ${sCode} | ${sFlight} | ${sAirline} | ${sRoute} | ${sDate} | ${sPass} | ${sStatus} | ${sStart} | ${sEnd}`;
          
          // Replace the old status line
          newContent += updatedStatusLine + '\n';
          updated = true;
        }
      } else {
        newContent += line + '\n';
      }
    }
    
    if (updated) {
      fs.writeFileSync(flightsFile, newContent, 'utf-8');
      console.log(`✅ Updated flight ${flight.code} ${flight.flightNumber} status to: ${newStatus}`);
    }
    
  } catch (error) {
    console.error('Error updating flight status:', error.message);
  }
}

async function checkAllFlights() {
  const flights = await readFlightsMonitor();
  
  if (flights.length === 0) {
    console.log('📭 No flights currently being monitored.');
    return;
  }
  
  console.log(`\n✈️ Checking ${flights.length} flight(s)...\n`);
  
  for (const flight of flights) {
    let result;
    
    switch (flight.airline.trim().toLowerCase()) {
      case 'united':
        result = await checkUnitedStatus(flight);
        break;
      case 'american':
        result = await checkAmericanStatus(flight);
        break;
      case 'delta':
        result = await checkDeltaStatus(flight);
        break;
      default:
        result = {
          status: 'unknown',
          message: `Unsupported airline: ${flight.airline}`
        };
    }
    
    // Log the check
    logStatusCheck(flight, result, flight.status);
    
    // Update status if changed
    if (result.status !== 'unknown' && result.status !== flight.status) {
      await updateFlightStatus(flight, result.status);
    }
  }
}

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('📋 Flight Status Checker');
    console.log('\nUsage:');
    console.log('  node check_flight_status.js                    Check all monitored flights');
    console.log('  node check_flight_status.js <code> <flight>   Check specific flight');
    console.log('\nSupported airlines: United, American, Delta');
    console.log('\nStatus check types:');
    console.log('  - Monitoring → Delayed → On Time → Arrived → Cancelled');
    process.exit(0);
  }
  
  // Check specific flight if args provided
  if (args.length === 3 && args[0] === 'status' && args[1] && args[2]) {
    const flightCode = args[1].toUpperCase();
    const flightNumber = args[2];
    
    // Find flight in monitor
    const flights = await readFlightsMonitor();
    const flight = flights.find(f => 
      f.code.trim().toUpperCase() === flightCode && 
      f.flightNumber?.trim() === flightNumber
    );
    
    if (!flight) {
      console.log(`❌ Flight ${flightCode} ${flightNumber} not found in monitor.`);
      process.exit(1);
    }
    
    console.log(`\n✈️ Checking flight ${flightCode} ${flightNumber}...\n`);
    
    let result;
    switch (flight.airline.trim().toLowerCase()) {
      case 'united':
        result = await checkUnitedStatus(flight);
        break;
      case 'american':
        result = await checkAmericanStatus(flight);
        break;
      case 'delta':
        result = await checkDeltaStatus(flight);
        break;
      default:
        result = {
          status: 'unknown',
          message: `Unsupported airline: ${flight.airline}`
        };
    }
    
    console.log(`\n📊 Status: ${result.status.toUpperCase()}`);
    if (result.delayInfo) {
      console.log(`   Delay: ${result.delayInfo}`);
    }
    if (result.url) {
      console.log(`   Source: ${result.url}`);
    }
    
    process.exit(0);
  }
  
  // Check all flights
  await checkAllFlights();
}

main().catch(error => {
  console.error('❌ Error:', error.message);
  process.exit(1);
});
