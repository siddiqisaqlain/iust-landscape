# A Campus Garden of the Karewa

An interactive 3D landscape master plan for the campus of the Islamic University of Science and Technology (IUST), Awantipora, Kashmir.

**Live:** https://siddiqisaqlain.github.io/iust-landscape/

## What it shows
- The campus as it is **today** and as **proposed**, on terrain that rises east toward the Wastarwan hills
- Nine designed places: Chinar Gate, Library Garden, the Khayaban (walking spine), Central Bagh, Karewa Terraces, Highway Woodland, Hostel Gardens, Rain Garden and Chinar Meadow
- Four seasons, time of day with night lighting, flowing water, walking people, traffic, and falling petals, leaves or snow
- A guided tour; link to one place with `#gate`, `#library`, `#khayaban`, `#bagh`, `#karewa`, `#woodland`, `#hostels`, `#rain` or `#meadow`

## Site data
- **Terrain:** real elevation from Mapzen / AWS Terrain Tiles (zoom 15, about 4 m), loaded live
- **Ground:** Esri World Imagery, zoom 16 for the surroundings and zoom 18 for the campus, draped on the terrain and graded for each season
- **Existing trees and houses:** read from the aerial photograph; dark, textured green becomes trees, and coloured tin, grey metal and teal roofs become houses
- If the data cannot load, the model falls back to a drawn site

## Notes
The plan is traced from satellite imagery (about 0.68 m per traced pixel), so positions, sizes, building heights and levels are approximate until a campus survey is available. Detected trees and houses are approximate. It is a single HTML file using three.js r128; there is no build step.

Imagery: Esri, Maxar, Earthstar Geographics · Terrain: Mapzen / AWS Terrain Tiles

Author: Saqlain Siddiqi
