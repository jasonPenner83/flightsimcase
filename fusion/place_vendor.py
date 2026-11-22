# Place 737DIYSIM modules (imported from vendor/ STEP into component "737DIYSIM C172 MIP (vendor STEP)")
# onto our folding halves, using the same 180-deg turn + offsets as build_case_mip, plus our shifts.
# Front envelopes (ZONE bodies) are generated from each placed module's bounding box for the fold check.
import adsk.core, adsk.fusion, math

# source occurrence name ('parent/child' for nested) -> (host, du mm, dy mm (+ = toward pilot)[, dz mm])
PLACE = {
    'G1000 v1:1':          ('Left half', 0.0, 0.0),
    '172 AV PNL v1:1':     ('Left half', 0.0, 0.0),
    'C172 Yoke Adapt:1':   ('Left half', 0.0, 0.0),
    'GMA-1347 v3:1':       ('Spacer', 10.0, -16.0),      # sunk flush into the spacer
    'G1000 V2 v1:1':       ('Right half', 25.0, 0.0),
    'ASI v1:1':            ('Right half', 90.0, 0.0),    # ASI + attitude + altimeter block moved right
    'Elt:1':               ('Right half', 25.0, 0.0),
    # lower panel: his fuse panels are fascias that stand 28 mm proud of his recessed 3 mm plate; brought
    # forward 12 mm their faces land flush with the MIP face and pass through cut-outs in our 9 mm lower plate.
    # The flaps lever comes forward 40 mm (lever stands proud like the real one, mechanism stays shallow).
    # Throttle (throt temp, 172 THROTTLE V2) and mixture (Mix Lever) are left out: Logitech quadrant does those.
    'Lower Panel Assy v1:1/LHS Fuse panel v1:1': ('Left half', 0.0, 12.0),
    'Lower Panel Assy v1:1/RHS Fuse Pnl v1:1':   ('Right half', 265.0, 12.0),   # off the seam: u 530-733
    'Lower Panel Assy v1:1/flaps lever v1:1':    ('Right half', 126.0, 40.0),   # u 790-872
    'C172 Start sw v1:1':  ('Left half', 227.0, 0.0, 121.5),                    # key: from pedestal to left lower, u 300
}
LOWER = ('LHS Fuse panel', 'RHS Fuse Pnl', 'flaps lever', 'C172 Start sw')
REMOVABLE = ('dUAL kNOB',)     # knobs that come off for travel (GMA volume knob)


def place():
    app = adsk.core.Application.get()
    d = adsk.fusion.Design.cast(app.activeProduct)
    root = d.rootComponent
    tbm = adsk.fusion.TemporaryBRepManager.get()
    hosts = {o.component.name: o for o in root.occurrences}
    vend = [o for o in root.occurrences if o.component.name.startswith('737DIYSIM')][0]
    top = vend.childOccurrences.item(0)
    R = adsk.core.Matrix3D.create()
    R.setToRotation(math.pi, adsk.core.Vector3D.create(0, 0, 1), adsk.core.Point3D.create(0, 0, 0))
    Tours = adsk.core.Matrix3D.create(); Tours.translation = adsk.core.Vector3D.create(7.0, 0.4, 15.05)

    def F(x, y, z):
        return adsk.core.Point3D.create(x / 10.0, -y / 10.0, z / 10.0)

    def box_world(lo, hi):
        c = adsk.core.Point3D.create((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2)
        return tbm.createBox(adsk.core.OrientedBoundingBox3D.create(c, adsk.core.Vector3D.create(1, 0, 0), adsk.core.Vector3D.create(0, 1, 0),
                                                                   hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]))

    placed = []
    srcs = []
    for src in top.childOccurrences:
        if src.name in PLACE:
            srcs.append((src, PLACE[src.name], None))
        for ch in src.childOccurrences:
            k = src.name + '/' + ch.name
            if k in PLACE:
                srcs.append((ch, PLACE[k], src))
    for src, spec, parent in srcs:
        host, du, dy = spec[:3]
        dz = spec[3] if len(spec) > 3 else 0.0
        W = src.transform2.copy()
        if parent is not None:
            W.transformBy(parent.transform2)
        W.transformBy(R)
        W.transformBy(Tours)
        Tm = adsk.core.Matrix3D.create(); Tm.translation = adsk.core.Vector3D.create(du / 10.0, -dy / 10.0, dz / 10.0)
        W.transformBy(Tm)
        occ = hosts[host].component.occurrences.addExistingComponent(src.component, W)
        occ.isGroundToParent = True
        placed.append((host, occ))
    vend.isLightBulbOn = False

    # front envelopes (y >= 0 in pilot frame = Fusion y <= 0), per placed module, as ZONE bodies in the host
    env = {}
    for host, occ in placed:
        lo = [1e9] * 3; hi = [-1e9] * 3
        stack = [occ]
        while stack:
            o = stack.pop()
            if any(o.name.startswith(r) for r in REMOVABLE) and host == 'Spacer':
                continue
            for b in o.bRepBodies:
                bb = b.boundingBox
                if bb.minPoint.y < -0.05:          # reaches in front of the panel face
                    lo = [min(lo[0], bb.minPoint.x), min(lo[1], bb.minPoint.y), min(lo[2], bb.minPoint.z)]
                    hi = [max(hi[0], bb.maxPoint.x), max(hi[1], min(bb.maxPoint.y, 0.0)), max(hi[2], bb.maxPoint.z)]
            for ch in o.childOccurrences:
                stack.append(ch)
        if hi[0] > lo[0]:
            env.setdefault(host, []).append(('ZONE %s front envelope' % occ.component.name[:30], box_world(lo, hi)))
            print('%-11s %-28s front: x %.0f..%.0f  depth %.0f mm  z %.0f..%.0f' % (host, occ.component.name[:28], lo[0]*10, hi[0]*10, -lo[1]*10, lo[2]*10, hi[2]*10))
    for host, items in env.items():
        comp = hosts[host].component
        bf = comp.features.baseFeatures.add(); bf.startEdit()
        for nm, b in items:
            nb = comp.bRepBodies.add(b, bf); nb.name = nm
            nb.opacity = 0.2
        bf.finishEdit()
    return placed


def run(_context: str):
    place()
