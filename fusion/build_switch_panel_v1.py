# C172 lower-left switch panels for the left wing (rev E case), built as real Fusion features
# (sketch + extrude) so the faceplates can be exported straight to STL/3MF.
# Units mm, frame: X right, Y toward pilot, Z up. Fusion Z-up: (x, -y, z) / 10.
import adsk.core, adsk.fusion, math

FLIP_H = False  # checked in render: labels read correctly from the pilot side
FLIP_V = True

# Faceplate standard: n bays tall (n x 88.9 - 0.8), edges on rail centerlines, half-hole notches
# on the edges; one M5 button head + 15 mm washer clamps the two neighbouring plates.
PLATE_T = 3.0
ROCKER = (15.0, 21.0)      # KCD1-style rocker cutout W x H (rocker moves up/down)
POCKET = (19.0, 25.0, 1.6) # back pocket so snap-in clips grip a 1.4 mm wall
POT_HOLE = 7.5             # 16 mm pot, M7 bushing
KEY_HOLE = 10.0            # 3/8 in rotary switch bushing
LABEL_H = 3.2              # label text height
ENGRAVE = 0.6


def build(rails_z=(10.0, 98.9, 187.8, 276.7, 365.6), inner=(-468.0, -198.0)):
    app = adsk.core.Application.get()
    d = adsk.fusion.Design.cast(app.activeProduct)
    root = d.rootComponent
    lw = None
    for o in root.occurrences:
        if o.component.name == 'Left wing':
            lw = o
    host = lw.component
    tbm = adsk.fusion.TemporaryBRepManager.get()

    def F(x, y, z):
        return adsk.core.Point3D.create(x / 10.0, -y / 10.0, z / 10.0)

    xz = host.xZConstructionPlane
    ny = xz.geometry.normal.y      # +1 if the XZ plane normal points to the back (my -y)
    flip_h = (ny > 0) if FLIP_H is None else FLIP_H

    def dir_toward_back():
        # extent direction that moves toward my -y (Fusion +y)
        return adsk.fusion.ExtentDirections.PositiveExtentDirection if ny > 0 else adsk.fusion.ExtentDirections.NegativeExtentDirection

    def dir_toward_front():
        return adsk.fusion.ExtentDirections.NegativeExtentDirection if ny > 0 else adsk.fusion.ExtentDirections.PositiveExtentDirection

    def tbox(x0, x1, y0, y1, z0, z1):
        a = F(x0, y0, z0); b = F(x1, y1, z1)
        lo = [min(a.x, b.x), min(a.y, b.y), min(a.z, b.z)]; hi = [max(a.x, b.x), max(a.y, b.y), max(a.z, b.z)]
        c = adsk.core.Point3D.create((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2)
        obb = adsk.core.OrientedBoundingBox3D.create(c, adsk.core.Vector3D.create(1, 0, 0), adsk.core.Vector3D.create(0, 1, 0),
                                                     hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2])
        return tbm.createBox(obb)

    def module(name, bay, x0, x1, holes, labels, standoffs, refs):
        """holes: list of ('rect', cx, cz, w, h) | ('circ', cx, cz, dia); labels: (text, cx, cz);
        standoffs: list of (cx, cz); refs: list of (name, box) reference bodies."""
        occ = host.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        comp = occ.component
        comp.name = name
        z0 = rails_z[bay - 1] + 0.4
        z1 = rails_z[bay] - 0.4
        plane0 = comp.xZConstructionPlane

        # --- faceplate with cutouts and edge notches
        sk = comp.sketches.add(plane0)
        sk.name = 'Faceplate'
        S = lambda x, z, y=0.0: sk.modelToSketchSpace(F(x, y, z))
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
        for i in range(n_notch):
            nx = x0 + 15 + i * (x1 - x0 - 30) / (n_notch - 1)
            for ez in (z0, z1):
                C.addByCenterRadius(S(nx, ez), 0.32)
        prof = max(list(sk.profiles), key=lambda p: p.areaProperties().area)
        ei = comp.features.extrudeFeatures.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        ei.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(PLATE_T / 10.0)), dir_toward_front())
        plate = comp.features.extrudeFeatures.add(ei).bodies.item(0)
        plate.name = 'PRINT %s faceplate' % name.split()[0]

        # --- back pockets for snap-in rockers
        rk = [h for h in holes if h[0] == 'rect']
        if rk:
            sp = comp.sketches.add(plane0)
            sp.name = 'Clip pockets'
            S2 = lambda x, z: sp.modelToSketchSpace(F(x, 0, z))
            for _, cx, cz, w, hh in rk:
                sp.sketchCurves.sketchLines.addTwoPointRectangle(S2(cx - POCKET[0] / 2, cz - POCKET[1] / 2), S2(cx + POCKET[0] / 2, cz + POCKET[1] / 2))
            coll = adsk.core.ObjectCollection.create()
            for p in sp.profiles:
                coll.add(p)
            ci = comp.features.extrudeFeatures.createInput(coll, adsk.fusion.FeatureOperations.CutFeatureOperation)
            ci.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(POCKET[2] / 10.0)), dir_toward_front())
            ci.participantBodies = [plate]
            comp.features.extrudeFeatures.add(ci)

        # --- Pico standoffs (M2 self-tap, 26 mm long so the board sits behind the rail plane)
        if standoffs:
            ss = comp.sketches.add(plane0)
            ss.name = 'Pico standoffs'
            S3 = lambda x, z: ss.modelToSketchSpace(F(x, 0, z))
            for cx, cz in standoffs:
                ss.sketchCurves.sketchCircles.addByCenterRadius(S3(cx, cz), 0.25)
                ss.sketchCurves.sketchCircles.addByCenterRadius(S3(cx, cz), 0.08)
            coll = adsk.core.ObjectCollection.create()
            for p in ss.profiles:
                a = p.areaProperties().area
                if a > 0.1:
                    coll.add(p)
            ji = comp.features.extrudeFeatures.createInput(coll, adsk.fusion.FeatureOperations.JoinFeatureOperation)
            ji.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(2.6)), dir_toward_back())
            ji.participantBodies = [plate]
            comp.features.extrudeFeatures.add(ji)

        # --- engraved labels on the front face
        pi = comp.constructionPlanes.createInput()
        pi.setByOffset(plane0, adsk.core.ValueInput.createByReal((-PLATE_T / 10.0) / ny))
        fplane = comp.constructionPlanes.add(pi)
        fplane.name = 'Front face'
        fplane.isLightBulbOn = False
        st = comp.sketches.add(fplane)
        st.name = 'Labels'
        texts = []
        for txt, cx, cz in labels:
            w = max(12.0, len(txt) * LABEL_H * 0.95)
            pa = st.modelToSketchSpace(F(cx - w / 2, PLATE_T, cz - LABEL_H))
            pb = st.modelToSketchSpace(F(cx + w / 2, PLATE_T, cz + LABEL_H))
            ti = st.sketchTexts.createInput2(txt, LABEL_H / 10.0)
            ti.setAsMultiLine(pa, pb, adsk.core.HorizontalAlignments.CenterHorizontalAlignment,
                              adsk.core.VerticalAlignments.MiddleVerticalAlignment, 0)
            ti.fontName = 'Arial'
            ti.isHorizontalFlip = flip_h
            ti.isVerticalFlip = FLIP_V
            texts.append(st.sketchTexts.add(ti))
        for t in texts:
            ti2 = comp.features.extrudeFeatures.createInput(t, adsk.fusion.FeatureOperations.CutFeatureOperation)
            ti2.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(ENGRAVE / 10.0)), dir_toward_back())
            ti2.participantBodies = [plate]
            comp.features.extrudeFeatures.add(ti2)

        # --- reference parts (not printed): switch bodies, knobs, Pico
        bf = comp.features.baseFeatures.add()
        bf.startEdit()
        for nm, b in refs:
            nb = comp.bRepBodies.add(b, bf)
            nb.name = nm
        bf.finishEdit()
        for b in comp.bRepBodies:
            if b.name.startswith('REF'):
                b.opacity = 0.6
        return occ

    xa, xb = inner[0] + 2, inner[1] - 2        # plate x range (266 wide)
    refs_common = []

    # ---------------- SW-1 (bay 2): ignition, MASTER (ALT|BAT), AVIONICS (BUS1|BUS2), STBY BATT, 2 dimmers
    zc = (rails_z[1] + rails_z[2]) / 2
    zr = zc - 6           # switch row, labels above/below
    X = lambda dx: xa + dx
    holes1 = [('circ', X(32), zr, KEY_HOLE),
              ('rect', X(76), zr, *ROCKER), ('rect', X(94), zr, *ROCKER),
              ('rect', X(128), zr, *ROCKER), ('rect', X(146), zr, *ROCKER),
              ('rect', X(180), zr, *ROCKER),
              ('circ', X(214), zr, POT_HOLE), ('circ', X(244), zr, POT_HOLE)]
    labels1 = [('MAGNETOS', X(32), zc + 30), ('OFF R L BOTH START', X(32), zr - 22),
               ('MASTER', X(85), zc + 30), ('ALT', X(76), zr - 18), ('BAT', X(94), zr - 18),
               ('AVIONICS', X(137), zc + 30), ('BUS1', X(128), zr - 18), ('BUS2', X(146), zr - 18),
               ('STBY BATT', X(180), zc + 30), ('PANEL', X(214), zc + 30), ('STBY IND', X(244), zc + 30)]
    so1 = []
    refs1 = [('REF key switch body (1P12T, stop at 5)', tbox(X(32) - 13, X(32) + 13, -30, 0, zr - 13, zr + 13)),
             ('REF printed key knob', tbox(X(32) - 4, X(32) + 4, 3, 28, zr - 14, zr + 14))]
    for dx in (76, 94, 128, 146, 180):
        refs1.append(('REF rocker body', tbox(X(dx) - 7, X(dx) + 7, -22, 0, zr - 10, zr + 10)))
        refs1.append(('REF rocker cap', tbox(X(dx) - 7.5, X(dx) + 7.5, 3, 11, zr - 10.5, zr + 10.5)))
    for dx in (214, 244):
        refs1.append(('REF pot body 16 mm', tbox(X(dx) - 8, X(dx) + 8, -12, 0, zr - 8, zr + 8)))
        refs1.append(('REF knob', tbox(X(dx) - 8, X(dx) + 8, 3, 21, zr - 8, zr + 8)))
    module('SW-1 Ignition/master panel', 2, xa, xb, holes1, labels1, so1, refs1)

    # ---------------- SW-2 (bay 1): FUEL PUMP, BCN, LAND, TAXI, NAV, STROBE, PITOT HEAT + Pico for both panels
    zc = (rails_z[0] + rails_z[1]) / 2
    zr = zc - 4
    names = ['FUEL PUMP', 'BCN', 'LAND', 'TAXI', 'NAV', 'STROBE', 'PITOT HT']
    holes2 = []; labels2 = []; refs2 = []
    for i, nm in enumerate(names):
        cx = X(24 + i * 26)
        holes2.append(('rect', cx, zr, *ROCKER))
        labels2.append((nm, cx, zc + 28))
        refs2.append(('REF rocker body', tbox(cx - 7, cx + 7, -22, 0, zr - 10, zr + 10)))
        refs2.append(('REF rocker cap', tbox(cx - 7.5, cx + 7.5, 3, 11, zr - 10.5, zr + 10.5)))
    labels2.append(('LIGHTS / ELEC', X(102), zr - 20))
    # Raspberry Pi Pico (51 x 21) behind the free right end, on 4 standoffs (hole pattern 47 x 11.4)
    pc_x, pc_z = X(232), zr
    so2 = [(pc_x - 5.7, pc_z - 23.5), (pc_x + 5.7, pc_z - 23.5), (pc_x - 5.7, pc_z + 23.5), (pc_x + 5.7, pc_z + 23.5)]
    refs2.append(('REF Raspberry Pi Pico', tbox(pc_x - 10.5, pc_x + 10.5, -27.6, -26, pc_z - 25.5, pc_z + 25.5)))
    module('SW-2 Lighting panel', 1, xa, xb, holes2, labels2, so2, refs2)
    print('switch panels built; XZ normal y =', ny, 'flip_h =', flip_h)


def run(_context: str):
    build()
