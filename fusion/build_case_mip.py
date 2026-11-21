# 737DIYSIM C172 MIP (V2) in our folding case - iteration 2, sized to his real modules.
# His G1000 knobs stand ~42 mm proud of the panel, so the folded face gap must be ~90 mm. His panel is cut
# between the PFD and the GMA 1347 (u 430) and between the GMA and the MFD (u 496); a new 85 mm spacer plate
# carries the GMA 1347 mounted FLUSH (sunk 16 mm) so nothing on the spacer sticks into the folded case.
# The right part (MFD, standby, ELT) moves 25 mm right. Panel face is flush with the front of the frame.
# Units mm. My frame: X right (pilot view), Y toward pilot, Z up; panel front at y = 0, bottom at z = 0.
# Final pilot coordinate u = x + 460.
import adsk.core, adsk.fusion, math

P = dict(
    T=20.0, t_panel=9.0,
    uB=431.5, uA=519.5,          # hinge axes (final u); 88 mm apart -> ~93 mm face gap when folded
    hg=1.5, kn=2.5,
    cut_left=430.0, cut_right=496.0, shift_right=25.0,
    gma_u=476.0, gma_w=48.0, gma_z0=129.5, gma_z1=327.5,
    gauge_shift=83.0,            # his ASI/attitude/altimeter block moves +83 mm (into the old copilot-yoke area)
    yoke_u=283.8, yoke_z=60.0, yoke_d=40.0,
    rear=70.0,                   # his ASI case is ~65 mm behind the panel
    foot=40.0,
)


def X(u):
    return u - 460.0


