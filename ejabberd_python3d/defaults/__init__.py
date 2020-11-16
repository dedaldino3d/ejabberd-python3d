from ejabberd_python3d.serializers import StringSerializer

from .enums import LogLevelOptions

loglevel_options_serializers = {
    LogLevelOptions.none: StringSerializer,
    LogLevelOptions.alert: StringSerializer,
    LogLevelOptions.emergency: StringSerializer,
    LogLevelOptions.error: StringSerializer,
    LogLevelOptions.critical: StringSerializer,
    LogLevelOptions.debug: StringSerializer,
    LogLevelOptions.info: StringSerializer,
    LogLevelOptions.notice: StringSerializer,
    LogLevelOptions.warning: StringSerializer,
}
