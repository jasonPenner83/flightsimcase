# PFD-1: GDU 1040 style PFD bezel for the center panel (rails 110-310).
# Shell bezel 15 mm deep: 3 mm mounting flanges on the rails, 2.5 mm face, open back.
# The 10.4 in 4:3 LCD module and the button/encoder PCBs sit INSIDE the bezel, in front of the rail plane;
# the LCD driver board and the controller sit behind the rails in the 30 mm rear zone.
# Printed in 3 pieces (left knob column, display frame, right knob column) to fit the 256 mm bed.
# Units mm. Frame: X right, Y toward pilot, Z up. Fusion Z-up: (x, -y, z) / 10.
import adsk.core, adsk.fusion, json, os

ART_JSON = r'D:/Admin/Documents/Projects/FlightSimCase/labels/panels.json'

D = 15.0            # bezel depth (rail face to bezel face)
FACE = 2.5          # face thickness
FL = 3.0            # mounting flange thickness (panel-plane standard)
WALL = 2.5
LCD = (228.6, 175.8, 7.6)      # 10.4 in 1024x768 LED-backlit module outline
ACTIVE = (211.2, 158.4)        # active area = GDU 1040 display window
EC11 = 7.5          # single encoder bushing hole
DUAL = 10.0         # dual concentric encoder bushing hole
BTN = (11.0, 6.0)   # button cap hole
SOFT = (11.0, 5.0)  # softkey cap hole


def layout(xa, xb, z0, z1):
    """Return holes, labels, ref parts for a bezel spanning plate x xa..xb, rails z0..z1."""
    xm = (xa + xb) / 2
    zl = z0 + 0.4; zh = z1 - 0.4
    lcd_z0 = zl + 16.6                     # room under the LCD for the softkey PCB
    lcd_zc = lcd_z0 + LCD[1] / 2
    win = (xm - ACTIVE[0] / 2, xm + ACTIVE[0] / 2, lcd_zc - ACTIVE[1] / 2, lcd_zc + ACTIVE[1] / 2)
    L = xm - 132; R = xm + 132
    holes = [('rect', xm, lcd_zc, ACTIVE[0], ACTIVE[1])]
    labels = []
    knobs = []   # (x, z, hole, knob dia, name)
    # left column
    knobs += [(L, zh - 20, EC11, 10, 'NAV VOL'), (L, zh - 55, DUAL, 22, 'NAV'), (L, zh - 105, EC11, 18, 'HDG'),
              (L, zl + 25, DUAL, 22, 'ALT')]
    # right column
    knobs += [(R, zh - 20, EC11, 10, 'COM VOL'), (R, zh - 55, DUAL, 22, 'COM'), (R, zh - 95, DUAL, 22, 'CRS / BARO'),
              (R, zh - 128, EC11, 16, 'RANGE'), (R, zl + 17, DUAL, 22, 'FMS')]
    for x, z, h, kd, nm in knobs:
        holes.append(('circ', x, z, h))
        if nm == 'FMS':
            continue                                   # no room: button grid sits right above it
        below = nm in ('NAV', 'COM')                   # keep clear of the frequency flip keys
        labels.append((nm, x, z - kd / 2 - 4 if below else z + kd / 2 + 4))
    btns = [(L, zh - 36, 'NAV <->'), (R, zh - 36, 'COM <->')]
    gx = (R - 8, R + 8)
    names = [('D->', 'MENU'), ('FPL', 'PROC'), ('CLR', 'ENT')]
    for i, (a, b) in enumerate(names):
        zb = zl + 58.6 - i * 13
        btns += [(gx[0], zb, a), (gx[1], zb, b)]
    for x, z, nm in btns:
        holes.append(('rect', x, z, BTN[0], BTN[1]))   # key legends go on the caps (cap stickers), not the face
    soft = []
    for i in range(12):
        x = xm - 96.8 + i * 17.6
        soft.append(x)
        holes.append(('rect', x, zl + 9.1, SOFT[0], SOFT[1]))
    return dict(win=win, lcd_z0=lcd_z0, lcd_zc=lcd_zc, holes=holes, labels=labels, knobs=knobs, btns=btns, soft=soft,
                zl=zl, zh=zh, xm=xm, L=L, R=R)


