# Stowage check: stowed items, pods, tubs and face pockets vs everything else on the same half (open state).
import adsk.core, adsk.fusion

NEW = ('PANEL rear', 'PRINT face pocket', 'PRINT pedestal', 'REF Logitech')


def check(host_name):
    d = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    host = [o for o in d.rootComponent.occurrences if o.component.name == host_name][0]
    coll = adsk.core.ObjectCollection.create()
    new = set()
    comp_new = {}

    def walk(o, is_new):
        for b in o.bRepBodies:
            if b.name.startswith('ZONE'):
                continue
            bb = b.boundingBox
            if bb.maxPoint.y < 0.85:            # only things behind the panel back can meet the storage
                continue
            coll.add(b)
        if o != host:
            n = o.component.name
            comp_new[n] = is_new if n not in comp_new or comp_new[n] == is_new else None   # None = shared, ambiguous
        for c in o.childOccurrences:
            walk(c, is_new or 'pod' in c.name)
    walk(host, False)
    ii = d.createInterferenceInput(coll); ii.areCoincidentFacesIncluded = False
    res = d.analyzeInterference(ii)
    hits = []
    for r in (res or []):
        a, b = r.entityOne, r.entityTwo
        def isnew(e):
            if e.name.startswith(NEW):
                return True
            return comp_new.get(e.parentComponent.name, False)
        na = isnew(a); nb = isnew(b)
        if na is None or nb is None:
            hits.append('?ambiguous %s/%s x %s/%s' % (a.parentComponent.name[:15], a.name[:15], b.parentComponent.name[:15], b.name[:15]))
            continue
        if na == nb:
            continue
        v = r.interferenceBody.volume * 1000
        bb = r.interferenceBody.boundingBox
        hits.append('%s x %s %.0f mm3 at u %.0f z %.0f' % (a.name[:26], b.name[:26], v, (bb.minPoint.x + bb.maxPoint.x) * 5 + 460, (bb.minPoint.z + bb.maxPoint.z) * 5))
    print(host_name, 'bodies', coll.count,  'hits', len(hits), hits[:12])
    return hits


def run(_context: str):
    check('Right half')
