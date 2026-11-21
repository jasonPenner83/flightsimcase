# Rev C: piano hinge | spacer | piano hinge folds, rear covers, built-in outriggers + desk clamps.
# Units in this file: mm. Frame: X = right, Y = toward pilot, Z = up. Panel bottom at z = 0, desk at z = -foot.
# Rails (2020) lie in y[-20,0]; uprights (2040) in y[-20,20], 20 mm proud of the rail face.
import adsk.core, adsk.fusion, math

P = dict(
    W=350.0,     # all three panels the same width (center inner 310 holds the 300 mm GDU 1040 PFD)
    WL=334.0,    # left wing narrower so its far edge clears the audio-panel knobs on the right spacer
    H=375.6,     # 4 bays of 88.9 mm (2U EIA-310) + 20 mm rail
    T=20.0,
    Fe=45.0,     # module envelope in front of rail face
    Be=30.0,     # module envelope behind rails (inside the rear cover)
    clr=5.0,
    pitch=88.9,
    proud=20.0,
    hg=1.0,      # half gap at each piano hinge
    spL=40.0,    # left spacer: one 2040, 40 wide
    spR=140.0,   # right spacer: two 2020 verticals + 3 mm skin, 140 wide (carries the audio panel)
    cover=3.0,   # rear cover sheet
    foot=40.0,   # feet / outrigger band under the panels (puts the yoke shaft mid-bay)
    out_c=135.0, # center outrigger length (two, stored end to end under the panel)
    out_w=250.0, # wing outrigger length
)


