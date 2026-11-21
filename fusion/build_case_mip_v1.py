# 737DIYSIM C172 MIP (V2) in our folding case.
# His panel (design "MIP" in the Flight Sim Case project, inserted as a referenced component) is copied,
# turned to face the pilot, and split into: LEFT (switch panel + PFD), SPACER (audio panel + 2-1/4 in ASI),
# RIGHT (MFD + attitude + altimeter + ELT). Piano hinges at both spacer edges; the spacer width sets the
# face-to-face gap when folded (Jason's "spacer at the audio panel" idea). The panel face is flush with the
# front of the aluminium frame (frame sits behind the panel).
# Units mm. My frame: X right (pilot view), Y toward pilot, Z up; panel front face at y = 0, bottom at z = 0.
# Pilot coordinate u = x + 460 (0 = pilot-left edge of his 920 mm panel).
import adsk.core, adsk.fusion, math

P = dict(
    T=20.0, t_panel=9.0,          # his panel is 9 mm (MDF in his build; 6-9 mm ACM/ply recommended)
    uA=501.0, uB=436.0,          # hinge axes (u): right hinge (fixed side) and left hinge
    hg=1.5, kn=2.5,              # half gap at hinges, knuckle axis in front of the face
    zone=33.5,                   # module depth in front of the face (15 mm bezel + 18.5 mm knob)
    zone_spacer=8.0,             # audio keys / ASI bezel depth on the spacer
    rear=50.0,                   # electronics depth behind the panel
    foot=40.0,
    gauges_u=(552.0, 642.0, 732.0), gauge_z=72.2,   # ASI / attitude / altimeter, moved right (no copilot yoke)
    yoke_u=283.8, yoke_z=60.0, yoke_d=40.0,   # pilot yoke through the panel (PFD centerline)
)


