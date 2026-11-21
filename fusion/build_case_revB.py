# Rev B: folding sim-cockpit case with double-hinge (link) folds.
# Units in this file: mm. Frame: X = right, Y = toward pilot, Z = up.
# Rails (2020) lie in y[-20,0]; uprights (2040, 40 deep) lie in y[-20,20], standing 20 mm proud
# of the rail face as side bumpers for the knob zone.
import adsk.core, adsk.fusion, math

P = dict(
    Wc=410.0,    # center panel outer width (GDU 1040 PFD 300 mm + audio panel)
    Ww=350.0,    # wing outer width
    H=375.6,     # 4 bays of 88.9 mm (2U EIA-310) + 20 mm rail
    T=20.0,
    g=4.0,       # gap between panels when open
    Fe=45.0,     # module envelope in front of rail face
    Be=30.0,     # module envelope behind rails
    clr=5.0,     # clearance between stacked panels when closed
    pitch=88.9,
    proud=20.0,  # upright projection in front of rail face
    yp=20.0,     # pivot line = upright front face (found by plan2d.py: simplest collision-free fold)
    plate_t=8.0, plate_w=20.0,
    base_len=559.0,
    desk_edge=20.0,   # y of desk front edge
    desk_z=-40.0,     # desk top (base top at -20 leaves room for gear + link layers under the panel)
)


