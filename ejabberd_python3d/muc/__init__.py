# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..serializers import BooleanSerializer, StringSerializer, PositiveIntegerSerializer
from .serializers import AllowVisitorPrivateMessageSerializer
from .enums import MUCRoomOption, MUCNodes

muc_room_options_serializers = {
    MUCRoomOption.allow_change_subj: BooleanSerializer,
    MUCRoomOption.allow_private_messages: BooleanSerializer,
    MUCRoomOption.allow_private_messages_from_visitors: AllowVisitorPrivateMessageSerializer,
    MUCRoomOption.allow_query_users: BooleanSerializer,
    MUCRoomOption.allow_user_invites: BooleanSerializer,
    MUCRoomOption.allow_visitor_nickchange: BooleanSerializer,
    MUCRoomOption.allow_visitor_status: BooleanSerializer,
    MUCRoomOption.anonymous: BooleanSerializer,
    MUCRoomOption.captcha_protected: BooleanSerializer,
    MUCRoomOption.logging: BooleanSerializer,
    MUCRoomOption.max_users: PositiveIntegerSerializer,
    MUCRoomOption.members_by_default: BooleanSerializer,
    MUCRoomOption.members_only: BooleanSerializer,
    MUCRoomOption.moderated: BooleanSerializer,
    MUCRoomOption.password: StringSerializer,
    MUCRoomOption.password_protected: BooleanSerializer,
    MUCRoomOption.persistent: BooleanSerializer,
    MUCRoomOption.public: BooleanSerializer,
    MUCRoomOption.public_list: BooleanSerializer,
    MUCRoomOption.title: StringSerializer
}

mucsub_room_nodes = {
    MUCNodes.mucsub_affiliations: StringSerializer,
    MUCNodes.mucsub_messages: StringSerializer,
    MUCNodes.mucsub_presence: StringSerializer,
    MUCNodes.mucsub_config: StringSerializer,
    MUCNodes.mucsub_subject: StringSerializer,
    MUCNodes.mucsub_subscribers: StringSerializer,
    MUCNodes.mucsub_system: StringSerializer
}
