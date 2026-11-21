# GDU 1040 (G1000 PFD/MFD) assembly as one component, built for real parts and real assembly.
#
# Stack (front to back, y = 0 is the rail face):
#   y 15.0 .. 12.5  bezel face (2.5 mm)            knobs / key caps proud of it
#   y 12.5 ..  5.8  LCD module (AUO G104XVN01.0 class, 238.6 x 175.8 x 6.7) against the face
#   y 12.5 ..  4.6  key/encoder PCBs on M2.5 heat-set bosses (switches face forward)
#   y  3.0 ..  0.0  mounting flanges on the rails (3 mm panel plane, edge clamps M5 + washer)
#   y -20  .. -23   printed electronics tray bolted to the BACK of the two rails (M5 + T-nuts)
#   y -23  .. -40   LVDS/HDMI driver board + Arduino Mega 2560 Pro on the tray
# Printing (Bambu A1): bezel in 3 pieces (33 / 240 / 33 mm), face down, no supports; each piece clamps
# to the rails on its own, so pieces are independently removable. Outsourced option: one-piece bezel body.
# Units mm. Frame: X right, Y toward pilot, Z up. Fusion Z-up: (x, -y, z) / 10.
import adsk.core, adsk.fusion, json, os

ART_JSON = r'D:/Admin/Documents/Projects/FlightSimCase/labels/panels.json'
D = 15.0; FACE = 2.5; FL = 3.0; WALL = 2.5
LCD = (238.6, 175.8, 6.7)          # AUO G104XVN01.0 outline
ACTIVE = (210.4, 157.8)            # active area -> display window
EC11 = 7.5                         # EC11 M7 bushing
DUAL = 9.5                         # PropWash dual concentric encoder bushing (verify on arrival)
JOY = 7.5                          # ALPS RKJXT1F42001 (4-way + encoder + push) for RANGE/PAN
SOFT = (11.0, 5.0); KEY = (11.0, 6.0)
PCB_Y = (3.0, 4.6)                 # PCB back / front face
SPLIT = 120.0                      # piece seams at xm +/- 120


