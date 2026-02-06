"""
OCR on 360 Images — Hands-On Demo
==================================

Run text recognition on panoramic images using PanoOCR and explore the results.

This demo processes two 360° photos:
  - Cambridge Central Square — graffiti alley & H-Mart parking lot
  - Bushwick, Brooklyn — under the elevated train tracks & storefronts

PanoOCR handles the hard part automatically:
  1. Splits the equirectangular panorama into overlapping perspective views
  2. Runs an OCR engine on each view
  3. Converts results to spherical coordinates (yaw/pitch)
  4. Deduplicates overlapping detections

Documentation: https://yz3440.github.io/panoocr/

Prerequisites
-------------
  macOS:         pip install "panoocr[macocr]"
  Windows/Linux: pip install "panoocr[paddleocr]"
"""

import os
import platform

from PIL import Image
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# 1. Configuration
# ---------------------------------------------------------------------------

PANORAMAS = [
    {
        "image": "assets/cambridge-central-square-pano.jpg",
        "json": "assets/cambridge-central-square-ocr.json",
        "label": "Cambridge Central Square — Graffiti Alley & H-Mart",
    },
    {
        "image": "assets/bushwick-test-pano.jpg",
        "json": "assets/bushwick-test-ocr.json",
        "label": "Bushwick, Brooklyn — Elevated Train & Storefronts",
    },
]

# ---------------------------------------------------------------------------
# 2. Set up the OCR engine
#    MacOCR on macOS (Apple Vision Framework), PaddleOCR elsewhere.
# ---------------------------------------------------------------------------

if platform.system() == "Darwin":
    from panoocr.engines.macocr import MacOCREngine

    engine = MacOCREngine()
    print("Using MacOCR (Apple Vision Framework)")
else:
    from panoocr.engines.paddleocr import PaddleOCREngine

    engine = PaddleOCREngine()
    print("Using PaddleOCR")

# ---------------------------------------------------------------------------
# 3. Set up PanoOCR with 90° FOV, 2000px perspective views
# ---------------------------------------------------------------------------

from panoocr import PanoOCR
from panoocr.image.perspectives import generate_perspectives

perspectives = generate_perspectives(fov=90, resolution=2000, overlap=0.5)
pano_ocr = PanoOCR(engine, perspectives=perspectives)

# ---------------------------------------------------------------------------
# 4. Process each panorama
# ---------------------------------------------------------------------------

for pano in PANORAMAS:
    image_path = pano["image"]
    json_path = pano["json"]
    label = pano["label"]

    print(f"\n{'=' * 60}")
    print(f"  {label}")
    print(f"{'=' * 60}")

    if not os.path.exists(image_path):
        print(f"  Skipping — image not found: {image_path}")
        continue

    # Load image
    img = Image.open(image_path)
    print(f"Image size: {img.size[0]} x {img.size[1]}")

    # Run OCR
    result = pano_ocr.recognize(image_path)
    print(f"Found {len(result.results)} text detections")

    # Print top results
    sorted_results = sorted(result.results, key=lambda r: r.confidence, reverse=True)

    print(f"\n{'Text':<30} {'Yaw':>6} {'Pitch':>6} {'Conf':>5}")
    print("-" * 52)
    for r in sorted_results[:20]:
        text_display = r.text[:28] + ".." if len(r.text) > 30 else r.text
        print(f"{text_display:<30} {r.yaw:>6.1f} {r.pitch:>6.1f} {r.confidence:>5.2f}")

    # Save JSON
    result.save_json(json_path)
    print(f"\nResults saved to {json_path}")

    # Visualize
    yaws = [r.yaw for r in result.results]
    pitches = [r.pitch for r in result.results]
    confs = [r.confidence for r in result.results]

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.imshow(img, extent=[-180, 180, -90, 90], aspect="auto", alpha=0.5)
    scatter = ax.scatter(yaws, pitches, c=confs, cmap="viridis", s=20, alpha=0.8)
    plt.colorbar(scatter, label="Confidence")
    ax.set_xlabel("Yaw (degrees)")
    ax.set_ylabel("Pitch (degrees)")
    ax.set_title(f"OCR Detections — {label}")
    plt.tight_layout()
    plt.show()

# ---------------------------------------------------------------------------
# 5. Interactive 3D preview
#    Open the preview tool to visualize OCR results on the panorama sphere:
#
#      cd preview
#      python -m http.server 8000
#
#    Then open http://localhost:8000 — the panorama and OCR results load
#    automatically from the assets/ directory.
#
#    You can also drag in different panorama images and JSON result files.
# ---------------------------------------------------------------------------
