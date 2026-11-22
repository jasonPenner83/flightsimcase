# Glareshield v3 (square top): straight left + right pieces on the same plane, sitting at the 3 mm top skin
# level (plate z 372..376) with a filler strip over the panel top edge. Each overhangs 46.5 mm = half the folded
# face gap, with a 20 mm brow, so folded they meet level in the middle of the gap and close the top.
# Middle piece over the spacer: deployed only, snaps between L and R on 6x3 mm magnets.
# Straight side + bottom of the folded gap: two 3 mm closure strips (side ~490 long, bottom 430), stowed upright
# in the deep right tub. Runs after build_storage. Units mm, frame as build_case_mip (u = x + 460).
import importlib.util
import adsk.core, adsk.fusion

BASE = r'D:/Admin/Documents/Projects/FlightSimCase/fusion/'
spec = importlib.util.spec_from_file_location('build_case_mip', BASE + 'build_case_mip.py')
bcm = importlib.util.module_from_spec(spec); spec.loader.exec_module(bcm)
P = bcm.P

G = dict(ztop=369.0, skin=3.0, gap=93.0, t=4.0, brow=20.0)


def X(u):
    return u - 460.0


def build_glareshield():
    app = adsk.core.Application.get()
    d = adsk.fusion.Design.cast(app.activeProduct)
    root = d.rootComponent
    tbm = adsk.fusion.TemporaryBRepManager.get()
    SUB = adsk.fusion.BooleanTypes.DifferenceBooleanType
    UNI = adsk.fusion.BooleanTypes.UnionBooleanType

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
    zt, sk, gap, t, brow = G['ztop'], G['skin'], G['gap'], G['t'], G['brow']
    tp = P['t_panel']
    ov = gap / 2.0
    zp = zt + sk                     # plate bottom = top-skin level

    def piece(u0, u1):
        b = box(X(u0), X(u1), -tp, ov, zp, zp + t)                        # plate
        op(b, box(X(u0), X(u1), -tp, 0.0, zt + 0.05, zp), UNI)            # filler over the panel top edge
        op(b, box(X(u0), X(u1), ov - 3, ov, zp - brow, zp), UNI)          # brow
        return b
    L = piece(-sk, l1)
    R = piece(r0, r1 + sk)
    M = piece(l1, r0)

    def mblock(u0, u1):              # magnet blocks under the plate at the joints (2 x 6x3 mm magnets per face)
        return box(X(u0), X(u1), 3.0, ov - 3, zp - 8, zp)
    op(L, mblock(l1 - 15, l1), UNI); op(R, mblock(r0, r0 + 15), UNI)
    op(M, mblock(l1, l1 + 15), UNI); op(M, mblock(r0 - 15, r0), UNI)
    for (bd, ue, sgn) in ((L, l1, -1), (R, r0, 1), (M, l1, 1), (M, r0, -1)):
        for yy in (12.0, ov - 12):
            op(bd, tbm.createCylinderOrCone(F(X(ue), yy, zp - 4), 0.31, F(X(ue) + sgn * 3.2, yy, zp - 4), 0.31), SUB)

    hosts = {o.component.name: o for o in root.occurrences}
    yb = -190.0 + 3.0 + 27.0          # just in front of the right rear frame (lid 190, frame 20 deep)
    items = {
        'Spacer': [('PRINT glareshield middle (magnetic, deployed only)', M)],
        'Left half': [('PRINT glareshield L (top closure)', L)],
        'Right half': [('PRINT glareshield R (top closure)', R),
                       ('PANEL side closure strip 3 mm (stowed)', box(X(780), X(780 + gap), yb, yb - 3, -122.0, 368.0)),
                       ('PANEL bottom closure strip 3 mm (stowed)', box(X(780), X(780 + gap), yb + 4, yb + 1, -110.0, 320.0))],
    }
    for h, its in items.items():
        comp = hosts[h].component
        bf = comp.features.baseFeatures.add(); bf.startEdit()
        for nm, bd in its:
            nb = comp.bRepBodies.add(bd, bf); nb.name = nm
        bf.finishEdit()
    print('glareshield v3: straight, plate z %.0f..%.0f, overhang %.1f; closure strips stowed in the right tub' % (zp, zp + t, ov))


def run(_context: str):
    build_glareshield()
