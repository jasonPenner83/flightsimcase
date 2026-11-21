import importlib.util, math
import adsk.core, adsk.fusion

BASE = r'D:/Admin/Documents/Projects/FlightSimCase/fusion/'


def load(n):
    spec = importlib.util.spec_from_file_location(n, BASE + n + '.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def setup(t):
    t.NAMES = ['Right half', 'Left half', 'Right outrigger A', 'Right outrigger B', 'Left outrigger outer', 'Left outrigger inner']
    t.MODULE_HOST.clear()
    t.MODULE_HOST.update({'SC-': 'Left half', 'PFD': 'Left half', 'LT-': 'Left half', 'YK-': 'Left half', 'CB-': 'Left half',
                          'AU-': 'Right half', 'MFD': 'Right half', 'SB-': 'Right half', 'CP-': 'Right half'})
    t.SIGN.update({'Fold hinge': 1.0, 'Right outrigger A swing': 1.0, 'Right outrigger B swing': -1.0,
                   'Left outrigger outer swing': 1.0, 'Left outrigger inner swing': -1.0})


def fold(t, deg):
    t.set_joint('Fold hinge', deg)
    adsk.core.Application.get().activeViewport.refresh()


def outriggers(t, deg):
    for n in ('Right outrigger A swing', 'Right outrigger B swing', 'Left outrigger outer swing', 'Left outrigger inner swing'):
        t.set_joint(n, deg)


def run(_context: str):
    t = load('tools'); setup(t)
    app, d = t._d()
    r = d.rootComponent
    while r.asBuiltJoints.count:
        r.asBuiltJoints.item(0).deleteMe()
    while r.occurrences.count:
        r.occurrences.item(0).deleteMe()
    load('build_case_bifold').build()
    load('c172_panels').build()
    t.apply_materials()
    print('open:', t.interference() or 'clear')
    outriggers(t, 90); print('outriggers out:', t.interference() or 'clear'); outriggers(t, 0)
    bad = []
    for a in range(0, 181, 5):
        fold(t, a)
        h = t.interference()
        if h:
            bad.append((a, h[:3]))
    print('fold sweep collisions:', bad or 'none (5 deg steps)')
    fold(t, 180)
    for n in t.NAMES:
        print(n, t.bbox_mm(t.occ(n)))
    fold(t, 0)
    print(t.case_weight())
    for k, v in sorted(t.cut_list().items()):
        print('CUT', k, v)
