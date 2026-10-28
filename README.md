# A Campus Garden of the Karewa

An interactive 3D landscape master plan for the campus of the Islamic University of Science and Technology (IUST), Awantipora, Kashmir.

**Live:** https://siddiqisaqlain.github.io/iust-landscape/

## What it shows
- The campus as it is **today** and as **proposed**, on terrain that rises east toward the Wastarwan hills
- Nine designed places: Chinar Gate, Library Garden, the Khayaban (walking spine), Central Bagh, Karewa Terraces, Highway Woodland, Hostel Gardens, Rain Garden and Chinar Meadow
- Four seasons, time of day with night lighting, flowing water, walking people, traffic, and falling petals, leaves or snow
- A guided tour; link to one place with `#gate`, `#library`, `#khayaban`, `#bagh`, `#karewa`, `#woodland`, `#hostels`, `#rain` or `#meadow`

## Site data
- **Buildings:** 112 building footprints from the campus outlines (`site-data/cad/IUST_outlines.dxf`), with plastered walls, windows, a stone plinth on sloping ground, hipped roofs (several overlapping roofs for the larger blocks, a two-tier roof for the octagonal Rumi Library), solar arrays, water tanks and the solar field. Roof colours are read from the aerial photograph
- **Terrain:** real elevation from Mapzen / AWS Terrain Tiles (zoom 15, about 4 m), loaded live
- **Ground:** Esri World Imagery, zoom 16 for the surroundings and zoom 18 for the campus, draped on the terrain and graded for each season
- **Existing trees and houses:** read from the aerial photograph; dark, textured green becomes trees, and coloured tin, grey metal and teal roofs become houses
- If the data cannot load, the model falls back to a drawn site

## Notes
Building footprints come from the campus outlines; storeys are estimated from each footprint's area (one to four storeys of 3.3 m), so heights and floor levels are approximate. The landscape plan is traced from satellite imagery (about 0.65 m per traced pixel). Reference material, including Google Earth views of the campus, is in `site-data/`. Detected trees and houses are approximate. It is a single HTML file using three.js r128; there is no build step.

Imagery: Esri, Maxar, Earthstar Geographics · Terrain: Mapzen / AWS Terrain Tiles

Author: Saqlain Siddiqi