def build(host_name='Center panel', name='PFD-1 GDU 1040 bezel', xa=-153.0, xb=153.0, rails=(110.0, 310.0)):
    app = adsk.core.Application.get()
    d = adsk.fusion.Design.cast(app.activeProduct)
    root = d.rootComponent
    host = [o for o in root.occurrences if o.component.name == host_name][0].component
    tbm = adsk.fusion.TemporaryBRepManager.get()

    def F(x, y, z):
        return adsk.core.Point3D.create(x / 10.0, -y / 10.0, z / 10.0)

    def box(x0, x1, y0, y1, z0, z1):
        a = F(x0, y0, z0); b = F(x1, y1, z1)
        lo = [min(a.x, b.x), min(a.y, b.y), min(a.z, b.z)]; hi = [max(a.x, b.x), max(a.y, b.y), max(a.z, b.z)]
        c = adsk.core.Point3D.create((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2)
        return tbm.createBox(adsk.core.OrientedBoundingBox3D.create(c, adsk.core.Vector3D.create(1, 0, 0), adsk.core.Vector3D.create(0, 1, 0),
                                                                   hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]))

    def ycyl(x, z, y0, y1, r):
        return tbm.createCylinderOrCone(F(x, y0, z), r / 10.0, F(x, y1, z), r / 10.0)

    def sub(a, b):
        tbm.booleanOperation(a, b, adsk.fusion.BooleanTypes.DifferenceBooleanType)

    z0, z1 = rails
    Ly = layout(xa, xb, z0, z1)
    zl, zh = Ly['zl'], Ly['zh']
    splits = [xa, Ly['xm'] - 116.0, Ly['xm'] + 116.0, xb]
    piece_names = ['left knob column', 'display frame', 'right knob column']
    bodies = []
    for i in range(3):
        px0, px1 = splits[i], splits[i + 1]
        b = box(px0, px1, 0, D, zl, zh)
        cx0 = max(px0, xa + WALL) - (0.01 if px0 > xa else 0)
        cx1 = min(px1, xb - WALL) + (0.01 if px1 < xb else 0)
        sub(b, box(cx0, cx1, FL, D - FACE, zl + WALL, zh - WALL))        # cavity in front of the flanges
        sub(b, box(cx0, cx1, -1, FL + 0.01, z0 + 10, z1 - 10))           # open back between the rails
        for h in Ly['holes']:
            if h[0] == 'rect':
                _, cx, cz, w, hh = h
                sub(b, box(cx - w / 2, cx + w / 2, -1, D + 1, cz - hh / 2, cz + hh / 2))
            else:
                _, cx, cz, dia = h
                sub(b, ycyl(cx, cz, -1, D + 1, dia / 2))
        bodies.append(('PRINT %s bezel %s' % (name.split()[0], piece_names[i]), b))
    # edge clamp notches on the flanges
    notch_x = [xa + 12, Ly['xm'] - 100, Ly['xm'], Ly['xm'] + 100, xb - 12]
    notches = [(nx, ez) for nx in notch_x for ez in (zl, zh)]
    for k, (nm, b) in enumerate(bodies):
        for nx, ez in notches:
            sub(b, ycyl(nx, ez, -1, D + 1, 3.2))

    # ---- reference parts (hidden by default)
    xm = Ly['xm']
    lcd_y0 = D - FACE - LCD[2]
    refs = [('REF LCD 10.4in 1024x768 module (228.6x175.8x7.6)', box(xm - LCD[0] / 2, xm + LCD[0] / 2, lcd_y0, D - FACE, Ly['lcd_z0'], Ly['lcd_z0'] + LCD[1])),
            ('REF LCD driver board HDMI (approx 100x65x15)', box(xm - 50, xm + 50, -20 - 16, -20 - 1, Ly['lcd_zc'] - 32, Ly['lcd_zc'] + 33)),
            ('REF Arduino Mega 2560 Pro Mini (MobiFlight)', box(xm + 60, xm + 115, -20 - 12, -20 - 1, Ly['lcd_zc'] - 19, Ly['lcd_zc'] + 19)),
            ('REF PCB softkeys', box(xm - 114, xm + 114, FL, FL + 1.6, zl + WALL + 0.5, Ly['lcd_z0'] - 0.5)),
            ('REF PCB left column', box(xa + WALL + 0.5, xm - 116.5, FL, FL + 1.6, zl + WALL + 0.5, zh - WALL - 0.5)),
            ('REF PCB right column', box(xm + 116.5, xb - WALL - 0.5, FL, FL + 1.6, zl + WALL + 0.5, zh - WALL - 0.5))]
    for x, z, h, kd, nm in Ly['knobs']:
        dual = h == DUAL
        refs.append(('REF encoder body %s' % ('dual' if dual else 'EC11'), box(x - 6.5, x + 6.5, (D - FACE - 15) if dual else FL + 1.6, D - FACE, z - 6.5, z + 6.5)))
        refs.append(('REF knob %s' % nm, ycyl(x, z, D, D + 18, kd / 2)))
    for x, z, nm in Ly['btns']:
        refs.append(('REF button cap', box(x - 5, x + 5, FL + 1.6, D + 2, z - 2.5, z + 2.5)))
    for x in Ly['soft']:
        refs.append(('REF softkey cap', box(x - 5, x + 5, FL + 1.6, D + 2, zl + 9.1 - 2, zl + 9.1 + 2)))

    occ = host.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    occ.isGroundToParent = True      # move with the wing when it folds
    comp = occ.component
    comp.name = name
    bf = comp.features.baseFeatures.add()
    bf.startEdit()
    for nm, b in bodies + refs:
        nb = comp.bRepBodies.add(b, bf)
        nb.name = nm
    bf.finishEdit()
    for b in comp.bRepBodies:
        if b.name.startswith('REF'):
            b.isLightBulbOn = False

    # ---- label artwork: one entry per printed piece (bezel face is the sticker surface)
    art = json.load(open(ART_JSON)) if os.path.exists(ART_JSON) else []
    tag = name.split()[0]
    art = [a for a in art if not a['name'].startswith(tag)]
    for i in range(3):
        px0, px1 = splits[i], splits[i + 1]
        inside = lambda x, w=0: px0 <= x <= px1
        hs = []
        for h in Ly['holes']:
            if h[0] == 'rect':
                _, cx, cz, w, hh = h
                lo, hi = max(px0, cx - w / 2), min(px1, cx + w / 2)
                if lo < hi:
                    hs.append(['rect', (lo + hi) / 2, cz, hi - lo, hh])
            elif inside(h[1]):
                hs.append(list(h))
        art.append(dict(name='%s%s %s' % (tag, 'abc'[i], piece_names[i]), host=host_name, x0=px0, x1=px1, z0=zl, z1=zh,
                        holes=hs, labels=[list(l) for l in Ly['labels'] if inside(l[1])],
                        notches=[(nx, ez) for nx, ez in notches if px0 - 3.2 <= nx <= px1 + 3.2], notch_r=3.2, label_h=2.3))
    json.dump(art, open(ART_JSON, 'w'), indent=1)
    print('PFD bezel built: LCD z %.1f-%.1f, window %s' % (Ly['lcd_z0'], Ly['lcd_z0'] + LCD[1], tuple(round(v, 1) for v in Ly['win'])))
    return occ


def run(_context: str):
    build()
