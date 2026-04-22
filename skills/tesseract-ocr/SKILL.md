---
name: tesseract-ocr
description: Tesseract OCR for image text extraction when vision LLMs are unavailable. Use for bowling scoreboards, receipts, documents, and other images where ZAI vision models are failing or unavailable. Includes image pre-processing techniques to improve OCR accuracy.
---

# Tesseract OCR

Use Tesseract CLI to extract text from images when vision LLMs are unavailable, rate-limited, or aborting requests.

## Quick start

Basic OCR extraction:
```
bash scripts/ocr.sh /path/to/image.jpg
```

## When to use this skill

- Vision LLMs (GLM-4.5V, GLM-4.6V) are failing or unavailable
- You need a reliable OCR fallback
- Working with complex documents (bowling scoreboards, receipts, forms)
- Rate limiting prevents frequent vision model calls

## Basic usage

Extract text from an image:
```
scripts/ocr.sh /path/to/image.jpg
```

Extract with specific pre-processing:
```
scripts/ocr.sh /path/to/image.jpg --threshold --sharpen
```

**All options for bowling scoreboards**:
```
scripts/ocr.sh /path/to/image.jpg --numbers --threshold --grayscale --psm 6 --despeckle --deskew --morph
```

**Additional cleanup** (requires ImageMagick):
- `--despeckle`: Removes small specks and noise spots
- `--deskew`: Auto-straightens angled/skewed images
- `--morph`: Morphology operations to open and clean text areas

**Note**: Default DPI is now 600 (much better than Tesseract's 300 default for detailed text and small numbers).

## Working configuration for bowling scoreboards

**Best results found:**
```
scripts/ocr.sh /path/to/image.jpg --numbers --threshold --grayscale --psm 6
```

**What this does:**
- `--numbers`: Restricts to digits 0-9 and basic punctuation (dots, dashes, slashes)
- `--threshold`: Applies 70% adaptive thresholding (converts grayscale to black/white)
- `--grayscale`: Converts to grayscale to reduce color noise
- `--psm 6`: Treats image as single text block (good for scoreboards)
- 600 DPI: Higher resolution than Tesseract's 300 default

**Requires ImageMagick**: Pre-processing features (--threshold, --sharpen, --grayscale) only work with ImageMagick installed.

## Improving OCR accuracy

See [IMPROVEMENTS.md](references/IMPROVEMENTS.md) for techniques to enhance Tesseract results on bowling scoreboards and other difficult documents.

### Common issues with bowling scoreboards

**Challenge**: Bowling scoreboards often have:
- Low contrast (dark LCD displays)
- Glare/reflection from glass
- Digital display artifacts
- Small text in complex layouts

**Symptoms**:
- Garbled characters
- Missed numbers
- Numbers read as letters (e.g., "5" → "S")
- Frame markers confused with scores

## Tesseract vs Vision LLMs

| Factor | Tesseract | Vision LLM |
|---------|------------|--------------|
| Speed | Fast | Slower |
| Accuracy | Variable | Higher (usually) |
| Context | None (raw text) | Understands layout/meaning |
| Cost | Free | API charges |
| Setup | Local install | API subscription |

**Recommendation**: Use Tesseract for raw extraction, then clean/parse results. Use vision LLMs when available for understanding context.
