# Helpers: fold angles, interference sweep, view, cut list. Units mm.
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


SIGN = {'Left link pivot': 1.0, 'Left wing pivot': 1.0, 'Right link pivot': -1.0, 'Right wing pivot': -1.0}
NAMES = ['Center panel', 'Left link', 'Left wing', 'Right link', 'Right wing']


def set_joint(name, deg):
    joint(name).jointMotion.rotationValue = SIGN[name] * math.radians(deg)


def set_fold(la, lb=None, ra=0, rb=None):
    """la/ra = link angle, lb/rb = wing angle relative to link (degrees). Closed = 90/90."""
    lb = la if lb is None else lb
    rb = ra if rb is None else rb
    set_joint('Left link pivot', la)
    set_joint('Left wing pivot', lb)
    set_joint('Right link pivot', ra)
    set_joint('Right wing pivot', rb)
    adsk.core.Application.get().activeViewport.refresh()


def bbox_mm(o):
    b = o.boundingBox
    mn, mx = b.minPoint, b.maxPoint
    # Fusion Z-up -> my frame: x, y_toward_pilot = -Y, z
    return dict(x=(mn.x * 10, mx.x * 10), y=(-mx.y * 10, -mn.y * 10), z=(mn.z * 10, mx.z * 10))


def check_bodies(include_base=True):
    app, d = _d()
    coll = adsk.core.ObjectCollection.create()
    names = NAMES + (['Base rail'] if include_base else [])
    for n in names:
        o = occ(n)
        for b in o.bRepBodies:
            if b.name.startswith(('BEZEL', 'ENVELOPE', 'PIN')):
                continue
            coll.add(b)
    return coll


def _owner(e):
    if e.assemblyContext:
        return e.assemblyContext.component.name
    return e.parentComponent.name


def interference(include_base=True, min_vol_mm3=1.0):
    app, d = _d()
    ii = d.createInterferenceInput(check_bodies(include_base))
    ii.areCoincidentFacesIncluded = False
    res = d.analyzeInterference(ii)
    hits = []
    for r in res:
        o1 = _owner(r.entityOne)
        o2 = _owner(r.entityTwo)
        if o1 == o2:
            continue
        vol = r.interferenceBody.volume * 1000.0
        if vol < min_vol_mm3:
            continue
        hits.append('%s/%s x %s/%s : %.0f mm3' % (o1, r.entityOne.name, o2, r.entityTwo.name, vol))
    return hits


def sweep(step=5):
    out = []
    for a in range(0, 91, step):          # left wing, both pivots together
        set_fold(a, a, 0, 0)
        out.append(('L link=%d wing=%d' % (a, a), interference()))
    for a in range(0, 91, step):          # right wing, left already closed
        set_fold(90, 90, a, a)
        out.append(('R link=%d wing=%d' % (a, a), interference()))
    set_fold(0, 0, 0, 0)
    return out


def view(direction=None):
    app, d = _d()
    vp = app.activeViewport
    if direction == 'iso':
        cam = vp.camera
        cam.viewOrientation = adsk.core.ViewOrientations.IsoTopRightViewOrientation
        vp.camera = cam
    vp.fit()
    vp.refresh()


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
                prof = '2040' if b.name.startswith('2040') else '2020'
                c[(prof, round(dims[2], 1), o.component.name)] += 1
    return c


def colorize():
    app, d = _d()
    lib = app.materialLibraries.itemByName('Fusion Appearance Library')

    def ap(n):
        a = d.appearances.itemByName(n)
        return a if a else d.appearances.addByCopy(lib.appearances.itemByName(n), n)
    m = {'20': 'Aluminum - Satin', 'Joiner': 'Aluminum - Anodized Rough (Grey)', 'PRINT': 'Plastic - Matte (Yellow)',
         'BEZEL': 'Plastic - Matte (Black)', 'ZONE front': 'Plastic - Glossy (Green)',
         'ZONE rear': 'Plastic - Glossy (Blue)', 'ENVELOPE': 'Plastic - Glossy (Red)', 'PULLEY': 'Plastic - Matte (Yellow)', 'LINK': 'Aluminum - Anodized Glossy (Red)', 'PIN': 'Aluminum - Satin'}
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
