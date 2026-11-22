# Glareshield v2 (runs after build_storage): left + right pieces on the SAME plane (z 369..373), each following its
# half's real top outline (sampled from his panel, incl. the big curved corners). Each covers its panel's top edge
# and overhangs 46.5 mm = half the folded face gap, with a 20 mm brow, so when folded the two meet level in the
# middle of the gap and close the top and curved corners. The right piece's curve is shifted 6 mm outward
# because the left half is 6 mm wider (folded outlines differ by 6).
# Middle piece over the spacer: deployed only, snaps between L and R on 6x3 mm magnets; stows in a rear tub.
# Straight side + bottom of the gap: two 3 mm closure strips, stowed on the inside of the rear lids.
# Units mm, frame as build_case_mip (X right, Y toward pilot, Z up, u = x + 460).
import importlib.util
import adsk.core, adsk.fusion

BASE = r'D:/Admin/Documents/Projects/FlightSimCase/fusion/'
spec = importlib.util.spec_from_file_location('build_case_mip', BASE + 'build_case_mip.py')
bcm = importlib.util.module_from_spec(spec); spec.loader.exec_module(bcm)
P = bcm.P

G = dict(a=236.0, b=153.0, ez=216.0, ztop=369.0, gap=93.0, t=4.0, brow=20.0)


def X(u):
    return u - 460.0


