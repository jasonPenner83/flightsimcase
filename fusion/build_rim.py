# Closing rim (Jason: keep the radius, extend the sides so it closes completely). Runs after build_storage.
# Each half gets a 3 mm skin that follows HIS panel outline (outer side, the big curved top corner, top run and
# bottom), from its rear lid to 46.5 mm in front of the panel face = half the folded face gap. Folded, the two
# rims meet edge to edge in the middle of the gap, so the case is closed on top, bottom and the outer side; the
# spacer closes the hinge side. Deployed, the top run of the rim is the glareshield (46.5 mm overhang).
# The outline is sampled from the real panel and used as a convex polygon (intersection of half-spaces), so the
# skin, the curved rear lid and the right half's 6 mm edge filler all share exactly the same curve.
# Also: seam-side walls of the rear boxes, and the magnetic middle glareshield piece over the spacer (deployed only).
# Units mm, frame as build_case_mip (X right, Y toward pilot, Z up, u = x + 460).
import importlib.util, math
import adsk.core, adsk.fusion

BASE = r'D:/Admin/Documents/Projects/FlightSimCase/fusion/'


def _load(n):
    spec = importlib.util.spec_from_file_location(n, BASE + n + '.py')
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


bcm = _load('build_case_mip')
P = bcm.P


def X(u):
    return u - 460.0


