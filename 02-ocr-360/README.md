# Chapter 2: OCR on 360 Images

> Run text recognition on panoramic images using PanoOCR, and explore the results in an interactive 3D preview.

## The Problem

OCR engines are trained on flat, perspective images — book pages, screenshots, photos taken with a regular camera. Feed them an equirectangular panorama and they'll struggle: text near the poles is heavily distorted, and the wide field of view means text appears at many different scales and orientations.

## The Solution: PanoOCR

**[PanoOCR](https://github.com/yz3440/panoocr)** is a Python library that handles this automatically. It follows the same split-process-aggregate pattern from this workshop:

1. **Split** the equirectangular panorama into multiple overlapping perspective views
2. **Run OCR** on each perspective view using your choice of engine
3. **Convert** bounding box results from 2D image coordinates to spherical coordinates (yaw/pitch)
4. **Deduplicate** overlapping detections across views

The output is a list of text detections positioned in spherical coordinates on the panorama.

![PanoOCR pipeline diagram](assets/panoocr-pipeline.png)

### Documentation

- GitHub: [github.com/yz3440/panoocr](https://github.com/yz3440/panoocr)
- Docs: [yz3440.github.io/panoocr](https://yz3440.github.io/panoocr/)

## Project Inspiration: all text in nyc

![all text in nyc screenshot](assets/alltext-nyc-screenshot.png)

**[all text in nyc](https://alltext.nyc)** is a search engine and visualization tool that lets you drift through NYC's textual landscape. The project applied OCR to **8 million+** Google Street View panoramas spanning 2007–2024, extracting **138 million+** text snippets — shop signs, graffiti, advertisements, protest signs, street names, and everything else visible on the city's surfaces.

The project received coverage in Fast Company, PCMag, Time Out, and was featured by The Pudding, where data storytelling revealed patterns like the concentration of "pizza" signs (111,290 results), "luxury" in new buildings, and ethnic communities identifiable through language.

**all text in nyc was built on the same PanoOCR pipeline we're using in this chapter.**

## Installation

```bash
# macOS (Apple Vision Framework — fast, accurate, recommended for Mac users)
pip install "panoocr[macocr]"

# Windows / Linux (PaddleOCR)
pip install "panoocr[paddleocr]"

# Or with other engines
pip install "panoocr[easyocr]"       # EasyOCR (cross-platform, 80+ languages)
pip install "panoocr[florence2]"     # Florence-2 (GPU recommended)
```

## Quick Start

```python
from panoocr import PanoOCR

# macOS
from panoocr.engines.macocr import MacOCREngine
engine = MacOCREngine()

# --- OR for Windows/Linux ---
# from panoocr.engines.paddleocr import PaddleOCREngine
# engine = PaddleOCREngine()

pano = PanoOCR(engine)
result = pano.recognize("my_panorama.jpg")
result.save_json("results.json")

for r in result.results:
    print(f"{r.text}  (yaw={r.yaw:.1f}°, pitch={r.pitch:.1f}°, conf={r.confidence:.2f})")
```

## Hands-On: Cambridge Central Square

We'll run PanoOCR on a 360° photo captured near the **Cambridge Central Square graffiti alley** and **H-Mart parking lot** — a spot dense with text on walls, signs, and street surfaces.

![Cambridge Central Square panorama](assets/IMG_20260207_010028_00_961.jpg)

### Step 1: Run OCR

Run the demo script to process the panorama and save the results as JSON:

```bash
cd 02-ocr-360
python ocr_demo.py
```

This will:
1. Load the panorama from `assets/IMG_20260207_010028_00_961.jpg`
2. Split it into perspective views and run OCR on each
3. Print detected text with yaw/pitch coordinates and confidence scores
4. Save results to `assets/ocr_results.json`
5. Show a matplotlib plot of detection positions overlaid on the panorama

### Step 2: Preview in 3D

Open the interactive preview to see OCR results positioned on the panorama sphere:

```bash
cd preview
python -m http.server 8000
```

Open [http://localhost:8000](http://localhost:8000) — the panorama and OCR results load automatically. You can also drag in different panorama images and JSON result files to explore other results.

### Output

The script exports `assets/ocr_results.json` in the PanoOCR format:

```json
{
  "results": [
    {
      "text": "GRAFFITI ALLEY",
      "yaw": -45.2,
      "pitch": 3.1,
      "width": 12.5,
      "height": 3.8,
      "confidence": 0.92
    }
  ]
}
```

Each detection includes the recognized `text`, its position on the sphere (`yaw`/`pitch` in degrees), angular size (`width`/`height`), and the OCR engine's `confidence` score.

---

**Previous:** [Chapter 1 — 3D Scanning from 360](../01-3d-scanning/) · **Next:** [Chapter 3 — Object Segmentation](../03-object-segmentation/)
