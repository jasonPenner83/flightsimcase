# Printable router jigs for the panel cut-outs (flush-trim / pattern bit with a top bearing riding on the jig).
# Each jig = an 8 mm plate whose opening is the exact cut-out, taken straight from the panel body in the model, with
# a border round it, centre-line notches on its edges for lining up with the traced lines, and the nearby screw holes
# as small drill-mark holes. Jigs wider than the 256 mm bed split in two with a half-lap joint and two M3 bolts.
# Writes STLs to fabrication/jigs and deletes its temporary component again. Units mm (u = x + 460).
import os
import adsk.core, adsk.fusion

OUT = r'D:/Admin/Documents/Projects/FlightSimCase/fabrication/jigs/'
T = 8.0          # jig thickness
BED = 250.0      # usable bed (256 minus margin)

# name, host, panel body prefix, feature region (u0, u1, z0, z1), border[, keep-solid boxes (u0, u1, z0, z1) where a
# neighbouring cut-out falls inside the region and must NOT open up in this jig]
JIGS = [
    ('J01_PFD_opening', 'Left half', 'PANEL 737', (134.0, 430.0, 131.0, 326.0), 22.0, [(100.0, 141.3, 100.0, 245.0)]),
    ('J02_switch_panel', 'Left half', 'PANEL 737', (19.0, 223.0, 28.0, 245.5), 17.0, [(141.3, 260.0, 137.5, 260.0)]),
    ('J03_yoke_hole_and_slot', 'Left half', 'PANEL 737', (260.0, 308.0, 0.0, 57.0), 20.0),   # hole + slot to the bottom edge
    ('J05_GMA1347_opening', 'Spacer', 'PANEL spacer', (448.0, 504.0, 125.0, 332.0), 20.0),
    ('J06_MFD_opening', 'Right half', 'PANEL 737', (530.0, 828.0, 131.0, 326.0), 22.0),
    ('J07_standby_ASI', 'Right half', 'PANEL 737', (523.0, 611.0, 28.0, 116.0), 20.0),
    ('J08_standby_attitude', 'Right half', 'PANEL 737', (613.0, 699.0, 28.0, 116.0), 20.0),
    ('J09_standby_altimeter', 'Right half', 'PANEL 737', (699.0, 791.0, 21.0, 116.0), 20.0),
    ('J10_ELT', 'Right half', 'PANEL 737', (834.0, 870.0, 247.0, 293.0), 20.0),
    ('J11_flaps_lever', 'Right half', 'PANEL 737', (829.0, 901.5, 25.0, 111.0), 20.0),   # flaps moved up to the main panel
    ('J12_left_fuse_panel', 'Lower panel (left)', 'PANEL lower', (19.5, 278.0, -155.5, -46.0), 20.0),
    ('J13_fuel_selector', 'Lower panel (left)', 'PANEL lower', (298.0, 412.0, -158.0, -40.0), 20.0),
    ('J14_throttle_mixture_condition', 'Lower panel (right)', 'PANEL lower', (618.0, 762.0, -128.0, -89.0), 20.0),
    ('J15_trim_wheel', 'Lower panel (right)', 'PANEL lower', (531.0, 613.0, -220.0, -40.0), 18.0),   # trim wheel case, left of the throttle
]


def X(u):
    return u - 460.0


