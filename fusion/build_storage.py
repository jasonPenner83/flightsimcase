# Storage for the MIP folding case (runs after build_lower):
#  - rear storage tubs on both halves: 3 mm walls following the panel outline (incl. the big top corner curves)
#    from the panel back to a removable 3 mm rear lid. Everything behind the panel is <= 77 mm deep, so a
#    130 mm tub leaves ~95-115 mm of clear stowage over most of each half.
#  - open face pockets (print trays) behind the pocket cut-outs in the panels (see build_case_mip P['pockets']).
#  - stowed items, so they are checked against the electronics: Logitech throttle quadrant (envelope),
#    clamp-on fuel selector pod and trim wheel pod (737DIYSIM FSP3 + Trim v15 in printed shells), and the
#    pedestal base / desk clamp the pods slide onto when deployed.
# Units mm, frame as build_case_mip (X right, Y toward pilot, Z up, u = x + 460).
import importlib.util, math
import adsk.core, adsk.fusion

BASE = r'D:/Admin/Documents/Projects/FlightSimCase/fusion/'
spec = importlib.util.spec_from_file_location('build_case_mip', BASE + 'build_case_mip.py')
bcm = importlib.util.module_from_spec(spec); spec.loader.exec_module(bcm)
P = bcm.P

S = dict(
    tub_back=130.0,      # rear lid outer face, mm behind the panel face
    wall=3.0,
    ell_a=236.0, ell_b=153.0, ell_z=216.0,   # his panel's top outer corner curve (approximated as a quarter ellipse)
    pocket_depth=60.0,
)
# stowed positions (pilot u / z of the stowed item's centre, pilot y range)
QUADRANT = dict(host='Right half', u=(560.0, 735.0), z=(140.0, 315.0), y=(-122.0, -32.0))   # 175 x 175 x 90
PED_BASE = dict(host='Left half', u=(30.0, 250.0), z=(175.0, 285.0), y=(-80.0, -35.0))
FUEL_POD = dict(host='Right half', src='FSP3 v1:1', mod_u=230.5, mod_z=-199.0, stow_u=852.0, stow_z=211.0, stow_c=-87.0, rot=180)
TRIM_POD = dict(host='Left half', src='Trim v15:1', mod_u=409.5, mod_z=-213.0, stow_u0=255.0, stow_yc=-74.0, stow_z=230.0, rot=90)


def X(u):
    return u - 460.0


