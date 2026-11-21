# Rev E: Vevor stock only (2020 / 2040). Uprights = 2040 + 2020 bumper bolted on the front (acts like 2060,
# 40 mm proud of the 2020 rails). Piano hinges mounted on the SIDE faces of the uprights (leaves hidden in the
# seam, knuckle on the front edge). 3 mm edge lips on top/bottom so the folded case is sealed.
# Single hinge on the left, hinge | 98 mm spacer | hinge on the right, outriggers + desk clamps.
# Units: mm. Frame: X = right, Y = toward pilot, Z = up. Panel bottom z = 0, desk at z = -foot.
import adsk.core, adsk.fusion, math

P = dict(
    W=350.0,     # center + right wing width (center inner 310 holds the 300 mm GDU 1040 PFD)
    WL=310.0,    # left wing: far edge must clear the audio-panel knobs on the right spacer when closed
    H=375.6,     # 4 bays of 88.9 mm (2U EIA-310) + 20 mm rail
    T=20.0,
    proud=40.0,  # 2060 uprights stand 40 mm in front of the rail face
    Fe=40.0,     # knob budget from rail face (fully inside the upright depth)
    Be=30.0,     # electronics behind rails, inside rear cover
    cover=3.0,
    clr=5.0,
    hg=1.5,      # half gap at hinges (two hinge leaves sit in the seam)
    kn=2.5,      # knuckle axis in front of the upright face (knuckle rides on the front edge)
    # rails placed per panel to suit realistic module sizes (rail centerlines, mm from panel bottom)
    rails_L=[10.0, 70.0, 170.0, 365.6],     # switch row 60 | flex bay 100 | standby instruments 195.6
    rails_C=[10.0, 110.0, 310.0, 365.6],    # yoke + dimmers 100 | PFD 200 | top strip 55.6
    rails_R=[10.0, 110.0, 310.0, 365.6],    # copilot yoke 100 | MFD 200 | top strip 55.6
    foot=40.0,
    out_c=135.0,
    out_w=230.0,
    yoke_x=0.0,      # pilot yoke on the PFD centerline (pilot sits square to the PFD, as in the C172)
    thr_x=250.0,     # throttle on the aircraft centerline (audio panel / MFD seam)
)


def geometry():
    W = P['W']; hg = P['hg']; pr = P['proud']
    yp = pr + P['kn']                                   # hinge axis line
    back = P['T'] + P['Be'] + P['cover']                # rail face to back of cover
    left_back = 2 * yp + back                           # closed left wing: back of its cover
    right_face = left_back + P['clr']                   # closed right wing: upright front face
    sR = right_face + pr - 2 * yp                       # right spacer pivot-to-pivot
    AL = (-W / 2 - hg, yp)
    AR = (W / 2 + hg, yp); BR = (AR[0] + sR, yp)
    return dict(yp=yp, left_back=left_back, right_face=right_face, sR=sR, AL=AL, AR=AR, BR=BR,
                knob_gap=2 * yp)


