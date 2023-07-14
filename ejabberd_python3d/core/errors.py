class ConnectionError(Exception):
    """Error when connecting to API"""
    pass


class AccessDeniedError(Exception):
    """Access denied, account unprivileged"""
    pass


class MissingArguments(ValueError):
    """Missing arguments in call"""
    pass


class BadArgument(ValueError):
    """Wrong Argument"""
    pass


class UserAlreadyRegisteredError(Exception):
    """User already registered"""
    pass
