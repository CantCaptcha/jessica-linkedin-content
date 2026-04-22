#!/usr/bin/env node
/**
 * Extract text from PDF using pdftotext
 * Usage: node pdf-to-text.js <path-to-pdf>
 */

const { execSync } = require('child_process');
const path = require('path');

const pdfPath = process.argv[2];

if (!pdfPath) {
    console.error('Usage: node pdf-to-text.js <path-to-pdf>');
    process.exit(1);
}

if (!require('fs').existsSync(pdfPath)) {
    console.error(`Error: File not found: ${pdfPath}`);
    process.exit(1);
}

console.log(`Extracting text from: ${path.basename(pdfPath)}\n`);

try {
    const result = execSync(`pdftotext "${pdfPath}"`, {
        encoding: 'utf8',
        maxBuffer: 10 * 1024 * 1024, // 10MB output buffer
        stdio: ['pipe', 'inherit'] // inherit stderr for error messages
    });

    console.log('\n=== EXTRACTED TEXT ===\n');
    console.log(result);
    
} catch (error) {
    console.error(`Error running pdftotext: ${error.message}`);
    process.exit(1);
}
