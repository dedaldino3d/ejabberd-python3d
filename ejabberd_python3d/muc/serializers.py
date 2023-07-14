# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
from six import string_types

from ..serializers import EnumSerializer
from .enums import MUCRoomOption, AllowVisitorPrivateMessage, Affiliation, MUCNodes


class MUCRoomOptionSerializer(EnumSerializer):
    enum_class = MUCRoomOption


class AllowVisitorPrivateMessageSerializer(EnumSerializer):
    enum_class = AllowVisitorPrivateMessage


class AffiliationSerializer(EnumSerializer):
    enum_class = Affiliation


class MUCNodesSerializer(EnumSerializer):
    enum_class = MUCNodes

    def to_api(self, value):
        if isinstance(value, self.enum_class):
            return value.value
        if isinstance(value, string_types):
            return value
        elif isinstance(value, int):
            return self.enum_class.get_by_value(value).name
        raise ValueError("Invalid value for enum %s: %s" % (self.enum_class, value))

    def to_builtin(self, value):
        if not isinstance(value, string_types):
            raise ValueError("Expects str or unicode , but got {}".format(type(value)))
        res = self.enum_class.get_by_name(value)
        if res is None:
            raise ValueError("Expects enum value for {}, but got {}".format(self.enum_class, type(value)))
