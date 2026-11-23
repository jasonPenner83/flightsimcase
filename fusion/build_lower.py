# Add-on pods (Jason 2026-11-23): the lower panel is gone. Trim wheel and throttle / mixture / condition push-pulls are
# two separate clamp-on pods that hang under the main unit's front edge when wanted (same knob-screw brackets) and pack
# separately. Each pod: a 9 mm front plate (cut where its module passes through), a 2020 top rail, and a stepped 3 mm
# box: 31 mm deep in the desk-edge strip (z -41..-3, clear of the desk edge 40 mm behind the face), full depth below
# the desk underside where the rods / trim wheel run back under the desk.
# Also makes the printed 135 x 109 face plate for the fuel selector on the main panel. Runs after place_vendor.
# Units mm, frame as build_case_mip (X right, Y toward pilot, Z up, u = x + 460).
import importlib.util
import adsk.core, adsk.fusion

BASE = r'D:/Admin/Documents/Projects/FlightSimCase/fusion/'
spec = importlib.util.spec_from_file_location('build_case_mip', BASE + 'build_case_mip.py')
bcm = importlib.util.module_from_spec(spec); spec.loader.exec_module(bcm)
P = bcm.P

# pod name -> (u0, u1, bottom z, box depth)
PODS = {'Pod: trim wheel (clamp-on)': (525.0, 612.0, -225.0, 140.0),
        'Pod: TPM quadrant (clamp-on)': (615.0, 778.0, -145.0, 190.0)}
HOST = {k: k for k in PODS}
BOX_DEPTH = {k: v[3] for k, v in PODS.items()}
LOWER = ('Throttle', 'Mixture', 'Condition', 'Trim')
FSP_FACE = dict(u0=796.0, u1=931.0, z0=0.0, z1=109.0, tab=(850.0, 931.0, 118.0), shaft=(858.0, 40.0, 16.0), lever=(890.0, 914.0, 87.0, 111.0))


def X(u):
    return u - 460.0


