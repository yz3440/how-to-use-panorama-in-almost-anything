"""
Working with Google Street View Panoramas — Hands-On Demo
==========================================================

Use the streetlevel library to find, download, and explore Google Street View
panoramas around the MIT campus. No API key needed.

Documentation: https://streetlevel.readthedocs.io/

Prerequisites
-------------
  pip install streetlevel Pillow matplotlib
"""

import os
import time

from PIL import Image
import matplotlib.pyplot as plt
from streetlevel import streetview

# ---------------------------------------------------------------------------
# 1. Find a panorama near MIT Media Lab
#    find_panorama() returns the nearest GSV panorama to a lat/lon coordinate.
# ---------------------------------------------------------------------------

MIT_LAT = 42.3601
MIT_LON = -71.0868

pano = streetview.find_panorama(MIT_LAT, MIT_LON)

if pano:
    print("Found panorama!")
    print(f"  ID:       {pano.id}")
    print(f"  Location: {pano.lat:.6f}, {pano.lon:.6f}")
    print(f"  Date:     {pano.date}")
    print(f"  Link:     {pano.permalink()}")
else:
    raise RuntimeError("No panorama found nearby.")

# ---------------------------------------------------------------------------
# 2. Download and display
#    The zoom parameter controls resolution (0 = lowest, 5 = highest).
#    zoom=4 is a good balance of quality and speed.
# ---------------------------------------------------------------------------

os.makedirs("assets", exist_ok=True)
output_path = f"assets/{pano.id}.jpg"

streetview.download_panorama(pano, output_path, zoom=4)
print(f"Saved to {output_path}")

img = Image.open(output_path)
print(f"Image size: {img.size[0]} x {img.size[1]}")

plt.figure(figsize=(16, 8))
plt.imshow(img)
plt.axis("off")
plt.title(f"Google Street View — {pano.date}")
plt.tight_layout()
plt.show()

# ---------------------------------------------------------------------------
# 3. Explore metadata
#    Each panorama comes with rich metadata. Fetch full details with
#    find_panorama_by_id().
# ---------------------------------------------------------------------------

full_pano = streetview.find_panorama_by_id(pano.id)

print("\n=== Panorama Metadata ===")
print(f"ID:        {full_pano.id}")
print(f"Location:  {full_pano.lat:.6f}, {full_pano.lon:.6f}")
print(f"Date:      {full_pano.date}")
print(f"Source:    {full_pano.source}")
print(f"Copyright: {full_pano.copyright_message}")
print(f"Country:   {full_pano.country_code}")

if full_pano.elevation is not None:
    print(f"Elevation: {full_pano.elevation:.1f}m")

if full_pano.address:
    addr_str = ", ".join(a.value for a in full_pano.address)
    print(f"Address:   {addr_str}")

if full_pano.image_sizes:
    for i, size in enumerate(full_pano.image_sizes):
        print(f"Zoom {i}:    {size.x} x {size.y}")

# ---------------------------------------------------------------------------
# 4. Explore neighbors
#    Neighbors are the nearby panoramas that the white navigation arrows in
#    Google Maps Street View link to.
# ---------------------------------------------------------------------------

print(f"\nThis panorama has {len(full_pano.neighbors)} neighbors:\n")

for i, neighbor in enumerate(full_pano.neighbors):
    lat_str = f"{neighbor.lat:.6f}" if neighbor.lat else "N/A"
    lon_str = f"{neighbor.lon:.6f}" if neighbor.lon else "N/A"
    print(f"  [{i}] {neighbor.id}  ({lat_str}, {lon_str})")

# ---------------------------------------------------------------------------
# 5. Historical imagery
#    Google often has multiple captures of the same location over the years.
# ---------------------------------------------------------------------------