def build_rim():
    st = _load('build_storage')
    app = adsk.core.Application.get()
    d = adsk.fusion.Design.cast(app.activeProduct)
    root = d.rootComponent
    tbm = adsk.fusion.TemporaryBRepManager.get()
    SUB = adsk.fusion.BooleanTypes.DifferenceBooleanType
    UNI = adsk.fusion.BooleanTypes.UnionBooleanType
    INT = adsk.fusion.BooleanTypes.IntersectionBooleanType

    def op(a, b, k):
        if not tbm.booleanOperation(a, b, k):
            raise RuntimeError('boolean failed')

    def F(x, y, z):
        return adsk.core.Point3D.create(x / 10.0, -y / 10.0, z / 10.0)

    def box(x0, x1, y0, y1, a, b):
        p = F(x0, y0, a); q = F(x1, y1, b)
        lo = [min(p.x, q.x), min(p.y, q.y), min(p.z, q.z)]; hi = [max(p.x, q.x), max(p.y, q.y), max(p.z, q.z)]
        c = adsk.core.Point3D.create((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2)
        return tbm.createBox(adsk.core.OrientedBoundingBox3D.create(c, adsk.core.Vector3D.create(1, 0, 0), adsk.core.Vector3D.create(0, 1, 0),
                                                                   hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]))

    uA, uB, hg = P['uA'], P['uB'], P['hg']
    l1 = uB - hg; r0 = uA + hg; r1 = 920.0 + P['shift_right']
    tp, zl, sk, rim, zt = P['t_panel'], P['z_low'], P['skin'], P['rim'], 369.0
    hosts = {o.component.name: o for o in root.occurrences}

    # --- sample his top outline from the left panel: (d, z), d = distance in from the outer edge
    pan = [b for b in hosts['Left half'].component.bRepBodies if b.name.startswith('PANEL 737')][0]

    def slab_top(dd):
        c = tbm.copy(pan); op(c, box(X(dd) - 0.05, X(dd) + 0.05, -20, 20, 150, 400), INT)
        return c.boundingBox.maxPoint.z * 10

    def slab_edge(z):
        c = tbm.copy(pan); op(c, box(X(-5), X(200), -20, 20, z - 0.05, z + 0.05), INT)
        return c.boundingBox.minPoint.x * 10 + 460
    pts = [(0.0, 216.0)] + [(slab_edge(z), z) for z in (225.0, 235.0, 245.0, 255.0, 265.0, 275.0)]
    pts += [(dd, slab_top(dd)) for dd in (12.0, 18, 25, 33, 42, 52, 64, 78, 94, 112, 132, 155, 180, 205, 225, 236)]
    pts = sorted(set((round(p[0], 2), round(p[1], 2)) for p in pts))
    pts.append((l1, zt))

    def interior(host, off, y0, y1, edge_shift=0.0):
        """region inside the half's outline grown outward by `off` (not at the seam), extruded y0..y1"""
        if host == 'Left half':
            body = box(X(-off), X(l1), y0, y1, zl - off, 470)
            umap = lambda dd: dd
            sgn = 1.0
        else:
            R = r1 + edge_shift
            body = box(X(r0), X(R + off), y0, y1, zl - off, 470)
            umap = lambda dd: R - dd
            sgn = -1.0
        for (d0, z0), (d1, z1) in zip(pts[:-1], pts[1:]):
            dd, dz = d1 - d0, z1 - z0
            ln = math.hypot(dd, dz)
            nd, nz = -dz / ln, dd / ln              # outward normal in (d, z)
            nu = sgn * nd
            mu, mz = (umap(d0) + umap(d1)) / 2.0, (z0 + z1) / 2.0
            cu = mu + nu * (off - 500.0); cz = mz + nz * (off - 500.0)
            tdir = adsk.core.Vector3D.create(umap(d1) - umap(d0), 0, dz); tdir.normalize()
            half = tbm.createBox(adsk.core.OrientedBoundingBox3D.create(F(X(cu), (y0 + y1) / 2.0, cz), tdir, adsk.core.Vector3D.create(0, 1, 0),
                                                                        400.0, abs(y1 - y0) / 10.0 + 0.2, 100.0))
            op(body, half, INT)
        return body

    sh = {'Left half': 0.0, 'Right half': P['r_ext']}
    items = {'Left half': [], 'Right half': [], 'Spacer': []}
    for h in ('Left half', 'Right half'):
        B = st.S['tub_back'][h]
        y0, y1 = -B + sk, rim
        skin = interior(h, sk, y0, y1, sh[h])
        op(skin, interior(h, 0.0, y0 - 1, y1 + 1, sh[h]), SUB)
        items[h].append(('PANEL rim skin, closes the case (3 mm)', skin))
        items[h].append(('PANEL rear lid (3 mm, removable)', interior(h, sk, -B, -B + sk, sh[h])))
        # seam-side wall of the rear box (outside the seam column, behind the seam angle)
        if h == 'Left half':
            items[h].append(('PANEL seam side wall (3 mm)', box(X(l1), X(l1) + sk, -B, -tp - 20, zl - sk, zt + sk)))
        else:
            items[h].append(('PANEL seam side wall (3 mm)', box(X(r0) - sk, X(r0), -B, -tp - 20, zl - sk, zt + sk)))
    # right half: 6 mm edge filler in the panel plane so both halves have the same outline (430 wide)
    fill = interior('Right half', 0.0, -tp, 0.0, P['r_ext'])
    op(fill, interior('Right half', 0.0, -tp - 1, 1.0, 0.0), SUB)
    items['Right half'].append(('PANEL edge filler 6 mm (right half)', fill))

    # middle glareshield piece over the spacer: deployed only, magnets into the rim ends
    M = box(X(l1), X(r0), -tp, rim, zt, zt + sk)
    op(M, box(X(l1), X(r0), -tp, 0, zt - 0.0, zt + sk), UNI)
    for ue, sgn in ((l1, 1), (r0, -1)):
        op(M, box(X(ue) if sgn > 0 else X(ue) - 15, X(ue) + 15 if sgn > 0 else X(ue), 3.0, rim - 3, zt + sk, zt + sk + 6), UNI)
    items['Spacer'].append(('PRINT glareshield middle (magnetic, deployed only)', M))

    for h, its in items.items():
        comp = hosts[h].component
        bf = comp.features.baseFeatures.add(); bf.startEdit()
        for nm, bd in its:
            nb = comp.bRepBodies.add(bd, bf); nb.name = nm
        bf.finishEdit()
    print('rim: 3 mm skins to %.1f mm in front of the face, outline points %d' % (rim, len(pts)))


def run(_context: str):
    build_rim()
