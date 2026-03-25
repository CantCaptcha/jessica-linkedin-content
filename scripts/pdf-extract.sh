#!/bin/bash
# PDF Text Extractor Wrapper for Stevie
# Usage: pdf-extract <input.pdf> [output.txt]

set -e

if [ -z "$1" ]; then
    echo "❌ Error: No input PDF specified"
    echo "Usage: pdf-extract <input.pdf> [output.txt]"
    exit 1
fi

INPUT_PDF="$1"
OUTPUT_TXT="${2:-/tmp/extracted-pdf.txt}"

echo "📄 Extracting text from: $INPUT_PDF"

# Run pdftotext
pdftotext "$INPUT_PDF" -o "$OUTPUT_TXT"

if [ $? -eq 0 ]; then
    echo "✅ Extraction complete!"
    echo "📄 Output: $OUTPUT_TXT"
    
    # Show size and line count
    SIZE=$(du -h "$OUTPUT_TXT" | cut -f1)
    LINES=$(wc -l < "$OUTPUT_TXT")
    echo "📊 Stats: $SIZE, $LINES lines"
else
    echo "❌ Extraction failed"
    exit 1
fi
