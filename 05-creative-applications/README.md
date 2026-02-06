# Chapter 5: Creative Applications

> Artistic and experimental uses of panoramic imagery — from generative landscapes to data-driven psychogeography.

The tools covered in this workshop aren't just for technical analysis. 360° imagery is a rich medium for creative and artistic work. Here are some projects that push panoramic images into unexpected territory.

---

## diffused·city

![diffused·city screenshot](assets/diffused-city-screenshot.png)

**[diffused·city](https://diffused.city)** is a collection, generator, and geoguessr of fictional city panoramas — imagined by a diffusion model.

### How It Works

The project uses DALL-E 2's **edit/inpainting mode** to generate seamless 360° panoramas:

1. Start with a prompt describing a city scene
2. Generate panels with overlapping edges using DALL-E 2's inpainting capability
3. Stitch the panels into a seamless equirectangular panorama
4. The result wraps into a continuous 360° view with no visible seams

This turns a 2D image generation model into a panoramic world generator — creating fictional streetscapes of real cities that you can explore as if you were standing inside them.

![diffused·city generation process](assets/diffused-city-process.png)

### Try It

Visit the project to explore the collection, generate your own fake panoramas, or play the geoguessr game (coming soon).

---

## J Train Simulator

![J Train Simulator screenshot](assets/j-train-simulator.jpg)

**[J Train Simulator](https://www.yufengzhao.com/)** — a soundscape and 3D gaussian splat scan of a J train stop in Brooklyn, NY.

### Behind the Scenes

- Captured entirely with 360° photos on a **long selfie stick** from an apartment balcony overlooking the train stop
- No drone was used — just creative camera placement
- The 360° images were split into perspective views (Chapter 1 approach) and reconstructed as a gaussian splat
- A spatial audio soundscape is layered on top, so the simulated train always arrives on time (unlike in real life)

This project demonstrates that compelling 3D scans can come from unconventional capture setups — a 360 camera on a stick can reach places a traditional camera or drone can't.

---

## all text in nyc

![all text in nyc screenshot](assets/alltext-nyc.png)

**[all text in nyc](https://alltext.nyc)** — a search engine for the textual landscape of New York City.

### From OCR to Cultural Cartography

What started as a technical OCR project (Chapter 2) became a tool for understanding cities through their text:

- **"pizza"** returns 111,290 results — a map of NYC's pizza obsession
- **"luxury"** clusters around new real estate developments
- **"iglesia"** and **"jerk"** trace ethnic neighborhoods through language
- **"for rent"** tells a story about the city's commercial landscape
- Historical imagery (2007–2024) reveals how neighborhoods change over time

The project was featured by The Pudding, where data storytelling revealed patterns invisible at street level but clear when viewed at city scale.

**Press:** Fast Company, PCMag, Time Out

---

## Ideas to Explore

Here are some directions for your own creative work with panoramic imagery:

### Time-Based

- **Panoramic time-lapse** — download historical Street View imagery of the same location across years (using `streetlevel` from Chapter 4) and create a time-lapse of urban change
- **Temporal composites** — blend old and new panoramas of the same location into a single image

### Generative

- **Style transfer on equirectangular images** — apply neural style transfer to panoramas (be aware of seam artifacts at the left/right edges)
- **AI-generated panoramic worlds** — extend the diffused·city approach with newer models (Stable Diffusion, DALL-E 3, etc.)
- **Panoramic collage** — combine fragments from different locations into a single impossible panorama

### Spatial / Immersive

- **VR experiences from found imagery** — place Street View panoramas in a VR headset for virtual walks through cities
- **Spatial audio mapping** — pair panoramic imagery with location-based sound recordings
- **3D scans from historical Street View** — use multi-year imagery of the same street to reconstruct 3D models that show change over time

### Data-Driven

- **Object frequency mapping** — use SAM 3 (Chapter 3) to count specific objects across thousands of panoramas and map their distribution
- **Color analysis** — extract dominant colors from panoramas to create city-scale color maps
- **Typography surveys** — use PanoOCR (Chapter 2) to catalog fonts, sign styles, and lettering across neighborhoods

---

**Previous:** [Chapter 4 — Found 360 Images](../04-found-360-images/) · **Back to:** [Workshop Home](../README.md)

---

## Suggested Assets to Add

| Filename | Description |
|----------|-------------|
| `assets/diffused-city-screenshot.png` | Screenshot from diffused.city showing a generated panorama |
| `assets/diffused-city-process.png` | Diagram showing the multi-panel inpainting → stitching process |
| `assets/j-train-simulator.jpg` | Screenshot from the J Train Simulator experience |
| `assets/alltext-nyc.png` | Screenshot of alltext.nyc showing search results on a map |