def build_jigs():
    app = adsk.core.Application.get()
    d = adsk.fusion.Design.cast(app.activeProduct)
    root = d.rootComponent
    tbm = adsk.fusion.TemporaryBRepManager.get()
    SUB = adsk.fusion.BooleanTypes.DifferenceBooleanType
    INT = adsk.fusion.BooleanTypes.IntersectionBooleanType

    def F(x, y, z):
        return adsk.core.Point3D.create(x / 10.0, -y / 10.0, z / 10.0)

    def box(x0, x1, y0, y1, a, b):
        p = F(x0, y0, a); q = F(x1, y1, b)
        lo = [min(p.x, q.x), min(p.y, q.y), min(p.z, q.z)]; hi = [max(p.x, q.x), max(p.y, q.y), max(p.z, q.z)]
        c = adsk.core.Point3D.create((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2)
        return tbm.createBox(adsk.core.OrientedBoundingBox3D.create(c, adsk.core.Vector3D.create(1, 0, 0), adsk.core.Vector3D.create(0, 1, 0),
                                                                   hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]))

    def ycyl(x, z, y0, y1, r):
        return tbm.createCylinderOrCone(F(x, y0, z), r / 10.0, F(x, y1, z), r / 10.0)

    hosts = {o.component.name: o.component for o in root.occurrences}
    for o in root.occurrences:
        for ch in o.childOccurrences:
            if ch.component.name.startswith('Lower panel'):
                hosts[ch.component.name] = ch.component
    os.makedirs(OUT, exist_ok=True)
    made = []
    for spec in JIGS:
        name, host, pre, (u0, u1, z0, z1), b = spec[:5]
        keep = spec[5] if len(spec) > 5 else []
        panel = [bd for bd in hosts[host].bRepBodies if bd.name.startswith(pre)][0]
        # the cut-out = feature region minus panel material, taken through the 9 mm panel slab
        hole = box(X(u0), X(u1), -9.5, 0.5, z0, z1)
        tbm.booleanOperation(hole, tbm.copy(panel), SUB)
        for (k0, k1, k2, k3) in keep:
            tbm.booleanOperation(hole, box(X(k0), X(k1), -10, 1, k2, k3), SUB)
        jig = box(X(u0 - b), X(u1 + b), -9.0, -1.0, z0 - b, z1 + b)       # 8 mm plate inside the panel slab
        tbm.booleanOperation(jig, hole, SUB)
        # centre-line notches (2 mm wide, 4 mm deep) on all four edges
        uc, zc = (u0 + u1) / 2, (z0 + z1) / 2
        for nb in (box(X(uc) - 1, X(uc) + 1, -10, 0, z1 + b - 4, z1 + b + 1), box(X(uc) - 1, X(uc) + 1, -10, 0, z0 - b - 1, z0 - b + 4),
                   box(X(u0 - b) - 1, X(u0 - b) + 4, -10, 0, zc - 1, zc + 1), box(X(u1 + b) - 4, X(u1 + b) + 1, -10, 0, zc - 1, zc + 1)):
            tbm.booleanOperation(jig, nb, SUB)
        W = (u1 - u0) + 2 * b; H = (z1 - z0) + 2 * b
        pieces = []
        if W > BED:
            m = uc; lap = 15.0
            A = tbm.copy(jig); tbm.booleanOperation(A, box(X(u0 - b) - 1, X(m + lap), -10, 0, z0 - b - 1, z1 + b + 1), INT)
            tbm.booleanOperation(A, box(X(m - lap), X(m + lap) + 1, -9.5, -5.0, z0 - b - 1, z1 + b + 1), SUB)
            B = tbm.copy(jig); tbm.booleanOperation(B, box(X(m - lap), X(u1 + b) + 1, -10, 0, z0 - b - 1, z1 + b + 1), INT)
            tbm.booleanOperation(B, box(X(m - lap) - 1, X(m + lap), -5.0, -0.5, z0 - b - 1, z1 + b + 1), SUB)
            for pc in (A, B):
                for zz in (z0 - b / 2, z1 + b / 2):
                    tbm.booleanOperation(pc, ycyl(X(m), zz, -10, 0, 1.7), SUB)
            pieces = [(name + '_A', A), (name + '_B', B)]
        else:
            pieces = [(name, jig)]
        for nm, pc in pieces:
            bb = pc.boundingBox
            made.append((nm, pc, round((bb.maxPoint.x - bb.minPoint.x) * 10, 1), round((bb.maxPoint.z - bb.minPoint.z) * 10, 1)))
    # temporary component to export from, removed afterwards
    occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    comp = occ.component; comp.name = 'ROUTER JIGS (temp export)'
    bf = comp.features.baseFeatures.add(); bf.startEdit()
    bodies = []
    for nm, pc, w, h in made:
        nb = comp.bRepBodies.add(pc, bf); nb.name = nm
        bodies.append((nb, w, h))
    bf.finishEdit()
    em = d.exportManager
    report = []
    for nb, w, h in [(comp.bRepBodies.itemByName(nm), w, h) for nm, pc, w, h in made]:
        opt = em.createSTLExportOptions(nb, OUT + nb.name + '.stl')
        opt.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
        em.execute(opt)
        report.append('%s %.0f x %.0f x %.0f %s' % (nb.name, w, h, T, 'OK' if max(w, h) <= 256 else 'TOO BIG'))
    occ.deleteMe()
    open(OUT + 'jig_list.txt', 'w').write('\n'.join(report) + '\n')
    print('\n'.join(report))


def run(_context: str):
    build_jigs()
