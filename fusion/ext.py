# Vevor 20-series aluminium extrusion profiles as real cross-sections (temporary BRep).
# 2020: 20x20, one T-slot per face, centre bore 4.2. 2040: 20x40, one slot per 20 face, two per 40 face,
# two bores. Slot: 6.2 mm opening x 1.8 mm lip, 11 mm wide cavity to 6.0 mm deep (T-slot undercut simplified).
# Use: prof = ext.make(tbm, F); body = prof(x0, x1, y0, y1, z0, z1) in the case frame (mm); the longest
# dimension is the extrusion axis, the other two must be 20x20 or 20x40.
import adsk.core, adsk.fusion

LIP_W, LIP_D, CAV_W, CAV_D, BORE = 6.2, 1.8, 11.0, 6.0, 4.2


def make(tbm, F):
    SUB = adsk.fusion.BooleanTypes.DifferenceBooleanType

    def box(lo, hi):
        p = F(*lo); q = F(*hi)
        a = [min(p.x, q.x), min(p.y, q.y), min(p.z, q.z)]; b = [max(p.x, q.x), max(p.y, q.y), max(p.z, q.z)]
        c = adsk.core.Point3D.create((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2)
        return tbm.createBox(adsk.core.OrientedBoundingBox3D.create(c, adsk.core.Vector3D.create(1, 0, 0), adsk.core.Vector3D.create(0, 1, 0),
                                                                   b[0] - a[0], b[1] - a[1], b[2] - a[2]))

    def prof(x0, x1, y0, y1, z0, z1):
        lo = [min(x0, x1), min(y0, y1), min(z0, z1)]; hi = [max(x0, x1), max(y0, y1), max(z0, z1)]
        dims = [hi[i] - lo[i] for i in range(3)]
        ax = dims.index(max(dims))
        c1, c2 = [i for i in range(3) if i != ax]
        body = box(lo, hi)

        def cut(l, h):
            l2 = list(l); h2 = list(h)
            l2[ax] = lo[ax] - 1; h2[ax] = hi[ax] + 1
            tbm.booleanOperation(body, box(l2, h2), SUB)
        for n, o in ((c1, c2), (c2, c1)):            # n: face-normal axis, o: along-face axis
            width = dims[o]
            centres = [lo[o] + width / 2] if width < 30 else [lo[o] + 10, lo[o] + 30]
            for side in (lo[n], hi[n]):
                sgn = 1 if side == lo[n] else -1
                for cc in centres:
                    for w, d0, d1 in ((LIP_W, 0, LIP_D), (CAV_W, LIP_D, CAV_D)):
                        l = [0, 0, 0]; h = [0, 0, 0]
                        l[o] = cc - w / 2; h[o] = cc + w / 2
                        a = side + sgn * d0; b = side + sgn * d1
                        if d0 == 0:
                            a = side - sgn * 0.5
                        l[n] = min(a, b); h[n] = max(a, b)
                        cut(l, h)
        # bores, one per 20x20 cell
        cells1 = [lo[c1] + 10] if dims[c1] < 30 else [lo[c1] + 10, lo[c1] + 30]
        cells2 = [lo[c2] + 10] if dims[c2] < 30 else [lo[c2] + 10, lo[c2] + 30]
        for p in cells1:
            for q in cells2:
                a = [0, 0, 0]; b = [0, 0, 0]
                a[c1] = b[c1] = p; a[c2] = b[c2] = q; a[ax] = lo[ax] - 1; b[ax] = hi[ax] + 1
                tbm.booleanOperation(body, tbm.createCylinderOrCone(F(*a), BORE / 20.0, F(*b), BORE / 20.0), SUB)
        return body
    return prof
