"""Turn IUST_outlines.dxf (UTM 43N) into building data for index.html.

Coordinates are converted to the model's metres (Web Mercator about 33.9255 N, 75.0187 E;
x east, z south). Each feature is classified by shape and, for buildings, its footprint is
split into rectangles that each carry a hipped roof.
Usage: python3 footprints.py cad/IUST_outlines.dxf > blocks.js, then paste over `const BLD = [...]` in index.html.
Needs: ezdxf, pyproj, shapely, numpy.
"""
import sys, math
import numpy as np, ezdxf
from pyproj import Transformer
from shapely.geometry import Polygon, box
from shapely import affinity

LAT0, LNG0, CIRC = 33.9255, 75.0187, 40075016.686
COS0 = math.cos(math.radians(LAT0))
T = Transformer.from_crs(32643, 4326, always_xy=True)
def tile(lng, lat, z=20):
    n = 2 ** z; y = math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
    return (lng + 180) / 360 * n, (1 - y / math.pi) / 2 * n
M = CIRC * COS0 / 2 ** 20; CX, CY = tile(LNG0, LAT0)
def local(x, y):
    tx, ty = tile(*T.transform(x, y)); return ((tx - CX) * M, (ty - CY) * M)

def obb(P):
    r = list(P.minimum_rotated_rectangle.exterior.coords)
    e1 = (r[1][0] - r[0][0], r[1][1] - r[0][1]); e2 = (r[2][0] - r[1][0], r[2][1] - r[1][1])
    l1, l2 = math.hypot(*e1), math.hypot(*e2)
    if l1 < l2: e1, l1, l2 = e2, l2, l1
    return math.atan2(e1[1], e1[0]), l1, l2

def largest_rect(mask):
    """largest all-true axis-aligned rectangle: (area, r0, r1, c0, c1), inclusive bounds"""
    h = np.zeros(mask.shape[1], int); best = (0, 0, 0, 0, 0)
    for r in range(mask.shape[0]):
        h = np.where(mask[r], h + 1, 0); st = []
        for c in range(len(h) + 1):
            cur = h[c] if c < len(h) else 0; start = c
            while st and st[-1][1] >= cur:
                s, hh = st.pop(); a = hh * (c - s)
                if a > best[0]: best = (a, r - hh + 1, r, s, c - 1)
                start = s
            st.append((start, cur))
    return best

def roof_rects(P, ang, cell=0.5):
    """cover the footprint with up to 8 overlapping rectangles, in its dominant direction"""
    c = P.centroid; Q = affinity.rotate(P, -ang, origin=c, use_radians=True)
    x0, y0, x1, y1 = Q.bounds; nx, ny = int((x1 - x0) / cell) + 1, int((y1 - y0) / cell) + 1
    from shapely import contains_xy
    gx, gy = np.meshgrid(x0 + (np.arange(nx) + .5) * cell, y0 + (np.arange(ny) + .5) * cell)
    inside = contains_xy(Q, gx, gy); todo = inside.copy(); rects = []
    total = inside.sum()
    while len(rects) < 8 and todo.sum() > total * .06:
        a, r0, r1, c0, c1 = largest_rect(todo)
        if a * cell * cell < 12: break
        # grow into already-covered cells so neighbouring roofs meet
        grew = True
        while grew:
            grew = False
            if r0 > 0 and inside[r0 - 1, c0:c1 + 1].all(): r0 -= 1; grew = True
            if r1 < ny - 1 and inside[r1 + 1, c0:c1 + 1].all(): r1 += 1; grew = True
            if c0 > 0 and inside[r0:r1 + 1, c0 - 1].all(): c0 -= 1; grew = True
            if c1 < nx - 1 and inside[r0:r1 + 1, c1 + 1].all(): c1 += 1; grew = True
        todo[r0:r1 + 1, c0:c1 + 1] = False
        w, d = (c1 - c0 + 1) * cell, (r1 - r0 + 1) * cell
        if min(w, d) < 3: continue
        mx, my = x0 + (c0 + c1 + 1) / 2 * cell, y0 + (r0 + r1 + 1) / 2 * cell
        # back to model space
        dx, dy = mx - c.x, my - c.y; ca, sa = math.cos(ang), math.sin(ang)
        rects.append([round(c.x + dx * ca - dy * sa, 2), round(c.y + dx * sa + dy * ca, 2), round(w, 2), round(d, 2), round(ang, 4)])
    return rects

out = []
doc = ezdxf.readfile(sys.argv[1])
for e in doc.modelspace():
    for path in e.paths:
        pts = [(v[0], v[1]) for v in path.vertices]
        if pts[0] == pts[-1]: pts = pts[:-1]
        P = Polygon([local(*p) for p in pts])
        if not P.is_valid: P = P.buffer(0)
        if P.area < 3: continue
        ang, L, S = obb(P); rect = P.area / P.minimum_rotated_rectangle.area; convex = P.area / P.convex_hull.area
        P = P.simplify(.15)
        f = [[round(x, 2), round(y, 2)] for x, y in list(P.exterior.coords)[:-1]]
        if rect < .3 or P.area > 5000:                       # ring road, paths and the highway woodland: the photo shows these
            continue
        if L / S > 5 and S < 3.6:                             # rows of solar panels or parked buses
            out.append({'t': 's', 'f': f}); continue
        n = len(pts); squareish = L / S < 1.3
        if squareish and convex > .96 and n >= 14 and P.area < 400:
            out.append({'t': 'k', 'f': f}); continue          # water tank
        if squareish and convex > .93 and n >= 7:
            out.append({'t': 'p', 'f': f}); continue          # octagonal library and pavilions: pyramid roof
        if rect < .45 and P.area < 120:
            continue                                          # ramps and steps
        c = P.centroid
        out.append({'t': 'b', 'f': f, 'r': roof_rects(P, ang) or [[round(c.x, 2), round(c.y, 2), round(L, 2), round(S, 2), round(ang, 4)]]})

def num(v): t = ('%.2f' % v).rstrip('0').rstrip('.'); return '0' if t in ('-0', '') else t
def arr(a): return '[' + ','.join(arr(x) if isinstance(x, list) else num(x) for x in a) + ']'
lines = ["  {t:'%s',f:%s%s}" % (b['t'], arr(b['f']), ',r:' + arr(b['r']) if 'r' in b else '') for b in out]
print("""/* Building footprints from the campus outlines (site-data/cad/IUST_outlines.dxf, WGS 84 / UTM 43N), in model metres.
   t: b building with hipped roofs over the rectangles r [x, z, length, width, angle]; p pyramid roof (library, pavilions);
   k water tank; s row of solar panels or parked buses. Regenerate with site-data/footprints.py. */
const BLD = [
""" + ',\n'.join(lines) + '\n];')
