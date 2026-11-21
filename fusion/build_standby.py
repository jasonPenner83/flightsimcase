# SB-1 standby instruments (ASI 2-1/4, attitude 3-1/8, altimeter 2-1/4) and SB-2 dimming block (4 knobs),
# side by side in the center panel's bottom section (rails 10-110). Same shell construction as the PFD bezel
# (3 mm flanges on the rails, 2.5 mm face, open back) but 20 mm deep so the round gauge LCDs sit inside.
# Units mm. Frame: X right, Y toward pilot, Z up. Fusion Z-up: (x, -y, z) / 10.
import adsk.core, adsk.fusion, json, os

ART_JSON = r'D:/Admin/Documents/Projects/FlightSimCase/labels/panels.json'
D = 20.0; FACE = 2.5; FL = 3.0; WALL = 2.5
POT_HOLE = 7.5


def build():
    app = adsk.core.Application.get()
    d = adsk.fusion.Design.cast(app.activeProduct)
    root = d.rootComponent
    host = [o for o in root.occurrences if o.component.name == 'Center panel'][0].component
    tbm = adsk.fusion.TemporaryBRepManager.get()
    from importlib import util as _u
    spec = _u.spec_from_file_location('bc', r'D:/Admin/Documents/Projects/FlightSimCase/fusion/build_case.py')
    bc = _u.module_from_spec(spec); spec.loader.exec_module(bc)
    PP = bc.P
    z0, z1 = PP['rails_C'][0], PP['rails_C'][1]
    zl, zh = z0 + 0.4, z1 - 0.4
    zc = (z0 + z1) / 2
    cxa = -PP['W'] / 2 + PP['T'] + 2

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

    def sub(a, b):
        tbm.booleanOperation(a, b, adsk.fusion.BooleanTypes.DifferenceBooleanType)

    art = json.load(open(ART_JSON)) if os.path.exists(ART_JSON) else []
    art = [a for a in art if not a['name'].startswith(('SB-1', 'SB-2'))]

    def shell(name, xa, xb, holes, labels, refs):
        b = box(xa, xb, 0, D, zl, zh)
        sub(b, box(xa + WALL, xb - WALL, FL, D - FACE, zl + WALL, zh - WALL))
        sub(b, box(xa + WALL, xb - WALL, -1, FL + 0.01, z0 + 10, z1 - 10))
        for h in holes:
            sub(b, ycyl(h[1], h[2], -1, D + 1, h[3] / 2))
        n = max(2, int((xb - xa) // 110) + 1)
        notches = [(xa + 12 + i * (xb - xa - 24) / (n - 1), ez) for i in range(n) for ez in (zl, zh)]
        for nx, ez in notches:
            sub(b, ycyl(nx, ez, -1, D + 1, 3.2))
        occ = host.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        occ.isGroundToParent = True      # move with the wing when it folds
        comp = occ.component
        comp.name = name
        bf = comp.features.baseFeatures.add()
        bf.startEdit()
        nb = comp.bRepBodies.add(b, bf); nb.name = 'PRINT %s bezel' % name.split()[0]
        for nm, rb in refs:
            r = comp.bRepBodies.add(rb, bf); r.name = nm
        bf.finishEdit()
        for r in comp.bRepBodies:
            if r.name.startswith('REF'):
                r.isLightBulbOn = False
        art.append(dict(name=name, host='Center panel', x0=xa, x1=xb, z0=zl, z1=zh, holes=[list(h) for h in holes],
                        labels=[list(l) for l in labels], notches=notches, notch_r=3.2, label_h=2.3))

    # SB-1: ASI | ATTITUDE | ALT  (212 mm wide)
    xa = cxa; xb = xa + 212
    g = [('AIRSPEED', xa + 33, 58.0, 2.1), ('ATTITUDE', xa + 106, 80.0, 2.8), ('ALTIMETER', xa + 179, 58.0, 2.1)]
    holes = [('circ', x, zc, dia) for _, x, dia, _ in g]
    refs = []
    for nm, x, dia, inch in g:
        mod = dia + 3
        refs.append(('REF round LCD %.1fin + ESP32-S3 (%s)' % (inch, nm.lower()), ycyl(x, zc, FL + 1, D - FACE, mod / 2)))
        refs.append(('REF gauge bezel ring', ycyl(x, zc, D, D + 3, dia / 2 + 1.5)))
    shell('SB-1 Standby instruments', xa, xb, holes, [], refs)

    # SB-2: dimming block, 2 x 2 knobs (58 mm wide)
    xa2 = xb + 1; xb2 = xa2 + 58
    kx = (xa2 + 16, xa2 + 42); kz = (zc + 18, zc - 22)
    names = [('SW/CN PNL', kx[0], kz[0]), ('STBY IND', kx[1], kz[0]), ('PEDESTAL', kx[0], kz[1]), ('AVIONICS', kx[1], kz[1])]
    holes2 = [('circ', x, z, POT_HOLE) for _, x, z in names]
    labels2 = [(nm, x, z + 14) for nm, x, z in names] + [('DIMMING', (xa2 + xb2) / 2, zh - 6)]
    refs2 = []
    for nm, x, z in names:
        refs2.append(('REF pot 16 mm (%s)' % nm, box(x - 8, x + 8, FL + 2, D - FACE, z - 8, z + 8)))
        refs2.append(('REF knob', ycyl(x, z, D, D + 16, 7)))
    refs2.append(('REF Arduino Pro Micro (4 dimmers, MobiFlight)', box(xa2 + 5, xa2 + 53, -20 - 10, -20 - 1, zc - 9, zc + 9)))
    shell('SB-2 Dimming panel', xa2, xb2, holes2, labels2, refs2)

    json.dump(art, open(ART_JSON, 'w'), indent=1)
    print('standby + dimming built: SB-1 x %.0f..%.0f, SB-2 x %.0f..%.0f' % (xa, xb, xa2, xb2))


def run(_context: str):
    build()
