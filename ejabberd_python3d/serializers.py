from abc import ABCMeta, abstractmethod
from six import string_types

from .abc.api import Enum, APIArgumentSerializer


class StringSerializer(APIArgumentSerializer):
    def to_api(self, value):
        if not isinstance(value, string_types):
            raise ValueError("Expects str or unicode, but got {}".format(type(value)))
        return value

    def to_builtin(self, value):
        if not isinstance(value, string_types):
            raise ValueError("Expects str or unicode, but got {}".format(type(value)))
        return value


class IntegerSerializer(APIArgumentSerializer):
    def to_api(self, value):
        if not isinstance(value, int):
            raise ValueError("Expects int or long, but got {}".format(type(value)))
        return str(value)

    def to_builtin(self, value):
        return int(value)


class PositiveIntegerSerializer(IntegerSerializer):
    def to_api(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Expects positive int or long, but got {}".format(type(value)))
        return super(PositiveIntegerSerializer, self).to_api(value)

    def to_builtin(self, value):
        res = super(PositiveIntegerSerializer, self).to_builtin(value)
        if res < 0:
            raise ValueError("Expects positive int or long, but got {}".format(type(value)))
        return res


class BooleanSerializer(APIArgumentSerializer):
    def to_api(self, value):
        if not isinstance(value, bool):
            raise ValueError("Expects boolean")
        return 'true' if value else 'false'

    def to_builtin(self, value):
        if value not in ('true', 'false'):
            raise ValueError("Expects true|false, but got {}".format(type(value)))
        return value == 'true'


class EnumSerializer(ABCMeta, StringSerializer):
    @abstractmethod
    @property
    def enum_class(self):
        pass

    def to_api(self, value):
        assert issubclass(self.enum_class, Enum)
        if isinstance(value, self.enum_class):
            return value.name
        elif isinstance(value, string_types):
            return value
        elif isinstance(value, int):
            return self.enum_class.get_by_value(value).name
        raise ValueError("Invalid value for enum %s: %s" % (self.enum_class, value))

    def to_builtin(self, value):
        assert issubclass(self.enum_class, Enum)
        if not isinstance(value, string_types):
            raise ValueError("Expects str or unicode , but got {}".format(type(value)))
        res = self.enum_class.get_by_name(value)
        if res is None:
            raise ValueError("Expects enum value for {}, but got {}".format(self.enum_class, type(value)))
