# C172 G1000 panel layout for the bifold case: every faceplate sized for its exact spot (not modular).
# Left half : SC-1 switch column (STBY BATT / MASTER / AVIONICS) | PFD-1      (displays section, rails 110-310)
#             LT-1 mags + lights | YK-1 pilot yoke | CB-1 circuit breakers   (lower section, rails 10-110)
# Right half: AU-1 audio | MFD-1                                             (displays section)
#             SB-1 standby gauges | SB-2 dimming | CP-1 copilot yoke         (lower section)
# Flat plates are 3 mm (panel plane), shells (bezels/standby) stand proud. Labels -> labels/panels.json.
import adsk.core, adsk.fusion, json, os
from importlib import util as _u

BASE = r'D:/Admin/Documents/Projects/FlightSimCase/fusion/'
ART_JSON = r'D:/Admin/Documents/Projects/FlightSimCase/labels/panels.json'
ROCKER = (15.0, 21.0); POCKET = (19.0, 25.0, 1.6)
KEY_HOLE = 10.0; POT_HOLE = 7.5; YOKE_HOLE = 40.0; CB_HOLE = 9.5


def _load(n):
    spec = _u.spec_from_file_location(n, BASE + n + '.py')
    m = _u.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def build():
    app = adsk.core.Application.get()
    d = adsk.fusion.Design.cast(app.activeProduct)
    root = d.rootComponent
    hosts = {o.component.name: o.component for o in root.occurrences}
    tbm = adsk.fusion.TemporaryBRepManager.get()
    bc = _load('build_case_bifold')
    PP = bc.P; G = bc.geometry(); T = PP['T']
    rails = PP['rails']
    art = []

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

    def notches(xa, xb, zl, zh):
        n = max(2, int((xb - xa) // 110) + 1)
        return [(xa + 12 + i * (xb - xa - 24) / (n - 1), ez) for i in range(n) for ez in (zl, zh)]

    def add(host, name, bodies):
        occ = hosts[host].occurrences.addNewComponent(adsk.core.Matrix3D.create())
        occ.isGroundToParent = True
        comp = occ.component
        comp.name = name
        bf = comp.features.baseFeatures.add()
        bf.startEdit()
        for nm, b in bodies:
            nb = comp.bRepBodies.add(b, bf)
            nb.name = nm
        bf.finishEdit()
        for b in comp.bRepBodies:
            if b.name.startswith('REF'):
                b.opacity = 0.6
                b.isLightBulbOn = False
        return occ

    def flat(host, name, section, xa, xb, holes, labels, refs, label_h=2.5):
        z0, z1 = section; zl, zh = z0 + 0.4, z1 - 0.4
        b = box(xa, xb, 0, 3, zl, zh)
        for h in holes:
            if h[0] == 'rect':
                _, cx, cz, w, hh = h
                sub(b, box(cx - w / 2, cx + w / 2, -1, 4, cz - hh / 2, cz + hh / 2))
                if (w, hh) == ROCKER:
                    sub(b, box(cx - POCKET[0] / 2, cx + POCKET[0] / 2, -1, POCKET[2], cz - POCKET[1] / 2, cz + POCKET[1] / 2))
            else:
                sub(b, ycyl(h[1], h[2], -1, 4, h[3] / 2))
        nts = notches(xa, xb, zl, zh)
        for nx, ez in nts:
            sub(b, ycyl(nx, ez, -1, 4, 3.2))
        add(host, name, [('PRINT %s faceplate' % name.split()[0], b)] + refs)
        art.append(dict(name=name, host=host, x0=xa, x1=xb, z0=zl, z1=zh, holes=[list(h) for h in holes],
                        labels=[list(l) for l in labels], notches=nts, notch_r=3.2, label_h=label_h))

    def shell(host, name, section, xa, xb, depth, holes, labels, refs):
        z0, z1 = section; zl, zh = z0 + 0.4, z1 - 0.4
        b = box(xa, xb, 0, depth, zl, zh)
        sub(b, box(xa + 2.5, xb - 2.5, 3, depth - 2.5, zl + 2.5, zh - 2.5))
        sub(b, box(xa + 2.5, xb - 2.5, -1, 3.01, z0 + 10, z1 - 10))
        for h in holes:
            sub(b, ycyl(h[1], h[2], -1, depth + 1, h[3] / 2))
        nts = notches(xa, xb, zl, zh)
        for nx, ez in nts:
            sub(b, ycyl(nx, ez, -1, depth + 1, 3.2))
        add(host, name, [('PRINT %s bezel' % name.split()[0], b)] + refs)
        art.append(dict(name=name, host=host, x0=xa, x1=xb, z0=zl, z1=zh, holes=[list(h) for h in holes],
                        labels=[list(l) for l in labels], notches=nts, notch_r=3.2, label_h=2.3))

    def rocker(cx, cz):
        return [('REF rocker body', box(cx - 7, cx + 7, -22, 0, cz - 10, cz + 10)),
                ('REF rocker cap', box(cx - 7.5, cx + 7.5, 3, 11, cz - 10.5, cz + 10.5))]

    def pico(cx, cz, label='REF Raspberry Pi Pico'):
        return (label, box(cx - 25.5, cx + 25.5, -28.6, -27, cz - 10.5, cz + 10.5))

    low = (rails[0], rails[1]); disp = (rails[1], rails[2])
    xl0, xl1 = G['left']; xr0, xr1 = G['right']
    Li0, Li1 = xl0 + T + 2, xl1 - T - 2        # left half usable x
    Ri0, Ri1 = xr0 + T + 2, xr1 - T - 2        # right half usable x
    pfd_xa = Li1 - 306.0
    yx = (pfd_xa + Li1) / 2                     # pilot yoke on the PFD centerline
    yz = 100.0 - PP['foot']
    zlow = (low[0] + low[1]) / 2

    # ---------------- LEFT HALF
    # SC-1 switch column beside the PFD: STBY BATT, MASTER ALT|BAT (red), AVIONICS BUS1|BUS2 (red)
    sa, sb = Li0, pfd_xa - 1
    cx = (sa + sb) / 2
    holes = [('rect', cx, 278, *ROCKER), ('rect', cx - 8.5, 222, *ROCKER), ('rect', cx + 8.5, 222, *ROCKER),
             ('rect', cx - 8.5, 166, *ROCKER), ('rect', cx + 8.5, 166, *ROCKER)]
    labels = [('STBY BATT', cx, 296), ('MASTER', cx, 240), ('ALT', cx - 8.5, 204), ('BAT', cx + 8.5, 204),
              ('AVIONICS', cx, 184), ('BUS1', cx - 8.5, 148), ('BUS2', cx + 8.5, 148)]
    refs = []
    for h in holes:
        refs += rocker(h[1], h[2])
    refs.append(('REF Raspberry Pi Pico (SC-1 + LT-1)', box(cx - 10.5, cx + 10.5, -28.6, -27, 190, 241)))
    flat('Left half', 'SC-1 Switch column', disp, sa, sb, holes, labels, refs)

    _load('build_pfd').build('Left half', 'PFD-1 GDU 1040 bezel', pfd_xa, Li1, tuple(disp))

    # LT-1 mags key + lights row, left of the yoke
    la, lb = Li0, yx - 26
    X = lambda dx: la + dx
    names = ['FUEL PUMP', 'BCN', 'LAND', 'TAXI', 'NAV', 'STROBE', 'PITOT HT']
    holes = [('circ', X(18), zlow, KEY_HOLE)]
    labels = [('MAGNETOS', X(18), zlow + 17), ('OFF R L BOTH START', X(18), zlow - 19), ('LIGHTS', X(99), zlow + 17)]
    refs = [('REF key switch body (1P12T, stop at 5)', box(X(18) - 13, X(18) + 13, -30, 0, zlow - 13, zlow + 13)),
            ('REF printed key knob', box(X(18) - 4, X(18) + 4, 3, 28, zlow - 13, zlow + 13))]
    for i, nm in enumerate(names):
        rx = X(45 + i * 18)
        holes.append(('rect', rx, zlow, *ROCKER))
        refs += rocker(rx, zlow)
        if nm == 'FUEL PUMP':
            labels += [('FUEL', rx, zlow + 17), ('PUMP', rx, zlow - 17)]
        elif nm == 'PITOT HT':
            labels += [('PITOT', rx, zlow + 17), ('HEAT', rx, zlow - 17)]
        else:
            labels.append((nm, rx, zlow - 17))
    labels = [l for l in labels if l[0] != 'OFF R L BOTH START']   # positions printed around the key on the sticker later
    flat('Left half', 'LT-1 Mags and lights', low, la, lb, holes, labels, refs)

    # YK-1 pilot yoke
    flat('Left half', 'YK-1 Pilot yoke plate', low, yx - 25, yx + 25, [('circ', yx, yz, YOKE_HOLE)], [], [])

    # CB-1 circuit breakers (2 x 6, 3/8 in bushing breakers or dummy caps)
    ca, cb = yx + 26, Li1
    holes = []; labels = [('ESSENTIAL BUS', (ca + cb) / 2, zlow + 36), ('AVIONICS BUS', (ca + cb) / 2, zlow - 2)]
    refs = []
    for row, zz in enumerate((zlow + 22, zlow - 16)):
        for i in range(6):
            bx = ca + 16 + i * 19
            holes.append(('circ', bx, zz, CB_HOLE))
            refs.append(('REF breaker body', box(bx - 6, bx + 6, -25, 0, zz - 8, zz + 8)))
            refs.append(('REF breaker cap', ycyl(bx, zz, 3, 15, 5.5)))
    flat('Left half', 'CB-1 Circuit breakers', low, ca, cb, holes, labels, refs)

    # ---------------- RIGHT HALF
    # AU-1 audio panel (63 wide) left of the MFD
    aa, ab = Ri0, Ri0 + 63
    acx = (aa + ab) / 2
    holes = []
    for rr in range(11):
        zz = disp[1] - 22 - rr * 13
        for dx in (-14, 14):
            holes.append(('rect', acx + dx, zz, 22.0, 8.0))
    holes.append(('circ', acx, disp[0] + 22, 10.0))
    refs = [('REF dual encoder (audio volume)', box(acx - 6.5, acx + 6.5, -15, 0, disp[0] + 15.5, disp[0] + 28.5)),
            ('REF Raspberry Pi Pico (audio keys)', box(acx - 10.5, acx + 10.5, -28.6, -27, disp[0] + 40, disp[0] + 91))]
    flat('Right half', 'AU-1 Audio panel', disp, aa, ab, holes, [('VOL', acx, disp[0] + 36)], refs, label_h=2.3)

    _load('build_pfd').build('Right half', 'MFD-1 GDU 1040 bezel', ab + 1, Ri1, tuple(disp))

    # SB-1 standby gauges (shell, 20 deep) | SB-2 dimming | CP-1 copilot yoke
    s1a, s1b = Ri0, Ri0 + 212
    g = [('AIRSPEED', s1a + 33, 58.0, 2.1), ('ATTITUDE', s1a + 106, 80.0, 2.8), ('ALTIMETER', s1a + 179, 58.0, 2.1)]
    holes = [('circ', x, zlow, dia) for _, x, dia, _ in g]
    refs = []
    for nm, x, dia, inch in g:
        refs.append(('REF round LCD %.1fin + ESP32-S3 (%s)' % (inch, nm.lower()), ycyl(x, zlow, 4, 17.5, (dia + 3) / 2)))
        refs.append(('REF gauge bezel ring', ycyl(x, zlow, 20, 23, dia / 2 + 1.5)))
    shell('Right half', 'SB-1 Standby instruments', low, s1a, s1b, 20.0, holes, [], refs)

    s2a, s2b = s1b + 1, s1b + 59
    kx = (s2a + 16, s2a + 42); kz = (zlow + 18, zlow - 22)
    dn = [('SW/CN PNL', kx[0], kz[0]), ('STBY IND', kx[1], kz[0]), ('PEDESTAL', kx[0], kz[1]), ('AVIONICS', kx[1], kz[1])]
    holes = [('circ', x, z, POT_HOLE) for _, x, z in dn]
    labels = [(nm, x, z + 14) for nm, x, z in dn] + [('DIMMING', (s2a + s2b) / 2, low[1] - 6.4)]
    refs = []
    for nm, x, z in dn:
        refs.append(('REF pot 16 mm (%s)' % nm, box(x - 8, x + 8, 5, 17.5, z - 8, z + 8)))
        refs.append(('REF knob', ycyl(x, z, 20, 36, 7)))
    refs.append(('REF Arduino Pro Micro (dimmers)', box(s2a + 5, s2a + 53, -30, -21, zlow - 9, zlow + 9)))
    shell('Right half', 'SB-2 Dimming panel', low, s2a, s2b, 20.0, holes, labels, refs)

    cop = 2 * PP['thr_x'] - yx
    flat('Right half', 'CP-1 Copilot yoke blank', low, s2b + 1, Ri1, [('circ', cop, yz, YOKE_HOLE)], [], [])

    os.makedirs(os.path.dirname(ART_JSON), exist_ok=True)
    old = json.load(open(ART_JSON)) if os.path.exists(ART_JSON) else []
    keep = [a for a in old if a['name'].split()[0][:3] in ('PFD', 'MFD')]   # written by build_pfd just now
    json.dump(keep + art, open(ART_JSON, 'w'), indent=1)
    print('C172 panels built; pilot yoke x %.1f, copilot yoke x %.1f, PFD x %.1f..%.1f' % (yx, cop, pfd_xa, Li1))


def run(_context: str):
    build()
