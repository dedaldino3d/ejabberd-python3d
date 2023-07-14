# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..abc.api import APIArgument
from .serializers import MUCRoomOptionSerializer, AffiliationSerializer, MUCNodesSerializer


class MUCRoomArgument(APIArgument):
    serializer_class = MUCRoomOptionSerializer


class AffiliationArgument(APIArgument):
    serializer_class = AffiliationSerializer


class MUCNodesArgument(APIArgument):
    serializer_class = MUCNodesSerializer
