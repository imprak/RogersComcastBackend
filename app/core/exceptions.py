class BackendError(Exception):
    pass


class NotFoundError(BackendError):
    pass


class ConflictError(BackendError):
    pass


class BadRequestError(BackendError):
    pass


class AuthenticationError(BackendError):
    pass