def build_storage():
    app = adsk.core.Application.get()
    d = adsk.fusion.Design.cast(app.activeProduct)
    root = d.rootComponent
    tbm = adsk.fusion.TemporaryBRepManager.get()
    SUB = adsk.fusion.BooleanTypes.DifferenceBooleanType
    UNI = adsk.fusion.BooleanTypes.UnionBooleanType
    INT = adsk.fusion.BooleanTypes.IntersectionBooleanType
    tp = P['t_panel']; zl = P['z_low']; T = P['T']; w = S['wall']

    def op(a, b, k):
        if not tbm.booleanOperation(a, b, k):
            raise RuntimeError('boolean failed')

    def F(x, y, z):
        return adsk.core.Point3D.create(x / 10.0, -y / 10.0, z / 10.0)

    def boxw(lo, hi):
        c = adsk.core.Point3D.create((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2)
        return tbm.createBox(adsk.core.OrientedBoundingBox3D.create(c, adsk.core.Vector3D.create(1, 0, 0), adsk.core.Vector3D.create(0, 1, 0),
                                                                   hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]))

    def box(x0, x1, y0, y1, a, b):
        p = F(x0, y0, a); q = F(x1, y1, b)
        return boxw([min(p.x, q.x), min(p.y, q.y), min(p.z, q.z)], [max(p.x, q.x), max(p.y, q.y), max(p.z, q.z)])

    uA, uB, hg = P['uA'], P['uB'], P['hg']
    l0, l1 = 0.0, uB - hg
    r0, r1 = uA + hg, 920.0 + P['shift_right']
    a, b, ez = S['ell_a'], S['ell_b'], S['ell_z']

    def prism(host, ins, y0, y1):
        """panel outline (inset by ins) extruded from pilot y0 to y1"""
        if host == 'Left half':
            u0, u1, ec, cu0, cu1 = l0, l1, l0 + a, l0, l0 + a
        else:
            u0, u1, ec, cu0, cu1 = r0, r1, r1 - a, r1 - a, r1
        body = box(X(u0 + ins), X(u1 - ins), y0, y1, zl + ins, ez)
        if host == 'Left half':
            op(body, box(X(ec), X(u1 - ins), y0, y1, ez - 1, 369.0 - ins), UNI)
        else:
            op(body, box(X(u0 + ins), X(ec), y0, y1, ez - 1, 369.0 - ins), UNI)
        ell = tbm.createEllipticalCylinderOrCone(F(X(ec), y0, ez), (a - ins) / 10.0, (b - ins) / 10.0, F(X(ec), y1, ez), (a - ins) / 10.0,
                                                 adsk.core.Vector3D.create(1, 0, 0))
        op(ell, box(X(cu0) - 1, X(cu1) + 1, y0 - 1, y1 + 1, ez - 1, 400), INT)
        op(body, ell, UNI)
        return body

    hosts = {o.component.name: o for o in root.occurrences}
    items = {'Left half': [], 'Right half': [], 'Spacer': []}
    back = -S['tub_back']
    for h in ('Left half', 'Right half'):
        walls = prism(h, 0.0, back + w, -tp)
        op(walls, prism(h, w, back, -tp + 1), SUB)
        # clear the frame members the walls run along (uprights, seam angle, lower rail)
        if h == 'Left half':
            op(walls, box(X(l0) - 1, X(l0) + T, -tp - 40, -tp + 1, zl - 1, 216.5), SUB)
            op(walls, box(X(l1) - 20, X(l1) + 1, -tp - 20, -tp + 1, zl - 1, 370), SUB)
        else:
            op(walls, box(X(r1) - T, X(r1) + 1, -tp - 40, -tp + 1, zl - 1, 216.5), SUB)
            op(walls, box(X(r0) - 1, X(r0) + 20, -tp - 20, -tp + 1, zl - 1, 370), SUB)
        op(walls, box(X(l0 if h == 'Left half' else r0) - 1, X(l1 if h == 'Left half' else r1) + 1, -tp - T, -tp + 1, zl - 1, zl + T), SUB)
        items[h].append(('PANEL rear tub walls (3 mm ply)', walls))
        items[h].append(('PANEL rear lid (3 mm ply, removable)', prism(h, 0.0, back, back + w)))

    # face pockets (open-front print trays behind the panel cut-outs)
    for h, p0, p1, q0, q1 in P['pockets']:
        tray = box(X(p0) - 2, X(p1) + 2, -tp - S['pocket_depth'] - 2, -tp, q0 - 2, q1 + 2)
        op(tray, box(X(p0), X(p1), -tp - S['pocket_depth'], -tp + 1, q0, q1), SUB)
        items[h].append(('PRINT face pocket tray', tray))

    # stowed: quadrant envelope + pedestal base
    q = QUADRANT
    items[q['host']].append(('REF Logitech throttle quadrant 175x175x90 (stowed)', box(X(q['u'][0]), X(q['u'][1]), q['y'][0], q['y'][1], q['z'][0], q['z'][1])))
    pb = PED_BASE
    base = box(X(pb['u'][0]), X(pb['u'][1]), pb['y'][0], pb['y'][1], pb['z'][0], pb['z'][1])
    items[pb['host']].append(('PRINT pedestal base + desk clamp (stowed)', base))

    for h, its in items.items():
        if not its:
            continue
        comp = hosts[h].component
        bf = comp.features.baseFeatures.add(); bf.startEdit()
        for nm, bd in its:
            nb = comp.bRepBodies.add(bd, bf); nb.name = nm
            if nm.startswith('REF'):
                nb.opacity = 0.35
        bf.finishEdit()

    # clamp-on pods: vendor module + printed shell, built about the module centre, then stowed
    vend = [o for o in root.occurrences if o.component.name.startswith('737DIYSIM')][0]
    top = vend.childOccurrences.item(0)
    R = adsk.core.Matrix3D.create(); R.setToRotation(math.pi, adsk.core.Vector3D.create(0, 0, 1), adsk.core.Point3D.create(0, 0, 0))
    Tours = adsk.core.Matrix3D.create(); Tours.translation = adsk.core.Vector3D.create(7.0, 0.4, 15.05)

    def pod(spec, name, shell_lo, shell_hi):
        src = [c for c in top.childOccurrences if c.name == spec['src']][0]
        rz = adsk.core.Matrix3D.create()
        rz.setToRotation(math.radians(spec['rot']), adsk.core.Vector3D.create(0, 0, 1), adsk.core.Point3D.create(0, 0, 0))
        Tm = adsk.core.Matrix3D.create()
        if spec['rot'] == 180:     # depth stays along y, flipped: pilot y_world = c - y_local
            Tm.translation = adsk.core.Vector3D.create(X(spec['stow_u']) / 10.0, -spec['stow_c'] / 10.0, spec['stow_z'] / 10.0)
        else:                      # 90: depth runs along +u, width along y
            Tm.translation = adsk.core.Vector3D.create(X(spec['stow_u0']) / 10.0 + (-shell_lo[1]) / 10.0, -spec['stow_yc'] / 10.0, spec['stow_z'] / 10.0)
        M = rz.copy(); M.transformBy(Tm)
        T1 = adsk.core.Matrix3D.create(); T1.translation = adsk.core.Vector3D.create(-X(spec['mod_u']) / 10.0, 0, -spec['mod_z'] / 10.0)
        W = src.transform2.copy(); W.transformBy(R); W.transformBy(Tours); W.transformBy(T1); W.transformBy(M)
        host = hosts[spec['host']]
        po = host.component.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        po.component.name = name
        po.isGroundToParent = True
        # shell in local (pilot) coords: shell_lo/hi = (x, y, z) mm, open front
        outer = box(shell_lo[0], shell_hi[0], shell_lo[1], shell_hi[1], shell_lo[2], shell_hi[2])
        op(outer, box(shell_lo[0] + w, shell_hi[0] - w, shell_lo[1] + w, shell_hi[1] + 1, shell_lo[2] + w, shell_hi[2] - w), SUB)
        # dovetail foot that slides onto the pedestal base
        foot = box(-30, 30, shell_lo[1] + 10, shell_hi[1] - 10, shell_lo[2] - 8, shell_lo[2])
        op(outer, foot, UNI)
        tbm.transform(outer, M)
        bf = po.component.features.baseFeatures.add(); bf.startEdit()
        nb = po.component.bRepBodies.add(outer, bf); nb.name = 'PRINT pod shell'
        bf.finishEdit()
        mo = po.component.occurrences.addExistingComponent(src.component, W)
        mo.isGroundToParent = True
        return po

    # fuel selector now lives on the panel (left lower), so only the trim wheel is a clamp-on pod
    # pod(FUEL_POD, 'Fuel selector pod (clamp-on)', (-69.0, -75.0, -66.0), (69.0, -8.0, 66.0))   # tucked between MFD, rail and the corner curve
    pod(TRIM_POD, 'Trim wheel pod (clamp-on)', (-41.5, -130.0, -90.0), (41.5, 0.0, 90.0))
    print('storage: tubs to %.0f mm behind face, pockets %d, stowed quadrant/base/pods' % (S['tub_back'], len(P['pockets'])))


def run(_context: str):
    build_storage()