def build():
    app = adsk.core.Application.get()
    d = adsk.fusion.Design.cast(app.activeProduct)
    if d.designIntent == adsk.fusion.DesignIntentTypes.PartDesignIntentType:
        d.designIntent = adsk.fusion.DesignIntentTypes.HybridDesignIntentType
    root = d.rootComponent
    zup = app.preferences.generalPreferences.defaultModelingOrientation == \
        adsk.core.DefaultModelingOrientations.ZUpModelingOrientation
    tbm = adsk.fusion.TemporaryBRepManager.get()

    def W_(x, y, z):
        if zup:
            return (x / 10.0, -y / 10.0, z / 10.0)
        return (x / 10.0, z / 10.0, y / 10.0)

    def P3(x, y, z):
        return adsk.core.Point3D.create(*W_(x, y, z))

    def tbox(x0, x1, y0, y1, z0, z1):
        a = W_(x0, y0, z0); b = W_(x1, y1, z1)
        lo = [min(a[i], b[i]) for i in range(3)]; hi = [max(a[i], b[i]) for i in range(3)]
        c = adsk.core.Point3D.create((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2)
        obb = adsk.core.OrientedBoundingBox3D.create(
            c, adsk.core.Vector3D.create(1, 0, 0), adsk.core.Vector3D.create(0, 1, 0),
            hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2])
        return tbm.createBox(obb)

    def vcyl(x, y, z0, z1, r):
        return tbm.createCylinderOrCone(P3(x, y, z0), r / 10.0, P3(x, y, z1), r / 10.0)

    def ycyl(x, z, y0, y1, r):
        return tbm.createCylinderOrCone(P3(x, y0, z), r / 10.0, P3(x, y1, z), r / 10.0)

    def cut(a, b):
        tbm.booleanOperation(a, b, adsk.fusion.BooleanTypes.DifferenceBooleanType)
        return a

    T = P['T']; H = P['H']; Wp = P['W']; Fe = P['Fe']; Be = P['Be']; pr = P['proud']; cv = P['cover']
    ft = P['foot']; hg = P['hg']
    G = geometry()
    yoke_z = 100.0 - ft

    def frame(xl, xr, rails_z):
        L = []
        for x0 in (xl, xr - T):
            L.append(('2040 Upright %d' % round(H), tbox(x0, x0 + T, -T, T, 0, H)))
            L.append(('2020 Upright bumper %d' % round(H), tbox(x0, x0 + T, T, pr, 0, H)))
        for zc in rails_z:
            L.append(('2020 Rail %d' % round(xr - xl - 2 * T), tbox(xl + T, xr - T, -T, 0, zc - T / 2, zc + T / 2)))
        L.append(('ZONE front (knobs/bezels)', tbox(xl + T, xr - T, 0, Fe, 0, H)))
        L.append(('ZONE rear (screens/boards)', tbox(xl + T, xr - T, -T - Be, -T, T, H - T)))
        L.append(('COVER rear sheet', tbox(xl, xr, -T - Be - cv, -T - Be, 0, H)))
        L.append(('COVER rear lip', tbox(xl, xl + T, -T - Be, -T, 0, H)))
        L.append(('COVER rear lip', tbox(xr - T, xr, -T - Be, -T, 0, H)))
        for z0 in (0, H - cv):
            L.append(('COVER rear lip', tbox(xl + T, xr - T, -T - Be, -T, z0, z0 + cv)))
            L.append(('SHEET front edge lip 3 mm', tbox(xl + T, xr - T, 0, pr, z0, z0 + cv)))
        return L

    def leaf(xface, side, label):
        # leaf on the side face of an upright, inside the seam (side=+1 leaf extends to +x of the face)
        x0, x1 = (xface, xface + side * 1.4)
        return (label, tbox(min(x0, x1), max(x0, x1), pr - 20, pr, 10, H - 10))

    def knuckle(axis, label):
        return (label, vcyl(axis[0], axis[1], 10, H - 10, 3.0))

    def yoke_plate(x, label, z0, z1):
        yk = tbox(x - 60, x + 60, 0, 3, z0 + 0.4, z1 - 0.4)
        cut(yk, ycyl(x, yoke_z, -1, 5, 20))
        return (label, yk)

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
        x0, x1 = (xp, xp + sign * length)
        return (label, tbox(min(x0, x1), max(x0, x1), -T, 0, -ft, -ft + 20))

    # ---------------- Center panel
    xl, xr = -Wp / 2, Wp / 2
    rc = P['rails_C']
    c = frame(xl, xr, rc)
    c.append(('BEZEL GDU 1040 PFD 300x196', tbox(-150, 150, 0, 15, (rc[1] + rc[2]) / 2 - 98, (rc[1] + rc[2]) / 2 + 98)))
    c.append(leaf(xl, -1, 'HINGE leaf L-center'))
    c.append(leaf(xr, +1, 'HINGE leaf R-center'))
    c.append(knuckle(G['AL'], 'HINGE knuckle L'))
    for xu in (xl, xr - T):
        c.append(('PRINT clamp foot', tbox(xu, xu + T, -T, pr, -ft, 0)))
        c.append(('PRINT desk clamp jaw', tbox(xu, xu + T, pr, pr + 12, -ft - 60, -ft)))
        c.append(('PRINT desk clamp jaw', tbox(xu, xu + T, -T, pr + 12, -ft - 72, -ft - 60)))
    occC = add_comp('Center panel', c)
    occOCL = add_comp('Center outrigger L', [outrigger(-140, P['out_c'], +1, '2020 Outrigger %d' % P['out_c'])])
    occOCR = add_comp('Center outrigger R', [outrigger(140, P['out_c'], -1, '2020 Outrigger %d' % P['out_c'])])

    # ---------------- Left wing: single piano hinge at the front corner
    AL = G['AL']
    wxr = AL[0] - hg; wxl = wxr - P['WL']
    rl = P['rails_L']
    lw = frame(wxl, wxr, rl)
    lw.append(('BEZEL standby instruments (placeholder)', tbox(wxl + T + 2, wxr - T - 2, 0, 15, rl[2] + 0.4, rl[3] - 0.4)))
    lw.append(leaf(wxr, +1, 'HINGE leaf L-wing'))
    occLW = add_comp('Left wing', lw)
    occOL = add_comp('Left wing outrigger', [outrigger(wxl + 30, P['out_w'], +1, '2020 Outrigger %d' % P['out_w']),
                                             ('PRINT outrigger riser', tbox(wxl + 20, wxl + 40, -T, 0, -ft + 20, 0))])

    # ---------------- Right spacer (two 2020 verticals at the front plane + 3 mm skin) and right wing
    AR, BR = G['AR'], G['BR']
    rx0 = AR[0] + hg; rx1 = BR[0] - hg
    rs = [('2020 Spacer vertical %d' % round(H), tbox(rx0, rx0 + T, pr - T, pr, 0, H)),
          ('2020 Spacer vertical %d' % round(H), tbox(rx1 - T, rx1, pr - T, pr, 0, H)),
          ('SKIN spacer 3 mm', tbox(rx0 + T, rx1 - T, pr - T, pr - T + cv, 0, H)),
          ('ZONE front (spacer modules)', tbox(rx0 + T, rx1 - T, pr - T + cv, pr + 37, 0, H)),
          ('BEZEL GMA audio (approx 64x196)', tbox((rx0 + rx1) / 2 - 32, (rx0 + rx1) / 2 + 32, pr - T + cv, pr - T + cv + 15, (P['rails_R'][1] + P['rails_R'][2]) / 2 - 98, (P['rails_R'][1] + P['rails_R'][2]) / 2 + 98)),
          leaf(rx0, -1, 'HINGE leaf R-spacer'), leaf(rx1, +1, 'HINGE leaf R-spacer'),
          ('PRINT spacer cap', tbox(rx0 + T, rx1 - T, pr - T + cv, pr + 37, 0, cv)),
          ('PRINT spacer cap', tbox(rx0 + T, rx1 - T, pr - T + cv, pr + 37, H - cv, H)),
          knuckle(AR, 'HINGE knuckle R-center'), knuckle(BR, 'HINGE knuckle R-wing')]
    occRS = add_comp('Right spacer', rs)

    wxl = BR[0] + hg; wxr = wxl + Wp
    rr = P['rails_R']
    rw = frame(wxl, wxr, rr)
    mx = (wxl + wxr) / 2
    rw.append(('BEZEL GDU 1040 MFD 300x196', tbox(mx - 150, mx + 150, 0, 15, (rr[1] + rr[2]) / 2 - 98, (rr[1] + rr[2]) / 2 + 98)))
    cop_x = 2 * P['thr_x'] - P['yoke_x']       # copilot yoke mirrored about the aircraft centerline
    if wxl + 80 < cop_x < wxr - 80:
        rw.append(yoke_plate(cop_x, 'BEZEL copilot yoke blank (future)', rr[0], rr[1]))
    rw.append(leaf(wxl, -1, 'HINGE leaf R-wing'))
    occRW = add_comp('Right wing', rw)
    occOR = add_comp('Right wing outrigger', [outrigger(wxr - 30, P['out_w'], -1, '2020 Outrigger %d' % P['out_w']),
                                              ('PRINT outrigger riser', tbox(wxr - 40, wxr - 20, -T, 0, -ft + 20, 0))])

    # ---------------- Desk-side items (not part of the case)
    yb = -T - Be - cv
    yx = P['yoke_x']; tx = P['thr_x']
    env = [
        ('ENVELOPE yoke shelf plate (on deployed center outriggers)', tbox(yx - 160, yx + 160, -350, yb - 25, -ft, -ft + 6)),
        ('ENVELOPE Logitech yoke housing (approx)', tbox(yx - 120, yx + 120, -320, yb - 30, -ft + 6, -ft + 146)),
        ('ENVELOPE Yoke shaft (through panel)', ycyl(yx, yoke_z, yb - 30, 150, 13)),
        ('ENVELOPE Yoke handles (approx)', tbox(yx - 140, yx + 140, 150, 200, yoke_z - 60, yoke_z + 60)),
        ('ENVELOPE Throttle quadrant at desk edge, aircraft centerline (approx)', tbox(tx - 50, tx + 50, pr + 15, pr + 145, -ft, -ft + 110)),
    ]
    occE = add_comp('Desk controls', env)

    occC.isGrounded = True
    occE.isGrounded = True
    for occ in (occC, occLW, occRS, occRW, occOCL, occOCR, occOL, occOR, occE):
        for b in occ.component.bRepBodies:
            if b.name.startswith('ZONE'):
                b.opacity = 0.15
            elif b.name.startswith('ENVELOPE'):
                b.opacity = 0.3

    def pivot_point(occ, px, py):
        comp = occ.component
        sk = comp.sketches.add(comp.xYConstructionPlane)
        sk.name = 'Hinge axis'
        w = W_(px, py, 0)
        sp = sk.sketchPoints.add(sk.modelToSketchSpace(adsk.core.Point3D.create(*w)))
        return sp.createForAssemblyContext(occ)

    vdir = adsk.fusion.JointDirections.ZAxisJointDirection if zup else adsk.fusion.JointDirections.YAxisJointDirection

    def joint(name, moving, fixed, piv):
        jg = adsk.fusion.JointGeometry.createByPoint(pivot_point(moving, piv[0], piv[1]))
        ji = root.asBuiltJoints.createInput(moving, fixed, jg)
        ji.setAsRevoluteJointMotion(vdir)
        j = root.asBuiltJoints.add(ji)
        j.name = name
        return j

    joint('Left wing hinge', occLW, occC, AL)
    joint('Right spacer hinge', occRS, occC, AR)
    joint('Right wing hinge', occRW, occRS, BR)
    joint('Center outrigger L swing', occOCL, occC, (-140, -10))
    joint('Center outrigger R swing', occOCR, occC, (140, -10))
    joint('Left outrigger swing', occOL, occLW, (AL[0] - hg - P['WL'] + 30, -10))
    joint('Right outrigger swing', occOR, occRW, (BR[0] + hg + Wp - 30, -10))
    print('geometry', G)


def run(_context: str):
    build()
