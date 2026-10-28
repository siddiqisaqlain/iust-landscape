# IUST Landscape – Reference Site Data

Reference site data for the IUST campus landscape study.

## Coordinate system

- **Projection:** WGS 84 / UTM zone 43N (EPSG:32643), units in metres (see `cad/IUST_outlines.prj`)
- **Extent (from DXF header):**
  - Min: E 501457.57, N 3753702.22
  - Max: E 501963.57, N 3754109.22
  - Roughly 506 m × 407 m, centred near 33.92° N, 75.02° E (approximate)

## Files

### `cad/`

| File | Description |
| --- | --- |
| `IUST_outlines.dxf` | Building footprint outlines – 139 solid-hatch polygons on layer `0` (AutoCAD 2004 / AC1018 format) |
| `IUST_outlines.prj` | Projection definition for the outlines (WGS 84 / UTM 43N) |
| `IUST_outlines.sbn` | Shapefile spatial index. Only usable together with the matching `.shp`, `.shx` and `.dbf`, which are not included yet |

The 3D model's buildings come from `IUST_outlines.dxf`. `footprints.py` converts it into the `BLD` list in `index.html`: it reprojects the outlines into the model's metres, drops roads, paths and the highway woodland, and sorts the rest into buildings, the library and pavilions, water tanks and rows of solar panels or parked buses. To regenerate:

```
pip install ezdxf pyproj shapely numpy
python3 site-data/footprints.py site-data/cad/IUST_outlines.dxf > blocks.js
```

### `images/`

| File | Description |
| --- | --- |
| `contours-over-orthophoto.webp` | Contour lines (yellow) over the drone orthophoto of the campus |
| `terrain-heatmap-overlay.webp` | Terrain/slope heatmap over a tinted orthophoto; red bands mark steep changes |
| `dem-elevation-grayscale.png` | Grayscale DEM of the site (lighter = higher) |
| `contours-red-overlay.webp` | Contour lines (red) over a tinted orthophoto |

### `images/google-earth/`

Oblique 3D screenshots from Google Earth, for visual reference only (not georeferenced).

| File | Description |
| --- | --- |
| `ge-01-oblique-highway-behind.webp` | Whole campus with the highway running across the top of the frame |
| `ge-02-oblique-highway-right.webp` | Whole campus with the highway curving down the right side; octagonal hall at centre right |
| `ge-03-oblique-main-entrance.webp` | View from the highway side: main entrance road, parking loop and octagonal hall in the foreground |
| `ge-04-oblique-central-quad.webp` | Closer view of the central quad, red-brick walkways and the dense block of smaller buildings |
| `ge-05-labelled-buildings.webp` | Same area with Google Earth place labels (see below) |
| `ge-06-oblique-octagonal-hall-foreground.webp` | Wide oblique with the octagonal hall and entrance parking in the foreground, highway on the right |
| `ge-07-top-down-wide-context.webp` | Near top-down wide view: campus on the left, highway at far left, surrounding orchards/fields and access road to the east |
| `ge-08-oblique-north-academic-blocks.webp` | Oblique of the academic blocks along the curved ring road, with the solar-panel field and bus parking at bottom |
| `ge-09-oblique-campus-and-highway.webp` | Whole campus with the highway down the right edge and town beyond |

Buildings named in `ge-05-labelled-buildings.webp`: Rumi Library, Academic Block 1st, School of Business Studies, Health Centre, Dean of Students, Administrative Block, Civil Engineering Department, Geotechnical Engineering Laboratory, Concrete Technology Laboratory, Fluid Mechanics Laboratory, Structural Engineering Laboratory, IUST Library (Kutub Khana), Department of Electronics and Communication, Jamia Masjid IUST.
