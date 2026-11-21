# Save the cockpit design by NAME (never "whatever document is active") with a version comment.
import adsk.core

DESIGN = 'Folding Cockpit Case'


def save(comment):
    app = adsk.core.Application.get()
    docs = [d for d in app.documents if d.name.startswith(DESIGN)]
    if not docs:
        raise RuntimeError('%s is not open in Fusion' % DESIGN)
    doc = docs[0]
    if app.activeDocument != doc:
        raise RuntimeError('%s is open but not active (active: %s); not saving to avoid touching the wrong design'
                           % (doc.name, app.activeDocument.name))
    return doc.save(comment)
