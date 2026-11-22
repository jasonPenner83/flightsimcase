# Fuse panels as FALSE FRONTS (Jason: they have no function). His fuse-panel fascia (5 mm plate 14 mm behind the
# panel face, breaker heads only ~17 mm deep) becomes a drop-down door on a printed bottom hinge with a magnet
# catch at the top; behind each one is a printed cubby running back to just inside the rear lid. Hardware lives
# in there: a powered USB hub (left) and a 12 V PSU (right) are placed as example envelopes.
# Runs after build_glareshield. Units mm, frame as build_case_mip (X right, Y toward pilot, Z up, u = x + 460).
import importlib.util
import adsk.core, adsk.fusion

BASE = r'D:/Admin/Documents/Projects/FlightSimCase/fusion/'
spec = importlib.util.spec_from_file_location('build_case_mip', BASE + 'build_case_mip.py')
bcm = importlib.util.module_from_spec(spec); spec.loader.exec_module(bcm)
P = bcm.P

W = 2.0                      # cubby wall
Y_FRONT, Y_BACK = -11.5, -122.0     # front stays clear of the seam-angle leaf (y -9..-11)
# (host, inner u0, u1, inner z0, z1)  - inner box contains the fascia footprint
CUBBIES = [('Left half', 23.0, 291.0, -103.0, -1.5)]   # (right fuse panel replaced by throttle/mixture/condition)   # top wall ends at z 0 (2020 rail)
HW = [  # (host, name, u0, u1, z0, z1, y0, y1)
    ('Left half', 'REF powered USB hub 7-port (115x45x25)', 150.0, 265.0, -103.0, -78.0, -115.0, -70.0),
    ('Right half', 'REF 12V PSU (LRS-50-12 size 99x82x30)', 528.0, 610.0, -103.0, -4.0, -45.0, -15.0),   # on edge, behind the blank right lower
]


def X(u):
    return u - 460.0


def build_falsefront():
    app = adsk.core.Application.get()
    d = adsk.fusion.Design.cast(app.activeProduct)
    root = d.rootComponent
    tbm = adsk.fusion.TemporaryBRepManager.get()
    SUB = adsk.fusion.BooleanTypes.DifferenceBooleanType
    UNI = adsk.fusion.BooleanTypes.UnionBooleanType

    def op(a, b, k):
        if not tbm.booleanOperation(a, b, k):
            raise RuntimeError('boolean failed')

    def F(x, y, z):
        return adsk.core.Point3D.create(x / 10.0, -y / 10.0, z / 10.0)

    def box(x0, x1, y0, y1, a, b):
        p = F(x0, y0, a); q = F(x1, y1, b)
        lo = [min(p.x, q.x), min(p.y, q.y), min(p.z, q.z)]; hi = [max(p.x, q.x), max(p.y, q.y), max(p.z, q.z)]
        c = adsk.core.Point3D.create((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2)
        return tbm.createBox(adsk.core.OrientedBoundingBox3D.create(c, adsk.core.Vector3D.create(1, 0, 0), adsk.core.Vector3D.create(0, 1, 0),
                                                                   hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]))

    hosts = {o.component.name: o for o in root.occurrences}
    items = {}
    for h, u0, u1, z0, z1 in CUBBIES:
        cub = box(X(u0 - W), X(u1 + W), Y_BACK, Y_FRONT, z0 - W, 0.0)
        op(cub, box(X(u0), X(u1), Y_BACK + W, Y_FRONT + 1, z0, z1), SUB)        # open front
        # cable pass-throughs into the rear tub (2 x 30x15 slots in the back wall)
        for uc in (u0 + 0.25 * (u1 - u0), u0 + 0.75 * (u1 - u0)):
            op(cub, box(X(uc) - 15, X(uc) + 15, Y_BACK - 1, Y_BACK + W + 1, z1 - 25, z1 - 10), SUB)
        items.setdefault(h, []).append(('PRINT false-front cubby (behind fuse panel)', cub))
        # bottom hinge strip + top magnet catch block for the fascia door (door = his fuse fascia on a carrier)
        items[h].append(('PRINT false-front hinge strip', box(X(u0 + 10), X(u1 - 10), -24.0, -19.0, z0, z0 + 6)))
        mc = (u0 + u1) / 2
        items[h].append(('PRINT false-front magnet catch', box(X(mc) - 10, X(mc) + 10, -26.0, -19.0, z1 - 6, z1)))
    for h, nm, u0, u1, z0, z1, y0, y1 in HW:
        items.setdefault(h, []).append((nm, box(X(u0), X(u1), y0, y1, z0, z1)))
    for h, its in items.items():
        comp = hosts[h].component
        bf = comp.features.baseFeatures.add(); bf.startEdit()
        for nm, bd in its:
            nb = comp.bRepBodies.add(bd, bf); nb.name = nm
            if nm.startswith('REF'):
                nb.opacity = 0.35
        bf.finishEdit()
    print('false front: cubby L u %.0f-%.0f, %d mm deep' % (CUBBIES[0][1], CUBBIES[0][2], -Y_BACK))


def run(_context: str):
    build_falsefront()