def geometry():
    T = P['T']; Wc = P['Wc']; g = P['g']; Fe = P['Fe']; Be = P['Be']; clr = P['clr']; yp = P['yp']
    yL = 2 * Fe + clr                    # left wing rail face when closed (facing center)
    yR = yL + T + Be + Fe + clr          # right wing rail face when closed
    sL = yL - 2 * yp
    sR = yR - 2 * yp
    # x: closed wing must line up with center. Ax + B0x = -(Wc + g) (left), +(Wc + g) (right)
    AL = ((-(Wc + g) + sL) / 2.0, yp); BL = ((-(Wc + g) - sL) / 2.0, yp)
    AR = (((Wc + g) - sR) / 2.0, yp); BR = (((Wc + g) + sR) / 2.0, yp)
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

    def W(x, y, z):
        if zup:
            return (x / 10.0, -y / 10.0, z / 10.0)
        return (x / 10.0, z / 10.0, y / 10.0)

    def P3(x, y, z):
        return adsk.core.Point3D.create(*W(x, y, z))

    def tbox(x0, x1, y0, y1, z0, z1):
        a = W(x0, y0, z0); b = W(x1, y1, z1)
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

    def union(a, b):
        tbm.booleanOperation(a, b, adsk.fusion.BooleanTypes.UnionBooleanType)
        return a

    def cut(a, b):
        tbm.booleanOperation(a, b, adsk.fusion.BooleanTypes.DifferenceBooleanType)
        return a

    T = P['T']; H = P['H']; Wc = P['Wc']; Ww = P['Ww']; g = P['g']
    Fe = P['Fe']; Be = P['Be']; pr = P['proud']; pt = P['plate_t']; pw = P['plate_w']
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
        return L

    def link_plates(A, B, label):
        out = []
        for z0, z1 in ((H + 2 + pt, H + 2 + 2 * pt), (-2 - 2 * pt, -2 - pt)):
            b = tbox(min(A[0], B[0]), max(A[0], B[0]), A[1] - pw / 2, A[1] + pw / 2, z0, z1)
            union(b, vcyl(A[0], A[1], z0, z1, pw / 2))
            union(b, vcyl(B[0], B[1], z0, z1, pw / 2))
            out.append((label, b))
        return out

    def pivot_pins(pt_xy, label):
        x, y = pt_xy
        return [(label, vcyl(x, y, H + 1, H + 2 + 2 * pt, 3.0)), (label, vcyl(x, y, -2 - 2 * pt, -1, 3.0))]

    def gears(pt_xy, r, label):
        # synchronising pulley, fixed to the panel, under the link plate. Pulleys at A and B are
        # tied by a crossed (figure-8) cable or twisted GT2 belt so both pivots turn by the same angle.
        x, y = pt_xy
        return [(label, vcyl(x, y, H + 1, H + 1 + pt, 15.0)), (label, vcyl(x, y, -1 - pt, -1, 15.0))]

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

    yoke_x = -Wc / 2 + T + 2 + 150.0
    yoke_z = 60.0

    # Center panel
    c_items = frame(-Wc / 2, Wc / 2)
    c_items.append(('BEZEL GDU 1040 PFD 300x196', tbox(-Wc / 2 + T + 2, -Wc / 2 + T + 302, 0, 15, H - 206, H - 10)))
    c_items.append(('BEZEL GMA audio (approx 64x196)', tbox(Wc / 2 - T - 66, Wc / 2 - T - 2, 0, 15, H - 206, H - 10)))
    yk = tbox(yoke_x - 60, yoke_x + 60, 0, 4, 22, 87)
    cut(yk, ycyl(yoke_x, yoke_z, -1, 5, 20))
    c_items.append(('BEZEL yoke pass-through plate (2U)', yk))
    for xu in (-Wc / 2, Wc / 2 - T):
        c_items.append(('PRINT base bracket', tbox(xu, xu + T, -T - 30, -T, 0, 30)))
    c_items += gears(G['AL'], G['sL'] / 2, 'PULLEY L-center')
    c_items += gears(G['AR'], G['sR'] / 2, 'PULLEY R-center')
    occC = add_comp('Center panel', c_items)

    # Left wing (open)
    xr = -Wc / 2 - g; xl = xr - Ww
    l_items = frame(xl, xr)
    l_items.append(('BEZEL standby/switch panel', tbox(xl + T + 10, xr - T - 10, 0, 15, H - 206, H - 10)))
    l_items.append(('PRINT base bracket', tbox(xl, xl + T, -T - 30, -T, 0, 30)))
    l_items += gears(G['BL'], G['sL'] / 2, 'PULLEY L-wing')
    occL = add_comp('Left wing', l_items)
    occLL = add_comp('Left link', link_plates(G['AL'], G['BL'], 'LINK plate L') + pivot_pins(G['AL'], 'PIN M6 L-center') + pivot_pins(G['BL'], 'PIN M6 L-wing'))

    # Right wing (open)
    xl = Wc / 2 + g; xr = xl + Ww
    r_items = frame(xl, xr)
    mx = (xl + xr) / 2
    r_items.append(('BEZEL GDU 1040 MFD 300x196', tbox(mx - 150, mx + 150, 0, 15, H - 206, H - 10)))
    r_items.append(('PRINT base bracket', tbox(xr - T, xr, -T - 30, -T, 0, 30)))
    r_items += gears(G['BR'], G['sR'] / 2, 'PULLEY R-wing')
    occR = add_comp('Right wing', r_items)
    occRL = add_comp('Right link', link_plates(G['AR'], G['BR'], 'LINK plate R') + pivot_pins(G['AR'], 'PIN M6 R-center') + pivot_pins(G['BR'], 'PIN M6 R-wing'))

    # Base rail + carriages (desk top at desk_z, desk front edge at desk_edge)
    BL = P['base_len']; dz = P['desk_z']; de = P['desk_edge']
    by0, by1 = -T - 40, -T
    b_items = []
    b_items.append(('2040 Base half %d' % BL, tbox(-BL, 0, by0, by1, dz, dz + 20)))
    b_items.append(('2040 Base half %d' % BL, tbox(0, BL, by0, by1, dz, dz + 20)))
    b_items.append(('Joiner plate 120x20x6', tbox(-60, 60, by0 - 6, by0, dz, dz + 20)))

    def front_carriage(xc, w, label, lip=False):
        out = []
        out.append(('PRINT %s saddle' % label, tbox(xc - w / 2, xc + w / 2, by1, by1 + 12, dz, dz + 20)))
        out.append(('PRINT %s plate' % label, tbox(xc - w / 2, xc + w / 2, by1 + 12, de, dz, dz + 6)))
        out.append(('PRINT %s desk-lip hook' % label, tbox(xc - w / 2, xc + w / 2, de, de + 6, dz - 40, dz + 6)))
        if lip:
            out.append(('PRINT %s clamp lip' % label, tbox(xc - w / 2, xc + w / 2, de + 6, de + 66, dz - 25, dz + 6)))
        return out

    yw = 240.0
    b_items.append(('PRINT Yoke carriage saddle', tbox(yoke_x - yw / 2, yoke_x + yw / 2, by0 - 18, by0 - 6, dz, dz + 20)))
    plate = tbox(yoke_x - yw / 2, yoke_x + yw / 2, -340, by0 - 18, dz, dz + 6)
    for sx in (-60, 60):
        cut(plate, tbox(yoke_x + sx - 4, yoke_x + sx + 4, -300, -200, dz - 1, dz + 7))
    b_items.append(('PRINT Yoke carriage plate (slotted)', plate))
    b_items.append(('PRINT Yoke clamp lip', tbox(yoke_x - yw / 2, yoke_x + yw / 2, -110, -90, dz + 6, dz + 31)))
    b_items.append(('ENVELOPE Logitech yoke housing (approx)', tbox(yoke_x - 120, yoke_x + 120, -320, -85, dz + 6, dz + 146)))
    b_items.append(('ENVELOPE Yoke shaft (through panel)', ycyl(yoke_x, yoke_z, -85, 150, 13)))
    b_items.append(('ENVELOPE Yoke handles (approx)', tbox(yoke_x - 140, yoke_x + 140, 150, 200, yoke_z - 60, yoke_z + 60)))

    thr_x = Wc / 2
    b_items += front_carriage(thr_x, 120, 'Throttle carriage', lip=True)
    b_items.append(('ENVELOPE Throttle quadrant (approx)', tbox(thr_x - 50, thr_x + 50, de + 6, de + 136, dz + 6, dz + 116)))
    b_items += front_carriage(-BL + 50, 60, 'End hook L')
    b_items += front_carriage(BL - 50, 60, 'End hook R')
    for xu in (-Wc / 2, Wc / 2 - T, -Wc / 2 - g - Ww, Wc / 2 + g + Ww - T):
        b_items.append(('PRINT base pad', tbox(xu, xu + T, -T - 30, -T, dz + 20, 0)))
    occB = add_comp('Base rail', b_items)

    occC.isGrounded = True
    occB.isGrounded = True

    for occ in (occC, occL, occR, occB, occLL, occRL):
        for b in occ.component.bRepBodies:
            if b.name.startswith('ZONE'):
                b.opacity = 0.15
            elif b.name.startswith('ENVELOPE'):
                b.opacity = 0.3

    def pivot_point(occ, px, py):
        comp = occ.component
        sk = comp.sketches.add(comp.xYConstructionPlane)
        sk.name = 'Hinge pivot'
        w = W(px, py, 0)
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

    joint('Left link pivot', occLL, occC, G['AL'])
    joint('Left wing pivot', occL, occLL, G['BL'])
    joint('Right link pivot', occRL, occC, G['AR'])
    joint('Right wing pivot', occR, occRL, G['BR'])
    print('geometry', G)


def run(_context: str):
    build()
