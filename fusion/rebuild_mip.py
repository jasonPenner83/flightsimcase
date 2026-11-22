# Rebuild the MIP folding case + vendor module placement only (no sweeps; run checks separately).
import importlib.util
import adsk.core, adsk.fusion

BASE = r'D:/Admin/Documents/Projects/FlightSimCase/fusion/'


def load(n):
    spec = importlib.util.spec_from_file_location(n, BASE + n + '.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def run(_context: str):
    app = adsk.core.Application.get()
    d = adsk.fusion.Design.cast(app.activeProduct)
    r = d.rootComponent
    while r.asBuiltJoints.count:
        r.asBuiltJoints.item(0).deleteMe()
    for i in range(r.occurrences.count - 1, -1, -1):
        o = r.occurrences.item(i)
        if o.component.name in ('Right half', 'Spacer', 'Left half', 'Glareshield (detachable)'):
            o.deleteMe()
    load('build_case_mip').build()
    load('place_vendor').place()
    load('build_lower').build_lower()
    load('build_storage').build_storage()
    lib = app.materialLibraries.itemByName('Fusion Material Library')
    mats = {'REF': 'ABS Plastic', 'PANEL': 'Plywood, Finish', 'ALU': 'Aluminum 6061', '20': 'Aluminum 6061', 'PRINT': 'PET Plastic'}
    for o in r.occurrences:
        if o.component.name in ('Right half', 'Spacer', 'Left half'):
            for b in o.component.bRepBodies:
                for k, v in mats.items():
                    if b.name.startswith(k):
                        b.material = lib.materials.itemByName(v)
                if b.name.startswith('ZONE'):
                    b.isLightBulbOn = False
        if o.name.startswith('MIP') or o.component.name.startswith('737DIYSIM'):
            o.isLightBulbOn = False
    print('rebuilt')
