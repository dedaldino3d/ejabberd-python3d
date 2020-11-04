


class ConnectionError(Exception):
    """Error when connecting to API"""
    pass


class AccessDeniedError(Exception):
    """Access denied, account unprevileged"""
    pass


class MissingArguments(Exception):
    """Missing arguments in call"""


class BadArgument(Exception):
    """Wrong Argument"""
    pass