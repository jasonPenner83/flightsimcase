# Lower panel for the 737DIYSIM MIP folding case. Runs AFTER place_vendor.place(): the 9 mm lower plates
# (same plane as the MIP panel) are cut wherever a placed lower module passes through the panel plane.
# Behind the plates: open-top printed cable bins in the negative space. Condition knob = placeholder.
# Units mm, frame as build_case_mip (X right, Y toward pilot, Z up, u = x + 460).
import importlib.util
import adsk.core, adsk.fusion

BASE = r'D:/Admin/Documents/Projects/FlightSimCase/fusion/'
spec = importlib.util.spec_from_file_location('build_case_mip', BASE + 'build_case_mip.py')
bcm = importlib.util.module_from_spec(spec); spec.loader.exec_module(bcm)
P = bcm.P

COND = dict(u=760.0, z=-55.0, knob_d=28.0, knob_h=22.0, shaft_d=6.0, hole_d=10.0)
# (host, u0, u1, z0, z1, depth) open-top bins behind the lower plates. Halves: inside the 2040 frame depth.
# Spacer: shallow, because the spacer's back faces outward when folded (a deeper bin widens the closed case).
BINS = [('Spacer', 436.0, 515.0, None, -5.0, 21.5),
        ('Right half', 878.0, 922.0, None, -5.0, 48.5)]
LOWER = ('LHS Fuse panel', 'RHS Fuse Pnl', 'flaps lever', 'FSP3')


def X(u):
    return u - 460.0


def build_lower():
    app = adsk.core.Application.get()
    d = adsk.fusion.Design.cast(app.activeProduct)
    root = d.rootComponent
    tbm = adsk.fusion.TemporaryBRepManager.get()
    SUB = adsk.fusion.BooleanTypes.DifferenceBooleanType
    UNI = adsk.fusion.BooleanTypes.UnionBooleanType
    tp = P['t_panel']; zl = P['z_low']; T = P['T']

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
    spans = {'Left half': (0.0, uB - hg), 'Spacer': (uB + hg, uA - hg), 'Right half': (uA + hg, 920.0 + P['shift_right'])}
    hosts = {o.component.name: o for o in root.occurrences}
    plates = {h: box(X(a), X(b), -tp, 0, zl, 0) for h, (a, b) in spans.items()}

    # cut-outs: union footprint (x, z) of each lower module's bodies that pass through the panel plane
    cuts = []
    for h in spans:
        for ch in hosts[h].childOccurrences:
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
            if hi[0] > lo[0]:
                c = 0.05   # 0.5 mm clearance
                tool = boxw([lo[0] - c, -0.1, lo[1] - c], [hi[0] + c, tp / 10.0 + 0.1, hi[1] + c])
                if not tbm.booleanOperation(plates[h], tool, SUB):
                    raise RuntimeError('cut failed ' + ch.name)
                cuts.append('%s %s u %.0f..%.0f z %.0f..%.0f' % (h, ch.component.name[:16], lo[0] * 10 + 460, hi[0] * 10 + 460, lo[1] * 10, hi[1] * 10))
    # condition knob hole (right lower)
    tbm.booleanOperation(plates['Right half'], ycyl(X(COND['u']), COND['z'], -tp - 1, 1, COND['hole_d'] / 2), SUB)

    items = {h: [('PANEL lower (%s)' % h.lower(), plates[h])] for h in spans}
    knob = ycyl(X(COND['u']), COND['z'], 0, COND['knob_h'], COND['knob_d'] / 2)
    tbm.booleanOperation(knob, ycyl(X(COND['u']), COND['z'], -35, 0, COND['shaft_d'] / 2), UNI)
    items['Right half'].append(('PRINT condition knob (placeholder)', knob))
    items['Right half'].append(('PRINT condition knob pot bracket', box(X(COND['u']) - 15, X(COND['u']) + 15, -tp - 25, -tp - 22, COND['z'] - 15, COND['z'] + 15)))

    for h, u0, u1, z0, z1, dep in BINS:
        z0 = (zl + T + 2) if (z0 is None and h != 'Spacer') else (zl + 5 if z0 is None else z0)
        y_front, y_back = -tp - 2.5, -tp - 2.5 - dep
        b = box(X(u0), X(u1), y_back, y_front, z0, z1)
        tbm.booleanOperation(b, box(X(u0) + 2, X(u1) - 2, y_back + 2, y_front - 2, z0 + 2, z1 + 5), SUB)
        items[h].append(('PRINT cable bin (%s)' % h.lower(), b))

    for h, its in items.items():
        comp = hosts[h].component
        bf = comp.features.baseFeatures.add(); bf.startEdit()
        for nm, b in its:
            nb = comp.bRepBodies.add(b, bf); nb.name = nm
        bf.finishEdit()
    print('lower panel: z %.0f..0, cuts:' % zl, cuts)
    return cuts


def run(_context: str):
    build_lower()
