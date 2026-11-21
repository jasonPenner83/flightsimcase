import importlib.util, math
import adsk.core, adsk.fusion

BASE = r'D:/Admin/Documents/Projects/FlightSimCase/fusion/'


def load(n):
    spec = importlib.util.spec_from_file_location(n, BASE + n + '.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def setup(t):
    t.NAMES = ['Right half', 'Spacer', 'Left half']
    t.MODULE_HOST.clear()
    t.SIGN.update({'Spacer hinge': 1.0, 'Left hinge': 1.0})


def fold(t, sp, lh=None):
    lh = sp if lh is None else lh
    t.set_joint('Spacer hinge', sp)
    t.set_joint('Left hinge', lh)
    adsk.core.Application.get().activeViewport.refresh()


def run(_context: str):
    t = load('tools'); setup(t)
    app, d = t._d()
    r = d.rootComponent
    while r.asBuiltJoints.count:
        r.asBuiltJoints.item(0).deleteMe()
    for i in range(r.occurrences.count - 1, -1, -1):
        o = r.occurrences.item(i)
        if o.component.name in ('Right half', 'Spacer', 'Left half', 'Glareshield (detachable)'):
            o.deleteMe()
    load('build_case_mip').build()
    load('place_vendor').place()
    for o in r.occurrences:
        if o.name.startswith('MIP'):
            o.isLightBulbOn = False
    t.apply_materials()
    # find fold directions: both pivots should bring parts toward the pilot (+y)
    t.SIGN['Spacer hinge'] = 1.0; t.SIGN['Left hinge'] = 1.0
    fold(t, 90, 0)
    if t.bbox_mm(t.occ('Spacer'))['y'][1] < 20:
        t.SIGN['Spacer hinge'] = -1.0
    fold(t, 90, 90)
    yl = t.bbox_mm(t.occ('Left half'))['y']
    if yl[0] < 20:
        t.SIGN['Left hinge'] = -1.0
    print('signs', t.SIGN['Spacer hinge'], t.SIGN['Left hinge'])
    fold(t, 0, 0)
    print('open:', t.interference(children=False) or 'clear')
    for mode in ('together', 'spacer_first', 'left_first'):
        bad = []
        for a in range(0, 91, 5):
            if mode == 'together':
                s, l = a, a
            elif mode == 'spacer_first':
                s, l = min(2 * a, 90), max(0, 2 * a - 90)
            else:
                s, l = max(0, 2 * a - 90), min(2 * a, 90)
            fold(t, s, l)
            h = t.interference(children=False)
            if h:
                bad.append(((s, l), h[:2]))
        print(mode, 'collisions:', bad[:3] if bad else 'none')
    fold(t, 90, 90)
    for n in t.NAMES:
        print(n, t.bbox_mm(t.occ(n)))
    fold(t, 0, 0)
    print(t.case_weight())
