import adsk.core


def look(eye, target=(0, -10, 12), extents=140):
    app = adsk.core.Application.get()
    vp = app.activeViewport
    cam = vp.camera
    cam.isSmoothTransition = False
    cam.cameraType = adsk.core.CameraTypes.OrthographicCameraType
    cam.target = adsk.core.Point3D.create(*target)
    cam.eye = adsk.core.Point3D.create(*eye)
    cam.upVector = adsk.core.Vector3D.create(0, 0, 1)
    cam.viewExtents = extents
    vp.camera = cam
    vp.refresh()
