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


SIGN = {'Left wing hinge': 1.0, 'Right spacer hinge': -1.0, 'Right wing hinge': -1.0,
        'Center outrigger L swing': 1.0, 'Center outrigger R swing': -1.0,
        'Left outrigger swing': 1.0, 'Right outrigger swing': -1.0, 'Left inner outrigger swing': -1.0}
NAMES = ['Center panel', 'Left wing', 'Right spacer', 'Right wing',
         'Center outrigger L', 'Center outrigger R', 'Left wing outrigger', 'Left wing inner outrigger', 'Right wing outrigger']


def set_joint(name, deg):
    joint(name).jointMotion.rotationValue = SIGN[name] * math.radians(deg)


def set_fold(left, rs=0, rw=None):
    """left: 0..180 (single hinge). rs/rw: right spacer / right wing hinge, 0..90 each."""
    rw = rs if rw is None else rw
    set_joint('Left wing hinge', left)
    set_joint('Right spacer hinge', rs)
    set_joint('Right wing hinge', rw)
    adsk.core.Application.get().activeViewport.refresh()


def set_outriggers(deg):
    for n in ('Center outrigger L swing', 'Center outrigger R swing', 'Left outrigger swing', 'Left inner outrigger swing', 'Right outrigger swing'):
        set_joint(n, deg)


def bbox_mm(o):
    b = o.boundingBox
    mn, mx = b.minPoint, b.maxPoint
    return dict(x=(round(mn.x * 10, 1), round(mx.x * 10, 1)), y=(round(-mx.y * 10, 1), round(-mn.y * 10, 1)),
                z=(round(mn.z * 10, 1), round(mx.z * 10, 1)))


MODULE_HOST = {'SW-': 'Left wing', 'YK-': 'Left wing', 'PFD': 'Left wing', 'CL-': 'Center panel', 'MFD': 'Center panel',
               'SB-': 'Center panel', 'CP-': 'Center panel', 'AU-': 'Center panel'}


def _owner(e):
    if e.assemblyContext:
        top = e.assemblyContext.fullPathName.split('+')[0]
        return top.rsplit(':', 1)[0]
    return e.parentComponent.name


def _bodies(o):
    for b in o.bRepBodies:
        yield b
    for c in o.childOccurrences:
        for b in _bodies(c):
            yield b


def interference(min_vol_mm3=1.0, names=None):
    app, d = _d()
    coll = adsk.core.ObjectCollection.create()
    tagged = []
    for n in (names or NAMES):
        for b in _bodies(occ(n)):
            if b.name.startswith(('BEZEL', 'ENVELOPE', 'HINGE', 'REF', 'OUTSOURCE')):
                continue
            coll.add(b)
            tagged.append((b, n))

    def owner(e):
        n = _owner(e)
        return MODULE_HOST.get(n[:3], n)   # modules live inside their host panel
    ii = d.createInterferenceInput(coll)
    ii.areCoincidentFacesIncluded = False
    res = d.analyzeInterference(ii)
    hits = []
    for r in res:
        o1 = owner(r.entityOne); o2 = owner(r.entityTwo)
        if o1 == o2:
            continue
        vol = r.interferenceBody.volume * 1000.0
        if vol < min_vol_mm3:
            continue
        hits.append('%s/%s x %s/%s : %.0f mm3' % (o1, r.entityOne.name, o2, r.entityTwo.name, vol))
    return hits


def sweep(step=5, mode='together'):
    out = []
    for a in range(0, 181, step):
        set_fold(a, 0, 0)
        out.append(('L hinge=%d' % a, interference()))

    def path(a):
        if mode == 'together':
            return (a, a)
        if mode == 'spacer_first':
            return (min(2 * a, 90), max(0, 2 * a - 90))
        return (max(0, 2 * a - 90), min(2 * a, 90))
    for a in range(0, 91, step):
        sa, wa = path(a)
        set_fold(180, sa, wa)
        out.append(('R %s spacer=%d wing=%d' % (mode, sa, wa), interference()))
    set_fold(0, 0, 0)
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
         'COVER': 'Plastic - Matte (Gray)', 'SKIN': 'Plastic - Matte (Gray)', 'SHEET': 'Plastic - Matte (Gray)'}
    m['PRINT SW'] = 'Plastic - Matte (Black)'
    m['PRINT CL'] = 'Plastic - Matte (Black)'
    for k in ('PRINT PFD', 'PRINT MFD', 'PRINT SB', 'PRINT YK', 'PRINT CP', 'PRINT AU', 'PRINT SC', 'PRINT LT', 'PRINT CB',
              'PRINT knob', 'PRINT key', 'PRINT softkey', 'PRINT LCD', 'PRINT electronics'):
        m[k] = 'Plastic - Matte (Black)'
    m['REF'] = 'Plastic - Matte (White)'
    for comp in d.allComponents:
        for b in comp.bRepBodies:
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
    apply_materials()


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


MATERIALS = [  # (body-name prefix, physical material) - first match wins
    ('2020', 'Aluminum 6061'), ('2040', 'Aluminum 6061'),
    ('HINGE', 'Aluminum 6061'), ('PIN', 'Stainless Steel'),
    ('PRINT', 'PET Plastic'),                     # PETG stand-in (similar density)
    ('OUTSOURCE', 'Nylon 12 (with Formlabs Fuse 1 3D Printer)'),
    ('COVER', 'ABS Plastic'), ('SHEET', 'ABS Plastic'), ('SKIN', 'ABS Plastic'),
    ('BEZEL', 'ABS Plastic'), ('REF', 'ABS Plastic'),
]
# real 20-series profiles are hollow: ratio of real mass to the solid box modelled here
PROFILE_FILL = {'2020': 0.46, '2040': 0.42}
NON_PARTS = ('ZONE', 'ENVELOPE', 'REF', 'BEZEL', 'OUTSOURCE')


def apply_materials(hide_refs=True):
    app, d = _d()
    lib = app.materialLibraries.itemByName('Fusion Material Library')
    cache = {}
    for comp in d.allComponents:
        for b in comp.bRepBodies:
            for pre, mat in MATERIALS:
                if b.name.startswith(pre):
                    if mat not in cache:
                        cache[mat] = lib.materials.itemByName(mat)
                    b.material = cache[mat]
                    break
            if hide_refs and b.name.startswith(('REF', 'OUTSOURCE')):
                b.isLightBulbOn = False
        for sk in comp.sketches:
            sk.isLightBulbOn = False
    colorize()      # appearances override the material's default look


def case_weight():
    """Estimated build weight (kg), hollow-profile corrected, placeholders/zones excluded."""
    app, d = _d()
    tot = {}
    for comp in d.allComponents:
        if comp.name == 'Desk controls':
            continue
        n_inst = max(1, len([o for o in d.rootComponent.allOccurrences if o.component == comp]))
        for b in comp.bRepBodies:
            if b.name.startswith(NON_PARTS):
                continue
            m = b.physicalProperties.mass * n_inst
            key = b.name.split()[0]
            if key in PROFILE_FILL:
                m *= PROFILE_FILL[key]
            grp = 'extrusion' if key in PROFILE_FILL else ('printed' if key == 'PRINT' else ('sheet' if key in ('COVER', 'SHEET', 'SKIN') else 'other'))
            tot[grp] = tot.get(grp, 0) + m
    return {k: round(v, 2) for k, v in tot.items()}, round(sum(tot.values()), 2)
