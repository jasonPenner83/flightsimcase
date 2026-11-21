import importlib.util

BASE = r'D:/Admin/Documents/Projects/FlightSimCase/fusion/'


def load(n):
    spec = importlib.util.spec_from_file_location(n, BASE + n + '.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def run(_context: str):
    t = load('tools')
    t.rebuild(load('build_case'))
    load('build_switch_panel').build()
    pf = load('build_pfd')
    pf.build('Left wing', 'PFD-1 GDU 1040 bezel', -538.0, -232.0)
    pf.build('Center panel', 'MFD-1 GDU 1040 bezel', -121.0, 185.0)
    load('build_standby').build()
    t.apply_materials()
    print('open, stored:', t.interference() or 'clear')
    t.set_outriggers(90)
    print('open, outriggers out:', t.interference() or 'clear')
    t.set_outriggers(0)
    for mode in ('together', 'spacer_first', 'wing_first'):
        res = [(k, h) for k, h in t.sweep(10 if mode != 'together' else 5, mode) if h]
        print(mode, 'collisions at:', [k for k, h in res] if res else 'none')
        if res:
            print('   first:', res[0][1][:4])
    t.set_fold(180, 90, 90)
    for n in t.NAMES:
        print(n, t.bbox_mm(t.occ(n)))
    t.set_fold(0, 0, 0)
    for k, v in sorted(t.cut_list().items()):
        print('CUT', k, v)