AUDIO_DEPTH = 3.0


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
        tbm.booleanOperation(a, b, kind)

    SUB = adsk.fusion.BooleanTypes.DifferenceBooleanType
    UNI = adsk.fusion.BooleanTypes.UnionBooleanType
    INT = adsk.fusion.BooleanTypes.IntersectionBooleanType
    T = P['T']; tp = P['t_panel']

    # ---- his panel: find, copy, turn 180 deg about Z (front to the pilot, pilot-left to -X), place
    src = None
    for o in root.allOccurrences:
        for b in o.bRepBodies:
            if b.boundingBox.maxPoint.x - b.boundingBox.minPoint.x > 90:     # the 920 mm panel (cm units)
                src = b
    panel = tbm.copy(src)
    m = adsk.core.Matrix3D.create()
    m.setToRotation(math.pi, adsk.core.Vector3D.create(0, 0, 1), adsk.core.Point3D.create(0, 0, 0))
    tbm.transform(panel, m)
    mt = adsk.core.Matrix3D.create()
    mt.translation = adsk.core.Vector3D.create(7.0, 0.4, 15.05)
    tbm.transform(panel, mt)

    # ---- our changes to his panel
    # 1) standby gauges moved right into the (dropped) copilot-yoke area: fill his three cutouts, re-cut 81 mm holes
    op(panel, box(X(434.0), X(702.0), -tp, 0, 22.0, 122.0), UNI)
    for gu in P['gauges_u']:
        op(panel, ycyl(X(gu), P['gauge_z'], -tp - 1, 1, 40.5), SUB)
        for dx in (-32, 32):
            for dz in (-32, 32):
                op(panel, ycyl(X(gu) + dx, P['gauge_z'] + dz, -tp - 1, 1, 2.2), SUB)
    # 2) pilot yoke through the panel
    op(panel, ycyl(X(P['yoke_u']), P['yoke_z'], -tp - 1, 1, P['yoke_d'] / 2), SUB)

    uA, uB, hg = P['uA'], P['uB'], P['hg']
    pieces = {'Left half': (0.0, uB - hg), 'Spacer': (uB + hg, uA - hg), 'Right half': (uA + hg, 920.0)}
    cutbox = {'Left half': (-20.0, uB - hg), 'Spacer': (uB + hg, uA - hg), 'Right half': (uA + hg, 940.0)}

    def piece(name):
        u0, u1 = cutbox[name]
        b = tbm.copy(panel)
        ok = tbm.booleanOperation(b, box(X(u0), X(u1), -tp - 5, 5, -5, 380), INT)
        if not ok:
            raise RuntimeError('panel split failed for ' + name)
        return b

    # module envelopes (stand-ins until his module files are placed): G1000 bezels + knobs, AV switch panel,
    # standby gauges, audio panel, ELT
    def g1000(uc, name):
        out = []
        zc = 228.8; zl, zh = zc - 98, zc + 98
        xc = X(uc)
        out.append(('ZONE %s bezel 300x196 (17 deep incl. caps)' % name, box(xc - 150, xc + 150, 0, 17, zl, zh)))
        L, R = xc - 132, xc + 132
        kn = [(L, zh - 20, 5, 27.5), (L, zh - 55, 11, 33.5), (L, zh - 105, 8, 27.5), (L, zl + 25, 11, 33.5),
              (R, zh - 20, 5, 27.5), (R, zh - 55, 11, 33.5), (R, zh - 95, 11, 33.5), (R, zh - 128, 8, 27.5), (R, zl + 17, 11, 33.5)]
        for x, z, r, dpt in kn:
            out.append(('ZONE %s knob' % name, ycyl(x, z, 0, dpt, r)))
        return out

    def frame(u0, u1, outer_left, outer_right, rails):
        L = []
        hz = 216.5      # side height of his panel outline
        if outer_left:
            L.append(('2040 Upright %d' % hz, box(X(u0), X(u0) + T, -tp - 40, -tp, 0, hz)))
        if outer_right:
            L.append(('2040 Upright %d' % hz, box(X(u1) - T, X(u1), -tp - 40, -tp, 0, hz)))
        for (a, b, zc) in rails:
            L.append(('2020 Rail %d' % round(b - a), box(X(a), X(b), -tp - T, -tp, zc - T / 2, zc + T / 2)))
        return L

    def seam_angle(u_edge, side):
        # 20 x 20 x 2 aluminium angle on the panel back at a seam edge, full height (369)
        x = X(u_edge)
        x0, x1 = (x - 2, x) if side < 0 else (x, x + 2)
        a = box(x0, x1, -tp - 20, -tp, 0, 369.0)
        x0, x1 = (x - 20, x) if side < 0 else (x, x + 20)
        op(a, box(x0, x1, -tp - 2, -tp, 0, 369.0), UNI)
        return ('ALU angle 20x20x2 (seam)', a)

    def zone(u0, u1, depth, z0=0.0, z1=369.0):
        return ('ZONE front (modules)', box(X(u0), X(u1), 0, depth, z0, z1))

    def rear_zone(u0, u1):
        return ('ZONE rear (electronics)', box(X(u0) + 2, X(u1) - 2, -tp - P['rear'], -tp, 20, 360))

    def add(name, items, grounded=False):
        occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        comp = occ.component; comp.name = name
        bf = comp.features.baseFeatures.add(); bf.startEdit()
        for nm, b in items:
            nb = comp.bRepBodies.add(b, bf); nb.name = nm
        bf.finishEdit()
        occ.isGrounded = grounded
        for b in comp.bRepBodies:
            if b.name.startswith('ZONE'):
                b.opacity = 0.15
        return occ

    ft = P['foot']
    l0, l1 = pieces['Left half']
    s0, s1 = pieces['Spacer']
    r0, r1 = pieces['Right half']
    yk = P['kn']
    left = [('PANEL 737DIYSIM MIP - left (switches + PFD)', piece('Left half')),
            seam_angle(l1, -1), rear_zone(l0, l1),
            ('ZONE AV switch panel (30 deep)', box(X(27), X(215.3), 0, 30, 36, 237.5)),
            ('HINGE leaf', box(X(l1), X(l1) + 1.4, -tp - 20, 0, 10, 359))]
    left += g1000(283.8, 'PFD')
    left += frame(l0, l1, True, False, [(l0 + T, l1 - 2, 10.0), (215.5, l1 - 2, 126.0)])
    spacer = [('PANEL 737DIYSIM MIP - spacer (audio + ASI)', piece('Spacer')),
              seam_angle(s0, +1), seam_angle(s1, -1),
              ('ZONE audio panel (keys 3 deep)', box(X(450), X(485), 0, AUDIO_DEPTH, 136, 321.5)),
              ('HINGE knuckle B', vcyl(X(uB), yk, 10, 359, 3.0)), ('HINGE knuckle A', vcyl(X(uA), yk, 10, 359, 3.0))]
    right = [('PANEL 737DIYSIM MIP - right (MFD + standby)', piece('Right half')),
             seam_angle(r0, +1), rear_zone(r0, r1),
             ('ZONE airspeed (15 deep)', ycyl(X(P['gauges_u'][0]), P['gauge_z'], 0, 15, 44)),
             ('ZONE attitude (15 deep)', ycyl(X(P['gauges_u'][1]), P['gauge_z'], 0, 15, 44)),
             ('ZONE altimeter (20 deep incl. knob)', ycyl(X(P['gauges_u'][2]), P['gauge_z'], 0, 20, 44)),
             ('ZONE ELT (12 deep)', box(X(810), X(844), 0, 12, 248, 292)),
             ('HINGE leaf', box(X(r0) - 1.4, X(r0), -tp - 20, 0, 10, 359))]
    right += g1000(654.2, 'MFD')
    right += frame(r0, r1, False, True, [(r0 + 2, r1 - T, 10.0), (r0 + 2, r1 - T, 126.0)])
    for xu in (X(r0) + 2, X(r1) - T):
        right.append(('PRINT clamp foot', box(xu, xu + T, -tp - 40, 0, -ft, 0)))
        right.append(('PRINT desk clamp jaw', box(xu, xu + T, 0, 12, -ft - 60, -ft)))
    for xu in (X(l0), X(l1) - 40):
        left.append(('PRINT foot', box(xu, xu + T, -tp - 40, 0, -ft, 0)))

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
    print('MIP case built: left u %.1f-%.1f, spacer %.1f-%.1f (%.1f wide), right %.1f-%.1f; hinge spacing %.1f'
          % (l0, l1, s0, s1, s1 - s0, r0, r1, uA - uB))


def run(_context: str):
    build()