if full_pano.historical:
    print(f"\nFound {len(full_pano.historical)} historical panorama(s):\n")
    for h in full_pano.historical:
        print(f"  {h.date}  —  {h.id}")

    # Download and compare: current vs oldest available
    oldest = full_pano.historical[-1]  # Usually the oldest is last
    oldest_path = f"assets/{oldest.id}.jpg"

    streetview.download_panorama(oldest, oldest_path, zoom=3)

    fig, axes = plt.subplots(1, 2, figsize=(20, 6))

    axes[0].imshow(Image.open(output_path))
    axes[0].set_title(f"Current: {full_pano.date}", fontsize=13)
    axes[0].axis("off")

    axes[1].imshow(Image.open(oldest_path))
    axes[1].set_title(f"Oldest: {oldest.date}", fontsize=13)
    axes[1].axis("off")

    plt.suptitle("Same Location, Different Years", fontsize=15)
    plt.tight_layout()
    plt.show()
else:
    print("\nNo historical imagery available at this location.")

# ---------------------------------------------------------------------------
# 6. Coverage tiles — find all panoramas in an area
#    Instead of searching point-by-point, fetch all panoramas within a map
#    tile. This is how large-scale collection projects work.
# ---------------------------------------------------------------------------

tile_panos = streetview.get_coverage_tile_by_latlon(MIT_LAT, MIT_LON)

print(f"\nFound {len(tile_panos)} panoramas in this tile\n")

for p in tile_panos[:10]:
    print(f"  {p.id}  ({p.lat:.6f}, {p.lon:.6f})")

if len(tile_panos) > 10:
    print(f"  ... and {len(tile_panos) - 10} more")

# Plot panorama locations on a scatter plot
lats = [p.lat for p in tile_panos if p.lat is not None]
lons = [p.lon for p in tile_panos if p.lon is not None]

plt.figure(figsize=(10, 10))
plt.scatter(lons, lats, s=3, alpha=0.6, c="blue")
plt.scatter(
    [MIT_LON], [MIT_LAT], s=100, c="red", marker="*", zorder=5, label="MIT Media Lab"
)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title(f"Google Street View Coverage ({len(tile_panos)} panoramas)")
plt.legend()
plt.axis("equal")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# ---------------------------------------------------------------------------
# 7. Batch download along a path
#    Download panoramas along a walk from MIT Media Lab to Kendall Square.
# ---------------------------------------------------------------------------

route_points = [
    (42.3601, -71.0868),  # MIT Media Lab
    (42.3610, -71.0855),  # Along Ames St
    (42.3621, -71.0843),  # Toward Main St
    (42.3629, -71.0835),  # Near Kendall
    (42.3636, -71.0853),  # Kendall Square
]

os.makedirs("assets/route", exist_ok=True)
route_panos = []

for i, (lat, lon) in enumerate(route_points):
    p = streetview.find_panorama(lat, lon)
    if p:
        path = f"assets/route/{i:02d}_{p.id}.jpg"
        streetview.download_panorama(p, path, zoom=3)
        route_panos.append((p, path))
        print(f"[{i}] Downloaded {p.id} ({p.date}) — {p.lat:.5f}, {p.lon:.5f}")
        time.sleep(0.5)  # Be polite to Google's servers
    else:
        print(f"[{i}] No panorama found near ({lat}, {lon})")

print(f"\nDownloaded {len(route_panos)} panoramas along the route.")

# Display the route panoramas
if route_panos:
    n = len(route_panos)
    fig, axes = plt.subplots(n, 1, figsize=(16, 4 * n))
    if n == 1:
        axes = [axes]

    for i, (p, path) in enumerate(route_panos):
        route_img = Image.open(path)
        axes[i].imshow(route_img)
        axes[i].set_title(
            f"Stop {i}: {p.date} — ({p.lat:.5f}, {p.lon:.5f})", fontsize=11
        )
        axes[i].axis("off")

    plt.suptitle("Panoramas Along Route: Media Lab → Kendall Square", fontsize=14)
    plt.tight_layout()
    plt.show()

# ---------------------------------------------------------------------------
# 8. Next steps
#    Now that you can download panoramas programmatically, combine this with
#    the other chapters:
#
#      Chapter 1: Split downloaded panoramas and reconstruct them in 3D
#      Chapter 2: Run PanoOCR on downloaded panoramas to extract text
#      Chapter 3: Run SAM 3 to segment objects across many panoramas
#
#    For large-scale systematic collection, see nyc-gsv-collector:
#      https://github.com/yz3440/nyc-gsv-collector
#    (grid sampling, SQLite storage, multi-threading across city boroughs)
# ---------------------------------------------------------------------------
