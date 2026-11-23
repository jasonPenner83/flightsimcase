# Lower panel pieces (left, spacer, right) for the 737DIYSIM MIP folding case. Runs AFTER place_vendor.place().
# Jason (2026-11-23): the lower panel is separate from the main unit, bolted to it, and hangs BELOW the desk top in
# front of the desk edge; packed, it stays on and forms the base of the closed case. The 9 mm plates (same plane as the
# MIP panel) are cut where a lower module passes through. Each side piece has a stepped 3 mm box: shallow in the desk-
# edge zone (z -41..-3, 31 mm deep so it clears the desk edge 40 mm behind the face), full depth below the desk
# underside (z -41) where the deep parts (push-pull rods, fuel selector, flaps mechanism) run back under the desk.
# Units mm, frame as build_case_mip (X right, Y toward pilot, Z up, u = x + 460).
import importlib.util
import adsk.core, adsk.fusion

BASE = r'D:/Admin/Documents/Projects/FlightSimCase/fusion/'
spec = importlib.util.spec_from_file_location('build_case_mip', BASE + 'build_case_mip.py')
bcm = importlib.util.module_from_spec(spec); spec.loader.exec_module(bcm)
P = bcm.P

HOST = {'Left half': 'Lower panel (left)', 'Spacer': 'Lower panel (spacer)', 'Right half': 'Lower panel (right)'}
BOX_DEPTH = {'Left half': 72.0, 'Right half': 190.0}   # same as the rear boxes above
LOWER = ('LHS Fuse panel', 'FSP3', 'Throttle', 'Mixture', 'Condition', 'Trim')


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
    spans = {'Left half': (0.0, uB - hg), 'Spacer': (uB + hg, uA - hg), 'Right half': (uA + hg, 920.0 + P['shift_right'] + P['r_ext'])}
    hosts = {}
    for o in root.occurrences:
        for ch in o.childOccurrences:
            if ch.component.name.startswith('Lower panel'):
                hosts[ch.component.name] = ch
    zbot = {h: (P['lower_bot_right'] if h == 'Right half' else zb_) for h in spans}
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
    items = {h: [('PANEL lower (%s)' % h.lower(), plates[h])] for h in spans}

    spx = importlib.util.spec_from_file_location('ext', BASE + 'ext.py')
    ext = importlib.util.module_from_spec(spx); spx.loader.exec_module(ext)
    prof = ext.make(tbm, F)
    for h in ('Left half', 'Right half'):
        a, b = spans[h]
        B = BOX_DEPTH[h]
        if h == 'Left half':
            so0, so1, ui0, ui1 = a - sk, a, a, b          # outer skin column, inner span
            ur0, ur1 = a + T, b - 20
        else:
            so0, so1, ui0, ui1 = b, b + sk, a, b
            ur0, ur1 = a + 20, b - T
        its = items[h]
        its.append(('2020 Lower rail %d' % round(ur1 - ur0), prof(X(ur0), X(ur1), -tp - T, -tp, zt_ - T, zt_)))
        zb_h = zbot[h]
        its.append(('PANEL lower box side, deep (3 mm)', box(X(so0), X(so1), -B, rim, zb_h - sk, zd_under - sk)))
        its.append(('PANEL lower box side, desk zone (3 mm)', box(X(so0), X(so1), fz, rim, zd_under - sk, zt_)))
        its.append(('PANEL lower box bottom (3 mm)', box(X(min(so0, ui0)), X(max(so1, ui1)), -B, rim, zb_h - sk, zb_h)))
        its.append(('PANEL lower box lid (3 mm)', box(X(ui0), X(ui1), -B, -B + sk, zb_h, zd_under - sk)))
        its.append(('PANEL lower box shelf under desk (3 mm)', box(X(ui0), X(ui1), -B, fz, zd_under - sk, zd_under)))
        its.append(('PANEL lower box desk-zone back (3 mm)', box(X(ui0), X(ui1), fz - sk, fz, zd_under, zt_)))

    for h, its in items.items():
        comp = hosts[HOST[h]].component
        bf = comp.features.baseFeatures.add(); bf.startEdit()
        for nm, b in its:
            nb = comp.bRepBodies.add(b, bf); nb.name = nm
        bf.finishEdit()
    print('lower panel pieces: z %.0f..%.0f, cuts:' % (zb_, zt_), cuts)
    return cuts


def run(_context: str):
    build_lower()
