# Improving Tesseract OCR Results

## Image Pre-processing for Bowling Scoreboards

### 1. Grayscale Conversion

**Why**: Reduces color noise and simplifies the image
**When to use**: Colorful displays, multiple color backgrounds
**Command**: `--grayscale`

```bash
convert input.jpg -colorspace Gray output.png
```

### 2. Thresholding

**Why**: Converts grayscale images to pure black/white, improves contrast
**When to use**: Low-contrast displays, glare, backlight issues
**Command**: `--threshold`

```bash
convert input.jpg -threshold 70% -negate output.png
```

**Tip**: Adjust threshold percentage (50-80) based on image. Lower = more aggressive.

### 3. Sharpening

**Why**: Enhances edges and makes characters more distinct
**When to use**: Slightly blurry images, small text, low resolution
**Command**: `--sharpen`

```bash
convert input.jpg -sharpen 0x1.2+1.5+0.2 output.png
```

### 4. Noise Reduction

**Why**: Removes artifacts that confuse Tesseract
**When to use**: Grainy images, scan artifacts
**ImageMagick command**:
```bash
convert input.jpg -median 3 output.png
convert input.jpg -despeckle 2 output.png
```

## Bowling Scoreboard-Specific Issues

### Digital Display Artifacts

**Problem**: LCD displays have visible pixels that confuse OCR
**Solution**:
1. Capture at higher resolution if possible
2. Use thresholding aggressively
3. Crop to scoreboard area only

### Glare and Reflection

**Problem**: Glass reflections create white/gray areas
**Solution**:
1. Change angle slightly
2. Use polarizer/anti-glare filter
3. Take photo from angle, not head-on

### Small Text

**Problem**: Frame numbers and player names are often small
**Solution**:
1. Use sharpening
2. Increase DPI/resolution
3. Test different Tesseract page segmentation modes (PSM)

## Tesseract Page Segmentation Modes (PSM)

Different modes work better for different layouts:

| Mode | Best For | Usage |
|-------|-----------|--------|
| 3 | Auto (default) | General purpose |
| 6 | Single block of text | Scoreboards, receipts |
| 7 | Single text line | Player names, totals |
| 11 | Sparse text | Frame-by-frame scores |
| 12 | Sparse with OSD | Auto-orientation text |

**To use custom PSM**:
```bash
tesseract image.jpg output -l eng --psm 6
```

## Language and Configuration

### Training Data

For better results on specific document types:
1. Collect sample images of that document type
2. Manually correct the OCR output
3. Generate Tesseract training data (.traineddata)
4. Use custom language file: `-l my-trained-data`

### Character Whitelist

**Why**: Restricts Tesseract to expected characters
**Best for**: Numbers-only displays, specific formats

**Example** (numbers only):
```bash
tesseract image.jpg output -l eng -c tessedit_char_whitelist=0123456789
```

**Example** (uppercase letters + numbers):
```bash
tesseract image.jpg output -l eng -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
```

## Post-Processing OCR Output

### Clean Up Common Errors

**Pattern substitutions** (for bowling scoreboards):
```
S → 5
O → 0
I → 1
l → 1
| → 1
```

### Validate with Context

**Check for reasonableness**:
- Bowling scores should be 0-300 per game
- Total should be ~3x individual game average
- Frame-by-frame should follow bowling rules
- Names should be consistent across games

### Use Regex Patterns

Extract structured data with confidence:
```python
import re

# Find scores (numbers typically 10-300)
scores = re.findall(r'\b(1?[0-9]{1,2}|300)\b', text)

# Find names (capitalized words, typically 3-10 letters)
names = re.findall(r'\b[A-Z][a-z]{2,9}\b', text)
```

## Testing and Iteration

### Iteration Process

1. **Capture** original image
2. **Run** basic Tesseract
3. **Identify** specific errors
4. **Apply** one pre-processing technique
5. **Compare** results
6. **Document** what works
7. **Repeat** for different techniques

### Common Failure Modes

| Symptom | Likely Cause | Fix |
|-----------|---------------|-----|
| All garbage | Severe blur/noise | Try thresholding + sharpening |
| Numbers read as letters | Low contrast | Increase threshold, use grayscale |
| Missed small text | Low resolution | Capture higher res, sharpen |
| Wrong frame numbers | Layout confusion | Try different PSM mode |

## Quick Reference Commands

```bash
# Basic OCR
scripts/ocr.sh image.jpg

# Aggressive for digital displays
scripts/ocr.sh image.jpg --threshold --grayscale

# For blurry photos
scripts/ocr.sh image.jpg --sharpen --grayscale

# All options combined
scripts/ocr.sh image.jpg --threshold --sharpen --grayscale
```
