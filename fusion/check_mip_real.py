# Fold check of the MIP layout with the REAL 737DIYSIM module bodies (not envelopes).
import importlib.util, time
import adsk.core, adsk.fusion

BASE = r'D:/Admin/Documents/Projects/FlightSimCase/fusion/'


def load(n):
    spec = importlib.util.spec_from_file_location(n, BASE + n + '.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def check(angles=((90, 90),), include_panels=True):
    t = load('tools'); rm = load('run_mip'); rm.setup(t)
    d = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    coll = adsk.core.ObjectCollection.create()
    groups = []
    tok = {}

    rm.fold(t, 0, 0)

    comp_host = {}

    def add_all(o, tag):
        comp_host[o.component.name] = tag
        for b in o.bRepBodies:
            if b.boundingBox.minPoint.y < -0.05:      # only parts in front of the panel face can collide
                coll.add(b); groups.append(tag); tok[b.entityToken] = tag
        for c in o.childOccurrences:
            add_all(c, tag)
    for o in d.rootComponent.occurrences:
        if o.component.name in ('Left half', 'Spacer', 'Right half'):
            if include_panels:
                for b in o.bRepBodies:
                    if b.name.startswith(('PANEL', 'ALU', 'PRINT')):
                        coll.add(b); groups.append(o.component.name); tok[b.entityToken] = o.component.name
            for ch in o.childOccurrences:
                add_all(ch, o.component.name)
    out = {}
    for sp, lh in angles:
        t0 = time.time()
        rm.fold(t, sp, lh)
        ii = d.createInterferenceInput(coll); ii.areCoincidentFacesIncluded = False
        res = d.analyzeInterference(ii)
        hits = []
        unk = 0
        dbg = []
        if res:
            for r in res:
                def host_of(e):
                    n = e.parentComponent.name
                    if n in ('Left half', 'Spacer', 'Right half'):
                        return n
                    return comp_host.get(n, '?' + n)
                ha = host_of(r.entityOne); hb = host_of(r.entityTwo)
                if len(dbg) < 6:
                    dbg.append((ha, r.entityOne.name[:20], hb, r.entityTwo.name[:20]))
                if '?' in (ha, hb):
                    unk += 1
                if ha == hb:
                    continue
                pa = r.entityOne.name; pb = r.entityTwo.name
                hits.append('%s/%s x %s/%s %.0f mm3' % (ha, pa[:25], hb, pb[:25], r.interferenceBody.volume * 1000))
        out[(sp, lh)] = hits
        print('fold', sp, lh, 'bodies', coll.count, 'secs', round(time.time() - t0), 'hits', len(hits), 'unmatched', unk, 'raw', (res.count if res else 0), hits[:4], dbg)
    rm.fold(t, 0, 0)
    return out


def run(_context: str):
    check()
