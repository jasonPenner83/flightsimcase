# C172-specific bifold case (first iteration, not modular).
# Two 414 mm halves on one side-mounted piano hinge at the seam (x = 0). The right half stays on the desk;
# the left half folds 180 deg onto it, face to face. Frame: 2040 upright + 2020 bumper (40 mm knob recess),
# 2020 rails where the panel faces need them, 3 mm rear covers and edge lips (sealed when closed).
# Units mm. Frame: X right, Y toward pilot, Z up. Panel bottom z = 0, desk at z = -foot.
import adsk.core, adsk.fusion, math

P = dict(
    W=414.0,          # each half (inner 374: switch column 62 + PFD 306 | audio 63 + MFD 306)
    H=375.6,
    T=20.0,
    proud=40.0,
    Fe=40.0, Be=30.0, cover=3.0, clr=5.0,
    hg=1.5, kn=2.5,
    foot=40.0,
    rails=[10.0, 110.0, 310.0, 365.6],      # same on both halves: lower 100 | displays 200 | top strip 55.6
    yoke_x=-177.0,     # pilot yoke on the PFD centerline
    thr_x=87.0,        # throttle / aircraft centerline at the audio panel / MFD seam
    out_c=135.0,       # right half outriggers
    out_lo=160.0, out_li=120.0,   # left half outriggers (carry the yoke shelf)
)


def geometry():
    yp = P['proud'] + P['kn']
    A = (0.0, yp)                                    # hinge axis at the seam
    xr0 = P['hg']; xr1 = xr0 + P['W']                # right half x range
    xl1 = -P['hg']; xl0 = xl1 - P['W']               # left half x range
    return dict(yp=yp, A=A, right=(xr0, xr1), left=(xl0, xl1), knob_gap=2 * yp)


