# Millar RFP Template Information

## Source
- From: Jessica Allen <jessica.allen@cybersecgru.com>
- Date: April 16, 2026, 12:15 PM EDT
- Subject: Template for RFP review and analysis

## Google Sheet Link
https://drive.google.com/open?id=1uZeDnYyh34YqEeG9IjkcxaL-A2IOWpfWYCkCVMZs0M8

## Template Structure (3 Tabs)

### Tab 1: Scoring Matrix
- **Purpose:** Score each MSP on specified categories
- **Initial capacity:** 2 MSP submissions
- **Note:** Must add more columns as more submissions are received
- **Categories:** Cost (15%), Technology (30%), Service Level (30%), Relationship (15%)
- **Total:** 90%

### Tab 2: Submission Summaries
- **Purpose:** Write a summary of the submission for each MSP
- **Note:** One summary per MSP submission

### Tab 3: Cost Comparison
- **Purpose:** Put costs into table for comparison
- **Initial capacity:** 2 MSP submissions
- **Note:** Must add more columns as more submissions are received

## Instructions from Jessica
- Template allows for 2 MSP submissions initially
- Will send MORE than 2 submissions
- Must add more columns to all 3 tabs as submissions are received
- **Total submissions expected: 6**
- Need to add 4 more columns (total: 6 MSP columns)

## Incoming Email Workflow
- Will receive **6 emails from Jessica**
- **Email subject:** Contains the responder's name
- **Email attachment:** Contains their RFP response (PDF or document)

## Continuation Files
- Some submissions may have **continuation files**
- **Email subject marker:** Will contain "continued" and responder's company name
- **Purpose:** Enrich the main submission with additional data
- **Handling:** Continuation files are linked to the main MSP company, not treated as separate submissions
- **File naming:** Continuation files marked with `_continued` suffix for easy identification

## Next Steps
1. Monitor for forwarded RFP submissions from Jessica
2. Download attachments to /msp-rfps/
3. Analyze each submission using scoring matrix
4. Populate all 3 tabs as submissions arrive
5. Send completed analysis when all submissions received

## Status
- ✅ **All 6 submissions downloaded successfully** (April 16, 2026 @ 5:28 PM EDT)
- ✅ **Script tested and working**
- ⏳ **Awaiting analysis of all submissions**
- ✅ **No continuation files detected yet** (6 main submissions)

## Processing Script
- Location: `/scripts/process-rfp-submissions.js`
- Usage: `node /home/rwhitaker/.openclaw/workspace/scripts/process-rfp-submissions.js`
- Features:
  * Checks for new emails from Jessica
  * Extracts MSP name from subject
  * Detects "continued" markers for continuation files
  * Downloads attachments
  * Links continuation files to main MSP submission
  * Tracks processed submissions in JSON file
  * Tracks MSP companies and their files separately
  * Skips already-downloaded files
  * Marks continuation files with `_continued` suffix
