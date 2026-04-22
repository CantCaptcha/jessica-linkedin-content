# Cleaning Service Quote Automation

**Created:** 2026-04-02 03:08 AM
**Status:** Setup phase (paused 2026-04-03)
**Discord Channel:** #project
**Project Owner:** Richard Whitaker

## Workflow

1. Customer fills out Google Form
2. Form results posted to Discord #project channel
3. Stevie reads form data from Discord
4. Stevie generates professional quotation
5. Quote delivered to customer (method TBD)

## Google Form URL
https://forms.gle/BFQiaQb4oUQZPW698

## What's Done ✅

- [x] Google Form created and live
- [x] Discord webhook configured (#project channel)
- [x] `form-to-discord.js` script created and tested
- [x] Form data posted to Discord on submission

## What's TBD (Need from Richard) 📋

- [ ] **Google Form field structure** — Full list of questions asked
- [ ] **Pricing model** — How pricing works (per sq ft, per hour, per service, base rate + add-ons?)
- [ ] **Quote format/template** — Email, PDF document, Discord reply to customer?
- [ ] **Business info** — Company name, contact details, policies, terms, etc.
- [ ] **Quote delivery method** — Email from Richard's account, automated Discord reply, or manual?
- [ ] **Quote calculation logic** — Base price formula, add-ons pricing, frequency discounts, etc.

## Project Files

- `/home/rwhitaker/.openclaw/workspace/projects/cleaning-service-quotes.md` — This file
- `/home/rwhitaker/.openclaw/workspace/cleaning-quote/` — Project directory
  - `form-to-discord.js` — Google Apps Script for webhook
  - `.git/` — Git repository initialized

## Next Steps (When Resuming)

1. **Get pricing model** from Richard (hourly rate, sq ft rate, add-ons)
2. **Get business info** (name, contact details, policies)
3. **Define quote format** (email template or document)
4. **Create quote generation script** — Calculate price based on form data
5. **Set up Discord reading** — Parse #project channel messages for form submissions
6. **Test with sample submission** — Full end-to-end test

## Important Notes

- **Paused:** 2026-04-03 14:21 — Richard taking break from project
- **No code changes needed yet** — Just configuration and business details needed
- **Form is functional** — Can collect data right now
- **Discord webhook is working** — Submissions post to #project channel

---

*Last updated: 2026-04-03 14:21* 🖤
