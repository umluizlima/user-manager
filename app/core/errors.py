class Error(Exception):
    pass


class ResourceNotFoundError(Error):
    pass


class ResourceAlreadyExistsError(Error):
    pass
