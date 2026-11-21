# Rev C helpers: fold angles, interference sweep, colours, cut list. Units mm.
import adsk.core, adsk.fusion, math


def _d():
    app = adsk.core.Application.get()
    return app, adsk.fusion.Design.cast(app.activeProduct)


def occ(name):
    app, d = _d()
    for o in d.rootComponent.occurrences:
        if o.component.name == name:
            return o


def joint(name):
    app, d = _d()
    return d.rootComponent.asBuiltJoints.itemByName(name)


SIGN = {'Left spacer hinge': 1.0, 'Left wing hinge': 1.0, 'Right spacer hinge': -1.0, 'Right wing hinge': -1.0,
        'Center outrigger L swing': 1.0, 'Center outrigger R swing': -1.0,
        'Left outrigger swing': 1.0, 'Right outrigger swing': -1.0}
NAMES = ['Center panel', 'Left spacer', 'Left wing', 'Right spacer', 'Right wing',
         'Center outrigger L', 'Center outrigger R', 'Left wing outrigger', 'Right wing outrigger']


def set_joint(name, deg):
    joint(name).jointMotion.rotationValue = SIGN[name] * math.radians(deg)


def set_fold(la, lb=None, ra=0, rb=None):
    lb = la if lb is None else lb
    rb = ra if rb is None else rb
    set_joint('Left spacer hinge', la)
    set_joint('Left wing hinge', lb)
    set_joint('Right spacer hinge', ra)
    set_joint('Right wing hinge', rb)
    adsk.core.Application.get().activeViewport.refresh()


def set_outriggers(deg):
    for n in ('Center outrigger L swing', 'Center outrigger R swing', 'Left outrigger swing', 'Right outrigger swing'):
        set_joint(n, deg)


def bbox_mm(o):
    b = o.boundingBox
    mn, mx = b.minPoint, b.maxPoint
    return dict(x=(round(mn.x * 10, 1), round(mx.x * 10, 1)), y=(round(-mx.y * 10, 1), round(-mn.y * 10, 1)),
                z=(round(mn.z * 10, 1), round(mx.z * 10, 1)))


def _owner(e):
    if e.assemblyContext:
        return e.assemblyContext.component.name
    return e.parentComponent.name


def interference(min_vol_mm3=1.0, names=None):
    app, d = _d()
    coll = adsk.core.ObjectCollection.create()
    for n in (names or NAMES):
        for b in occ(n).bRepBodies:
            if b.name.startswith(('BEZEL', 'ENVELOPE', 'HINGE')):
                continue
            coll.add(b)
    ii = d.createInterferenceInput(coll)
    ii.areCoincidentFacesIncluded = False
    res = d.analyzeInterference(ii)
    hits = []
    for r in res:
        o1 = _owner(r.entityOne); o2 = _owner(r.entityTwo)
        if o1 == o2:
            continue
        vol = r.interferenceBody.volume * 1000.0
        if vol < min_vol_mm3:
            continue
        hits.append('%s/%s x %s/%s : %.0f mm3' % (o1, r.entityOne.name, o2, r.entityTwo.name, vol))
    return hits


def sweep(step=5, mode='together'):
    """mode: together (both hinges of a side move equally), spacer_first, wing_first."""
    out = []

    def path(a):
        if mode == 'together':
            return (a, a)
        if mode == 'spacer_first':
            return (min(2 * a, 90), max(0, 2 * a - 90))
        return (max(0, 2 * a - 90), min(2 * a, 90))
    for a in range(0, 91, step):
        sa, wa = path(a)
        set_fold(sa, wa, 0, 0)
        out.append(('L %s spacer=%d wing=%d' % (mode, sa, wa), interference()))
    for a in range(0, 91, step):
        sa, wa = path(a)
        set_fold(90, 90, sa, wa)
        out.append(('R %s spacer=%d wing=%d' % (mode, sa, wa), interference()))
    set_fold(0, 0, 0, 0)
    return out


def colorize():
    app, d = _d()
    lib = app.materialLibraries.itemByName('Fusion Appearance Library')

    def ap(n):
        a = d.appearances.itemByName(n)
        return a if a else d.appearances.addByCopy(lib.appearances.itemByName(n), n)
    m = {'20': 'Aluminum - Satin', 'PRINT': 'Plastic - Matte (Yellow)', 'BEZEL': 'Plastic - Matte (Black)',
         'ZONE front': 'Plastic - Glossy (Green)', 'ZONE rear': 'Plastic - Glossy (Blue)',
         'ENVELOPE': 'Plastic - Glossy (Red)', 'HINGE': 'Aluminum - Anodized Glossy (Red)',
         'COVER': 'Plastic - Matte (Gray)', 'SKIN': 'Plastic - Matte (Gray)'}
    for o in d.rootComponent.occurrences:
        for b in o.component.bRepBodies:
            for k, v in m.items():
                if b.name.startswith(k):
                    b.appearance = ap(v)


def rebuild(build_mod):
    app, d = _d()
    r = d.rootComponent
    while r.asBuiltJoints.count:
        r.asBuiltJoints.item(0).deleteMe()
    while r.occurrences.count:
        r.occurrences.item(0).deleteMe()
    build_mod.build()
    colorize()


def cut_list():
    app, d = _d()
    from collections import Counter
    c = Counter()
    for o in d.rootComponent.occurrences:
        for b in o.component.bRepBodies:
            if b.name.startswith('20'):
                bb = b.boundingBox
                dims = sorted([(bb.maxPoint.x - bb.minPoint.x) * 10, (bb.maxPoint.y - bb.minPoint.y) * 10,
                               (bb.maxPoint.z - bb.minPoint.z) * 10])
                prof = b.name.split()[0]
                c[(prof, round(dims[2], 1), o.component.name)] += 1
    return c
