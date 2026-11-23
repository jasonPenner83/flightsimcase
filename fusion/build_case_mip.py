# 737DIYSIM C172 MIP (V2) in our folding case - iteration 2, sized to his real modules.
# His G1000 knobs stand ~42 mm proud of the panel, so the folded face gap must be ~90 mm. His panel is cut
# between the PFD and the GMA 1347 (u 430) and between the GMA and the MFD (u 496); a new 85 mm spacer plate
# carries the GMA 1347 mounted FLUSH (sunk 16 mm) so nothing on the spacer sticks into the folded case.
# The right part (MFD, standby, ELT) moves 25 mm right. Panel face is flush with the front of the frame.
# Units mm. My frame: X right (pilot view), Y toward pilot, Z up; panel front at y = 0, bottom at z = 0.
# Final pilot coordinate u = x + 460.
import adsk.core, adsk.fusion, math, importlib.util

P = dict(
    T=20.0, t_panel=9.0,
    uB=431.5, uA=519.5,          # hinge axes (final u); 88 mm apart -> ~93 mm face gap when folded
    hg=1.5, kn=2.5,
    cut_left=430.0, cut_right=496.0, shift_right=25.0,
    gma_u=476.0, gma_w=48.0, gma_z0=129.5, gma_z1=327.5,
    gauge_shift=90.0,            # his ASI/attitude/altimeter block moves +90 mm (old copilot-yoke area; clears the seam edge + rear tub wall)
    yoke_u=283.8, yoke_z=33.0, yoke_d=40.0,  # Logitech yoke shaft ~36 mm above the desk (desk top = z -3): hole + slot to the bottom edge
    rear=70.0,                   # his ASI case is ~65 mm behind the panel
    foot=40.0,
    z_low=0.0,                   # bottom of the MAIN unit panels; the main unit sits on the desk (its 3 mm bottom skin at z -3..0)
    desk_z=-3.0, desk_edge=40.0, desk_t=38.0,   # deployed: desk top, desk front edge 40 mm behind the panel face, 1.5 in thick
    lower_top=-3.0, lower_bot=-173.0,            # separate lower panel pieces hang below the desk top, in front of its edge
    lower_drop=48.0,             # lower modules move down 48 mm so everything deep sits under the desk (underside z -41)
    yoke_box=(158.8, 408.8, 250.0, 71.25),        # Logitech yoke housing: u range, depth, height (on the desk, front at the desk edge)
    tunnel=(153.0, 409.0, -5.0, 75.0),           # tunnel through the left box for the housing (u0, u1, z0, z1)
    # open face pockets (u0, u1, z0, z1): blank panel areas that face the other half's protruding parts when
    # closed, so they double as storage pockets; between the 2020 rails at z 10 and z 126
    square_top=False,            # Jason: KEEP his curved top corners
    r_ext=6.0,                   # right half is 6 mm narrower than the left (424 vs 430): a 6 mm edge filler on its outer
                                 # edge evens them so the forward-extended rims meet exactly when folded
    rim=46.5,                    # each half's rim (top, curved corner, outer side, bottom) runs this far in front of the face
    skin=3.0,
    pockets=(),                  # face pockets removed (left: yoke tunnel; right: flaps lever moved up there)
    flaps_cut=(867.0, 931.5, 154.0, 232.0),       # flaps lever: right of the MFD, below the ELT
    fsp_cut=(811.0, 921.0, 1.0, 112.0),           # fuel selector (trimmed 109 mm face) right of the standby gauges, under the MFD
    key_cut=(339.5, 383.5, 69.5, 113.5),          # ignition key, left half between the yoke and the seam, above the yoke housing
    lower_bot_right=-225.0,      # right lower piece is taller: the trim wheel (172 mm case) sits left of the throttle
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
    T = P['T']; tp = P['t_panel']; zl = P['z_low']

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
    # slot from the yoke hole down to the bottom edge: the main unit lowers straight down over the yoke shaft
    op(left_panel, box(X(P['yoke_u'] - P['yoke_d'] / 2), X(P['yoke_u'] + P['yoke_d'] / 2), -tp - 1, 1, -1.0, P['yoke_z']), SUB)
    # standby gauges: re-use HIS cutout shapes (ASI / attitude / altimeter + screw holes), moved +83 mm into the
    # old copilot-yoke area: plugs = slab minus his panel over the gauge region, then fill + re-cut
    plugs = box(X(434.0), X(702.0), -tp, 0, 22.0, 122.0)
    op(plugs, panel, SUB)
    mg = adsk.core.Matrix3D.create(); mg.translation = adsk.core.Vector3D.create(P['gauge_shift'] / 10.0, 0, 0)
    tbm.transform(plugs, mg)
    op(right_panel, box(X(P['cut_right'] + dR), X(702.0 + P['gauge_shift']), -tp, 0, 22.0, 122.0), UNI)
    op(right_panel, plugs, SUB)
    for host, p0, p1, q0, q1 in P['pockets']:
        tgt = left_panel if host == 'Left half' else right_panel
        if not op(tgt, box(X(p0), X(p1), -tp - 1, 1, q0, q1), SUB):
            raise RuntimeError('pocket cut failed')
    for nm_, tgt_ in (('flaps_cut', 'R'), ('fsp_cut', 'R'), ('key_cut', 'L')):
        fc = P[nm_]
        op(right_panel if tgt_ == 'R' else left_panel, box(X(fc[0]), X(fc[1]), -tp - 1, 1, fc[2], fc[3]), SUB)
    if P['square_top']:          # fill his curved top corners (quarter-ellipse-ish NURBS from z 216 / 236 mm in)
        op(left_panel, box(X(0.0), X(237.0), -tp, 0, 215.0, 369.0), UNI)
        op(right_panel, box(X(920.0 + dR - 237.0), X(920.0 + dR), -tp, 0, 215.0, 369.0), UNI)
    s0, s1 = uB + hg, uA - hg
    spacer_panel = box(X(s0), X(s1), -tp, 0, 0, 369.0)
    op(spacer_panel, box(X(P['gma_u'] - P['gma_w'] / 2), X(P['gma_u'] + P['gma_w'] / 2), -tp - 1, 1, P['gma_z0'], P['gma_z1']), SUB)
    l0, l1 = 0.0, uB - hg
    r0, r1 = uA + hg, 920.0 + dR

    _sp = importlib.util.spec_from_file_location('ext', r'D:/Admin/Documents/Projects/FlightSimCase/fusion/ext.py')
    _ext = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_ext)
    prof = _ext.make(tbm, F)        # real Vevor 2020 / 2040 cross-sections

    def frame(u0, u1, outer_left, outer_right, rails):
        L = []
        hz = 369.0 if P['square_top'] else 216.5
        if outer_left:
            L.append(('2040 Upright %d' % (hz - zl), prof(X(u0), X(u0) + T, -tp - 40, -tp, zl, hz)))
        if outer_right:
            L.append(('2040 Upright %d' % (hz - zl), prof(X(u1) - T, X(u1), -tp - 40, -tp, zl, hz)))
        for (a, b, zc) in rails:
            L.append(('2020 Rail %d' % round(b - a), prof(X(a), X(b), -tp - T, -tp, zc - T / 2, zc + T / 2)))
        return L

    def seam_angle(u_edge, side, leaf=20.0):
        x = X(u_edge)
        x0, x1 = (x - 2, x) if side < 0 else (x, x + 2)
        a = box(x0, x1, -tp - 20, -tp, zl, 369.0)
        x0, x1 = (x - leaf, x) if side < 0 else (x, x + leaf)
        op(a, box(x0, x1, -tp - 2, -tp, zl, 369.0), UNI)
        return ('ALU angle 20x20x2 (seam)' if leaf == 20.0 else 'ALU angle 20x%dx2 (seam, trimmed)' % leaf, a)

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
            ('HINGE leaf', box(X(l1), X(l1) + 1.4, -tp - 20, 0, zl + 10, 359))]
    left += frame(l0, l1, True, False, [(l0 + T, P['tunnel'][0], 10.0), (215.5, l1 - 20, 126.0), (240.0, l1 - 20, 359.0)])
    spacer = [('PANEL spacer (GMA 1347, flush)', spacer_panel), seam_angle(s0, +1, 16.0), seam_angle(s1, -1, 16.0),   # leaves trimmed: the flush GMA 1347 base plate sits between them
             
              ('HINGE knuckle B', vcyl(X(uB), yk, zl + 10, 359, 3.0)), ('HINGE knuckle A', vcyl(X(uA), yk, zl + 10, 359, 3.0))]
    rs_name, rs_body = seam_angle(r0, +1)
    op(rs_body, box(X(r0) - 1, X(r0) + 21, -tp - 2.5, -tp + 0.5, 18.0, 126.0), SUB)   # leaf notched behind the ASI faceplate
    right = [('PANEL 737DIYSIM MIP - right (MFD + standby)', right_panel), (rs_name + ' notched', rs_body),
             ('HINGE leaf', box(X(r0) - 1.4, X(r0), -tp - 20, 0, zl + 10, 359))]
    r1f = r1 + P['r_ext']           # outer frame line of the right half (after the edge filler)
    right += frame(r0, r1f, False, True, [(r0 + 20, 795.0, 10.0), (r0 + 20, r1f - T, 126.0), (r0 + 20, 705.0, 359.0)])   # bottom rail stops at the fuel selector
    occR = add('Right half', right, grounded=True)
    occS = add('Spacer', spacer)
    occL = add('Left half', left)
    # add-on pods (Jason 2026-11-23): trim wheel and throttle/mixture/condition, each its own clamp-on piece that hangs
    # under the main unit's front edge when wanted and packs separately
    for nm in ('Pod: trim wheel (clamp-on)', 'Pod: TPM quadrant (clamp-on)'):
        po = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        po.component.name = nm
        po.isGrounded = True

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
