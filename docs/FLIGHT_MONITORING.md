# Flight Monitoring System - User Guide

## Quick Start

**Automatic Flight Monitoring:**
- Forward flight confirmation emails to `stevieai@agentmail.to`
- Stevie automatically detects and adds flights to monitor
- Stevie checks flight status every few hours
- You get Discord alerts for delays, cancellations, gate changes

**Manual Flight Monitoring:**
- Tell Stevie: "Watch flight UA1234"
- Stevie tracks that specific flight
- Tell Stevie: "Stop watching UA1234" to end monitoring
- Total control over what gets tracked

---

## Flight Parser Details

**What I Detect:**

| Airline | Email Pattern | Confirmation Code Format |
|----------|-----------------|-------------------------|
| United Airlines | "eTicket Itinerary and Receipt for Confirmation..." | MSXXXXXX |
| United Airlines | "Flight MS1234" | MS + 2 digits |
| American Airlines | "Confirmation..." | AAXXXXXXX or AA + 6 digits |
| Delta | "Confirmation..." | DL + 6 digits |

**What I Extract:**
- Confirmation code (MS/DL/AA patterns)
- Flight number (when available in email body)
- Route (origin → destination)
- Departure date/time
- Passenger names

---

## Flight Status Checker

**Supported Airlines:**
✅ **United Airlines** — Checks united.com
✅ **American Airlines** — Checks aa.com  
✅ **Delta** — Checks delta.com

**Status Check Types:**
- 🕐 **Delayed** — Flight is delayed (with delay duration if available)
- 🚫 **Cancelled** — Flight is cancelled
- 🚶 **On Time** — Gate change, boarding time update
- ✅ **Boarding** — Gate assigned, ready to board
- ✅ **Landed** — Flight has arrived
- ❓ **Unknown** — Could not determine status

**Check Frequency:** Every 2-3 hours
**Log Location:** `logs/flight_status_checks.log`

---

## Manual Commands

**Add Flight to Monitor:**
```
Watch flight UA1234
```

**Check Flight Status:**
```bash
node scripts/check_flight_status.js UA1234
```

**Check All Flights:**
```bash
node scripts/check_flight_status.js
```

**View Flight Monitor:**
```bash
cat tasks/flights.md
```

**View Status Logs:**
```bash
cat logs/flight_status_checks.log
```

---

## Status Alerting

**Discord Channel:** `#bot`
**Alert Conditions:**
- Any status change (scheduled → delayed → on time → boarded → landed → cancelled)
- Significant delays (>30 minutes)
- Cancellations

**Departure Day Alerting:**
- On departure day, check frequency increases to every 2 hours
- Alerts sent if any changes from "scheduled" status

---

## Workflow Example

**Scenario: You book a flight to Miami**

1. **You receive confirmation email** from United: "eTicket Itinerary... Confirmation MS123456"
2. **You forward to Stevie** (stevieai@agentmail.to)
3. **Stvie parses email** → Extracts code: MS123456, flight details
4. **Stvie adds to monitor** → Creates entry in `tasks/flights.md`
5. **Stvie confirms** → "✅ Flight added: MS123456 (United) → CVG → MIA | 2024-04-15 08:00 | Monitoring"

**Now monitoring is active!**
- Stevie checks status every few hours
- On departure day, checks more frequently
- You get Discord alerts for any status changes

**Manual trigger example:**
```
You: Watch flight MS123456
Stevie: ✅ Watching MS123456 (United) → CVG → MIA | Departure: 2024-04-15 08:00 | Monitoring
```

---

## Files

| File | Purpose |
|-------|----------|
| `scripts/parse_flight_email.js` | Parse flight confirmations from AgentMail |
| `scripts/check_flight_status.js` | Check flight status on airline websites |
| `tasks/flights.md` | Track all monitored flights |
| `logs/flight_status_checks.log` | Status check history |

---

## Tips

**Forward flight emails immediately** — Don't wait until later, Stevie can detect them right away
**Use consistent subject lines** — Include airline name in manual adds (e.g., "United flight UA1234")
**Check status manually** — Use the command if you need an immediate update

---

**Questions or Issues?**

1. Forward a flight confirmation and Stevie didn't detect it?
2. Want to check a specific flight's status right now?
3. Flight status not updating?
4. Want to stop monitoring a flight?

Just ask Stevie! I'm ready to help. 🖤
