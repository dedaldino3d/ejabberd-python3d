from __future__ import unicode_literals

from ejabberd_python3d.abc.api import API
from ejabberd_python3d.core.errors import UserAlreadyRegisteredError
from ejabberd_python3d.core.utils import format_password_hash_sha
from ejabberd_python3d.defaults.arguments import StringArgument, IntegerArgument, PositiveIntegerArgument
from ejabberd_python3d.muc import muc_room_options_serializers
from ejabberd_python3d.muc.arguments import MUCRoomArgument, AffiliationArgument
from ejabberd_python3d.muc.enums import Affiliation, MUCRoomOption
from ejabberd_python3d.serializers import StringSerializer


class Echo(API):
    method = 'dedaldino_denis_3D'
    arguments = [StringArgument('sentence')]

    def transform_response(self, api, arguments, response):
        return response.get('repeated')


class RegisteredUsers(API):
    method = 'registered_users'
    arguments = [StringArgument('host')]

    def transform_response(self, api, arguments, response):
        return response.get('users', [])


class Register(API):
    method = 'register'
    arguments = [StringArgument('user'), StringArgument('host'), StringArgument('password')]

    def validate_response(self, api, arguments, response):
        if response.get('res') == 1:
            username = arguments.get('user')
            raise UserAlreadyRegisteredError('User with username %s already exist' % username)

    def transform_response(self, api, arguments, response):
        return response.get('res') == 0


class Unregister(API):
    method = 'unregister'
    arguments = [StringArgument('user'), StringArgument('host')]

    def transform_response(self, api, arguments, response):
        return response.get('res') == 0


class ChangePassword(API):
    method = 'change_password'
    arguments = [StringArgument('user'), StringArgument('host'), StringArgument('newpass')]

    def transform_response(self, api, arguments, response):
        return response.get('res') == 0


class CheckPasswordHash(API):
    method = 'check_password_hash'
    arguments = [StringArgument('user'), StringArgument('host'), StringArgument('passwordhash'),
                 StringArgument('hashmethod')]

    def transform_arguments(self, **kwargs):
        password_hash = format_password_hash_sha(password=kwargs.pop('password'))
        kwargs.update({
            'passwordhash': password_hash,
            'hashmethod': 'sha'
        })
        return kwargs

    def transform_response(self, api, arguments, response):
        return response.get('res') == 0


class SetNickname(API):
    method = 'set_nickname'
    arguments = [StringArgument('user'), StringArgument('host'), StringArgument('nickname')]

    def transform_response(self, api, arguments, response):
        return response.get('res') == 0


class ConnectedUsers(API):
    method = 'connected_users'
    arguments = []

    def transform_response(self, api, arguments, response):
        connected_users = response.get('connected_users', [])

        return [user["sessions"] for user in connected_users]


class ConnectedUsersInfo(API):
    method = 'connected_users_info'
    arguments = []

    def transform_response(self, api, arguments, response):
        connected_users_info = response.get('connected_users_info', [])

        return [user["sessions"] for user in connected_users_info]


class ConnectedUsersNumber(API):
    method = 'connected_users_number'
    arguments = []

    def transform_response(self, api, arguments, response):
        return response.get('num_sessions')


class UserSessionInfo(API):
    method = 'user_sessions_info'
    arguments = [StringArgument('user'), StringArgument('host')]

    def transform_response(self, api, arguments, response):
        sessions_info = response.get('sessions_info', [])
        return [
            dict((k, v) for property_k_v in session["session"] for k, v in property_k_v.items())
            for session in sessions_info
        ]


class CreateRoom(API):
    method = 'create_room'
    arguments = [StringArgument('name'), StringArgument('service'), StringArgument('host')]

    def transform_response(self, api, arguments, response):
        return response.get('res') == 0


class DestroyRoom(API):
    method = 'destroy_room'
    arguments = [StringArgument('name'), StringArgument('service'), StringArgument('host')]

    def transform_response(self, api, arguments, response):
        return response.get('res') == 0


