"""
OCR on 360 Images — Hands-On Demo
==================================

Run text recognition on a panoramic image using PanoOCR and explore the results.

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

SAMPLE_IMAGE = "assets/sample_panorama.jpg"

# ---------------------------------------------------------------------------
# 2. Load a sample panorama
#    Place an equirectangular panorama at assets/sample_panorama.jpg, or
#    this script will download one from Google Street View automatically.
# ---------------------------------------------------------------------------

if not os.path.exists(SAMPLE_IMAGE):
    print("No sample image found. Downloading from Google Street View...")
    from streetlevel import streetview

    # Near MIT Media Lab — a spot with plenty of visible text
    pano = streetview.find_panorama(42.3625, -71.0862)
    if pano:
        os.makedirs("assets", exist_ok=True)
        streetview.download_panorama(pano, SAMPLE_IMAGE, zoom=4)
        print(f"Downloaded panorama {pano.id} ({pano.date})")
    else:
        raise FileNotFoundError(
            "Could not find a panorama. "
            "Please place an image at assets/sample_panorama.jpg"
        )

img = Image.open(SAMPLE_IMAGE)
print(f"Image size: {img.size[0]} x {img.size[1]}")

plt.figure(figsize=(16, 8))
plt.imshow(img)
plt.axis("off")
plt.title("Sample Panorama (equirectangular)")
plt.tight_layout()
plt.show()

# ---------------------------------------------------------------------------
# 3. Set up the OCR engine
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
# 4. Run OCR on the panorama
#    PanoOCR generates perspective views, runs the engine on each,
#    converts results to spherical coords, and deduplicates.
#    This may take a minute depending on image size and your machine.
# ---------------------------------------------------------------------------

from panoocr import PanoOCR

pano_ocr = PanoOCR(engine)
result = pano_ocr.recognize(SAMPLE_IMAGE)

print(f"Found {len(result.results)} text detections")

# ---------------------------------------------------------------------------
# 5. Explore the results
#    Each result has:
#      text       — the recognized text
#      yaw        — horizontal position in degrees (-180 to 180)
#      pitch      — vertical position in degrees (-90 to 90)
#      confidence — OCR confidence score
#      width, height — angular size in degrees
# ---------------------------------------------------------------------------

sorted_results = sorted(result.results, key=lambda r: r.confidence, reverse=True)

print(f"\n{'Text':<30} {'Yaw':>6} {'Pitch':>6} {'Conf':>5}")
print("-" * 52)
for r in sorted_results[:20]:
    text_display = r.text[:28] + ".." if len(r.text) > 30 else r.text
    print(f"{text_display:<30} {r.yaw:>6.1f} {r.pitch:>6.1f} {r.confidence:>5.2f}")

# ---------------------------------------------------------------------------
# 6. Save results as JSON
#    The JSON file works with PanoOCR's interactive 3D preview tool.
# ---------------------------------------------------------------------------

output_path = "assets/ocr_results.json"
result.save_json(output_path)
print(f"\nResults saved to {output_path}")

# ---------------------------------------------------------------------------
# 7. Visualize: plot detection positions on the panorama
# ---------------------------------------------------------------------------

yaws = [r.yaw for r in result.results]
pitches = [r.pitch for r in result.results]
confs = [r.confidence for r in result.results]

fig, ax = plt.subplots(figsize=(16, 8))
ax.imshow(img, extent=[-180, 180, -90, 90], aspect="auto", alpha=0.5)
scatter = ax.scatter(yaws, pitches, c=confs, cmap="viridis", s=20, alpha=0.8)
plt.colorbar(scatter, label="Confidence")
ax.set_xlabel("Yaw (degrees)")
ax.set_ylabel("Pitch (degrees)")
ax.set_title("OCR Detections on Panorama")
plt.tight_layout()
plt.show()

# ---------------------------------------------------------------------------
# 8. Interactive 3D preview (optional)
#    For a much richer visualization, use PanoOCR's web-based preview tool:
#
#      git clone https://github.com/yz3440/panoocr.git
#      cd panoocr/preview
#      python -m http.server 8000
#
#    Then open http://localhost:8000 and drag in:
#      1. The panorama image  (assets/sample_panorama.jpg)
#      2. The JSON results    (assets/ocr_results.json)
#
#    You'll see the OCR results positioned on an interactive 3D sphere.
# ---------------------------------------------------------------------------