def build_lower():
    app = adsk.core.Application.get()
    d = adsk.fusion.Design.cast(app.activeProduct)
    root = d.rootComponent
    tbm = adsk.fusion.TemporaryBRepManager.get()
    SUB = adsk.fusion.BooleanTypes.DifferenceBooleanType
    UNI = adsk.fusion.BooleanTypes.UnionBooleanType
    tp = P['t_panel']; zt_, zb_ = P['lower_top'], P['lower_bot']; T = P['T']; sk = P['skin']; rim = P['rim']
    zd_under = P['desk_z'] - P['desk_t']          # desk underside, -41
    fz = -(P['desk_edge'] - 9.0)                   # back of the desk-edge zone: -31 (9 mm clear of the desk edge)

    def F(x, y, z):
        return adsk.core.Point3D.create(x / 10.0, -y / 10.0, z / 10.0)

    def boxw(lo, hi):          # world (Fusion cm) corners
        c = adsk.core.Point3D.create((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2)
        return tbm.createBox(adsk.core.OrientedBoundingBox3D.create(c, adsk.core.Vector3D.create(1, 0, 0), adsk.core.Vector3D.create(0, 1, 0),
                                                                   hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]))

    def box(x0, x1, y0, y1, a, b):
        p = F(x0, y0, a); q = F(x1, y1, b)
        return boxw([min(p.x, q.x), min(p.y, q.y), min(p.z, q.z)], [max(p.x, q.x), max(p.y, q.y), max(p.z, q.z)])

    def ycyl(x, z, y0, y1, r):
        return tbm.createCylinderOrCone(F(x, y0, z), r / 10.0, F(x, y1, z), r / 10.0)

    uA, uB, hg = P['uA'], P['uB'], P['hg']
    spans = {k: (v[0], v[1]) for k, v in PODS.items()}
    hosts = {o.component.name: o for o in root.occurrences}
    zbot = {k: v[2] for k, v in PODS.items()}
    plates = {h: box(X(a), X(b), -tp, 0, zbot[h], zt_) for h, (a, b) in spans.items()}

    # cut-outs: union footprint (x, z) of each lower module's bodies that pass through the panel plane
    cuts = []
    for h in spans:
        for ch in hosts[HOST[h]].childOccurrences:
            if not ch.component.name.startswith(LOWER):
                continue
            lo = [1e9, 1e9]; hi = [-1e9, -1e9]
            stack = [ch]
            while stack:
                o = stack.pop()
                for b in o.bRepBodies:
                    bb = b.boundingBox
                    if bb.minPoint.y < 2.0 and bb.maxPoint.y > 0.01 and bb.minPoint.z * 10 < 0:   # anything within 20 mm behind the face (fascia plates sit 14 mm back)
                        lo = [min(lo[0], bb.minPoint.x), min(lo[1], bb.minPoint.z)]
                        hi = [max(hi[0], bb.maxPoint.x), max(hi[1], bb.maxPoint.z)]
                stack.extend(list(o.childOccurrences))
            if hi[0] > lo[0] and ch.component.name.startswith(('Throttle', 'Mixture', 'Condition')):
                # push-pulls get a ROUND hole on the rod axis: 31 mm for the throttle friction screw, 27 mm for the
                # mixture screw (check both against the 737DIYSIM throttle guide before drilling)
                axis = None
                for o in ch.childOccurrences:
                    if 'rod' in o.name or 'Tube' in o.name:
                        # (a just-placed occurrence's own bbox is still empty: use its bodies, at any depth)
                        xs, zs, st2 = [], [], [o]
                        while st2:
                            q = st2.pop()
                            for bd in q.bRepBodies:
                                bb = bd.boundingBox
                                xs += [bb.minPoint.x, bb.maxPoint.x]; zs += [bb.minPoint.z, bb.maxPoint.z]
                            st2.extend(list(q.childOccurrences))
                        axis = ((min(xs) + max(xs)) / 2, (min(zs) + max(zs)) / 2)
                dia = 2.7 if ch.component.name.startswith('Mixture') else 3.1
                hole = tbm.createCylinderOrCone(adsk.core.Point3D.create(axis[0], -0.1, axis[1]), dia / 2,
                                                adsk.core.Point3D.create(axis[0], tp / 10.0 + 0.1, axis[1]), dia / 2)
                if not tbm.booleanOperation(plates[h], hole, SUB):
                    raise RuntimeError('cut failed ' + ch.name)
                cuts.append('%s %s round %.0f at u %.1f z %.1f' % (h, ch.component.name[:10], dia * 10, axis[0] * 10 + 460, axis[1] * 10))
            elif hi[0] > lo[0]:
                c = 0.05   # 0.5 mm clearance
                tool = boxw([lo[0] - c, -0.1, lo[1] - c], [hi[0] + c, tp / 10.0 + 0.1, hi[1] + c])
                if not tbm.booleanOperation(plates[h], tool, SUB):
                    raise RuntimeError('cut failed ' + ch.name)
                cuts.append('%s %s u %.0f..%.0f z %.0f..%.0f' % (h, ch.component.name[:16], lo[0] * 10 + 460, hi[0] * 10 + 460, lo[1] * 10, hi[1] * 10))
    items = {h: [('PANEL pod front plate 9 mm (%s)' % h.split(':')[1].split('(')[0].strip(), plates[h])] for h in spans}

    spx = importlib.util.spec_from_file_location('ext', BASE + 'ext.py')
    ext = importlib.util.module_from_spec(spx); spx.loader.exec_module(ext)
    prof = ext.make(tbm, F)
    for h in PODS:
        a, b = spans[h]
        B = BOX_DEPTH[h]
        zb_h = zbot[h]
        its = items[h]
        its.append(('2020 Pod top rail %d' % round(b - a - 6), prof(X(a + 3), X(b - 3), -tp - T, -tp, zt_ - T, zt_)))
        for (so0, so1) in ((a - sk, a), (b, b + sk)):
            its.append(('PANEL pod box side, deep (3 mm)', box(X(so0), X(so1), -B, rim, zb_h - sk, zd_under - sk)))
            its.append(('PANEL pod box side, desk zone (3 mm)', box(X(so0), X(so1), fz, rim, zd_under - sk, zt_)))
        its.append(('PANEL pod box bottom (3 mm)', box(X(a - sk), X(b + sk), -B, rim, zb_h - sk, zb_h)))
        its.append(('PANEL pod box lid (3 mm)', box(X(a), X(b), -B, -B + sk, zb_h, zd_under - sk)))
        its.append(('PANEL pod box shelf under desk (3 mm)', box(X(a), X(b), -B, fz, zd_under - sk, zd_under)))
        its.append(('PANEL pod box desk-zone back (3 mm)', box(X(a), X(b), fz - sk, fz, zd_under, zt_)))
        its.append(('PRINT pod hanger bracket (pair)', box(X(a + 10), X(a + 30), -tp - 2, -tp, zt_, zt_ + 30)))

    # fuel selector face plate: HIS face plate trimmed to 135 x 109 (+ a tab under the shut-off lever) so it fits under
    # the MFD bezel; printed by Jason from his file with the same trim
    import math
    f = FSP_FACE
    vend = [o for o in root.occurrences if o.component.name.startswith('737DIYSIM')][0]
    top = vend.childOccurrences.item(0)
    fsp = [c for c in top.childOccurrences if c.name == 'FSP3 v1:1'][0]
    face = [c for c in fsp.childOccurrences if c.name.startswith('1 Facepanel')][0]
    R = adsk.core.Matrix3D.create(); R.setToRotation(math.pi, adsk.core.Vector3D.create(0, 0, 1), adsk.core.Point3D.create(0, 0, 0))
    M = adsk.core.Matrix3D.create(); M.translation = adsk.core.Vector3D.create(7.0, 0.4, 15.05); R.transformBy(M)
    Tm = adsk.core.Matrix3D.create(); Tm.translation = adsk.core.Vector3D.create(633.0 / 10.0, -8.0 / 10.0, 252.0 / 10.0); R.transformBy(Tm)
    keep = box(X(f['u0']) - 1, X(f['u1']) + 1, -5.0, 20.0, f['z0'], f['z1'])
    tbm.booleanOperation(keep, box(X(f['tab'][0]), X(f['tab'][1]) + 1, -5.0, 20.0, f['z1'] - 1, f['tab'][2]), UNI)
    plate = None
    st = [face]
    while st:
        q = st.pop()
        for bd in q.bRepBodies:
            c = tbm.copy(bd); tbm.transform(c, R)
            if plate is None:
                plate = c
            else:
                tbm.booleanOperation(plate, c, UNI)
        st.extend(list(q.childOccurrences))
    tbm.booleanOperation(plate, keep, adsk.fusion.BooleanTypes.IntersectionBooleanType)
    items_main = [('PRINT fuel selector face plate (his plate trimmed to 135 x 109)', plate)]
    comp = hosts['Right half'].component
    bf = comp.features.baseFeatures.add(); bf.startEdit()
    for nm, bd in items_main:
        nb = comp.bRepBodies.add(bd, bf); nb.name = nm
    bf.finishEdit()

    for h, its in items.items():
        comp = hosts[HOST[h]].component
        bf = comp.features.baseFeatures.add(); bf.startEdit()
        for nm, b in its:
            nb = comp.bRepBodies.add(b, bf); nb.name = nm
        bf.finishEdit()
    print('pods: cuts:', cuts)
    return cuts


def run(_context: str):
    build_lower()