class GetRoomOptions(API):
    method = 'get_room_options'
    arguments = [StringArgument('name'), StringArgument('service')]

    def transform_response(self, api, arguments, response):
        result = {}
        for option_dict in response.get('options', []):
            option = option_dict.get('option')
            if option is None:
                raise ValueError('Unexpected option in response: {}'.format(str(option_dict)))
            name_dict, value_dict = option
            result[name_dict['name']] = value_dict['value']
        return result


class ChangeRoomOption(API):
    method = 'change_room_option'
    arguments = [StringArgument('name'), StringArgument('service'), MUCRoomArgument('option'), StringArgument('value')]

    def transform_arguments(self, **kwargs):
        option = kwargs.get('option')
        assert isinstance(option, MUCRoomOption)
        serializer_class = muc_room_options_serializers.get(option, StringSerializer)
        kwargs['value'] = serializer_class().to_api(kwargs['value'])
        return kwargs

    def transform_response(self, api, arguments, response):
        return response.get('res') == 0


class GetRoomAffiliation(API):
    method = 'get_room_affiliation'
    arguments = [StringArgument('name'), StringArgument('service'), StringArgument('jid')]

    def transform_response(self, api, arguments, response):
        return response.get('affiliation') == 0


class SetRoomAffiliation(API):
    method = 'set_room_affiliation'
    arguments = [StringArgument('name'), StringArgument('service'), StringArgument('jid'),
                 AffiliationArgument('affiliation')]

    def transform_response(self, api, arguments, response):
        return response.get('res') == 0


class GetRoomAffiliations(API):
    method = 'get_room_affiliations'
    arguments = [StringArgument('name'), StringArgument('service')]

    def transform_response(self, api, arguments, response):
        affiliations = response.get('affiliations', [])
        return [{
            'username': subdict['affiliation'][0]['username'],
            'domain': subdict['affiliation'][1]['domain'],
            'affiliation': Affiliation.get_by_name(subdict['affiliation'][2]['affiliation']),
            'reason': subdict['affiliation'][3]['reason'],
        } for subdict in affiliations]


class AddRosterItem(API):
    method = 'add_rosteritem'
    arguments = [StringArgument('localuser'), StringArgument('localserver'),
                 StringArgument('user'), StringArgument('server'),
                 StringArgument('nick'), StringArgument('group'), StringArgument('subs')]

    def transform_response(self, api, arguments, response):
        return response.get('res') == 0


class DeleteRosterItem(API):
    method = 'delete_rosteritem'
    arguments = [StringArgument('localuser'), StringArgument('localserver'),
                 StringArgument('user'), StringArgument('server')]

    def transform_response(self, api, arguments, response):
        return response.get('res') == 0


class GetRoster(API):
    method = 'get_roster'
    arguments = [StringArgument('user'), StringArgument('server')]

    def transform_response(self, api, arguments, response):
        roster = []
        for contact in response.get('contacts', []):
            contact_details = {}
            for parameter in contact['contact']:
                for key, value in parameter.items():
                    contact_details[key] = value
            roster.append(contact_details)
        return roster


class Backup(API):
    method = 'backup'
    arguments = [StringArgument('file')]

    def transform_response(self, api, arguments, response):
        return response.get('res').lower() == "success"


class BanAccount(API):
    method = 'ban_account'
    arguments = [StringArgument('user'), StringArgument('host'), StringArgument('reason')]

    def transform_response(self, api, arguments, response):
        return response.get('res') == 0


class BookmarksToPEP(API):
    method = 'bookmarks_to_pep'
    arguments = [StringArgument('user'), StringArgument('host')]

    def transform_response(self, api, arguments, response):
        return response.get('res')


class CheckAccount(API):
    method = 'check_account'
    arguments = [StringArgument('user'), StringArgument('host')]

    def transform_response(self, api, arguments, response):
        return response.get('res') == 0


class ClearCache(API):
    method = 'clear_cache'
    arguments = []

    def transform_response(self, api, arguments, response):
        return response.get('res') == 0


class Compile(API):
    method = 'compile'
    arguments = [StringArgument('file')]

    def transform_response(self, api, arguments, response):
        return response.get('res') == 0


