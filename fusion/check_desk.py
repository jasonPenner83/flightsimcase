# Deployed check against the desk and the Logitech yoke housing (temporary bodies, removed again).
# Desk: top at z -3 (under the main unit's bottom skin), front edge 40 mm behind the panel face, 38 mm thick.
# Yoke housing: 250 x 250 x 71.25 mm on the desk, front at the desk edge, centred on the yoke hole (chamfers ignored,
# so the check is conservative). Writes the result to check_desk.log.
import importlib.util
import adsk.core, adsk.fusion

BASE = r'D:/Admin/Documents/Projects/FlightSimCase/fusion/'


def load(n):
    spec = importlib.util.spec_from_file_location(n, BASE + n + '.py')
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def check():
    P = load('build_case_mip').P
    t = load('tools'); rm = load('run_mip'); rm.setup(t)
    d = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    root = d.rootComponent
    rm.fold(t, 0, 0)
    tbm = adsk.fusion.TemporaryBRepManager.get()

    def box(u0, u1, y0, y1, z0, z1):
        lo = [(u0 - 460) / 10.0, -max(y0, y1) / 10.0, z0 / 10.0]; hi = [(u1 - 460) / 10.0, -min(y0, y1) / 10.0, z1 / 10.0]
        c = adsk.core.Point3D.create((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2)
        return tbm.createBox(adsk.core.OrientedBoundingBox3D.create(c, adsk.core.Vector3D.create(1, 0, 0), adsk.core.Vector3D.create(0, 1, 0),
                                                                   hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]))
    dz, de, dt = P['desk_z'], P['desk_edge'], P['desk_t']
    yu0, yu1, ydep, yh = P['yoke_box']
    occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    comp = occ.component; comp.name = 'TEMP desk check'
    bf = comp.features.baseFeatures.add(); bf.startEdit()
    desk = comp.bRepBodies.add(box(-300, 1300, -de, -de - 700, dz - dt, dz), bf); desk.name = 'DESK'
    yoke = comp.bRepBodies.add(box(yu0, yu1, -de, -de - ydep, dz, dz + yh), bf); yoke.name = 'YOKE HOUSING'
    bf.finishEdit()
    coll = adsk.core.ObjectCollection.create()
    for b in occ.bRepBodies:
        coll.add(b)

    def walk(o):
        for b in o.bRepBodies:
            if not b.name.startswith('ZONE') and 'middle' not in b.name:
                coll.add(b)
        for c in o.childOccurrences:
            walk(c)
    for o in root.occurrences:
        if o.component.name in ('Left half', 'Spacer', 'Right half'):
            walk(o)
    ii = d.createInterferenceInput(coll); ii.areCoincidentFacesIncluded = False
    res = d.analyzeInterference(ii)
    hits = []
    for r in (res or []):
        a, b = r.entityOne, r.entityTwo
        na, nb = a.name in ('DESK', 'YOKE HOUSING'), b.name in ('DESK', 'YOKE HOUSING')
        if na == nb:
            continue
        other, ref = (b, a) if na else (a, b)
        bb = r.interferenceBody.boundingBox
        hits.append('%s x %s/%s %.0f mm3 u %.0f..%.0f z %.0f..%.0f y %.0f..%.0f' % (ref.name, other.parentComponent.name[:16], other.name[:22], r.interferenceBody.volume * 1000,
                    bb.minPoint.x * 10 + 460, bb.maxPoint.x * 10 + 460, bb.minPoint.z * 10, bb.maxPoint.z * 10, -bb.maxPoint.y * 10, -bb.minPoint.y * 10))
    occ.deleteMe()
    msg = 'desk/yoke check: bodies %d hits %d\n  %s' % (coll.count, len(hits), '\n  '.join(hits[:25]))
    open(BASE + 'check_desk.log', 'w').write(msg + '\n')
    print(msg)
    return hits


def run(_context: str):
    check()