def build():
    app = adsk.core.Application.get()
    d = adsk.fusion.Design.cast(app.activeProduct)
    if d.designIntent == adsk.fusion.DesignIntentTypes.PartDesignIntentType:
        d.designIntent = adsk.fusion.DesignIntentTypes.HybridDesignIntentType
    root = d.rootComponent
    tbm = adsk.fusion.TemporaryBRepManager.get()

    def P3(x, y, z):
        return adsk.core.Point3D.create(x / 10.0, -y / 10.0, z / 10.0)

    def tbox(x0, x1, y0, y1, z0, z1):
        a = P3(x0, y0, z0); b = P3(x1, y1, z1)
        lo = [min(a.x, b.x), min(a.y, b.y), min(a.z, b.z)]; hi = [max(a.x, b.x), max(a.y, b.y), max(a.z, b.z)]
        c = adsk.core.Point3D.create((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2)
        return tbm.createBox(adsk.core.OrientedBoundingBox3D.create(c, adsk.core.Vector3D.create(1, 0, 0), adsk.core.Vector3D.create(0, 1, 0),
                                                                   hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]))

    def vcyl(x, y, z0, z1, r):
        return tbm.createCylinderOrCone(P3(x, y, z0), r / 10.0, P3(x, y, z1), r / 10.0)

    def ycyl(x, z, y0, y1, r):
        return tbm.createCylinderOrCone(P3(x, y0, z), r / 10.0, P3(x, y1, z), r / 10.0)

    T = P['T']; H = P['H']; Fe = P['Fe']; Be = P['Be']; pr = P['proud']; cv = P['cover']; ft = P['foot']
    G = geometry()
    rails = P['rails']

    def frame(xl, xr):
        L = []
        for x0 in (xl, xr - T):
            L.append(('2040 Upright %d' % round(H), tbox(x0, x0 + T, -T, T, 0, H)))
            L.append(('2020 Upright bumper %d' % round(H), tbox(x0, x0 + T, T, pr, 0, H)))
        for zc in rails:
            L.append(('2020 Rail %d' % round(xr - xl - 2 * T), tbox(xl + T, xr - T, -T, 0, zc - T / 2, zc + T / 2)))
        L.append(('ZONE front (knobs/bezels)', tbox(xl + T, xr - T, 0, Fe, 0, H)))
        L.append(('ZONE rear (screens/boards)', tbox(xl + T, xr - T, -T - Be, -T, T, H - T)))
        L.append(('COVER rear sheet', tbox(xl, xr, -T - Be - cv, -T - Be, 0, H)))
        for x0 in (xl, xr - T):
            L.append(('COVER rear lip', tbox(x0, x0 + T, -T - Be, -T, 0, H)))
        for z0 in (0, H - cv):
            L.append(('COVER rear lip', tbox(xl + T, xr - T, -T - Be, -T, z0, z0 + cv)))
            L.append(('SHEET front edge lip 3 mm', tbox(xl + T, xr - T, 0, pr, z0, z0 + cv)))
        return L

    def leaf(xface, side, label):
        x0, x1 = xface, xface + side * 1.4
        return (label, tbox(min(x0, x1), max(x0, x1), pr - 20, pr, 10, H - 10))

    def add_comp(name, items):
        occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        comp = occ.component
        comp.name = name
        bf = comp.features.baseFeatures.add()
        bf.startEdit()
        for nm, b in items:
            nb = comp.bRepBodies.add(b, bf)
            nb.name = nm
        bf.finishEdit()
        return occ

    def outrigger(xp, length, sign, label):
        x0, x1 = xp, xp + sign * length
        return (label, tbox(min(x0, x1), max(x0, x1), -T, 0, -ft, -ft + 20))

    # right half (stays on the desk; clamp feet + outriggers)
    xr0, xr1 = G['right']
    r = frame(xr0, xr1)
    r.append(leaf(xr0, -1, 'HINGE leaf R'))
    r.append(('HINGE knuckle', vcyl(G['A'][0], G['A'][1], 10, H - 10, 3.0)))
    for xu in (xr0, xr1 - T):
        r.append(('PRINT clamp foot', tbox(xu, xu + T, -T, pr, -ft, 0)))
        r.append(('PRINT desk clamp jaw', tbox(xu, xu + T, pr, pr + 12, -ft - 60, -ft)))
        r.append(('PRINT desk clamp jaw', tbox(xu, xu + T, -T, pr + 12, -ft - 72, -ft - 60)))
    occR = add_comp('Right half', r)
    xm = (xr0 + xr1) / 2
    occRO1 = add_comp('Right outrigger A', [outrigger(xm - 140, P['out_c'], +1, '2020 Outrigger %d' % P['out_c'])])
    occRO2 = add_comp('Right outrigger B', [outrigger(xm + 140, P['out_c'], -1, '2020 Outrigger %d' % P['out_c'])])

    # left half (folds); two outriggers carry the yoke shelf under the PFD
    xl0, xl1 = G['left']
    l = frame(xl0, xl1)
    l.append(leaf(xl1, +1, 'HINGE leaf L'))
    occL = add_comp('Left half', l)
    occLO = add_comp('Left outrigger outer', [outrigger(xl0 + 30, P['out_lo'], +1, '2020 Outrigger %d' % P['out_lo']),
                                             ('PRINT outrigger riser', tbox(xl0 + 20, xl0 + 40, -T, 0, -ft + 20, 0))])
    occLI = add_comp('Left outrigger inner', [outrigger(xl1 - 30, P['out_li'], -1, '2020 Outrigger %d' % P['out_li']),
                                             ('PRINT outrigger riser', tbox(xl1 - 40, xl1 - 20, -T, 0, -ft + 20, 0))])

    # desk-side envelopes
    yb = -T - Be - cv
    yx = P['yoke_x']; tx = P['thr_x']; yoke_z = 100.0 - ft
    env = [
        ('ENVELOPE yoke shelf plate (on the two left outriggers)', tbox(yx - 160, yx + 160, -350, yb - 25, -ft, -ft + 6)),
        ('ENVELOPE Logitech yoke housing (approx)', tbox(yx - 120, yx + 120, -320, yb - 30, -ft + 6, -ft + 146)),
        ('ENVELOPE Yoke shaft (through panel)', ycyl(yx, yoke_z, yb - 30, 150, 13)),
        ('ENVELOPE Yoke handles (approx)', tbox(yx - 140, yx + 140, 150, 200, yoke_z - 60, yoke_z + 60)),
        ('ENVELOPE Throttle quadrant at desk edge (approx)', tbox(tx - 50, tx + 50, pr + 15, pr + 145, -ft, -ft + 110)),
    ]
    occE = add_comp('Desk controls', env)

    occR.isGrounded = True
    occE.isGrounded = True
    for occ in (occR, occL, occRO1, occRO2, occLO, occLI, occE):
        for b in occ.component.bRepBodies:
            if b.name.startswith('ZONE'):
                b.opacity = 0.15
            elif b.name.startswith('ENVELOPE'):
                b.opacity = 0.3

    def pivot_point(occ, px, py):
        comp = occ.component
        sk = comp.sketches.add(comp.xYConstructionPlane)
        sk.name = 'Hinge axis'
        sp = sk.sketchPoints.add(sk.modelToSketchSpace(P3(px, py, 0)))
        sk.isLightBulbOn = False
        return sp.createForAssemblyContext(occ)

    def joint(name, moving, fixed, piv):
        jg = adsk.fusion.JointGeometry.createByPoint(pivot_point(moving, piv[0], piv[1]))
        ji = root.asBuiltJoints.createInput(moving, fixed, jg)
        ji.setAsRevoluteJointMotion(adsk.fusion.JointDirections.ZAxisJointDirection)
        j = root.asBuiltJoints.add(ji)
        j.name = name
        return j

    joint('Fold hinge', occL, occR, G['A'])
    joint('Right outrigger A swing', occRO1, occR, (xm - 140, -10))
    joint('Right outrigger B swing', occRO2, occR, (xm + 140, -10))
    joint('Left outrigger outer swing', occLO, occL, (xl0 + 30, -10))
    joint('Left outrigger inner swing', occLI, occL, (xl1 - 30, -10))
    print('bifold geometry', G)


def run(_context: str):
    build()