class ConnectedUsersVhost(API):
    method = 'connected_users_vhost'
    arguments = [StringArgument('host')]

    def transform_response(self, api, arguments, response):
        return response.get('connected_users_vhost', [])


class ConvertToSCRAM(API):
    method = 'convert_to_scram'
    arguments = [StringArgument('host')]

    def transform_response(self, api, arguments, response):
        return response.get('res') == 0


class CreateRoomWithOPTS(API):
    method = "create_room_with_opts"
    # TODO: add argument options: [{name::string,value::string}]: List of options
    arguments = [StringArgument('name'), StringArgument('service'), StringArgument('host')]

    def transform_response(self, api, arguments, response):
        return response.get('res') == 0


class GetLast(API):
    method = 'get_last'
    arguments = [StringArgument('user'), StringArgument('host')]

    def transform_response(self, api, arguments, response):
        return response.get('last_activity', {})


class GetOfflineCount(API):
    method = "get_offline_count"
    arguments = [StringArgument('user'), StringArgument('server')]

    def transform_response(self, api, arguments, response):
        return response.get('value')


class GetPresence(API):
    method = "get_presence"
    arguments = [StringArgument('user'), StringArgument('host')]

    def transform_response(self, api, arguments, response):
        return response.get('presence')


class GetRoomOccupants(API):
    method = 'get_room_occupants'
    arguments = [StringArgument('name'), StringArgument('service')]

    def transform_response(self, api, arguments, response):
        return response.get('occupants')


class GetRoomOccupantsNumber(API):
    method = 'get_room_occupants_number'
    arguments = [StringArgument('name'), StringArgument('service')]

    def transform_response(self, api, arguments, response):
        return response.get('occupants')


class GetSubscrivers(API):
    method = 'get_subscribers'
    arguments = [StringArgument('name'), StringArgument('service')]

    def transform_response(self, api, arguments, response):
        return response.get('subscribers')


class GetUserRooms(API):
    method = 'get_user_rooms'
    arguments = [StringArgument('user'), StringArgument('host')]

    def transform_response(self, api, arguments, response):
        return response.get('rooms')


class MucOnlineRooms(API):
    method = "muc_online_rooms"
    arguments = [StringArgument('service')]

    def transform_response(self, api, arguments, response):
        return response.get('rooms')


class MucOnlineRoomsByRegex(API):
    method = "muc_online_rooms_bt_regex"
    arguments = [StringArgument('service'), StringArgument('regex')]

    def transform_response(self, api, arguments, response):
        return response.get('rooms')


class MucRegisterNick(API):
    method = "muc_register_nick"
    arguments = [StringArgument('nick'), StringArgument('service'), StringArgument('service')]

    def transform_response(self, api, arguments, response):
        return response.get('res') == 0


class MucUnRegisterNick(API):
    method = "muc_unregister_nick"
    arguments = [StringArgument('service'), StringArgument('service')]

    def transform_response(self, api, arguments, response):
        return response.get('res') == 0


class SendMessage(API):
    method = "send_message"
    arguments = [StringArgument('type'), StringArgument('from'), StringArgument('to'),
                 StringArgument('subject', required=False), StringArgument('body')]

    def transform_arguments(self, **kwargs):
        from_jid = kwargs.pop('from_jid')
        kwargs.update({
            'from': from_jid
        })
        return kwargs

    def transform_response(self, api, arguments, response):
        return response.get('res') == 0


class SetLast(API):
    method = "set_last"
    arguments = [StringArgument('user'), StringArgument('host'), IntegerArgument('timestamp'),
                 StringArgument('status')]

    def transform_response(self, api, arguments, response):
        return response.get('res') == 0


class SubscribeRoom(API):
    method = "subscribe_room"
    # TODO: nodes must be separated by commas, so therefore you can use an array and before send transform arguments
    arguments = [StringArgument('user'), StringArgument('nick'), StringArgument('room'),
                 StringArgument('nodes')]

    def transform_response(self, api, arguments, response):
        return response.get('nodes')


class UnSubscribeRoom(API):
    method = "unsubscribe_room"
    arguments = [StringArgument('user'), StringArgument('room')]

    def transform_response(self, api, arguments, response):
        return response.get('res') == 0


