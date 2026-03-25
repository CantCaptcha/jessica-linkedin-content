#!/bin/bash
# Tesseract OCR Installation Script
# Enables PDF text extraction from image-based or scanned documents

set -e

echo "📄 Installing Tesseract OCR..."

# Check if already installed
if command -v tesseract &>/dev/null; then
    echo "✅ Tesseract already installed!"
    tesseract --version
    exit 0
fi

# Update package list
echo "📦 Updating package list..."
sudo apt-get update -qq

# Install Tesseract OCR and English language data
echo "📦 Installing tesseract-ocr..."
sudo apt-get install -y tesseract-ocr tesseract-ocr-eng

# Verify installation
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Installation successful!"
    echo ""
    echo "📄 Tesseract version:"
    tesseract --version
    echo ""
    echo "📝 Available languages:"
    tesseract --list-langs
    echo ""
    echo "📋 Usage:"
    echo "  tesseract <image.png> output.txt -l eng"
    echo "  tesseract --list-langs        # List installed languages"
    echo ""
    echo "🎯 For PDFs:"
    echo "  # First convert PDF pages to images"
    echo "  pdftoppm input.pdf output-page.png"
    echo "  # Then OCR each page"
    echo "  tesseract output-page.png page-text.txt -l eng"
    echo ""
    echo "✨ Stevie can now help process scanned PDFs!"
else
    echo "❌ Installation failed"
    exit 1
fi