def build(host_name, name, xa, xb, rails=(110.0, 310.0)):
    app = adsk.core.Application.get()
    d = adsk.fusion.Design.cast(app.activeProduct)
    root = d.rootComponent
    host = [o for o in root.occurrences if o.component.name == host_name][0].component
    tbm = adsk.fusion.TemporaryBRepManager.get()

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

    def uni(a, b):
        tbm.booleanOperation(a, b, adsk.fusion.BooleanTypes.UnionBooleanType)

    z0, z1 = rails
    zl, zh = z0 + 0.4, z1 - 0.4
    xm = (xa + xb) / 2
    L, R = xm - 132, xm + 132
    lcd_z0 = zl + 16.6
    lcd_zc = lcd_z0 + LCD[1] / 2
    lcd_y0 = D - FACE - LCD[2]

    # ---------------- face layout (GDU 1040)
    knobs = [  # x, z, hole, kind, name
        (L, zh - 20, EC11, 'small', 'NAV VOL'), (L, zh - 55, DUAL, 'dual', 'NAV'), (L, zh - 105, EC11, 'single', 'HDG'),
        (L, zl + 25, DUAL, 'dual', 'ALT'),
        (R, zh - 20, EC11, 'small', 'COM VOL'), (R, zh - 55, DUAL, 'dual', 'COM'), (R, zh - 95, DUAL, 'dual', 'CRS / BARO'),
        (R, zh - 128, JOY, 'single', 'RANGE'), (R, zl + 17, DUAL, 'dual', 'FMS')]
    keys = [(L, zh - 36, 'NAV FLIP'), (R, zh - 36, 'COM FLIP')]
    for i, (a, b) in enumerate([('D->', 'MENU'), ('FPL', 'PROC'), ('CLR', 'ENT')]):
        zb = zl + 58.6 - i * 13
        keys += [(R - 5.5, zb, a), (R + 10.5, zb, b)]     # left key flange clears the LCD edge
    soft = [(xm - 96.8 + i * 17.6, zl + 9.1) for i in range(12)]
    holes = [('rect', xm, lcd_zc, ACTIVE[0], ACTIVE[1])]
    holes += [('circ', x, z, h) for x, z, h, k, n in knobs]
    holes += [('rect', x, z, KEY[0], KEY[1]) for x, z, n in keys]
    holes += [('rect', x, z, SOFT[0], SOFT[1]) for x, z in soft]
    labels = []
    for x, z, h, k, n in knobs:
        if n == 'FMS':
            continue
        r = {'small': 5, 'single': 8, 'dual': 11}[k]
        labels.append((n, x, z - r - 4 if n in ('NAV', 'COM') else z + r + 4))

    # ---------------- boss positions (all checked clear of encoders, keys and the LCD outline)
    clip_bosses = [(xm - 80, zh - 3.0), (xm + 80, zh - 3.0), (xm - 117, lcd_z0 - 3.6), (xm + 117, lcd_z0 - 3.6)]
    pcb_bosses = [(L - 3.5, zl + 5.5), (L - 3.5, zh - 5.5), (R + 3.5, zl + 5.5), (R + 3.5, zh - 5.5),
                  (xm - 107, zl + 9.1), (xm + 107, zl + 9.1)]

    def shell_piece(px0, px1):
        b = box(px0, px1, 0, D, zl, zh)
        cx0 = max(px0, xa + WALL) - (0.01 if px0 > xa else 0)
        cx1 = min(px1, xb - WALL) + (0.01 if px1 < xb else 0)
        sub(b, box(cx0, cx1, FL, D - FACE, zl + WALL, zh - WALL))
        sub(b, box(cx0, cx1, -1, FL + 0.01, z0 + 10, z1 - 10))
        for x, z in clip_bosses + pcb_bosses:
            if px0 <= x <= px1:
                top = lcd_y0 if (x, z) in clip_bosses else PCB_Y[1]
                boss = ycyl(x, z, top, D - FACE + 0.01, 3.0)
                uni(b, boss)
                sub(b, ycyl(x, z, top - 0.1, top + 5.0, 1.65))   # M2.5 heat-set insert bore (3.3 mm)
        for h in holes:
            if h[0] == 'rect':
                _, cx, cz, w, hh = h
                sub(b, box(cx - w / 2, cx + w / 2, -1, D + 1, cz - hh / 2, cz + hh / 2))
            else:
                sub(b, ycyl(h[1], h[2], -1, D + 1, h[3] / 2))
        return b

    splits = [xa, xm - SPLIT, xm + SPLIT, xb]
    names = ['left column', 'display frame', 'right column']
    notch_x = [xa + 12, xm - 100, xm, xm + 100, xb - 12]
    notches = [(nx, ez) for nx in notch_x for ez in (zl, zh)]
    parts = []
    for i in range(3):
        b = shell_piece(splits[i], splits[i + 1])
        for nx, ez in notches:
            sub(b, ycyl(nx, ez, -1, D + 1, 3.2))
        parts.append(('PRINT %s bezel %s' % (name.split()[0], names[i]), b))
    one = shell_piece(xa, xb)
    for nx, ez in notches:
        sub(one, ycyl(nx, ez, -1, D + 1, 3.2))
    parts.append(('OUTSOURCE %s bezel one-piece (SLA / MJF)' % name.split()[0], one))

    # ---------------- printed hardware
    for i, (x, z) in enumerate(clip_bosses):
        # L-clip: screws onto the boss with M3, tongue presses the LCD back edge
        if z > lcd_zc:
            clip = box(x - 6, x + 6, lcd_y0 - 2.0, lcd_y0, lcd_z0 + LCD[1] - 4, zh - WALL - 0.1)
        else:
            dx = -1 if x < xm else 1          # tongue points toward the LCD center
            clip = box(x - 3, x + 3, lcd_y0 - 2.0, lcd_y0, z - 3, z + 3)
            uni(clip, box(min(x, x - dx * 6), max(x, x - dx * 6), lcd_y0 - 2.0, lcd_y0, z, lcd_z0 + 4))
        sub(clip, ycyl(x, z, lcd_y0 - 3, lcd_y0 + 1, 1.4))   # M2.5 clearance
        parts.append(('PRINT LCD clip', clip))
    for x, z, n in keys:
        cap = box(x - KEY[0] / 2 + 0.3, x + KEY[0] / 2 - 0.3, 9.0, D + 2.0, z - KEY[1] / 2 + 0.3, z + KEY[1] / 2 - 0.3)
        uni(cap, box(x - KEY[0] / 2 - 1.0, x + KEY[0] / 2 + 1.0, 9.0, 10.5, z - KEY[1] / 2 - 1.0, z + KEY[1] / 2 + 1.0))
        parts.append(('PRINT key cap %s' % n, cap))
    for x, z in soft:
        cap = box(x - SOFT[0] / 2 + 0.3, x + SOFT[0] / 2 - 0.3, 9.0, D + 2.0, z - SOFT[1] / 2 + 0.3, z + SOFT[1] / 2 - 0.3)
        uni(cap, box(x - SOFT[0] / 2 - 1.0, x + SOFT[0] / 2 + 1.0, 9.0, 10.5, z - SOFT[1] / 2 - 1.0, z + SOFT[1] / 2 + 1.0))
        parts.append(('PRINT softkey cap', cap))
    for x, z, h, k, n in knobs:
        if k == 'dual':
            outer = ycyl(x, z, D + 0.5, D + 10.5, 11.0); sub(outer, ycyl(x, z, D, D + 11, 4.0))
            parts.append(('PRINT knob outer %s' % n, outer))
            parts.append(('PRINT knob inner %s' % n, ycyl(x, z, D + 10.5, D + 18.5, 7.0)))
        else:
            r = 5.0 if k == 'small' else 8.0
            parts.append(('PRINT knob %s' % n, ycyl(x, z, D + 0.5, D + 12.5, r)))
    # electronics tray behind the rails: 200 x 210, tabs on the rail backs
    tray = box(xm - 100, xm + 100, -23, -20, z0 - 5, z1 + 5)
    for tx in (xm - 85, xm + 85):
        for tz in (z0, z1):
            sub(tray, ycyl(tx, tz, -24, -19, 2.75))              # M5 to rail T-nuts
    for bx, bz in [(xm - 92, lcd_zc - 28), (xm + 2, lcd_zc - 28), (xm - 92, lcd_zc + 28), (xm + 2, lcd_zc + 28),
                   (xm + 30, lcd_zc - 22), (xm + 80, lcd_zc - 22), (xm + 30, lcd_zc + 22), (xm + 80, lcd_zc + 22)]:
        so = ycyl(bx, bz, -28, -23, 3.0); sub(so, ycyl(bx, bz, -29, -24.5, 2.0)); uni(tray, so)
    for cx in (xm - 40, xm + 55):
        sub(tray, box(cx - 15, cx + 15, -24, -19, z0 + 15, z0 + 30))                 # cable pass-throughs
    parts.append(('PRINT electronics tray', tray))

    # ---------------- reference (purchased) parts, hidden by default
    refs = [('REF LCD AUO G104XVN01.0 10.4in 1024x768 LED (238.6x175.8x6.7)', box(xm - LCD[0] / 2, xm + LCD[0] / 2, lcd_y0, D - FACE, lcd_z0, lcd_z0 + LCD[1])),
            ('REF LVDS-HDMI driver board (approx 100x65x15)', box(xm - 97, xm + 3, -38, -28, lcd_zc - 32, lcd_zc + 33)),
            ('REF Arduino Mega 2560 Pro (MobiFlight)', box(xm + 27, xm + 83, -36, -28, lcd_zc - 19, lcd_zc + 19)),
            ('REF PCB softkeys 222x13', box(xm - 111, xm + 111, PCB_Y[0], PCB_Y[1], zl + WALL + 0.5, lcd_z0 - 0.5)),
            ('REF PCB left column 30x194', box(xa + WALL + 0.5, xm - SPLIT - 0.5, PCB_Y[0], PCB_Y[1], zl + WALL + 0.5, zh - WALL - 0.5)),
            ('REF PCB right column 30x194', box(xm + SPLIT + 0.5, xb - WALL - 0.5, PCB_Y[0], PCB_Y[1], zl + WALL + 0.5, zh - WALL - 0.5))]
    for x, z, h, k, n in knobs:
        if k == 'dual':
            refs.append(('REF dual encoder PropWash (%s)' % n, box(x - 6.5, x + 6.5, D - FACE - 15, D - FACE, z - 6.5, z + 6.5)))
        elif n == 'RANGE':
            refs.append(('REF ALPS RKJXT1F42001 joystick encoder', box(x - 6.5, x + 6.5, PCB_Y[1], D - FACE, z - 6.5, z + 6.5)))
        else:
            refs.append(('REF EC11 encoder (%s)' % n, box(x - 6, x + 6, PCB_Y[1], PCB_Y[1] + 6.5, z - 6, z + 6)))
    for x, z, n in keys:
        refs.append(('REF tact switch Omron B3F', box(x - 3, x + 3, PCB_Y[1], PCB_Y[1] + 4.3, z - 3, z + 3)))
    for x, z in soft:
        refs.append(('REF tact switch Omron B3F', box(x - 3, x + 3, PCB_Y[1], PCB_Y[1] + 4.3, z - 3, z + 3)))

    occ = host.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    occ.isGroundToParent = True
    comp = occ.component
    comp.name = name
    bf = comp.features.baseFeatures.add()
    bf.startEdit()
    for nm, b in parts + refs:
        nb = comp.bRepBodies.add(b, bf)
        nb.name = nm
    bf.finishEdit()
    for b in comp.bRepBodies:
        if b.name.startswith(('REF', 'OUTSOURCE')):
            b.isLightBulbOn = False

    # label artwork per printed bezel piece
    art = json.load(open(ART_JSON)) if os.path.exists(ART_JSON) else []
    tag = name.split()[0]
    art = [a for a in art if not a['name'].startswith(tag)]
    for i in range(3):
        px0, px1 = splits[i], splits[i + 1]
        hs = []
        for h in holes:
            if h[0] == 'rect':
                _, cx, cz, w, hh = h
                lo, hi = max(px0, cx - w / 2), min(px1, cx + w / 2)
                if lo < hi:
                    hs.append(['rect', (lo + hi) / 2, cz, hi - lo, hh])
            elif px0 <= h[1] <= px1:
                hs.append(list(h))
        art.append(dict(name='%s%s %s' % (tag, 'abc'[i], names[i]), host=host_name, x0=px0, x1=px1, z0=zl, z1=zh, holes=hs,
                        labels=[list(l) for l in labels if px0 <= l[1] <= px1],
                        notches=[(nx, ez) for nx, ez in notches if px0 - 3.2 <= nx <= px1 + 3.2], notch_r=3.2, label_h=2.3))
    json.dump(art, open(ART_JSON, 'w'), indent=1)
    print('%s built: %d printed bodies, %d reference parts' % (name, len(parts) - 1, len(refs)))
    return occ
