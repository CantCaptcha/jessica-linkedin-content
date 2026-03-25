#!/bin/bash
# PDF Parsing Setup Script
# Run this manually, then let Stevie know when complete

set -e

echo "📄 Setting up PDF parsing..."

# Check if already installed
if command -v pdftotext &>/dev/null; then
    echo "✅ pdftotext already installed!"
    pdftotext -v
    exit 0
fi

# Install poppler-utils (contains pdftotext)
echo "📦 Installing poppler-utils..."
sudo apt-get update -qq
sudo apt-get install -y poppler-utils

# Verify installation
if command -v pdftotext &>/dev/null; then
    echo ""
    echo "✅ Installation complete!"
    echo "📄 Command: pdftotext"
    echo ""
    echo "Usage:"
    echo "  pdftotext <input.pdf> -o <output.txt>"
    echo "  pdftotext <input.pdf> - | cat  # Pipe output directly"
    echo ""
    echo "Test:"
    echo "  pdftotext ~/Downloads/example.pdf -o /tmp/extracted.txt"
else
    echo "❌ Installation failed"
    exit 1
fi
