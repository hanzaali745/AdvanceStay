# Social Media Preview Images Guide

## Overview

Each blog post needs a custom social media preview image (Open Graph image) that displays when the article is shared on Twitter, LinkedIn, Facebook, etc. This guide explains the requirements and tools to create them.

---

## Image Specifications

### Dimensions
- **Standard:** 1200 × 630 pixels (16:9 aspect ratio)
- **Square (LinkedIn):** 1200 × 1200 pixels (1:1 aspect ratio)
- **Mobile:** 600 × 315 pixels (for mobile shares)

### File Format
- **Format:** JPG or PNG
- **File size:** < 300 KB (optimized)
- **Color space:** sRGB

### Best Practices
- **Brand colors:** Use gold (#FDB022) and dark navy (#0a0e27) prominently
- **Text:** Large, readable headlines (minimum 24px)
- **Contrast:** Ensure text is readable on both light and dark backgrounds
- **Logo:** Include "The Next Gen AI" wordmark in corner
- **Consistency:** All images should follow the same design template

---

## Template Design Elements

### Header Section
- Gold stripe (4px) on left edge
- Brand name: "the**next**genai" (wordmark) in top-right corner
- Dark navy background with subtle gradient

### Content Area
- **Main headline:** Bold, white text (48-60px)
- **Subtitle:** Secondary text (18-24px) in light gray
- **Icon/Badge:** Content-type indicator (Tutorial, How-To, Tool Review, Guide)

### Footer Section
- "Verified & Tested" badge with gold accent
- Optional: Publication date
- Optional: Author name

---

## Tools to Create Images

### Option 1: Figma (Recommended)
**Best for:** Professional, branded templates

1. Sign up free at https://figma.com
2. Create a new file (1200 × 630px)
3. Set background to dark navy (#0a0e27)
4. Add:
   - Gold left stripe (4px width)
   - Blog headline (use Cera Pro font family or similar serif)
   - Small gold accent element
   - Logo in corner
5. Export as JPG/PNG
6. Save as template, duplicate for each post

**Template starting point:**
```
Background: #0a0e27
Left stripe: #FDB022 (4px)
Text color: #f0f4f9
Accent color: #4B7AFF
Logo position: top-right (120x40px)
```

### Option 2: Canva (Quick & Easy)
**Best for:** Fast creation, design inspiration

1. Go to https://canva.com
2. Create → Search "Open Graph Image" (1200×630)
3. Use dark theme template
4. Customize with:
   - Your blog headline
   - Gold accent elements
   - Brand colors
5. Download as PNG
6. Optimize with https://tinypng.com

### Option 3: Adobe Express (Free)
**Best for:** Professional results, brand kits

1. Visit https://express.adobe.com/create/social-media-graphic
2. Choose 1200×630 template
3. Upload or create:
   - Custom background
   - Text overlay
   - Brand elements
4. Download and optimize

### Option 4: Python (Automation)
**Best for:** Batch creation across many posts

Install required packages:
```bash
pip install pillow requests
```

Sample script:
```python
from PIL import Image, ImageDraw, ImageFont

def create_og_image(title, filename, category="Tutorial"):
    # Create image
    img = Image.new('RGB', (1200, 630), color='#0a0e27')
    draw = ImageDraw.Draw(img)
    
    # Add gold stripe
    draw.rectangle([(0, 0), (4, 630)], fill='#FDB022')
    
    # Add text (requires font file)
    try:
        title_font = ImageFont.truetype("fonts/CeraPro-Bold.ttf", 56)
        category_font = ImageFont.truetype("fonts/Inter-Bold.ttf", 20)
    except:
        title_font = ImageFont.load_default()
        category_font = ImageFont.load_default()
    
    # Category badge
    draw.text((50, 50), category, font=category_font, fill='#FDB022')
    
    # Title (text wrap)
    lines = title.split('\n') if '\n' in title else [title]
    y = 200
    for line in lines:
        draw.text((50, y), line, font=title_font, fill='#f0f4f9')
        y += 80
    
    # Badge
    draw.text((50, 550), "Verified & Tested", font=category_font, fill='#FDB022')
    
    img.save(filename)

# Usage
create_og_image("How to Use Claude AI Effectively", "og-claude-tutorial.png", "Tutorial")
```

---

## File Naming Convention

Name images consistently for organization:

```
og-{topic}-{type}.jpg

Examples:
- og-claude-tutorial.jpg
- og-chatgpt-review.jpg
- og-ai-productivity-guide.jpg
- og-best-ai-tools-2026.jpg
```

---

## Implementation in HTML

Update each blog post's Open Graph tags:

```html
<meta property="og:image" content="https://thenextgenai.com/images/og/og-claude-tutorial.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:type" content="image/jpeg">

<!-- Twitter Card -->
<meta name="twitter:image" content="https://thenextgenai.com/images/og/og-claude-tutorial.jpg">
<meta name="twitter:image:alt" content="How to Use Claude AI Effectively">
```

---

## Checklist Before Uploading

- [ ] Image is 1200×630px (or 1200×1200 for LinkedIn)
- [ ] File size is under 300KB
- [ ] Text is readable (minimum 18px)
- [ ] Brand colors are prominent (gold and navy)
- [ ] "Verified & Tested" badge is visible
- [ ] Logo/wordmark is in corner
- [ ] No em-dashes or special characters render incorrectly
- [ ] Gold left stripe is 4px width
- [ ] File is named with consistent convention
- [ ] Uploaded to `/images/og/` folder on server

---

## Testing

After uploading, test on each platform:

1. **Twitter:** https://cards-dev.twitter.com/validator
2. **Facebook:** https://developers.facebook.com/tools/debug/og/object/
3. **LinkedIn:** Post in draft and preview
4. **Slack:** Paste link in Slack and preview

---

## Storage Location

All images should be stored:
```
/public/images/og/
├── og-claude-tutorial.jpg
├── og-chatgpt-review.jpg
├── og-ai-productivity-guide.jpg
└── ...
```

Update the `og:image` URL in each blog post to:
```
https://thenextgenai.com/images/og/og-{topic}-{type}.jpg
```

---

## Quick Start (Next 3 Posts)

For your first three blog posts, I recommend:

1. **Use Canva** (fastest): 15 mins per image
2. **Create a template** with your brand colors
3. **Duplicate template** for each post
4. **Swap headline** and category
5. **Download & optimize** with TinyPNG
6. **Upload to server**

**Time estimate:** 1 hour for 3 complete, branded images.

---

## Resources

- **Figma:** https://figma.com (free plan available)
- **Canva:** https://canva.com (free + paid)
- **Adobe Express:** https://express.adobe.com
- **TinyPNG:** https://tinypng.com (image optimization)
- **Twitter Card Validator:** https://cards-dev.twitter.com/validator
- **Facebook Debugger:** https://developers.facebook.com/tools/debug/og/object/

---

## Next Steps

1. Create 3 sample OG images for your first blog posts
2. Test on Twitter and Facebook
3. Refine design based on feedback
4. Create 2-3 variations to test engagement
5. Build batch process for future posts

