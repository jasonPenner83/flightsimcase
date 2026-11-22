"""Tiled 1:1 tracing PDF (US Letter) of the case panels, from panels.json (extracted from the Fusion model).

Every sheet: 1:1 drawing tile, a 50 mm alignment grid in panel coordinates (shared by neighbouring sheets, so
overlapping sheets line up on the grid crosses), overlap guides naming the neighbour sheet, and a scale-check bar
(100 mm and 4 in). Print at 100 % / Actual size. Pure-Python PDF writer, no dependencies.
Usage: python make_trace_pdf.py  -> Panel_Tracing_1to1_Letter.pdf
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
K = 72.0 / 25.4                      # mm -> pt
PW, PH = 215.9, 279.4                # US Letter, mm
M = 12.7                             # page margin (0.5 in, inside every printer's printable area)
FX0, FX1 = M, PW - M                 # drawing frame
FY0, FY1 = 30.0, PH - M
OV = 15.0                            # overlap between neighbouring tiles
SX, SY = (FX1 - FX0) - OV, (FY1 - FY0) - OV
PAD = 10.0                           # blank border around each panel
GRID = 50.0
# router jigs (same regions as fusion/build_jigs.py) -> label the cut-outs they cut
JIGS = [('J01', 'Left main', (134, 430, 131, 326)), ('J02', 'Left main', (19, 223, 28, 245.5)), ('J03', 'Left main', (260, 308, 36, 84)),
        ('J04', 'Left main', (334, 409, 20, 116)), ('J05', 'Spacer panel', (448, 504, 125, 332)), ('J06', 'Right main', (530, 828, 131, 326)),
        ('J07', 'Right main', (523, 611, 28, 116)), ('J08', 'Right main', (613, 699, 28, 116)), ('J09', 'Right main', (699, 791, 21, 116)),
        ('J10', 'Right main', (834, 870, 247, 293)), ('J11', 'Right main', (796, 919, 20, 116)), ('J12', 'Left lower', (19.5, 278, -107.5, 0)),
        ('J13', 'Left lower', (298, 412, -110, 0)), ('J14', 'Right lower', (618, 762, -80, -41)), ('J15', 'Right lower', (804, 877, -95.5, -9.5))]


class Pdf:
    def __init__(self):
        self.pages = []

    def page(self):
        self.pages.append([])
        return self.pages[-1]

    def save(self, path):
        objs = []

        def add(s):
            objs.append(s)
            return len(objs)
        cat = add(None); pages = add(None)
        font = add('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>')
        fontb = add('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>')
        kids = []
        for ops in self.pages:
            data = '\n'.join(ops).encode('latin-1')
            cs = add(b'<< /Length %d >>\nstream\n' % len(data) + data + b'\nendstream')
            kids.append(add('<< /Type /Page /Parent %d 0 R /MediaBox [0 0 %.2f %.2f] /Contents %d 0 R '
                            '/Resources << /Font << /F1 %d 0 R /F2 %d 0 R >> >> >>' % (pages, PW * K, PH * K, cs, font, fontb)))
        objs[cat - 1] = '<< /Type /Catalog /Pages %d 0 R /ViewerPreferences << /PrintScaling /None >> >>' % pages
        objs[pages - 1] = '<< /Type /Pages /Kids [%s] /Count %d >>' % (' '.join('%d 0 R' % k for k in kids), len(kids))
        out = bytearray(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n')
        offs = []
        for i, o in enumerate(objs, 1):
            offs.append(len(out))
            body = o if isinstance(o, bytes) else o.encode('latin-1')
            out += b'%d 0 obj\n' % i + body + b'\nendobj\n'
        xref = len(out)
        out += b'xref\n0 %d\n0000000000 65535 f \n' % (len(objs) + 1)
        for o in offs:
            out += b'%010d 00000 n \n' % o
        out += b'trailer\n<< /Size %d /Root %d 0 R >>\nstartxref\n%d\n%%%%EOF\n' % (len(objs) + 1, cat, xref)
        open(path, 'wb').write(out)


def esc(t):
    return t.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')


def text(ops, x, y, s, size=8, bold=False, gray=0.0):
    ops.append('BT /%s %.1f Tf %.2f g %.2f %.2f Td (%s) Tj ET' % ('F2' if bold else 'F1', size, gray, x * K, y * K, esc(s)))


def line(ops, pts, w=0.5, gray=0.0, dash=None, close=False):
    ops.append('q %.2f w %.2f G %s' % (w, gray, ('[%s] 0 d' % ' '.join('%.1f' % (d * K) for d in dash)) if dash else '[] 0 d'))
    ops.append('%.2f %.2f m ' % (pts[0][0] * K, pts[0][1] * K) + ' '.join('%.2f %.2f l' % (p[0] * K, p[1] * K) for p in pts[1:])
               + (' h S' if close else ' S') + ' Q')


def scale_bar(ops, x, y):
    line(ops, [(x, y), (x + 100, y)], w=0.8)
    for i in range(11):
        line(ops, [(x + 10 * i, y), (x + 10 * i, y - (2.5 if i % 5 else 4))], w=0.5)
    for i in range(5):
        xi = x + 25.4 * i
        line(ops, [(xi, y), (xi, y + (3 if i else 4))], w=0.5)
    text(ops, x + 101.5, y - 3.2, '100 mm', 6)
    text(ops, x + 103.0, y + 1.2, '4 in', 6)
    text(ops, x, y - 7.5, 'SCALE CHECK: bottom ticks must measure exactly 100 mm, top ticks exactly 1 in apart.', 6)


def tiles_for(bb):
    u0, u1, z0, z1 = bb[0] - PAD, bb[1] + PAD, bb[2] - PAD, bb[3] + PAD
    nc = max(1, math.ceil(((u1 - u0) - OV) / SX - 1e-9))
    nr = max(1, math.ceil(((z1 - z0) - OV) / SY - 1e-9))
    return u0, z1, nc, nr


def tile_name(r, c):
    return '%s%d' % (chr(65 + r), c + 1)


def main():
    panels = json.load(open(os.path.join(HERE, 'panels.json')))
    pdf = Pdf()
    # ---------- cover / index
    cover = pdf.page()
    text(cover, M, PH - 22, 'C172 Folding Cockpit Case - panel tracing sheets, 1:1', 15, bold=True)
    y = PH - 32
    for s in ('PRINT AT 100 % / "Actual size". Turn OFF "Fit to page" / "Shrink oversized pages".',
              'Check the scale bar at the bottom of every sheet before tracing (100 mm and 4 in).',
              'Sheets overlap by 15 mm. Line up neighbouring sheets on the grey 50 mm grid crosses, then tape.',
              'Grid labels are panel coordinates in mm, the same on every sheet of a panel.',
              'All views are of the FRONT face (the side the pilot sees). Trace outlines and cut-outs.',
              'Solid black = cut line. Small circles with a cross = drill / screw holes (centre marked).',
              'Router jigs for the big cut-outs: fabrication/jigs (flush-trim pattern bit, see README).'):
        text(cover, M, y, s, 8.5)
        y -= 5.2
    y -= 4
    text(cover, M, y, 'Panel                                           Size (mm)          Thick   Sheets', 9, bold=True)
    y -= 5.5
    layout = []
    page_no = 2
    for p in panels:
        outer = [l for l in p['loops'] if l['outer']][0]['pts']
        bb = (min(q[0] for q in outer), max(q[0] for q in outer), min(q[1] for q in outer), max(q[1] for q in outer))
        u0, ztop, nc, nr = tiles_for(bb)
        layout.append((p, bb, u0, ztop, nc, nr, page_no))
        text(cover, M, y, p['name'], 8.5)
        text(cover, M + 88, y, '%.0f x %.0f' % (bb[1] - bb[0], bb[3] - bb[2]), 8.5)
        text(cover, M + 122, y, '%d mm' % p['thickness'], 8.5)
        text(cover, M + 140, y, '%d (pp. %d-%d, %d x %d)' % (nc * nr, page_no, page_no + nc * nr - 1, nr, nc), 8.5)
        page_no += nc * nr
        y -= 5
    y -= 3
    for s in ('Not drawn (plain rectangles): seam side walls 3 mm, 43 x 500 (left) and 161 x 500 (right).',
              'Rim skins: bend to the panel outline; developed sizes in the BOM (about 1270 x 116 left, 1270 x 234 right).',
              'Throttle / condition holes 31 mm, mixture 27 mm: check against the 737DIYSIM throttle guide before cutting.',
              'Cut-outs marked "jig Jxx" have a printable router jig (fabrication/jigs, flush-trim bit, see README).'):
        text(cover, M, y, s, 8)
        y -= 4.6
    # thumbnails with the tile grid
    y -= 4
    tx, ty, tw = M, y, (PW - 2 * M - 16) / 3.0
    col = 0
    for (p, bb, u0, ztop, nc, nr, pg) in layout:
        w = nc * SX + OV; h = nr * SY + OV
        sc = min(tw / w, 28.0 / h)
        bx, by = tx + col * (tw + 8), ty - h * sc
        if by < 16:
            break
        for l in p['loops']:
            pts = [(bx + (q[0] - u0) * sc, by + (q[1] - (ztop - h)) * sc) for q in l['pts']]
            line(cover, pts, w=0.3, close=True)
        for r in range(nr):
            for c in range(nc):
                x0 = bx + c * SX * sc; y1 = by + h * sc - r * SY * sc
                line(cover, [(x0, y1), (x0 + (SX + OV) * sc, y1), (x0 + (SX + OV) * sc, y1 - (SY + OV) * sc), (x0, y1 - (SY + OV) * sc)],
                     w=0.3, gray=0.6, dash=(1, 1), close=True)
                text(cover, x0 + 1, y1 - 3.5, tile_name(r, c), 5, gray=0.4)
        text(cover, bx, by - 3.5, '%s  (p. %d-)' % (p['name'], pg), 6)
        col += 1
        if col == 3:
            col = 0
            ty = ty - 28.0 - 9
    scale_bar(cover, PW - M - 112, 18)

    # ---------- tiles
    for (p, bb, u0, ztop, nc, nr, pg) in layout:
        for r in range(nr):
            for c in range(nc):
                ops = pdf.page()
                wx0 = u0 + c * SX; wz1 = ztop - r * SY             # world coords of the frame's top-left corner

                def tp(q):
                    return (FX0 + (q[0] - wx0), FY1 - (wz1 - q[1]))
                ops.append('q %.2f %.2f %.2f %.2f re W n' % (FX0 * K, FY0 * K, (FX1 - FX0) * K, (FY1 - FY0) * K))
                # 50 mm grid + crosses
                gx = math.floor(wx0 / GRID) * GRID
                while gx <= wx0 + (FX1 - FX0):
                    x = FX0 + gx - wx0
                    line(ops, [(x, FY0), (x, FY1)], w=0.25, gray=0.75, dash=(1.5, 1.5))
                    text(ops, x + 0.8, FY0 + 1.2, 'x %d' % gx, 5, gray=0.5)
                    gx += GRID
                gz = math.floor((wz1 - (FY1 - FY0)) / GRID) * GRID
                while gz <= wz1:
                    yv = FY1 - (wz1 - gz)
                    line(ops, [(FX0, yv), (FX1, yv)], w=0.25, gray=0.75, dash=(1.5, 1.5))
                    text(ops, FX0 + 1, yv + 0.8, 'z %d' % gz, 5, gray=0.5)
                    gz += GRID
                gx = math.floor(wx0 / GRID) * GRID
                while gx <= wx0 + (FX1 - FX0):
                    gz = math.floor((wz1 - (FY1 - FY0)) / GRID) * GRID
                    while gz <= wz1:
                        x, yv = FX0 + gx - wx0, FY1 - (wz1 - gz)
                        line(ops, [(x - 4, yv), (x + 4, yv)], w=0.4, gray=0.45)
                        line(ops, [(x, yv - 4), (x, yv + 4)], w=0.4, gray=0.45)
                        gz += GRID
                    gx += GRID
                # panel
                for l in p['loops']:
                    pts = [tp(q) for q in l['pts']]
                    line(ops, pts, w=0.6, close=True)
                    if not l['outer']:
                        xs = [q[0] for q in l['pts']]; zs = [q[1] for q in l['pts']]
                        cx, cz = (min(xs) + max(xs)) / 2, (min(zs) + max(zs)) / 2
                        s = 3.0 if max(max(xs) - min(xs), max(zs) - min(zs)) < 8 else 6.0
                        a, b = tp((cx, cz))
                        line(ops, [(a - s, b), (a + s, b)], w=0.25, gray=0.3)
                        line(ops, [(a, b - s), (a, b + s)], w=0.25, gray=0.3)
                        if s > 3:
                            for jn, pn, (j0, j1, j2, j3) in JIGS:
                                if p['name'].startswith(pn) and j0 <= cx <= j1 and j2 <= cz <= j3:
                                    text(ops, a + 2, b + 2, 'jig ' + jn, 7, bold=True, gray=0.35)
                                    break
                ops.append('Q')
                # overlap guides
                if c < nc - 1:
                    line(ops, [(FX1 - OV, FY0), (FX1 - OV, FY1)], w=0.3, gray=0.5, dash=(4, 2))
                    text(ops, FX1 - OV + 1, FY0 + 6, 'overlap ->', 5, gray=0.4)
                    text(ops, FX1 - OV + 1, FY0 + 3, tile_name(r, c + 1), 6, bold=True, gray=0.4)
                if r < nr - 1:
                    line(ops, [(FX0, FY0 + OV), (FX1, FY0 + OV)], w=0.3, gray=0.5, dash=(4, 2))
                    text(ops, FX0 + 30, FY0 + OV - 4, 'overlap - next sheet below: %s' % tile_name(r + 1, c), 6, gray=0.4)
                line(ops, [(FX0, FY0), (FX1, FY0), (FX1, FY1), (FX0, FY1)], w=0.4, gray=0.3, close=True)
                # footer
                text(ops, M, 22, '%s  -  sheet %s  (row %d of %d, column %d of %d)' % (p['name'], tile_name(r, c), r + 1, nr, c + 1, nc), 8, bold=True)
                text(ops, M, 17.5, '%d mm material, FRONT face. Print at 100 %%.' % p['thickness'], 6.5)
                scale_bar(ops, PW - M - 112, 22)
    pdf.save(os.path.join(HERE, 'Panel_Tracing_1to1_Letter.pdf'))
    print('pages', len(pdf.pages))


if __name__ == '__main__':
    main()
