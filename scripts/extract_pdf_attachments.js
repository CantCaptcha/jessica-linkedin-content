#!/usr/bin/env node
const { MailParser } = require('mailparser-mit');
const fs = require('fs');
const path = require('path');

async function extractPDFs() {
    const emlPath = '/home/rwhitaker/.openclaw/workspace/msp-rfps/raw_message.eml';
    const outputDir = '/home/rwhitaker/.openclaw/workspace/msp-rfps';

    console.log('Parsing EML file:', emlPath);

    // Read the EML file
    const emlContent = fs.readFileSync(emlPath);

    // Create parser
    const parser = new MailParser();

    // Parse the email
    const parsed = await new Promise((resolve, reject) => {
        parser.write(emlContent);
        parser.end();

        parser.on('end', resolve);
        parser.on('error', reject);
    });

    console.log('\nEmail structure:');
    console.log('  Subject:', parsed.subject);
    console.log('  From:', parsed.from ? parsed.from.text || parsed.from : 'Unknown');
    console.log('  Has attachments?', parsed.attachments ? parsed.attachments.length : 0);

    // Extract PDF attachments
    if (parsed.attachments && parsed.attachments.length > 0) {
        console.log('\nAll attachments:');
        for (const att of parsed.attachments) {
            console.log(`  - ${att.contentType}: filename=${att.filename}, size=${att.size}`);
        }
        console.log('\nExtracting PDFs...\n');

        for (const att of parsed.attachments) {
            if (att.contentType === 'application/pdf' && att.filename) {
                const outputPath = path.join(outputDir, att.filename);

                console.log(`Processing: ${att.filename}`);
                console.log(`  Size: ${att.size} bytes`);

                // Save attachment
                fs.writeFileSync(outputPath, att.content);

                const savedSize = fs.statSync(outputPath).size;
                console.log(`  ✓ Saved (${savedSize} bytes)\n`);
            } else {
                console.log(`Skipping: ${att.filename} (${att.contentType})`);
            }
        }
    }
}

extractPDFs().catch(console.error);
