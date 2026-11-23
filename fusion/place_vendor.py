# Place 737DIYSIM modules (imported from vendor/ STEP into component "737DIYSIM C172 MIP (vendor STEP)")
# onto our folding halves, using the same 180-deg turn + offsets as build_case_mip, plus our shifts.
# Front envelopes (ZONE bodies) are generated from each placed module's bounding box for the fold check.
import adsk.core, adsk.fusion, math

# source occurrence name ('parent/child' for nested) -> (host, du mm, dy mm (+ = toward pilot)[, dz mm])
PLACE = {
    'G1000 v1:1':          ('Left half', 0.0, 0.0),
    '172 AV PNL v1:1':     ('Left half', 0.0, 0.0),
    'C172 Yoke Adapt:1':   ('Left half', 0.0, 0.0, -27.0),   # follows the yoke hole down to the Logitech shaft height
    'GMA-1347 v3:1':       ('Spacer', 10.0, -16.0),      # sunk flush into the spacer
    'G1000 V2 v1:1':       ('Right half', 25.0, 0.0),
    'ASI v1:1':            ('Right half', 90.0, 0.0),    # ASI + attitude + altimeter block moved right
    'Elt:1':               ('Right half', 25.0, 0.0),
    # lower panel: his fuse panels are fascias that stand 28 mm proud of his recessed 3 mm plate; brought
    # forward 12 mm their faces land flush with the MIP face and pass through cut-outs in our 9 mm lower plate.
    # The flaps lever comes forward 40 mm (lever stands proud like the real one, mechanism stays shallow).
    'Lower Panel Assy v1:1/LHS Fuse panel v1:1': ('Lower panel (left)', 0.0, 12.0, -48.0),
    # (RHS fuse panel removed: throttle / mixture / condition push-pulls take its place, see SPLIT)
    'Lower Panel Assy v1:1/flaps lever v1:1':    ('Right half', 151.0, 40.0, 120.0),   # main panel, right of the standby gauges (u 815-897, z 25-111)
    'Trim v15:1':          ('Lower panel (right)', 162.0, 0.0, 83.0),   # built into the right lower piece, left of the throttle (u 535-609)   # u 790-872
    # fuel selector on the left lower in the old start-key spot (Jason: keep the key that's in the LHS fuse panel).
    # Face u 288-423, z -119..11 (overlaps the MIP bottom edge by 11 mm), face plate on the panel front; support body
    # fits exactly between the lower 2020 rail (z -105) and the MIP panel bottom (z 0).
    'FSP3 v1:1':           ('Lower panel (left)', 125.0, 8.0, 97.0),
}
# His lower-panel push-pull throttle and mixture (slide-pot type), plus a second throttle used as the CONDITION
# knob, on the right lower where the RHS fuse panel was. Modelled PUSHED IN (storage/fold state): knob, rod and
# ferrule move 62 mm (throttle) / 60 mm (mixture) back from his pulled-out pose, so knobs stand ~46 mm proud and the
# rods reach ~171 mm behind the face (right rear tub is deeper for this). Each is placed child by child into a
# wrapper component.  (key, wrapper name, host, du, dy, dz, {child-name prefix: extra dy, None = leave out})
MOVE_T = {'8mm x 198mm brass rod': -62.0, '5 Throttle Knob (1)': -62.0, '8 Ferrule (1)': -62.0, '5 Throttle Knob (2)': None}
MOVE_M = {'Mix Tube': -60.0, '3 Mix Knob': -60.0, '8 Ferrule': -60.0}
SPLIT = [
    ('Lower Panel Assy v1:1/throt temp v1:1', 'Throttle (push-pull, pushed in)', 'Lower panel (right)', 74.0, 12.0, -48.0, MOVE_T),   # knob u 640
    ('Lower Panel Assy v1:1/Mix Lever v1:1', 'Mixture (push-pull, pushed in)', 'Lower panel (right)', 73.0, 12.0, -48.0, MOVE_M),     # knob u 690
    ('Lower Panel Assy v1:1/throt temp v1:1', 'Condition (throttle copy, pushed in)', 'Lower panel (right)', 174.0, 12.0, -48.0, MOVE_T),  # knob u 740
]
LOWER = ('LHS Fuse panel', 'FSP3', 'Throttle', 'Mixture', 'Condition', 'Trim')
REMOVABLE = ('dUAL kNOB',)     # knobs that come off for travel (GMA volume knob)


def place():
    app = adsk.core.Application.get()
    d = adsk.fusion.Design.cast(app.activeProduct)
    root = d.rootComponent
    tbm = adsk.fusion.TemporaryBRepManager.get()
    hosts = {o.component.name: o for o in root.occurrences}
    for o in list(hosts.values()):
        for ch in o.childOccurrences:
            if ch.component.name.startswith('Lower panel'):
                hosts[ch.component.name] = ch
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
    lookup = {}
    for src in top.childOccurrences:
        for ch in src.childOccurrences:
            lookup[src.name + '/' + ch.name] = (ch, src)
    for key, wname, host, du, dy, dz, moves in SPLIT:
        src, parent = lookup[key]
        wo = hosts[host].component.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        wo.component.name = wname
        wo.isGroundToParent = True
        for ch in src.childOccurrences:
            extra = 0.0
            hit = [k for k in moves if ch.name.startswith(k)]
            if hit:
                extra = moves[max(hit, key=len)]
                if extra is None:
                    continue
            W = ch.transform2.copy()          # proxy transform2 is already the full (world) transform
            W.transformBy(R)
            W.transformBy(Tours)
            Tm = adsk.core.Matrix3D.create(); Tm.translation = adsk.core.Vector3D.create(du / 10.0, -(dy + extra) / 10.0, dz / 10.0)
            W.transformBy(Tm)
            o = wo.component.occurrences.addExistingComponent(ch.component, W)
            o.isGroundToParent = True
        placed.append((host, wo))
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
