# Chapter 0: Capturing 360 Photos

> Hands-on portion — we'll head outside with an Insta360 X4 to capture 360° photos around the Media Lab.

## Equipment

- **Insta360 X4** — dual-lens 360° camera (8K photo, 5.7K video)
- **Extended selfie stick** — the stick is invisible in the final image because it sits right on the stitch line between the two lenses. This means you get a floating-camera effect with no visible support.

![Insta360 X4 on extended selfie stick](assets/insta360-x4-setup.jpg)

## How a 360 Camera Works

The Insta360 X4 has **two fisheye lenses** pointing in opposite directions. Each lens captures slightly more than a hemisphere. The camera (or software) stitches these two fisheye images together into a single **equirectangular** image.

![Dual fisheye raw file vs. equirectangular output](assets/dual-fisheye-vs-equirectangular.jpg)

### What is Equirectangular Projection?

Equirectangular is the standard format for 360° images:

- **2:1 aspect ratio** — the full 360° horizontal × 180° vertical field of view is mapped onto a flat rectangle
- **Poles are stretched**, equator is accurate (same distortion pattern as a world map in Mercator-like projection)
- This is the same format used by Google Street View, Facebook 360 photos, and web panorama viewers

## Camera Settings

| Setting | Recommendation | Notes |
|---------|---------------|-------|
| **Mode** | Photo (72MP / 8K) | Maximum detail for post-processing |
| **Exposure** | Auto | Works well outdoors; consider manual for tricky lighting |
| **HDR** | On for static scenes | Improves dynamic range but requires holding still |
| **Interval shooting** | 1–2 sec intervals | Essential for 3D scanning walks (Chapter 1) |
| **File format** | Default (.insp) | Proprietary dual-fisheye; we convert later |

![Interval shooting settings on the Insta360 app](assets/interval-shooting-settings.png)

### Tips for Good Captures

- **Hold the stick vertical** — tilt causes the stitch line to shift, creating artifacts
- **Walk slowly** when doing interval captures for 3D scanning
- **Avoid reflective surfaces** close to the camera — mirrors and glass confuse the stitching
- **Mind the stitch line** — objects right at the seam between the two lenses may show artifacts
- The selfie stick holder's **arm** may appear if it extends past the stitch line

## Post-Capture: Insta360 Studio

The raw files from the camera (`.insp` for photos, `.insv` for video) are in Insta360's proprietary dual-fisheye format. You need **Insta360 Studio** (free desktop app) to convert them.

**Download:** [Insta360 Studio](https://www.insta360.com/download/insta360-x4)

### Conversion Workflow

1. **Import** — drag `.insp` / `.insv` files into Insta360 Studio
2. **Horizon correction** — enable FlowState stabilization to level the horizon. This is important: a tilted horizon breaks downstream processing.
3. **Export** — choose **Equirectangular** projection, export as JPEG (photos) or MP4 (video)
4. **Batch export** — select multiple files and export at once (no quantity limit)

![Insta360 Studio export settings](assets/insta360-studio-export.png)

### Output

After export, you'll have standard equirectangular JPEGs (typically 5888×2944 or larger) that work with any panorama viewer or processing tool.

These are the files we'll use in all subsequent chapters.

---

**Next:** [Chapter 1 — 3D Scanning from 360](../01-3d-scanning/)

---

## Suggested Assets to Add

| Filename | Description |
|----------|-------------|
| `assets/insta360-x4-setup.jpg` | Photo of the Insta360 X4 mounted on the extended selfie stick |
| `assets/dual-fisheye-vs-equirectangular.jpg` | Side-by-side: raw dual-fisheye `.insp` file vs. exported equirectangular JPEG |
| `assets/interval-shooting-settings.png` | Screenshot of interval shooting settings in the Insta360 app |
| `assets/insta360-studio-export.png` | Screenshot of Insta360 Studio's export dialog with equirectangular selected |
| `assets/equirectangular-example.jpg` | A sample equirectangular panorama captured during the workshop |
