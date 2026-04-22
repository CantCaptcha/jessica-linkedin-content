#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

// Simple MIME boundary parser
function extractAttachments(emlPath, outputDir) {
    const emlContent = fs.readFileSync(emlPath, 'utf8');
    const attachments = [];

    // Find all attachment blocks
    const attachmentPattern = /Content-Type: application\/pdf[^]*\r\nContent-Transfer-Encoding: base64[^]*\r\n(?:Content-Disposition: attachment[^]*\r\n)?(?:Content-ID: [^]*\r\n)?(?:X-Attachment-Id: [^]*\r\n)?(?:Content-Disposition: attachment; filename="([^"]+)"[^]*\r\n)?\r\n([A-Za-z0-9+/=]+)/gi;

    let match;
    while ((match = attachmentPattern.exec(emlContent)) !== null) {
        const filename = match[1] || 'attachment.pdf';
        const base64Data = match[2];

        // Clean up base64 (remove line breaks and whitespace)
        const cleanBase64 = base64Data.replace(/\s/g, '');

        // Decode base64
        try {
            const buffer = Buffer.from(cleanBase64, 'base64');

            // Check if it's a valid PDF
            const pdfHeader = buffer.slice(0, 4).toString();
            if (pdfHeader === '%PDF') {
                attachments.push({
                    filename: filename,
                    size: buffer.length,
                    buffer: buffer
                });
                console.log(`Found valid PDF: ${filename} (${buffer.length} bytes)`);
            } else {
                console.log(`Skipping invalid PDF: ${filename} (header: ${pdfHeader})`);
            }
        } catch (err) {
            console.log(`Failed to decode ${filename}: ${err.message}`);
        }
    }

    // Save attachments
    for (const att of attachments) {
        const outputPath = path.join(outputDir, att.filename);
        fs.writeFileSync(outputPath, att.buffer);
        console.log(`✓ Saved: ${att.filename} (${att.size} bytes)`);
    }

    return attachments;
}

const emlPath = '/home/rwhitaker/.openclaw/workspace/msp-rfps/raw_message.eml';
const outputDir = '/home/rwhitaker/.openclaw/workspace/msp-rfps';

console.log('Extracting attachments from:', emlPath);
console.log('='*60);

const attachments = extractAttachments(emlPath, outputDir);

console.log('\n' + '='*60);
console.log(`Total attachments extracted: ${attachments.length}`);
