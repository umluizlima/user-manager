from . import authentication, users


def configure(app, settings):
    for router in [authentication, users]:
        router.configure(app, settings)
