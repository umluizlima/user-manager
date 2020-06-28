from . import users


def configure(app, settings):
    for router in [users]:
        router.configure(app, settings)
