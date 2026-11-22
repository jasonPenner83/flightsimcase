# Glareshield check: open (vs its own half's panel/modules) or folded (vs everything), bodies above z 200.
import importlib.util
import adsk.core, adsk.fusion

BASE = r'D:/Admin/Documents/Projects/FlightSimCase/fusion/'


def load(n):
    spec = importlib.util.spec_from_file_location(n, BASE + n + '.py')
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def check(sp=0, lh=0):
    t = load('tools'); rm = load('run_mip'); rm.setup(t)
    d = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    rm.fold(t, sp, lh)
    coll = adsk.core.ObjectCollection.create()

    def walk(o):
        for b in o.bRepBodies:
            if b.isVisible and not b.name.startswith('ZONE') and b.boundingBox.maxPoint.z * 10 > 200:
                coll.add(b)
        for c in o.childOccurrences:
            walk(c)
    for o in d.rootComponent.occurrences:
        if o.component.name in ('Left half', 'Spacer', 'Right half'):
            walk(o)
    ii = d.createInterferenceInput(coll); ii.areCoincidentFacesIncluded = False
    res = d.analyzeInterference(ii)
    hits = []
    for r in (res or []):
        n1, n2 = r.entityOne.name, r.entityTwo.name
        if 'glareshield' in n1 or 'glareshield' in n2:
            bb = r.interferenceBody.boundingBox
            hits.append('%s/%s x %s/%s %.0f mm3 at x %.0f z %.0f' % (r.entityOne.parentComponent.name[:12], n1[:22], r.entityTwo.parentComponent.name[:12], n2[:22],
                                                               r.interferenceBody.volume * 1000, (bb.minPoint.x + bb.maxPoint.x) * 5, (bb.minPoint.z + bb.maxPoint.z) * 5))
    msg = 'fold %s %s bodies %d glareshield hits %d %s' % (sp, lh, coll.count, len(hits), hits[:10])
    print(msg)
    with open(BASE + 'check_glare.log', 'a') as f:
        f.write(msg + chr(10))
    rm.fold(t, 0, 0)
    return hits


def run(_context: str):
    check(90, 90)