def build_glareshield():
    app = adsk.core.Application.get()
    d = adsk.fusion.Design.cast(app.activeProduct)
    root = d.rootComponent
    tbm = adsk.fusion.TemporaryBRepManager.get()
    SUB = adsk.fusion.BooleanTypes.DifferenceBooleanType
    UNI = adsk.fusion.BooleanTypes.UnionBooleanType
    INT = adsk.fusion.BooleanTypes.IntersectionBooleanType

    def op(x, y, k):
        if not tbm.booleanOperation(x, y, k):
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
    zt = G['ztop']
    hosts = {o.component.name: o for o in root.occurrences}

    # --- sample HIS real top outline (the corner is a NURBS, fuller than an ellipse) from the left panel:
    # points (d, z), d = distance in from the outer edge
    pan = [b for b in hosts['Left half'].component.bRepBodies if b.name.startswith('PANEL 737')][0]

    def slab_top(d):
        c = tbm.copy(pan)
        op(c, box(X(d) - 0.05, X(d) + 0.05, -20, 20, 150, 400), INT)
        return c.boundingBox.maxPoint.z * 10

    def slab_edge(z):
        c = tbm.copy(pan)
        op(c, box(X(-5), X(200), -20, 20, z - 0.05, z + 0.05), INT)
        return c.boundingBox.minPoint.x * 10 + 460
    pts = [(slab_edge(z), z) for z in (P['z_low'] + 345.0, 225.0, 235.0, 245.0, 255.0, 265.0, 275.0)]
    pts += [(dd, slab_top(dd)) for dd in (12.0, 18, 25, 33, 42, 52, 64, 78, 94, 112, 132, 155, 180, 205, 225, 236)]
    pts = sorted(set((round(p[0], 2), round(p[1], 2)) for p in pts))
    pts.append((l1, zt))                       # straight top run to the seam

    def band(host, o_out, o_in, y0, y1, shift=0.0):
        """band between the outline offset outward by o_in and o_out (negative = inside the panel)"""
        sgn = 1.0 if host == 'Left half' else -1.0
        res = None
        for (d0, z0), (d1, z1) in zip(pts[:-1], pts[1:]):
            if host == 'Left half':
                ua, ub = d0, d1
            else:
                ua = r1 - d0 + shift * (1 - min(d0, 236.0) / 236.0)    # shift tapers out at the top
                ub = r1 - d1 + shift * (1 - min(d1, 236.0) / 236.0)
                if d1 >= 236.0 and d0 >= 236.0:      # straight run: right half goes from u r1-236 to r0
                    ua, ub = r1 - 236.0, r0
            dd, dz = d1 - d0, z1 - z0
            ln = (dd * dd + dz * dz) ** 0.5
            nd, nz = -dz / ln, dd / ln               # outward normal in (d, z)
            nu = sgn * nd
            off = (o_in + o_out) / 2.0
            cu = (ua + ub) / 2.0 + nu * off; cz = (z0 + z1) / 2.0 + nz * off
            p = F(X(cu), (y0 + y1) / 2.0, cz)
            ldir = adsk.core.Vector3D.create((ub - ua), 0, dz); ldir.normalize()
            seg = tbm.createBox(adsk.core.OrientedBoundingBox3D.create(p, ldir, adsk.core.Vector3D.create(0, 1, 0),
                                                                     (ln + 1.2) / 10.0, abs(y1 - y0) / 10.0, (o_out - o_in) / 10.0))
            if res is None:
                res = seg
            else:
                op(res, seg, UNI)
        return res

    gap, t, brow = G['gap'], G['t'], G['brow']
    sh = 6.0     # folded, the left outline sits 6 mm further out than the right one (left half is 6 mm wider)
    ov = gap / 2.0          # each piece overhangs half the folded gap: closed, they meet in the middle, level
    s0, s1 = uB + hg, uA - hg
    # left / right pieces: same plane (z 369..373), plate over the panel top edge + 46.5 mm overhang, 20 mm brow
    L = band('Left half', t + 0.05, 0.05, -P['t_panel'], ov)
    op(L, band('Left half', 0.01, -brow, ov - 3, ov), UNI)
    R = band('Right half', t + 0.05, 0.05, -P['t_panel'], ov, sh)
    op(R, band('Right half', 0.01, -brow, ov - 3, ov, sh), UNI)
    # middle piece over the spacer (deployed only): same section, snaps between L and R on magnets
    M = box(X(l1), X(r0), -P['t_panel'], ov, zt, zt + t)
    op(M, box(X(l1), X(r0), ov - 3, ov, zt - brow, zt), UNI)
    # magnet blocks under the plate at the joints (2 x 6x3 mm magnets per face)
    def mblock(u0, u1):
        blk = box(X(u0), X(u1), 3.0, ov - 3, zt - 8, zt)
        return blk
    op(L, mblock(l1 - 15, l1), UNI); op(R, mblock(r0, r0 + 15), UNI)
    op(M, mblock(l1, l1 + 15), UNI); op(M, mblock(r0 - 15, r0), UNI)
    for (bd, ue, sgn) in ((L, l1, -1), (R, r0, 1), (M, l1, 1), (M, r0, -1)):
        for yy in (12.0, ov - 12):
            mag = tbm.createCylinderOrCone(F(X(ue), yy, zt - 4), 0.31, F(X(ue) + sgn * 3.2, yy, zt - 4), 0.31)
            op(bd, mag, SUB)

    tp = P['t_panel']; back = 130.0
    items = {
        'Spacer': [('PRINT glareshield middle (magnetic, deployed only)', M)],
        'Left half': [('PRINT glareshield L (top closure)', L),
                      ('PANEL bottom closure strip 3 mm (stowed on lid)', box(X(4), X(424), -back + 3, -back + 6, -118, -118 + gap))],
        'Right half': [('PRINT glareshield R (top closure)', R),
                       ('PANEL side closure strip 3 mm (stowed on lid)', box(X(800), X(800 + gap), -back + 3, -back + 6, -120, 221))],
    }
    for h, its in items.items():
        comp = hosts[h].component
        bf = comp.features.baseFeatures.add(); bf.startEdit()
        for nm, bd in its:
            nb = comp.bRepBodies.add(bd, bf); nb.name = nm
        bf.finishEdit()
    print('glareshield v2: L/R level, overhang %.1f each, middle piece on spacer; closure strips stowed' % ov)


def run(_context: str):
    build_glareshield()