def geometry():
    W = P['W']; hg = P['hg']
    yL = 2 * P['Fe'] + P['clr']                          # closed left-wing rail face
    yR = yL + P['T'] + P['Be'] + P['cover'] + P['Fe'] + P['clr']   # closed right-wing rail face
    sL = P['spL'] + 2 * hg
    sR = P['spR'] + 2 * hg
    ypL = (yL - sL) / 2.0
    ypR = (yR - sR) / 2.0
    AL = (-W / 2 - hg, ypL); BL = (AL[0] - sL, ypL)
    AR = (W / 2 + hg, ypR); BR = (AR[0] + sR, ypR)
    return dict(yL=yL, yR=yR, sL=sL, sR=sR, AL=AL, BL=BL, AR=AR, BR=BR)


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
    rails_z = [T / 2 + P['pitch'] * k for k in range(int(round((H - T) / P['pitch'])) + 1)]

    def frame(xl, xr):
        L = []
        L.append(('2040 Upright %d' % round(H), tbox(xl, xl + T, -T, pr, 0, H)))
        L.append(('2040 Upright %d' % round(H), tbox(xr - T, xr, -T, pr, 0, H)))
        for zc in rails_z:
            L.append(('2020 Rail %d' % round(xr - xl - 2 * T), tbox(xl + T, xr - T, -T, 0, zc - T / 2, zc + T / 2)))
        L.append(('ZONE front (knobs/bezels)', tbox(xl + T, xr - T, 0, Fe, 0, H)))
        L.append(('ZONE rear (screens/boards)', tbox(xl + T, xr - T, -T - Be, -T, T, H - T)))
        # rear cover: 3 mm sheet + side/top/bottom lips, so the back of every panel is closed
        L.append(('COVER rear sheet', tbox(xl, xr, -T - Be - cv, -T - Be, 0, H)))
        L.append(('COVER rear lip', tbox(xl, xl + T, -T - Be, -T, 0, H)))
        L.append(('COVER rear lip', tbox(xr - T, xr, -T - Be, -T, 0, H)))
        return L

    def hinge_pad(x0, x1, label):
        # piano hinge leaf on a printed riser, full height minus 10 mm each end
        return (label, tbox(x0, x1, pr, pr + 3.0, 10, H - 10))

    def knuckle(axis, label):
        return (label, vcyl(axis[0], axis[1], 10, H - 10, 3.0))

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

    yoke_x = 0.0
    yoke_z = 100.0 - ft    # 100 mm above the desk

    def outrigger(xp, y0, length, sign, zlayer, label):
        # stored along the panel's bottom-rear, pivots 90 deg about a vertical pin at xp to point backward
        z0, z1 = zlayer
        x0, x1 = (xp, xp + sign * length) if sign > 0 else (xp + sign * length, xp)
        b = tbox(min(x0, x1), max(x0, x1), y0 - T, y0, z0, z1)
        return (label, b)

    # ---------------- Center panel
    xl, xr = -Wp / 2, Wp / 2
    c = frame(xl, xr)
    c.append(('BEZEL GDU 1040 PFD 300x196', tbox(-150, 150, 0, 15, H - 206, H - 10)))
    yk = tbox(yoke_x - 60, yoke_x + 60, 0, 4, 22, 87)
    cut(yk, ycyl(yoke_x, yoke_z, -1, 5, 20))
    c.append(('BEZEL yoke pass-through plate (2U)', yk))
    c.append(hinge_pad(xl, xl + 15, 'HINGE leaf L-center'))
    c.append(hinge_pad(xr - 15, xr, 'HINGE leaf R-center'))
    # clamp feet: 40 mm blocks under the uprights with a desk-edge C-clamp jaw at the front
    for xu in (xl, xr - T):
        c.append(('PRINT clamp foot', tbox(xu, xu + T, -T, pr, -ft, 0)))
        c.append(('PRINT desk clamp jaw', tbox(xu, xu + T, pr, pr + 12, -ft - 60, -ft)))
        c.append(('PRINT desk clamp jaw', tbox(xu, xu + T, -T, pr + 12, -ft - 72, -ft - 60)))
    occC = add_comp('Center panel', c)

    # center outriggers (stored behind the bottom of the center panel, two layers)
    yb = -T - Be - cv          # back face of the rear cover
    # all outriggers are stored UNDER their panel (y -20..0, in the 40 mm foot band) and swing 90 deg backward
    occOCL = add_comp('Center outrigger L', [outrigger(-140, 0, P['out_c'], +1, (-ft, -ft + 20), '2020 Outrigger %d' % P['out_c'])])
    occOCR = add_comp('Center outrigger R', [outrigger(140, 0, P['out_c'], -1, (-ft, -ft + 20), '2020 Outrigger %d' % P['out_c'])])

    # ---------------- Left spacer + wing
    AL, BL = G['AL'], G['BL']
    sx1 = AL[0] - hg; sx0 = sx1 - P['spL']
    ls = [('2040 Spacer %d' % round(H), tbox(sx0, sx1, 0, pr, 0, H)),
          hinge_pad(sx1 - 15, sx1, 'HINGE leaf L-spacer'), hinge_pad(sx0, sx0 + 15, 'HINGE leaf L-spacer'),
          knuckle(AL, 'HINGE knuckle L-center'), knuckle(BL, 'HINGE knuckle L-wing')]
    occLS = add_comp('Left spacer', ls)

    wxr = BL[0] - hg; wxl = wxr - P['WL']
    lw = frame(wxl, wxr)
    lw.append(('BEZEL standby/switch panel', tbox(wxl + T + 10, wxr - T - 10, 0, 15, H - 206, H - 10)))
    lw.append(hinge_pad(wxr - 15, wxr, 'HINGE leaf L-wing'))
    occLW = add_comp('Left wing', lw)
    occOL = add_comp('Left wing outrigger', [outrigger(wxl + 30, 0, P['out_w'], +1, (-ft, -ft + 20), '2020 Outrigger %d' % P['out_w']),
                                             ('PRINT outrigger foot', tbox(wxl + 20, wxl + 40, -T, 0, -ft + 20, 0))])

    # ---------------- Right spacer + wing
    AR, BR = G['AR'], G['BR']
    rx0 = AR[0] + hg; rx1 = rx0 + P['spR']
    rs = [('2020 Spacer vertical %d' % round(H), tbox(rx0, rx0 + T, 0, pr, 0, H)),
          ('2020 Spacer vertical %d' % round(H), tbox(rx1 - T, rx1, 0, pr, 0, H)),
          ('SKIN spacer 3 mm', tbox(rx0 + T, rx1 - T, 0, cv, 0, H)),
          ('ZONE front (spacer modules)', tbox(rx0 + T, rx1 - T, cv, cv + 40, 0, H)),
          ('BEZEL GMA audio (approx 64x196)', tbox((rx0 + rx1) / 2 - 32, (rx0 + rx1) / 2 + 32, cv, cv + 15, H - 206, H - 10)),
          hinge_pad(rx0, rx0 + 15, 'HINGE leaf R-spacer'), hinge_pad(rx1 - 15, rx1, 'HINGE leaf R-spacer'),
          knuckle(AR, 'HINGE knuckle R-center'), knuckle(BR, 'HINGE knuckle R-wing')]
    occRS = add_comp('Right spacer', rs)

    wxl = BR[0] + hg; wxr = wxl + Wp
    rw = frame(wxl, wxr)
    rw.append(('BEZEL GDU 1040 MFD 300x196', tbox((wxl + wxr) / 2 - 150, (wxl + wxr) / 2 + 150, 0, 15, H - 206, H - 10)))
    rw.append(hinge_pad(wxl, wxl + 15, 'HINGE leaf R-wing'))
    occRW = add_comp('Right wing', rw)
    occOR = add_comp('Right wing outrigger', [outrigger(wxr - 30, 0, P['out_w'], -1, (-ft, -ft + 20), '2020 Outrigger %d' % P['out_w']),
                                              ('PRINT outrigger foot', tbox(wxr - 40, wxr - 20, -T, 0, -ft + 20, 0))])

    # ---------------- Desk-side items (not part of the case)
    env = []
    env.append(('ENVELOPE yoke shelf plate (on deployed center outriggers)', tbox(-160, 160, -350, yb - 25, -ft, -ft + 6)))
    env.append(('ENVELOPE Logitech yoke housing (approx)', tbox(yoke_x - 120, yoke_x + 120, -320, yb - 30, -ft + 6, -ft + 146)))
    env.append(('ENVELOPE Yoke shaft (through panel)', ycyl(yoke_x, yoke_z, yb - 30, 150, 13)))
    env.append(('ENVELOPE Yoke handles (approx)', tbox(yoke_x - 140, yoke_x + 140, 150, 200, yoke_z - 60, yoke_z + 60)))
    env.append(('ENVELOPE Throttle quadrant at desk edge (approx)', tbox(Wp / 2 + 20, Wp / 2 + 120, pr + 15, pr + 145, -ft, -ft + 110)))
    occE = add_comp('Desk controls', env)

    occC.isGrounded = True
    occE.isGrounded = True

    allocc = (occC, occLS, occLW, occRS, occRW, occOCL, occOCR, occOL, occOR, occE)
    for occ in allocc:
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

    joint('Left spacer hinge', occLS, occC, AL)
    joint('Left wing hinge', occLW, occLS, BL)
    joint('Right spacer hinge', occRS, occC, AR)
    joint('Right wing hinge', occRW, occRS, BR)
    # outriggers: pivot pins at their stored inner ends
    joint('Center outrigger L swing', occOCL, occC, (-140, -10))
    joint('Center outrigger R swing', occOCR, occC, (140, -10))
    joint('Left outrigger swing', occOL, occLW, (BL[0] - hg - P['WL'] + 30, -10))
    joint('Right outrigger swing', occOR, occRW, (BR[0] + hg + Wp - 30, -10))
    print('geometry', G)


def run(_context: str):
    build()
