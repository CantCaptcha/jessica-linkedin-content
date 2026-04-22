#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function extractPDFsFromEML(emlPath, outputDir) {
    const emlContent = fs.readFileSync(emlPath, 'utf8');
    const extracted = [];

    // Find the first boundary
    const boundaryMatch = emlContent.match(/boundary="([^"]+)"/);
    if (!boundaryMatch) {
        console.log('No boundary found');
        return extracted;
    }

    const boundary = boundaryMatch[1];
    console.log('Boundary:', boundary);
    console.log();

    // Split by boundary
    const parts = emlContent.split(`--${boundary}`);

    for (const part of parts) {
        // Find PDF content
        const pdfMatch = part.match(/Content-Type: application\/pdf[^]*name="([^"]+)"[^]*\r\n\r\n([\s\S]*?)(?=--|$)/i);

        if (pdfMatch) {
            const filename = pdfMatch[1];
            const base64Data = pdfMatch[2].trim();

            // Clean up base64 (remove trailing boundary if present)
            const cleanBase64 = base64Data.replace(/--[^]*$/, '');

            console.log(`Found: ${filename}`);
            console.log(`  Base64 size: ${cleanBase64.length}`);

            try {
                // Decode base64
                const buffer = Buffer.from(cleanBase64, 'base64');

                // Check if valid PDF
                const pdfHeader = buffer.slice(0, 4).toString();
                if (pdfHeader === '%PDF') {
                    const outputPath = path.join(outputDir, filename);
                    fs.writeFileSync(outputPath, buffer);

                    console.log(`  ✓ Saved (${buffer.length} bytes)\n`);
                    extracted.push({ filename, size: buffer.length });
                } else {
                    console.log(`  ✗ Invalid PDF header: ${pdfHeader}\n`);
                }
            } catch (err) {
                console.log(`  ✗ Failed to decode: ${err.message}\n`);
            }
        }
    }

    return extracted;
}

const emlPath = '/home/rwhitaker/.openclaw/workspace/msp-rfps/raw_message.eml';
const outputDir = '/home/rwhitaker/.openclaw/workspace/msp-rfps';

console.log('='.repeat(60));
console.log('Extracting PDFs from EML');
console.log('='.repeat(60));
console.log();

const extracted = extractPDFsFromEML(emlPath, outputDir);

console.log('='.repeat(60));
console.log(`Total PDFs extracted: ${extracted.length}`);
console.log('='.repeat(60));
