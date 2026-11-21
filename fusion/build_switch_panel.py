# Panel modules built as real Fusion features (sketch + extrude) so faceplates export straight to STL.
#  SW-1  left wing, rails 10-70: one-row C172 switch panel (mags key + 12 rockers)
#  CL-1  center panel, rails 10-110: yoke pass-through + PANEL / STBY IND dimmers
# Units mm, frame: X right, Y toward pilot, Z up. Fusion Z-up: (x, -y, z) / 10.
import adsk.core, adsk.fusion, math

FLIP_H = False   # checked in render: labels read correctly from the pilot side
FLIP_V = True

PLATE_T = 3.0
ROCKER = (15.0, 21.0)       # KCD1-style rocker cutout W x H (rocker moves up/down)
POCKET = (19.0, 25.0, 1.6)  # back pocket so snap-in clips grip a 1.4 mm wall
POT_HOLE = 7.5
KEY_HOLE = 10.0
YOKE_HOLE = 40.0
ENGRAVE = 0.6
ENGRAVE_LABELS = False   # labels come from stickers / outsourced panels; True engraves them into the print
ART_JSON = r'D:/Admin/Documents/Projects/FlightSimCase/labels/panels.json'
ARTWORK = []


def build():
    ARTWORK.clear()
    app = adsk.core.Application.get()
    d = adsk.fusion.Design.cast(app.activeProduct)
    root = d.rootComponent
    hosts = {o.component.name: o for o in root.occurrences}
    tbm = adsk.fusion.TemporaryBRepManager.get()

    def F(x, y, z):
        return adsk.core.Point3D.create(x / 10.0, -y / 10.0, z / 10.0)

    def tbox(x0, x1, y0, y1, z0, z1):
        a = F(x0, y0, z0); b = F(x1, y1, z1)
        lo = [min(a.x, b.x), min(a.y, b.y), min(a.z, b.z)]; hi = [max(a.x, b.x), max(a.y, b.y), max(a.z, b.z)]
        c = adsk.core.Point3D.create((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2)
        obb = adsk.core.OrientedBoundingBox3D.create(c, adsk.core.Vector3D.create(1, 0, 0), adsk.core.Vector3D.create(0, 1, 0),
                                                     hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2])
        return tbm.createBox(obb)

    def module(host_name, name, z_rails, x0, x1, holes, labels, standoffs, refs, label_h=2.5):
        host = hosts[host_name].component
        occ = host.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        occ.isGroundToParent = True      # move with the wing when it folds
        comp = occ.component
        comp.name = name
        plane0 = comp.xZConstructionPlane
        ny = plane0.geometry.normal.y
        to_back = adsk.fusion.ExtentDirections.PositiveExtentDirection if ny > 0 else adsk.fusion.ExtentDirections.NegativeExtentDirection
        to_front = adsk.fusion.ExtentDirections.NegativeExtentDirection if ny > 0 else adsk.fusion.ExtentDirections.PositiveExtentDirection
        dist = lambda mm: adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(mm / 10.0))
        z0 = z_rails[0] + 0.4
        z1 = z_rails[1] - 0.4

        # faceplate with cutouts and half-hole edge notches
        sk = comp.sketches.add(plane0)
        sk.name = 'Faceplate'
        S = lambda x, z: sk.modelToSketchSpace(F(x, 0, z))
        L = sk.sketchCurves.sketchLines
        C = sk.sketchCurves.sketchCircles
        L.addTwoPointRectangle(S(x0, z0), S(x1, z1))
        for h in holes:
            if h[0] == 'rect':
                _, cx, cz, w, hh = h
                L.addTwoPointRectangle(S(cx - w / 2, cz - hh / 2), S(cx + w / 2, cz + hh / 2))
            else:
                _, cx, cz, dia = h
                C.addByCenterRadius(S(cx, cz), dia / 20.0)
        n_notch = max(2, int((x1 - x0) // 110) + 1)
        notches = []
        for i in range(n_notch):
            nx = x0 + 12 + i * (x1 - x0 - 24) / (n_notch - 1)
            for ez in (z0, z1):
                C.addByCenterRadius(S(nx, ez), 0.32)
                notches.append((nx, ez))
        ARTWORK.append(dict(name=name, host=host_name, x0=x0, x1=x1, z0=z0, z1=z1, holes=[list(h) for h in holes],
                            labels=[list(l) for l in labels], notches=notches, notch_r=3.2, label_h=label_h))
        prof = max(list(sk.profiles), key=lambda p: p.areaProperties().area)
        ei = comp.features.extrudeFeatures.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        ei.setOneSideExtent(dist(PLATE_T), to_front)
        plate = comp.features.extrudeFeatures.add(ei).bodies.item(0)
        plate.name = 'PRINT %s faceplate' % name.split()[0]

        rk = [h for h in holes if h[0] == 'rect']
        if rk:
            sp = comp.sketches.add(plane0)
            sp.name = 'Clip pockets'
            for _, cx, cz, w, hh in rk:
                sp.sketchCurves.sketchLines.addTwoPointRectangle(
                    sp.modelToSketchSpace(F(cx - POCKET[0] / 2, 0, cz - POCKET[1] / 2)),
                    sp.modelToSketchSpace(F(cx + POCKET[0] / 2, 0, cz + POCKET[1] / 2)))
            coll = adsk.core.ObjectCollection.create()
            for p in sp.profiles:
                coll.add(p)
            ci = comp.features.extrudeFeatures.createInput(coll, adsk.fusion.FeatureOperations.CutFeatureOperation)
            ci.setOneSideExtent(dist(POCKET[2]), to_front)
            ci.participantBodies = [plate]
            comp.features.extrudeFeatures.add(ci)

        if standoffs:
            ss = comp.sketches.add(plane0)
            ss.name = 'Standoffs'
            for cx, cz in standoffs:
                ss.sketchCurves.sketchCircles.addByCenterRadius(ss.modelToSketchSpace(F(cx, 0, cz)), 0.25)
                ss.sketchCurves.sketchCircles.addByCenterRadius(ss.modelToSketchSpace(F(cx, 0, cz)), 0.08)
            coll = adsk.core.ObjectCollection.create()
            for p in ss.profiles:
                if p.areaProperties().area > 0.1:
                    coll.add(p)
            ji = comp.features.extrudeFeatures.createInput(coll, adsk.fusion.FeatureOperations.JoinFeatureOperation)
            ji.setOneSideExtent(dist(26.0), to_back)
            ji.participantBodies = [plate]
            comp.features.extrudeFeatures.add(ji)

        pi = comp.constructionPlanes.createInput()
        pi.setByOffset(plane0, adsk.core.ValueInput.createByReal((-PLATE_T / 10.0) / ny))
        fplane = comp.constructionPlanes.add(pi)
        fplane.name = 'Front face'
        fplane.isLightBulbOn = False
        st = comp.sketches.add(fplane)
        st.name = 'Labels'
        st.isLightBulbOn = False   # reference only; labels are stickers / outsourced
        texts = []
        for txt, cx, cz in labels:
            w = max(12.0, len(txt) * label_h * 0.95)
            pa = st.modelToSketchSpace(F(cx - w / 2, PLATE_T, cz - label_h))
            pb = st.modelToSketchSpace(F(cx + w / 2, PLATE_T, cz + label_h))
            ti = st.sketchTexts.createInput2(txt, label_h / 10.0)
            ti.setAsMultiLine(pa, pb, adsk.core.HorizontalAlignments.CenterHorizontalAlignment,
                              adsk.core.VerticalAlignments.MiddleVerticalAlignment, 0)
            ti.fontName = 'Arial'
            ti.isHorizontalFlip = FLIP_H
            ti.isVerticalFlip = FLIP_V
            texts.append(st.sketchTexts.add(ti))
        for t in (texts if ENGRAVE_LABELS else []):
            ti2 = comp.features.extrudeFeatures.createInput(t, adsk.fusion.FeatureOperations.CutFeatureOperation)
            ti2.setOneSideExtent(dist(ENGRAVE), to_back)
            ti2.participantBodies = [plate]
            comp.features.extrudeFeatures.add(ti2)

        if refs:
            bf = comp.features.baseFeatures.add()
            bf.startEdit()
            for nm, b in refs:
                nb = comp.bRepBodies.add(b, bf)
                nb.name = nm
            bf.finishEdit()
            for b in comp.bRepBodies:
                if b.name.startswith('REF'):
                    b.opacity = 0.6
                    b.isLightBulbOn = False      # placeholders hidden by default
        return occ

    def rocker_refs(cx, cz):
        return [('REF rocker body', tbox(cx - 7, cx + 7, -22, 0, cz - 10, cz + 10)),
                ('REF rocker cap', tbox(cx - 7.5, cx + 7.5, 3, 11, cz - 10.5, cz + 10.5))]

    # ---------------- left wing bottom section (rails 10-110): switches either side of the pilot yoke
    from importlib import util as _u
    spec = _u.spec_from_file_location('bc', r'D:/Admin/Documents/Projects/FlightSimCase/fusion/build_case.py')
    bc = _u.module_from_spec(spec); spec.loader.exec_module(bc)
    PP = bc.P; G = bc.geometry()
    T = PP['T']
    wxr = G['AL'][0] - PP['hg']; wxl = wxr - PP['WL']
    rl = PP['rails_L']
    zr = (rl[0] + rl[1]) / 2                          # switch row = yoke shaft height
    yx = PP['yoke_x']; yz = 100.0 - PP['foot']
    lab_lo = zr - 16.5
    lab_hi = zr + 16.5

    # SW-1L: magnetos + MASTER (ALT|BAT) + STBY BATT + AVIONICS (BUS1|BUS2), left of the yoke
    xa = wxl + T + 2; xb = xa + 127
    X = lambda dx: xa + dx
    key_x = 16.0
    lay1 = [('ALT', 38.5), ('BAT', 55.5), ('STBY BATT', 76.5), ('BUS 1', 97.5), ('BUS 2', 114.5)]
    holes = [('circ', X(key_x), zr, KEY_HOLE)] + [('rect', X(dx), zr, *ROCKER) for _, dx in lay1]
    labels = [('IGN', X(key_x), lab_hi), ('MASTER', X(47), lab_hi), ('STBY', X(76.5), lab_hi), ('AVIONICS', X(106), lab_hi),
              ('ALT', X(38.5), lab_lo), ('BAT', X(55.5), lab_lo), ('BATT', X(76.5), lab_lo), ('BUS 1', X(97.5), lab_lo), ('BUS 2', X(114.5), lab_lo)]
    refs = [('REF key switch body (1P12T, stop at 5)', tbox(X(key_x) - 13, X(key_x) + 13, -30, 0, zr - 13, zr + 13)),
            ('REF printed key knob', tbox(X(key_x) - 4, X(key_x) + 4, 3, 28, zr - 13, zr + 13))]
    for _, dx in lay1:
        refs += rocker_refs(X(dx), zr)
    refs.append(('REF Raspberry Pi Pico (SW-1L + SW-1R)', tbox(yx - 25.5, yx + 25.5, -28.6, -27, rl[1] - 10.5, rl[1] + 10.5)))
    module('Left wing', 'SW-1L Master/avionics panel', (rl[0], rl[1]), xa, xb, holes, labels, [], refs, label_h=2.5)

    # YK-1: pilot yoke pass-through
    module('Left wing', 'YK-1 Pilot yoke plate', (rl[0], rl[1]), xb + 1, xb + 51, [('circ', yx, yz, YOKE_HOLE)], [], [], [], label_h=2.5)

    # SW-1R: lights row + fuel pump + pitot heat, right of the yoke
    xa2 = xb + 52; xb2 = wxr - T - 2
    X2 = lambda dx: xa2 + dx
    lay2 = ['FUEL PUMP', 'BCN', 'LAND', 'TAXI', 'NAV', 'STROBE', 'PITOT HT']
    holes2 = []; labels2 = [('LIGHTS', X2(63.5), lab_hi)]; refs2 = []
    for i, nm in enumerate(lay2):
        cx = X2(9.5 + i * 18)
        holes2.append(('rect', cx, zr, *ROCKER))
        refs2 += rocker_refs(cx, zr)
        if nm == 'FUEL PUMP':
            labels2 += [('FUEL', cx, lab_hi), ('PUMP', cx, lab_lo)]
        elif nm == 'PITOT HT':
            labels2 += [('PITOT', cx, lab_hi), ('HEAT', cx, lab_lo)]
        else:
            labels2.append((nm, cx, lab_lo))
    module('Left wing', 'SW-1R Lights panel', (rl[0], rl[1]), xa2, xb2, holes2, labels2, [], refs2, label_h=2.5)

    # ---------------- AU-1: GMA 1347 style audio panel, center top-left (rails 110-310), 63 mm wide
    ra = PP['rails_C']
    ax0 = -PP['W'] / 2 + T + 2; ax1 = ax0 + 63
    acx = (ax0 + ax1) / 2
    au_holes = []; au_refs = []
    for r in range(11):                       # 2 columns x 11 rows of keys (COM/NAV/MKR/etc.), legends on the caps
        zz = ra[2] - 22 - r * 13
        for dx in (-14, 14):
            au_holes.append(('rect', acx + dx, zz, 22.0, 8.0))
    au_holes.append(('circ', acx, ra[1] + 22, 10.0))   # PILOT/COPLT volume dual knob
    au_refs.append(('REF dual encoder (audio volume)', tbox(acx - 6.5, acx + 6.5, -15, 0, ra[1] + 15.5, ra[1] + 28.5)))
    au_refs.append(('REF Raspberry Pi Pico (audio keys)', tbox(acx - 10.5, acx + 10.5, -28.6, -27, ra[1] + 40, ra[1] + 91)))
    module('Center panel', 'AU-1 Audio panel', (ra[1], ra[2]), ax0, ax1, au_holes, [('VOL', acx, ra[1] + 36)], [], au_refs, label_h=2.3)

    # ---------------- center bottom right: copilot yoke blank (mirror of the pilot yoke about the aircraft centerline)
    rc = PP['rails_C']
    cop_x = 2 * PP['thr_x'] - yx
    cxb = PP['W'] / 2 - T - 2
    module('Center panel', 'CP-1 Copilot yoke blank', (rc[0], rc[1]), cxb - 98, cxb, [('circ', cop_x, yz, YOKE_HOLE)], [], [], [], label_h=2.5)
    import json, os
    os.makedirs(os.path.dirname(ART_JSON), exist_ok=True)
    with open(ART_JSON, 'w') as f:
        json.dump(ARTWORK, f, indent=1)
    print('modules built; label artwork data ->', ART_JSON)


def run(_context: str):
    build()
