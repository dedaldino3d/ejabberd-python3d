

class ConnectionError(Exception):
    """Error when connecting to API"""
    pass


class AccessDeniedError(Exception):
    """Access denied, account unprevileged"""
    pass


class MissingArguments(ValueError):
    """Missing arguments in call"""


class BadArgument(ValueError):
    """Wrong Argument"""
    pass