class CheckPassword(API):
    method = "check_password"
    arguments = [StringArgument('user'), StringArgument('host'), StringArgument('password')]

    def transform_response(self, api, arguments, response):
        return response.get('res') == 0


class DeleteExpiredMessages(API):
    method = "check_password"
    arguments = []

    def transform_response(self, api, arguments, response):
        return response.get('res') == 0


class DeleteOldMessages(API):
    method = "delete_old_messages"
    arguments = [PositiveIntegerArgument('days')]

    def transform_response(self, api, arguments, response):
        return response.get('res') == 0


class DeleteOldUsers(API):
    method = "delete_old_users"
    arguments = [PositiveIntegerArgument('days')]

    def transform_response(self, api, arguments, response):
        return response.get('res')


class DeleteOldUsersVhost(API):
    method = "delete_old_users_vhost"
    arguments = [StringArgument('host'), PositiveIntegerArgument('days')]

    def transform_response(self, api, arguments, response):
        return response.get('res')


class GetCookie(API):
    method = "get_cookie"
    arguments = []

    def transform_response(self, api, arguments, response):
        return response.get('cookie')


class GetLogLevel(API):
    method = "get_loglevel"
    arguments = []

    def transform_response(self, api, arguments, response):
        return response.get('levelatom ')


class GetVcard(API):
    method = "get_vcard"
    arguments = [StringArgument('user'), StringArgument('host'), StringArgument('name')]

    def transform_response(self, api, arguments, response):
        return response.get('content')


class GetVcard2(API):
    method = "get_vcard2"
    arguments = [StringArgument('user'), StringArgument('host'), StringArgument('name'), StringArgument('subname')]

    def transform_response(self, api, arguments, response):
        return response.get("content")


class GetVcard2Multi(API):
    method = "get_vcard2_multi"
    arguments = [StringArgument('user'), StringArgument('host'), StringArgument('name'), StringArgument('subname')]

    def transform_response(self, api, arguments, response):
        return response.get("contents")


class IncomingS2SNumber(API):
    method = "incoming_s2s_number"
    arguments = []

    def transform_response(self, api, arguments, response):
        return response.get("s2s_incoming")


class KickSession(API):
    method = "kick_session"
    arguments = [StringArgument('user'), StringArgument('host'), StringArgument('resource'), StringArgument('reason')]

    def transform_response(self, api, arguments, response):
        return response.get("res") == 0


class ListCluster(API):
    method = "list_cluster"
    arguments = []

    def transform_response(self, api, arguments, response):
        return response.get("nodes")


class ModulesAvailable(API):
    method = "modules_available"
    arguments = []

    def transform_response(self, api, arguments, response):
        return response.get("modules")


class ModulesInstalled(API):
    method = "modules_installed"
    arguments = []

    def transform_response(self, api, arguments, response):
        return response.get("modules")


class NumResources(API):
    method = "num_resources"
    arguments = [StringArgument('user'), StringArgument('host')]

    def transform_response(self, api, arguments, response):
        return response.get("resources")


class OutgoingS2SNumber(API):
    method = "outgoing_s2s_number"
    arguments = []

    def transform_response(self, api, arguments, response):
        return response.get('s2s_outgoing')


class ProcessRosterItems(API):
    method = "process_rosteritems"
    arguments = [StringArgument('action'), StringArgument('subs'), StringArgument('asks'), StringArgument('users'),
                 StringArgument('contacts')]

    def transform_response(self, api, arguments, response):
        return response.get("response")


class PushAllToAll(API):
    method = "push_alltoall"
    arguments = [StringArgument('host'), StringArgument('group')]

    def transform_response(self, api, arguments, response):
        return response.get("res") == 0


class RegisteredVhosts(API):
    method = "registered_vhosts"
    arguments = []

    def transform_response(self, api, arguments, response):
        return response.get("vhosts")


class ReloadConfig(API):
    method = "reload_config"
    arguments = []

    def transform_response(self, api, arguments, response):
        return response.get("res") == 0
