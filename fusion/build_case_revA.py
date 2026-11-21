# Builds the folding sim-cockpit case in the active Fusion design.
# Units in this file: mm. Frame: X = right, Y = toward pilot, Z = up.
import adsk.core, adsk.fusion, math

P = dict(
    Wc=410.0,    # center panel outer width (GDU 1040 PFD 300 mm + audio panel)
    Ww=350.0,    # wing outer width (left: switches/standby, right: GDU 1040 MFD)
    H=375.6,     # 4 bays of 88.9 mm (2U of EIA-310 rack) + 20 mm rail
    T=20.0,      # 2020 extrusion
    g=4.0,       # gap between panels when open
    Fe=45.0,     # module envelope in front of rail face (bezel + knobs)
    Be=30.0,     # module envelope behind rails (screen + boards)
    clr=5.0,     # clearance between stacked panels when closed
    pitch=88.9,   # 3.5 in = 2 x 1.75 in rack units
    base_len=559.0,   # each 2040 base half
    reach=280.0,      # carriage reach from base rail to desk lip
)


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

    def tbox(x0, x1, y0, y1, z0, z1):
        a = W(x0, y0, z0)
        b = W(x1, y1, z1)
        lo = [min(a[i], b[i]) for i in range(3)]
        hi = [max(a[i], b[i]) for i in range(3)]
        c = adsk.core.Point3D.create((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2)
        obb = adsk.core.OrientedBoundingBox3D.create(
            c, adsk.core.Vector3D.create(1, 0, 0), adsk.core.Vector3D.create(0, 1, 0),
            hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2])
        return tbm.createBox(obb)

    def cut(body, tool):
        tbm.booleanOperation(body, tool, adsk.fusion.BooleanTypes.DifferenceBooleanType)
        return body

    T = P['T']; H = P['H']; Wc = P['Wc']; Ww = P['Ww']; g = P['g']
    Fe = P['Fe']; Be = P['Be']; clr = P['clr']
    rails_z = [T / 2 + P['pitch'] * k for k in range(int(round((H - T) / P['pitch'])) + 1)]

    # Fold geometry
    yL_closed = 2 * Fe + clr                 # left wing front face when closed
    yR_closed = yL_closed + T + Be + Fe + clr  # right wing front face when closed
    pivL = (-Wc / 2 - g / 2, yL_closed / 2)
    pivR = (Wc / 2 + g / 2, yR_closed / 2)

    def frame(xl, xr):
        L = []
        L.append(('2020 Upright %d' % round(H), tbox(xl, xl + T, -T, 0, 0, H)))
        L.append(('2020 Upright %d' % round(H), tbox(xr - T, xr, -T, 0, 0, H)))
        for zc in rails_z:
            L.append(('2020 Rail %d' % round(xr - xl - 2 * T), tbox(xl + T, xr - T, -T, 0, zc - T / 2, zc + T / 2)))
        L.append(('ZONE front (knobs/bezels)', tbox(xl + T, xr - T, 0, Fe, 0, H)))
        L.append(('ZONE rear (screens/boards)', tbox(xl + T, xr - T, -T - Be, -T, T, H - T)))
        return L

    def knuckles(x0, x1, piv, zs, label):
        # arm from the upright face out to the pivot, rounded (r=10) around the pin
        out = []
        for z0 in zs:
            b = tbox(x0, x1, 0, piv[1], z0, z0 + 30)
            a = W(piv[0], piv[1], z0)
            c = W(piv[0], piv[1], z0 + 30)
            cyl = tbm.createCylinderOrCone(adsk.core.Point3D.create(*a), 1.0, adsk.core.Point3D.create(*c), 1.0)
            tbm.booleanOperation(b, cyl, adsk.fusion.BooleanTypes.UnionBooleanType)
            out.append((label, b))
        return out

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

    # Center panel
    c_items = frame(-Wc / 2, Wc / 2)
    c_items += knuckles(-Wc / 2, -Wc / 2 + T, pivL, [20, H - 50], 'PRINT hinge knuckle L-center')
    c_items += knuckles(Wc / 2 - T, Wc / 2, pivR, [20, H - 50], 'PRINT hinge arm R-center')
    c_items.append(('BEZEL GDU 1040 PFD 300x196', tbox(-Wc / 2 + T + 2, -Wc / 2 + T + 302, 0, 15, H - 206, H - 10)))
    c_items.append(('BEZEL GMA audio (approx 64x196)', tbox(Wc / 2 - T - 66, Wc / 2 - T - 2, 0, 15, H - 206, H - 10)))
    c_items.append(('PRINT base bracket', tbox(-Wc / 2, -Wc / 2 + T, -T - 10, -T, 0, 30)))
    c_items.append(('PRINT base bracket', tbox(Wc / 2 - T, Wc / 2, -T - 10, -T, 0, 30)))
    occC = add_comp('Center panel', c_items)

    # Left wing (open position)
    xr = -Wc / 2 - g
    xl = xr - Ww
    l_items = frame(xl, xr)
    l_items += knuckles(xr - T, xr, pivL, [50, H - 80], 'PRINT hinge knuckle L-wing')
    l_items.append(('BEZEL standby/switch panel', tbox(xl + T + 10, xr - T - 10, 0, 15, H - 206, H - 10)))
    occL = add_comp('Left wing', l_items)

    # Right wing (open position)
    xl = Wc / 2 + g
    xr = xl + Ww
    r_items = frame(xl, xr)
    r_items += knuckles(xl, xl + T, pivR, [50, H - 80], 'PRINT hinge arm R-wing')
    mx = (xl + xr) / 2
    r_items.append(('BEZEL GDU 1040 MFD 300x196', tbox(mx - 150, mx + 150, 0, 15, H - 206, H - 10)))
    occR = add_comp('Right wing', r_items)

    # Base rail + carriages
    BL = P['base_len']; reach = P['reach']
    b_items = []
    b_items.append(('2040 Base half %d' % BL, tbox(-BL, 0, -30, 10, -20, 0)))
    b_items.append(('2040 Base half %d' % BL, tbox(0, BL, -30, 10, -20, 0)))
    b_items.append(('Joiner plate 120x20x6', tbox(-60, 60, -36, -30, -20, 0)))

    def carriage(xc, w, label):
        out = []
        out.append(('PRINT %s carriage saddle' % label, tbox(xc - w / 2, xc + w / 2, 10, 22, -20, 0)))
        plate = tbox(xc - w / 2, xc + w / 2, 22, 10 + reach, -20, -14)
        for sx in (-w / 4, w / 4):
            cut(plate, tbox(xc + sx - 4, xc + sx + 4, 120, 220, -21, -13))
        out.append(('PRINT %s carriage plate (slotted)' % label, plate))
        out.append(('PRINT %s desk-lip hook' % label, tbox(xc - w / 2, xc + w / 2, 10 + reach, 16 + reach, -60, -14)))
        return out

    yoke_x = -Wc / 2 + T + 2 + 150.0
    thr_x = Wc / 2
    b_items += carriage(yoke_x, 160, 'Yoke')
    b_items += carriage(thr_x, 120, 'Throttle')
    b_items.append(('ENVELOPE Logitech yoke (approx)', tbox(yoke_x - 120, yoke_x + 120, 80, 280, -14, 116)))
    b_items.append(('ENVELOPE Throttle quadrant (approx)', tbox(thr_x - 50, thr_x + 50, 150, 280, -14, 96)))
    occB = add_comp('Base rail', b_items)

    occC.isGrounded = True
    occB.isGrounded = True

    # Appearance: translucent zones and envelopes
    for occ in (occC, occL, occR, occB):
        for b in occ.component.bRepBodies:
            if b.name.startswith('ZONE'):
                b.opacity = 0.15
            elif b.name.startswith('ENVELOPE'):
                b.opacity = 0.3

    # Joints: revolute about vertical pivot lines
    def pivot_point(occ, px, py):
        comp = occ.component
        sk = comp.sketches.add(comp.xYConstructionPlane)
        sk.name = 'Hinge pivot'
        w = W(px, py, 0)
        sp = sk.sketchPoints.add(sk.modelToSketchSpace(adsk.core.Point3D.create(w[0], w[1], w[2])))
        return sp.createForAssemblyContext(occ)

    vdir = adsk.fusion.JointDirections.ZAxisJointDirection if zup else adsk.fusion.JointDirections.YAxisJointDirection
    joints = {}
    for nm, occ, piv in (('Left fold', occL, pivL), ('Right fold', occR, pivR)):
        jg = adsk.fusion.JointGeometry.createByPoint(pivot_point(occ, piv[0], piv[1]))
        ji = root.asBuiltJoints.createInput(occ, occC, jg)
        ji.setAsRevoluteJointMotion(vdir)
        j = root.asBuiltJoints.add(ji)
        j.name = nm
        joints[nm] = j

    print('zup', zup, 'pivL', pivL, 'pivR', pivR, 'rails_z', rails_z)
    return joints


def run(_context: str):
    build()
