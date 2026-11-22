"""Contact sheet (SVG) of the router-jig STLs: front face of each jig, to scale, with its size and bed check."""
import glob, os, struct

HERE = os.path.dirname(os.path.abspath(__file__))


def tris(path):
    data = open(path, 'rb').read()
    if data[:5] == b'solid' and b'facet' in data[:300]:
        out = []
        cur = []
        for ln in data.decode('ascii', 'ignore').splitlines():
            ln = ln.strip()
            if ln.startswith('facet normal'):
                n = tuple(map(float, ln.split()[2:5])); cur = []
            elif ln.startswith('vertex'):
                cur.append(tuple(map(float, ln.split()[1:4])))
                if len(cur) == 3:
                    out.append((n, cur))
        return out
    n = struct.unpack('<I', data[80:84])[0]
    out = []
    for i in range(n):
        v = struct.unpack('<12f', data[84 + 50 * i: 84 + 50 * i + 48])
        out.append((v[0:3], [v[3:6], v[6:9], v[9:12]]))
    return out


def main():
    files = sorted(glob.glob(os.path.join(HERE, 'jigs', '*.stl')))
    cells = []
    for f in files:
        T = tris(f)
        # STL units are mm (Fusion export), plate normal along y
        face = [t for n, t in T if n[1] < -0.9] or [t for n, t in T if n[1] > 0.9]
        xs = [p[0] for t in face for p in t]; zs = [p[2] for t in face for p in t]
        cells.append((os.path.basename(f)[:-4], face, min(xs), max(xs), min(zs), max(zs)))
    col_w, row_h, per_row, s = 270, 300, 4, 1.0
    W = col_w * per_row; H = row_h * ((len(cells) + per_row - 1) // per_row)
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Helvetica" font-size="11">' % (W, H, W, H),
           '<rect width="100%" height="100%" fill="white"/>']
    for i, (nm, face, x0, x1, z0, z1) in enumerate(cells):
        cx, cy = (i % per_row) * col_w + 8, (i // per_row) * row_h + 24
        out.append('<rect x="%d" y="%d" width="256" height="256" fill="none" stroke="#bbb" stroke-dasharray="4 3"/>' % (cx, cy))
        pts = []
        for t in face:
            pts.append('M' + ' L'.join('%.1f,%.1f' % (cx + (p[0] - x0), cy + (z1 - p[2])) for p in t) + 'Z')
        out.append('<path d="%s" fill="#3a6ea5" stroke="#3a6ea5" stroke-width="0.3"/>' % ' '.join(pts))
        w, h = x1 - x0, z1 - z0
        out.append('<text x="%d" y="%d">%s</text>' % (cx, cy - 8, nm))
        out.append('<text x="%d" y="%d" fill="%s">%.0f x %.0f x 8 mm  %s</text>' % (cx, cy + 272, 'green' if max(w, h) <= 256 else 'red', w, h, 'fits 256 bed' if max(w, h) <= 256 else 'TOO BIG'))
    out.append('</svg>')
    open(os.path.join(HERE, 'jigs', 'jig_contact_sheet.svg'), 'w').write('\n'.join(out))
    print(len(cells), 'jigs')


if __name__ == '__main__':
    main()