def build():
    app = adsk.core.Application.get()
    d = adsk.fusion.Design.cast(app.activeProduct)
    root = d.rootComponent
    tbm = adsk.fusion.TemporaryBRepManager.get()

    def F(x, y, z):
        return adsk.core.Point3D.create(x / 10.0, -y / 10.0, z / 10.0)

    def box(x0, x1, y0, y1, a, b):
        p = F(x0, y0, a); q = F(x1, y1, b)
        lo = [min(p.x, q.x), min(p.y, q.y), min(p.z, q.z)]; hi = [max(p.x, q.x), max(p.y, q.y), max(p.z, q.z)]
        c = adsk.core.Point3D.create((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2)
        return tbm.createBox(adsk.core.OrientedBoundingBox3D.create(c, adsk.core.Vector3D.create(1, 0, 0), adsk.core.Vector3D.create(0, 1, 0),
                                                                   hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]))

    def ycyl(x, z, y0, y1, r):
        return tbm.createCylinderOrCone(F(x, y0, z), r / 10.0, F(x, y1, z), r / 10.0)

    def vcyl(x, y, z0, z1, r):
        return tbm.createCylinderOrCone(F(x, y, z0), r / 10.0, F(x, y, z1), r / 10.0)

    def op(a, b, kind):
        return tbm.booleanOperation(a, b, kind)

    SUB = adsk.fusion.BooleanTypes.DifferenceBooleanType
    UNI = adsk.fusion.BooleanTypes.UnionBooleanType
    INT = adsk.fusion.BooleanTypes.IntersectionBooleanType
    T = P['T']; tp = P['t_panel']

    # ---- his panel (inserted design "MIP"), turned to face the pilot
    src = None
    for o in root.allOccurrences:
        if o.fullPathName.startswith('MIP'):
            for b in o.bRepBodies:
                if b.boundingBox.maxPoint.x - b.boundingBox.minPoint.x > 90:
                    src = b
    panel = tbm.copy(src)
    m = adsk.core.Matrix3D.create()
    m.setToRotation(math.pi, adsk.core.Vector3D.create(0, 0, 1), adsk.core.Point3D.create(0, 0, 0))
    tbm.transform(panel, m)
    mt = adsk.core.Matrix3D.create(); mt.translation = adsk.core.Vector3D.create(7.0, 0.4, 15.05)
    tbm.transform(panel, mt)

    uA, uB, hg = P['uA'], P['uB'], P['hg']
    dR = P['shift_right']
    left_panel = tbm.copy(panel)
    if not op(left_panel, box(X(-20), X(P['cut_left']), -tp - 5, 5, -5, 380), INT):
        raise RuntimeError('left split failed')
    right_panel = tbm.copy(panel)
    if not op(right_panel, box(X(P['cut_right']), X(940), -tp - 5, 5, -5, 380), INT):
        raise RuntimeError('right split failed')
    mv = adsk.core.Matrix3D.create(); mv.translation = adsk.core.Vector3D.create(dR / 10.0, 0, 0)
    tbm.transform(right_panel, mv)
    op(left_panel, ycyl(X(P['yoke_u']), P['yoke_z'], -tp - 1, 1, P['yoke_d'] / 2), SUB)
    # standby gauges: re-use HIS cutout shapes (ASI / attitude / altimeter + screw holes), moved +83 mm into the
    # old copilot-yoke area: plugs = slab minus his panel over the gauge region, then fill + re-cut
    plugs = box(X(434.0), X(702.0), -tp, 0, 22.0, 122.0)
    op(plugs, panel, SUB)
    mg = adsk.core.Matrix3D.create(); mg.translation = adsk.core.Vector3D.create(P['gauge_shift'] / 10.0, 0, 0)
    tbm.transform(plugs, mg)
    op(right_panel, box(X(P['cut_right'] + dR), X(702.0 + P['gauge_shift']), -tp, 0, 22.0, 122.0), UNI)
    op(right_panel, plugs, SUB)
    s0, s1 = uB + hg, uA - hg
    spacer_panel = box(X(s0), X(s1), -tp, 0, 0, 369.0)
    op(spacer_panel, box(X(P['gma_u'] - P['gma_w'] / 2), X(P['gma_u'] + P['gma_w'] / 2), -tp - 1, 1, P['gma_z0'], P['gma_z1']), SUB)
    l0, l1 = 0.0, uB - hg
    r0, r1 = uA + hg, 920.0 + dR

    def frame(u0, u1, outer_left, outer_right, rails):
        L = []
        hz = 216.5
        if outer_left:
            L.append(('2040 Upright %d' % hz, box(X(u0), X(u0) + T, -tp - 40, -tp, 0, hz)))
        if outer_right:
            L.append(('2040 Upright %d' % hz, box(X(u1) - T, X(u1), -tp - 40, -tp, 0, hz)))
        for (a, b, zc) in rails:
            L.append(('2020 Rail %d' % round(b - a), box(X(a), X(b), -tp - T, -tp, zc - T / 2, zc + T / 2)))
        return L

    def seam_angle(u_edge, side):
        x = X(u_edge)
        x0, x1 = (x - 2, x) if side < 0 else (x, x + 2)
        a = box(x0, x1, -tp - 20, -tp, 0, 369.0)
        x0, x1 = (x - 20, x) if side < 0 else (x, x + 20)
        op(a, box(x0, x1, -tp - 2, -tp, 0, 369.0), UNI)
        return ('ALU angle 20x20x2 (seam)', a)

    def add(name, items, grounded=False):
        occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        comp = occ.component; comp.name = name
        bf = comp.features.baseFeatures.add(); bf.startEdit()
        for nm, b in items:
            nb = comp.bRepBodies.add(b, bf); nb.name = nm
        bf.finishEdit()
        occ.isGrounded = grounded
        return occ

    ft = P['foot']; yk = P['kn']
    left = [('PANEL 737DIYSIM MIP - left (switches + PFD)', left_panel), seam_angle(l1, -1),
            ('HINGE leaf', box(X(l1), X(l1) + 1.4, -tp - 20, 0, 10, 359))]
    left += frame(l0, l1, True, False, [(l0 + T, l1 - 2, 10.0), (215.5, l1 - 2, 126.0)])
    for xu in (X(l0), X(l1) - 40):
        left.append(('PRINT foot', box(xu, xu + T, -tp - 40, 0, -ft, 0)))
    spacer = [('PANEL spacer (GMA 1347, flush)', spacer_panel), seam_angle(s0, +1), seam_angle(s1, -1),
              ('HINGE knuckle B', vcyl(X(uB), yk, 10, 359, 3.0)), ('HINGE knuckle A', vcyl(X(uA), yk, 10, 359, 3.0))]
    right = [('PANEL 737DIYSIM MIP - right (MFD + standby)', right_panel), seam_angle(r0, +1),
             ('HINGE leaf', box(X(r0) - 1.4, X(r0), -tp - 20, 0, 10, 359))]
    right += frame(r0, r1, False, True, [(r0 + 2, r1 - T, 10.0), (r0 + 2, r1 - T, 126.0)])
    for xu in (X(r0) + 2, X(r1) - T):
        right.append(('PRINT clamp foot', box(xu, xu + T, -tp - 40, 0, -ft, 0)))
        right.append(('PRINT desk clamp jaw', box(xu, xu + T, 0, 12, -ft - 60, -ft)))

    occR = add('Right half', right, grounded=True)
    occS = add('Spacer', spacer)
    occL = add('Left half', left)

    def pivot_point(occ, px, py):
        comp = occ.component
        sk = comp.sketches.add(comp.xYConstructionPlane)
        sk.name = 'Hinge axis'
        sp = sk.sketchPoints.add(sk.modelToSketchSpace(F(px, py, 0)))
        sk.isLightBulbOn = False
        return sp.createForAssemblyContext(occ)

    def joint(name, moving, fixed, px):
        jg = adsk.fusion.JointGeometry.createByPoint(pivot_point(moving, px, yk))
        ji = root.asBuiltJoints.createInput(moving, fixed, jg)
        ji.setAsRevoluteJointMotion(adsk.fusion.JointDirections.ZAxisJointDirection)
        j = root.asBuiltJoints.add(ji); j.name = name
        return j

    joint('Spacer hinge', occS, occR, X(uA))
    joint('Left hinge', occL, occS, X(uB))
    print('MIP case v2: left u 0-%.1f, spacer %.1f-%.1f (%.0f wide), right %.1f-%.1f; panel now %.0f wide'
          % (l1, s0, s1, s1 - s0, r0, r1, r1))


def run(_context: str):
    build()
