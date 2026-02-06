# Chapter 4: Working with Found 360 Images

> Download and work with Google Street View panoramas programmatically — no API key needed.

## The Biggest Source of 360 Images

You don't always need to capture your own panoramas. **Google Street View** is the largest collection of street-level 360° imagery in the world, covering most roads in major cities with historical imagery going back to 2007.

The **[streetlevel](https://github.com/sk-zk/streetlevel)** Python library lets you search for, download, and inspect Google Street View panoramas (and imagery from other providers) without needing an API key.

## Installation

```bash
pip install streetlevel
```

## Key Concepts

### Finding Panoramas

```python
from streetlevel import streetview

# Find the nearest panorama to a coordinate
pano = streetview.find_panorama(42.3601, -71.0868)  # MIT Media Lab
print(pano.id)          # Panorama ID
print(pano.lat, pano.lon)  # Actual location
print(pano.date)        # Capture date (year, month)
```

### Downloading Panoramas

```python
# Download full-resolution equirectangular JPEG
streetview.download_panorama(pano, f"{pano.id}.jpg")

# Or get it as a PIL image
image = streetview.get_panorama(pano, zoom=5)  # zoom 0-5, 5 is highest
```

### Exploring Metadata

Each panorama comes with rich metadata:

```python
pano = streetview.find_panorama_by_id("some_pano_id")

# Neighbors — nearby panoramas you can navigate to
for neighbor in pano.neighbors:
    print(neighbor.id, neighbor.lat, neighbor.lon)

# Historical — older captures at the same location
for old in pano.historical:
    print(old.id, old.date)

# Generate a Google Maps link
print(pano.permalink())
```

### Coverage Tiles

For area-based searches, you can fetch all panoramas within a map tile:

```python
# Get all panoramas in the tile containing a point
panos = streetview.get_coverage_tile_by_latlon(42.3601, -71.0868)
print(f"Found {len(panos)} panoramas in this tile")
```

This is useful for systematic data collection across a region.

## Hands-On: MIT Campus Exercise

See **[`gsv_demo.ipynb`](gsv_demo.ipynb)** for the interactive notebook.

The exercise walks through:

1. Finding a panorama near the MIT Media Lab
2. Downloading and displaying it
3. Exploring metadata (date, address, neighbors, historical captures)
4. Fetching coverage for a tile around MIT
5. Batch downloading a set of panoramas

## Systematic Collection at Scale

For large-scale projects (like [all text in nyc](https://alltext.nyc), which processed 8M+ panoramas), you need a more structured approach: grid sampling coordinates, querying each one, and storing results in a database.

**Reference:** [**nyc-gsv-collector**](https://github.com/yz3440/nyc-gsv-collector) — a Python tool that systematically collects Google Street View panorama metadata across NYC boroughs using:

- Grid-based coordinate sampling (configurable spacing, default 5m)
- Multi-threaded panorama search
- SQLite database for persistent storage and resume capability
- Progress tracking

The collector gathers panorama IDs, locations, dates, and copyright info — which you can then use with `streetlevel` to download the actual images.

## Supported Providers

`streetlevel` isn't limited to Google. It also supports:

- Apple Look Around
- Baidu Panorama
- Kakao Road View
- Naver Street View
- Yandex Panorama
- Bing Streetside
- Mapy.cz Panorama

## Important Notes

- `streetlevel` uses **internal/unofficial APIs** — it may break if Google changes their endpoints
- Be mindful of **rate limiting** — add delays between requests for bulk operations
- For production or commercial use, consider the [official Google Street View API](https://developers.google.com/maps/documentation/streetview) (requires API key, has usage quotas and billing)
- Downloaded imagery is subject to Google's copyright and terms of service

---

**Previous:** [Chapter 3 — Object Segmentation](../03-object-segmentation/) · **Next:** [Chapter 5 — Creative Applications](../05-creative-applications/)

---

## Suggested Assets to Add

| Filename | Description |
|----------|-------------|
| `assets/gsv-mit-media-lab.jpg` | A downloaded GSV panorama near the MIT Media Lab |
| `assets/coverage-tile-visualization.png` | Map visualization showing panorama locations in a coverage tile |
| `assets/gsv-metadata-example.png` | Screenshot showing panorama metadata (date, address, neighbors) |
