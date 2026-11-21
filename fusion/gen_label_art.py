"""Make 1:1 label artwork (SVG, mm units) for every faceplate from labels/panels.json.

The JSON is written by build_switch_panel.py each time the modules are rebuilt in Fusion.
Outputs, per panel, in labels/:
  <panel>_label.svg  black background, white text, red 0.1 mm cut lines (outline, holes, edge notches).
                     Use for printed vinyl stickers (kiss-cut on the red lines) or to send to an engraving/UV-print shop.
  all_labels_sheet.svg  every panel on one sheet, 5 mm apart.
Run:  python gen_label_art.py
"""
import json, os, html

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'labels')
FONT = "Arial, Helvetica, sans-serif"
CUT = 'stroke="#ff0000" stroke-width="0.1" fill="none"'


def panel_svg(p, ox=0.0, oy=0.0):
    w = p['x1'] - p['x0']; h = p['z1'] - p['z0']
    X = lambda x: ox + (x - p['x0'])
    Y = lambda z: oy + (p['z1'] - z)
    out = ['<g id="%s">' % html.escape(p['name'])]
    out.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="#111111"/>' % (ox, oy, w, h))
    fs = p['label_h'] * 1.4
    for txt, cx, cz in p['labels']:
        out.append('<text x="%.2f" y="%.2f" font-family="%s" font-size="%.2f" font-weight="bold" fill="#ffffff" '
                   'text-anchor="middle" dominant-baseline="central">%s</text>' % (X(cx), Y(cz), FONT, fs, html.escape(txt)))
    out.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" %s/>' % (ox, oy, w, h, CUT))
    for hl in p['holes']:
        if hl[0] == 'rect':
            _, cx, cz, hw, hh = hl
            out.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" %s/>' % (X(cx) - hw / 2, Y(cz) - hh / 2, hw, hh, CUT))
        else:
            _, cx, cz, dia = hl
            out.append('<circle cx="%.2f" cy="%.2f" r="%.2f" %s/>' % (X(cx), Y(cz), dia / 2, CUT))
    for nx, nz in p['notches']:
        out.append('<circle cx="%.2f" cy="%.2f" r="%.2f" %s/>' % (X(nx), Y(nz), p['notch_r'], CUT))
    out.append('</g>')
    return '\n'.join(out), w, h


def wrap(body, w, h):
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg xmlns="http://www.w3.org/2000/svg" width="%.2fmm" height="%.2fmm" viewBox="0 0 %.2f %.2f">\n%s\n</svg>\n'
            % (w, h, w, h, body))


def main():
    panels = json.load(open(os.path.join(BASE, 'panels.json')))
    sheet = []; y = 5.0; maxw = 0.0
    for p in panels:
        tag = p['name'].split()[0]
        body, w, h = panel_svg(p)
        open(os.path.join(BASE, '%s_label.svg' % tag), 'w', encoding='utf-8').write(wrap(body, w, h))
        sb, _, _ = panel_svg(p, 5.0, y)
        sheet.append(sb); y += h + 5.0; maxw = max(maxw, w)
        print('wrote %s_label.svg (%.1f x %.1f mm, %d labels, %d holes)' % (tag, w, h, len(p['labels']), len(p['holes'])))
    open(os.path.join(BASE, 'all_labels_sheet.svg'), 'w', encoding='utf-8').write(wrap('\n'.join(sheet), maxw + 10, y))
    print('wrote all_labels_sheet.svg')


if __name__ == '__main__':
    main()
