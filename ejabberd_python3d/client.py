from __future__ import print_function

import copy
from urllib.parse import urlparse
from xmlrpc import client as xmlrpc_client

from ejabberd_python3d.abc import methods
from ejabberd_python3d.abc.api import API, APIArgument, EjabberdBaseAPI
from ejabberd_python3d.core.errors import MissingArguments
from ejabberd_python3d.defaults.constants import XMLRPC_API_PROTOCOL, XMLRPC_API_SERVER, \
    XMLRPC_API_PORT


# noinspection PyTypeChecker
class EjabberdAPIClient(EjabberdBaseAPI):
    """
    Python client for Ejabberd XML-RPC Administration API.
    """

    def __init__(self, host, username, password, server=XMLRPC_API_SERVER, port=XMLRPC_API_PORT,
                 protocol=XMLRPC_API_PROTOCOL, admin=True, verbose=False):
        """
        Init XML-RPC server proxy.
        """
        self.host = host
        self.username = username
        self.password = password
        self.server = server
        self.port = port
        self.admin = admin
        self.protocol = protocol
        self.verbose = verbose
        self._server_proxy = None

    @staticmethod
    def get_instance(service_url, verbose=False):
        """
        Return a EjabberdAPIClient instance based on a '12factor app' compliant service_url

        :param service_url: A connection string in the format:
            <http|https>://<username>:<password>@<host>(:port)/user_domain
        :type service_url: str|unicode
        :param verbose:
        :type verbose: bool
        :return: EjabberdAPIClient instance
        """
        format_error = "expects service_url like https://username:password@HOST:PORT/DOMAIN"

        o = urlparse(service_url)
        protocol = o.scheme
        assert protocol in ('http', 'https'), format_error

        netloc_parts = o.netloc.split('@')
        assert len(netloc_parts) == 2, format_error

        auth, server = netloc_parts
        auth_parts = auth.split(':')
        assert len(auth_parts) == 2, format_error

        username, password = auth_parts
        server_parts = server.split(':')
        assert len(server_parts) <= 2, format_error

        if len(server_parts) == 2:
            host, port = server_parts
            port = int(port)
        else:
            host, port = server_parts[0], XMLRPC_API_PORT
        path_parts = o.path.lstrip('/').split('/')
        assert len(path_parts) == 1, format_error

        server = path_parts[0]
        return EjabberdAPIClient(host, username, password, server, port, protocol=protocol, verbose=verbose)

    @property
    def service_url(self):
        """
        Returns the FQDN to the Ejabberd server's XML-RPC endpoint
        """
        # TODO: add endpoint parameter
        return "{}://{}:{}".format(self.protocol, self.host, self.port)

    @property
    def server_proxy(self):
        """
        Returns the proxy object that is used to perform the calls to the XML-RPC endpoint
        """
        if self._server_proxy is None:
            self._server_proxy = xmlrpc_client.ServerProxy(self.service_url, verbose=(1 if self.verbose else 0))
        return self._server_proxy

    @property
    def auth(self):
        """
        Returns a dictionary containing the basic authorization info
        """
        return {
            'user': self.username,
            'server': self.server,
            'password': self.password,
            'admin': self.admin
        }

    def _validate_and_serialize_arguments(self, api_class, arguments):
        """
        Internal method to validate and serialize arguments
        :param api_class: An instance of an API class
        :type api_class: API
        :param arguments: A dictionary of arguments that will be passed to the method
        :type arguments: dict
        :return: The serialized arguments
        :rtype: dict
        """
        ser_args = {}

        for i in range(len(api_class.arguments)):
            arg_desc = api_class.arguments[i]
            assert isinstance(arg_desc, APIArgument)

            # validate argument presence
            arg_name = str(arg_desc.name)
            if arg_desc.required and arg_name not in arguments:
                raise MissingArguments("Missing required argument '%s'" % arg_name)

            # serialize argument value
            ser_args[arg_desc.name] = arg_desc.serializer_class().to_api(arguments.get(arg_name))

        return ser_args

    def _report_method_call(self, method, arguments):
        """
        Internal method to print info about a method call

        :param method: The name of the method to call
        :type method: str|unicode
        :param arguments: A dictionary of arguments that will be passed to the method
        :type: arguments: dict
        """
        if self.verbose:
            print("===> %s(%s)" % (method, ', '.join(['%s=%s' % (k, v) for k, v in arguments.items()])))

    def _call_api(self, api_class, **kwargs):
        """
        Internal method used to perform api calls

        :param api_class:
        :type api_class: API
        :param kwargs:
        :type kwargs: dict
        :rtype: object
        :return: Return value of the XMLRPC Method call
        """

        # validate api_class
        assert issubclass(api_class, API)

        # create api instance
        api = api_class()
        # copy arguments
        args = copy.copy(kwargs)

        # transform arguments
        args = api.transform_arguments(**args)
        # validate and serialize arguments
        args = self._validate_and_serialize_arguments(api, args)
        # retrieve method
        try:
            method = getattr(self.server_proxy, str(api.method))
        except xmlrpc_client.Fault as e:
            # TODO: add it to logger
            raise Exception(f"{e.faultString} - code: {e.faultCode}")

        # print method call with arguments
        self._report_method_call(api.method, args)

        # perform call
        try:
            if not api.authenticate:
                response = method(args)
            else:
                response = method(self.auth, args)
        except xmlrpc_client.Fault as e:
            raise Exception(f"{e.faultString} - code: {e.faultCode}")

        # validate response
        api.validate_response(api, args, response)
        # transform response
        result = api.transform_response(api, args, response)
        return result

    def echo(self, sentence):
        """Echo the input back"""
        return self._call_api(methods.Echo, sentence=sentence)

    def registered_users(self, host):
        """
        List all registered users in the host

        :param host: The XMPP_DOMAIN
        :type host: str|unicode
        :rtype: Iterable
        :return: A List of registered accounts usernames
        """
        return self._call_api(methods.RegisteredUsers, host=host)

    def register(self, user, host, password):
        """
        Register a user to the ejabberd server

        :param user: The username for the new user
        :type user: str|unicode
        :param host: The XMPP_DOMAIN
        :type host: str|unicode
        :param password: The password for the new user
        :type password: str|unicode
        :rtype: bool
        :return: A boolean indicating if the registration has succeeded
        """
        return self._call_api(methods.Register, user=user, host=host, password=password)

    def unregister(self, user, host):
        """
        Unregister a user from the ejabberd server

        :param user: The username for the new user
        :type user: str|unicode
        :param host: The XMPP_DOMAIN
        :type host: str|unicode
        :rtype: bool
        :return: A boolean indicating if user unregistered
        """
        return self._call_api(methods.Unregister, user=user, host=host)

    def change_password(self, user, host, newpass):
        """
        Change the password for a given user

        :param user: The username for the user we want to change the password for
        :type user: str|unicode
        :param host: The XMPP_DOMAIN
        :type host: str|unicode
        :param newpass: The new password
        :type newpass: str|unicode
        :rtype: bool
        :return: A boolean indicating if the password change has succeeded
        """
        return self._call_api(methods.ChangePassword, user=user, host=host, newpass=newpass)

    def check_password_hash(self, user, host, password):
        """
        Checks whether a password is correct for a given user. The used hash-method is fixed to sha1.

        :param user: The username for the user we want to check the password for
        :type user: str|unicode
        :param host: The XMPP_DOMAIN
        :type host: str|unicode
        :param password: The password we want to check for the user
        :type password: str|unicode
        :return: A boolean indicating if the given password matches the user's password
        :rtype: bool
        """
        return self._call_api(methods.CheckPasswordHash, user=user, host=host, password=password)

    def add_rosteritem(self,
                       localuser, localhost,
                       user, host,
                       nick="", group="", subs="to"):
        """
        Add an item to a user's roster
        Group can be several groups separated by ; for example: "g1;g2;g3"

        :param localuser: User name
        :type localuser: str
        :param localhost:Server name
        :type localhost: str
        :param user: Contact user name
        :type user: str
        :param host: Contact server name
        :type host: str
        :param nick: Nickname, default: ""
        :type nick: str
        :param group: Subscription, default: ""
        :type group: str
        :param subs: Subscription, default: ""
        :type subs: str
        :return: Status code
        :rtype: bool
        """
        return self._call_api(methods.AddRosterItem, localuser=localuser,
                              localhost=localhost,
                              user=user,
                              host=host,
                              nick=nick,
                              group=group,
                              subs=subs)

    def backup(self, file):
        """
        Store the database to backup file
        :param file: Full path for the destination backup file
        :type file: str
        :return: raw string result
        :rtype: str
        """
        return self._call_api(methods.Backup, file=file)

    def ban_account(self, user, host, reason):
        """
        Ban an account: kick sessions and set random password

        :param user: User name to ban
        :type user: str
        :param host: Server name
        :type host: str
        :param reason: Reason for banning user
        :type reason: str
        :return: Status code
        :rtype: True on success, False otherwise)
        """
        return self._call_api(methods.BanAccount, user=user,
                              host=host,
                              reason=reason)

    def check_account(self, user, host):
        """
        Check if an account exists or not

        :param user: User name to check
        :type user: str
        :param host: Server to check
        :type host: str
        :return: Status code
        :rtype: True on success, False otherwise)
        """
        return self._call_api(methods.CheckAccount, user=user, host=host)

    def check_password(self, user, host, password):
        """
        Check if a password is correct

        :param user: User name to check
        :type user: str
        :param host: Server to check
        :type host: str
        :param password: Password to check
        :type password: str
        :return: Status code
        :rtype: True on success, False otherwise)
        """
        return self._call_api(methods.CheckPassword, user=user,
                              host=host,
                              password=password)

    # TODO def compile(self, file):
    # Recompile and reload Erlang source code file

    def connected_users(self):
        """
        List all established sessions

        :return: List of users sessions
        :rtype: list
        """
        return self._call_api(methods.ConnectedUsers)

    def connected_users_info(self):
        """
        List all established sessions and their information

        :return: A dict with established connections
        :rtype: list
        """
        return self._call_api(methods.ConnectedUsersInfo)

    def connected_users_number(self):
        """
        Get the number of established sessions

        :return: Number of established sessions
        :rtype: int
        """
        return self._call_api(methods.ConnectedUsersNumber)

    def connected_users_vhost(self, host):
        """
        Get the list of established sessions in a vhost

        :param host: Server name
        :return: List of established sessions
        :rtype: list
        """
        return self._call_api(methods.ConnectedUsersVhost, host=host)

    # TODO def convert_to_scram(self, host):
    # Convert the passwords in ‘users’ SQL table to SCRAM

    # TODO def convert_to_yaml(self, in, out):
    # Convert the input file from Erlang to YAML format

    def create_room_with_opts(self, name, service, host, options):
        """
        Create a MUC room name@service in host with given options

        :param name: Room name
        :type name: str
        :param service: MUC service
        :type service: str
        :param host: Server host
        :type host: str
        :param options: Room options. Example: options = [{"name": "members_only","value": "False"},
                                                        {"name": "moderated","value": "False"}]
        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.CreateRoomWithOpts, name=name, service=service, host=host, options=options)

    # TODO def create_rooms_file(self, file):
    # Create the rooms indicated in file

    def delete_expired_messages(self):
        """
        Delete expired offline messages from database

        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.DeleteExpiredMessages)

    # TODO def delete_mnesia(self, host):
    # Export all tables as SQL queries to a file

    # TODO def delete_old_mam_messages(self, type, days):
    # Delete MAM messages older than DAYS

    def delete_old_messages(self, days):
        """
        Delete offline messages older than DAYS

        :param days: Last login age in days of accounts that should be removed
        :type days: int
        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.DeleteOldMessages, days=days)

    def delete_old_users(self, days):
        """
        Delete users that didn't log in last days, or that never logged

        To protect admin accounts, configure this in your ejabberd.yml
         example: access_rules: protect_old_users: - allow: admin - deny: all
        :param days: Last login age in days of accounts that should be removed
        :type days: int
        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.DeleteOldUsers, days=days)

    def delete_old_users_vhost(self, host, days):
        """
        Delete users that didn't log in last days in vhost, or that never logged

        To protect admin accounts, configure this in your ejabberd.yml
        for example: access_rules: delete_old_users: - deny: admin - allow: all
        :param host:
        :type host: str
        :param days: Last login age in days of accounts that should be removed
        :type days: int
        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.DeleteOldUsersVhost,
                              host=host, days=days)

    def delete_rosteritem(self, localuser, localhost, user, host):
        """
         Delete an item from a user's roster (supports ODBC)

        :param localuser: User name
        :type localuser: str
        :param localhost: Server name
        :type localhost: str
        :param user: Contact user name
        :type user: str
        :param host: Contact server name
        :type host: str
        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.DeleteRosterItem, localuser=localuser,
                              localserver=localhost,
                              user=user,
                              server=host)

    # TODO def destroy_room(self, name, service):
    # Destroy a MUC room

    # TODO def destroy_rooms_file(self, file):
    # Destroy the rooms indicated in file. Provide one room JID per line.

    # TODO def dump(self, file):
    # Dump the database to text file

    # TODO def dump_table(self, file, table):
    # Dump a table to text file

    # TODO def export2sql(self, host, file):
    # Export virtual host information from Mnesia tables to SQL files

    # TODO def export_piefxis(self, dir):
    # Export data of all users in the server to PIEFXIS files (XEP-0227)

    # TODO def export_piefxis_host(self, dir, host):
    # Export data of users in a host to PIEFXIS files (XEP-0227)

    # TODO def gen_html_doc_for_commands(self, file, regexp, examples):
    # Generates html documentation for ejabberd_commands

    # TODO def gen_markdown_doc_for_commands(self, file, regexp, examples):
    # Generates markdown documentation for ejabberd_commands

    def muc_online_rooms(self, service="global"):
        """
        List existing rooms ('global' to get all vhosts)

        :param service: MUC service, default: 'global' for all
        :type service: str
        :return: List of rooms
        :rtype: list
        """
        return self._call_api(methods.MucOnlineRooms, service=service)

    def create_room(self, name, service, host):
        """
        Create a MUC room name@service in host

        :param name: Room name
        :type name: str
        :param service: MUC service
        :type service: str
        :param host: Server host
        :type host: str
        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.CreateRoom, name=name, service=service, host=host)

    def destroy_room(self, name, service):
        """
        Destroy a MUC room

        :param name: Room name
        :type name: str
        :param service: MUC service
        :type service: str
        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.DestroyRoom, name=name, service=service)

    def get_room_options(self, name, service):
        """
        Get options from a MUC room

        :param name: Room name
        :param service: MUC Service
        :return: List of room options dict with name and value
        :rtype: list
        """
        return self._call_api(methods.GetRoomOptions, name=name, service=service)

    def change_room_option(self, name, service, option, value):
        """
        Change an option in a MUC room

        :param name: Room name
        :param service: MUC Service
        :param option: Option name
        :param value: Value to assign
        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.ChangeRoomOption, name=name, service=service, option=option, value=value)

    def set_room_affiliation(self, name, service, jid, affiliation):
        """
        Change an affiliation in a MUC room

        :param name: Room name
        :type name: str
        :param service: MUC Service
        :type service: str
        :param jid: User JID
        :type jid: str
        :param affiliation: Affiliation to set
        :type affiliation: str
        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.GetRoomAffiliation, name=name, service=service, jid=jid, affiliation=affiliation)

    def get_room_affiliations(self, name, service):
        """
        Get the list of affiliations of a MUC room

        :param name: Room name
        :type name: str
        :param service: MUC Service
        :type service: str
        :return: The list of affiliations with username, domain, affiliation and reason
        :rtype: list
        """
        return self._call_api(methods.GetRoomAffiliations, name=name, service=service)

    def get_cookie(self):
        """
        Get the Erlang cookie of this node

        :return: Erlang cookie used for authentication by ejabberd
        :rtype: str
        """
        return self._call_api(methods.GetCookie)

    def get_last(self, user, host):
        """
        Get last activity information

        Timestamp is UTC and XEP-0082 format, for example: 2017-02-23T22:25:28.063062Z ONLINE
        :param user: User name
        :param host: Server name
        :return: Last activity timestamp and status
        :rtype: dict
        """
        return self._call_api(methods.GetLast, user=user, host=host)

    def get_loglevel(self):
        """
        Get the current loglevel

        :return: Tuple with the log level number, its keyword and description
        :rtype: str
        """
        return self._call_api(methods.GetLogLevel)

    # TODO def get_offline_count(self):
    # Get the number of unread offline messages

    # TODO def get_room_affiliations(self, name, service):
    # Get the list of affiliations of a MUC room

    def get_room_occupants(self, name, service):
        # Get the list of occupants of a MUC room
        return self._call_api(methods.GetRoomOccupants, name=name, service=service)

    # TODO def get_room_occupants_number(self, name, service):
    # Get the number of occupants of a MUC room

    # TODO def get_room_options(self, name, service):
    # Get options from a MUC room

    def get_roster(self, user, server):
        """
        Get roster of a local user

        :param user: User name
        :param server: Server name
        :return: List of subscriptions
        :rtype: list
        """
        return self._call_api(methods.GetRoster, user=user, server=server)

    def get_subscribers(self, name, service):
        """
        List subscribers of a MUC conference

        :param name: Room name
        :type name: str
        :param service: MUC service
        :type service: str
        :return: The list of users that are subscribed to that room
        :rtype: list
        """
        return self._call_api(methods.GetSubscribers, name=name, service=service)

    def get_user_rooms(self, user, host):
        """
        Get the list of rooms where this user is occupant

        :param user: Username
        :param host: Server host
        :return: List of user rooms
        :rtype: list
        """
        return self._call_api(methods.GetUserRooms, user=user, host=host)

    def get_vcard(self, user, host, name):
        """
        Get content from a vCard field

        Some vcard field names in get/set_vcard are:
        FN - Full Name
        NICKNAME - Nickname
        BDAY - Birthday
        TITLE - Work: Position
        ROLE - Work: Role
        For a full list of vCard fields check XEP-0054: vcard-temp at http://www.xmpp.org/extensions/xep-0054.html

        :param user: User name
        :type user: str
        :param host: Server name
        :type host: str
        :param name: Field name
        :type name: str
        :return: Field content
        :rtype: str
        """
        return self._call_api(methods.GetVcard, user=user,
                              host=host,
                              name=name)

    def get_vcard2(self, user, host, name, subname):
        """
        Get content from a vCard subfield

        Some vcard field names and subnames in get/set_vcard2 are:
        N FAMILY - Family name
        N GIVEN - Given name
        N MIDDLE - Middle name
        ADR CTRY - Address: Country
        ADR LOCALITY - Address: City
        TEL HOME - Telephone: Home
        TEL CELL - Telephone: Cellphone
        TEL WORK - Telephone: Work
        TEL VOICE - Telephone: Voice
        EMAIL USERID - E-Mail Address
        ORG ORGNAME - Work: Company
        ORG ORGUNIT - Work: Department
        For a full list of vCard fields check XEP-0054: vcard-temp at http://www.xmpp.org/extensions/xep-0054.html

        :param user: User name
        :type user: str
        :param host: Server name
        :type host: str
        :param name: Field name
        :type name: str
        :param subname: Subfield name
        :type subname: str
        :return: Field content
        :rtype: str
        """
        return self._call_api(methods.GetVcard2, user=user,
                              host=host,
                              name=name,
                              subname=subname)

    def get_vcard2_multi(self, user, host, name, subname):
        """
        Get multiple contents from a vCard field

        Some vcard field names and subnames in get/set_vcard2 are:
        N FAMILY - Family name
        N GIVEN - Given name
        N MIDDLE - Middle name
        ADR CTRY - Address: Country
        ADR LOCALITY - Address: City
        TEL HOME - Telephone: Home
        TEL CELL - Telephone: Cellphone
        TEL WORK - Telephone: Work
        TEL VOICE - Telephone: Voice
        EMAIL USERID - E-Mail Address
        ORG ORGNAME - Work: Company
        ORG ORGUNIT - Work: Department
        For a full list of vCard fields check XEP-0054: vcard-temp at http://www.xmpp.org/extensions/xep-0054.html

        :param user: User name
        :type user: str
        :param host: Server name
        :type host: str
        :param name: Field name
        :type name: str
        :param subname: Subfield name
        :type subname: str
        :return: Field content
        :rtype: str
        """
        return self._call_api(methods.GetVcard2Multi, user=user,
                              host=host,
                              name=name,
                              subname=subname)

    # TODO def import_dir(self, file):
    # Import users data from jabberd14 spool dir

    # TODO def import_file(self, file):
    # Import users data from jabberd14 spool file

    # TODO def import_piefxis(self, file):
    # Import users data from a PIEFXIS file (XEP-0227)

    # TODO def import_prosody(self, dir) Import data from Prosody

    def incoming_s2s_number(self):
        """
        Number of incoming s2s connections on the node

        :return: s2s number
        :rtype: int
        """
        return self._call_api(methods.IncomingS2SNumber)

    # TODO def install_fallback(self, file):
    # Install the database from a fallback file

    # TODO def join_cluster(self, node):
    # Join this node into the cluster handled by Node

    def kick_session(self, user, host, resource, reason):
        """
        Kick a user session
        """
        return self._call_api(methods.KickSession, user=user,
                              host=host,
                              resource=resource,
                              reason=reason)

    def kick_user(self, user, host):
        """
        Disconnect user's active sessions

        :param user: User name
        :type user: str
        :param host: Server name
        :type host: str
        :return: Number of resources that were kicked
        :rtype: int
        """
        return self._call_api(methods.KickUser, user=user, host=host)

    # TODO def leave_cluster(self, node):
    # Remove node handled by Node from the cluster

    def list_cluster(self):
        """
        List nodes that are part of the cluster handled by Node

        :return: List of clusters
        :rtype: list
        """
        return self._call_api(methods.ListCluster)

    # TODO def load(self, file):
    # Restore the database from text file

    # TODO def mnesia_change_nodename(self,
    #                                 oldnodename,
    #                                 newnodename,
    #                                 oldbackup,
    #                                 newbackup):
    # Change the erlang node name in a backup file

    # TODO def module_check(self, module):

    # TODO def module_install(self, module):

    # TODO def module_uninstall(self, module):

    # TODO def module_upgrade(self, module):

    def modules_available(self):
        """
        List the contributed modules available to install

        :return: List of dict with module name and description
        :rtype: list
        """
        return self._call_api(methods.ModulesAvailable)

    def modules_installed(self):
        """
        List the contributed modules already installed

        :return: List of dict with module name and description
        :rtype: list
        """
        return self._call_api(methods.ModulesInstalled)

    # TODO def modules_update_specs(self):

    # TODO def muc_online_rooms(self, host):
    # List existing rooms (‘global’ to get all vhosts)

    # TODO def muc_unregister_nick(self, nick):
    # Unregister the nick in the MUC service

    def num_resources(self, user, host):
        """
        Get the number of resources of a user

        :param user: User name
        :type user: str
        :param host: Server name
        :type host: str
        :return: Number of active resources for a user
        :rtype: int
        """
        return self._call_api(methods.NumResources, user=user, host=host)

    def outgoing_s2s_number(self):
        """
        Number of outgoing s2s connections on the node

        :return: Number of outgoing s2s connections
        :rtype: int
        """
        return self._call_api(methods.OutgoingS2SNumber)

    # TODO def privacy_set(self, user, host, xmlquery):
    # Send a IQ set privacy stanza for a local account

    # TODO def private_get(self, user, host, element, ns):
    # Get some information from a user private storage

    # TODO def private_set(self, user, host, element):
    # Set to the user private storage

    def process_rosteritems(self, action, subs, asks, users, contacts):
        """
        List/delete rosteritems that match filter

        :param action:
        :type action: str
        :param subs:
        :type subs: str
        :param asks:
        :type asks: str
        :param users:
        :type users: str
        :param contacts:
        :type contacts: str
        :return:
        """
        return self._call_api(methods.ProcessRosterItems, action=action,
                              subs=subs,
                              asks=asks,
                              users=users,
                              contacts=contacts)

    def push_alltoall(self, host, group):
        """
        Add all the users to all the users of Host in Group

        :param host: Server name
        :param group: Group name
        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.PushAllToAll, host=host, group=group)

    # TODO def push_roster(self, file, user, host):
    # Push template roster from file to a user

    # TODO def push_roster_all(self, file):
    # Push template roster from file to all those users

    def registered_vhosts(self):
        """
        List all registered vhosts in SERVER

        :return: List of available vhosts
        :rtype: list
        """
        return self._call_api(methods.RegisteredVhosts)

    def reload_config(self):
        """
        Reload config file in memory
        (only affects ACL and Access)

        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.ReloadConfig)

    def reopen_log(self):
        """
        Reopen the log files

        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.ReopenLog)

    def resource_num(self, user, host, num):
        """
        Resource string of a session number

        :param user: User name
        :type user: str
        :param host: Server name
        :type host: str
        :param num: ID of resource to return
        :type num: int
        :return: Name of user resource
        :rtype: str
        """
        return self._call_api(methods.ResourceNum, user=user,
                              host=host,
                              num=num)

    def restart(self):
        """
        Restart ejabberd gracefully

        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.Restart)

    # TODO def restore(self, file):
    # Restore the database from backup file

    # TODO def rooms_unused_destroy(self, host, days):
    # Destroy the rooms that are unused for many days in host

    # TODO def rooms_unused_list(self, host, days):
    # List the rooms that are unused for many days in host

    # TODO def rotate_log(self):
    # Rotate the log files

    # TODO def send_direct_invitation(self,
    #                                 name,
    #                                 service,
    #                                 password,
    #                                 reason,
    #                                 users):
    # Send a direct invitation to several destinations

    def send_message(self, type, from_jid, to, body, subject=""):
        """
        Send a message to a local or remote bare of full JID

        When sending a groupchat message to a MUC room, FROM must be the full JID of a room occupant,
        or the bare JID of a MUC service admin, or the bare JID of a MUC/Sub subscribed user.

        :param type:  Message type: normal, chat, headline, groupchat
        :type type: str
        :param from_jid: Sender JID
        :type from_jid: str
        :param to: Receiver JID
        :type to: str
        :param body: Body
        :type body: str
        :param subject: Subject, or empty string
        :type subject: str
        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.SendMessage, type=type,
                              from_jid=from_jid, to=to,
                              subject=subject,
                              body=body)

    # TODO def send_stanza(self, from, to, stanza):
    # Send a stanza; provide From JID and valid To JID

    def send_stanza_c2s(self, user, host, resource, stanza):
        """
        Send a stanza as if sent from a c2s session

        :param user: Username
        :param host: Server name
        :param resource: Resource
        :param stanza: Stanza
        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.SendStanzaC2S, user=user,
                              host=host,
                              resource=resource,
                              stanza=stanza)

    def set_last(self, user, host, timestamp, status):
        """
        Set last activity information
        Timestamp is the seconds since 1970-01-01 00:00:00 UTC, for example: date +%s

        :param user: User name
        :param host: Server name
        :param timestamp: Number of seconds since epoch
        :param status: Status message
        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.SetLast, user=user,
                              host=host,
                              timestamp=timestamp,
                              status=status)

    def set_loglevel(self, loglevel):
        """
        Set the loglevel

        :param loglevel: Desired logging level: none | emergency | alert | critical | error
        | warning | notice | info | debug
        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        try:
            return self._call_api(methods.SetLogLevel, loglevel=loglevel)
        except xmlrpc_client.Fault as e:
            msg = 'set_loglevel is NOT available in your version of ejabberd'
            raise Exception('{}\n{} - code: {}\n '.format(msg, e.faultString, e.faultCode))

    def set_master(self, nodename):
        """
        Set master node of the clustered Mnesia tables
        If you provide as nodename "self", this node will be set as its own master.

        :param nodename: Name of the erlang node that will be considered master of this node
        :type nodename: str
        :return: Raw result string
        :rtype: bool
        """
        return self._call_api(methods.SetMaster, nodename=nodename)

    def set_nickname(self, user, host, nickname):
        """
        Set nickname in a user's vCard

        :param user: Username
        :type user: str
        :param host: Server name
        :type host: str
        :param nickname: Nickname
        :type nickname: str
        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.SetNickname, user=user,
                              host=host,
                              nickname=nickname)

    def set_presence(self, user, host, resource, type, show, status, priority):
        """
        Set presence of a session

        :param user: Username
        :type user: str
        :param host: Server name
        :type host: str
        :param resource: Resource
        :type resource: str
        :param type: Type: available, error, probe..
        :type type: str
        :param show: Show: away, chat, dnd, xa
        :type show: str
        :param status: Status text
        :type status: str
        :param priority: Priority, provide this value as an integer
        :type priority: str
        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.SetPresence, user=user,
                              host=host,
                              resource=resource,
                              type=type,
                              show=show,
                              status=status,
                              priority=priority)

    # TODO def set_room_affiliation(self, name, service, jid, affiliation):
    # Change an affiliation in a MUC room

    def set_vcard(self, user, host, name, content):
        """
        Set content in a vCard field

        Some vcard field names in get/set_vcard are:
        FN - Full Name
        NICKNAME - Nickname
        BDAY - Birthday
        TITLE - Work: Position
        ROLE - Work: Role
        For a full list of vCard fields check XEP-0054: vcard-temp at http://www.xmpp.org/extensions/xep-0054.html

        :param user: User name
        :param host: Server name
        :param name: Field name
        :param content: Value
        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.SetVcard, user=user,
                              host=host,
                              name=name,
                              content=content)

    def set_vcard2(self, user, host, name, subname, content):
        """
        Set content in a vCard subfield

        :param user: User name
        :param host: Server name
        :param name: Field name
        :param subname: Subfield name
        :param content: Value
        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.SetVcard2, user=user,
                              host=host,
                              name=name,
                              subname=subname,
                              content=content)

    def set_vcard2_multi(self, user, host, name, subname, contents):
        """
        Set multiple contents in a vCard subfield

        :param user: User name
        :type user: str
        :param host: Server name
        :type host: str
        :param name: Field name
        :type name: str
        :param subname: Subfield name
        :type subname: str
        :param contents: Contents
        :type contents: dict
        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.SetVcardMulti, user=user,
                              host=host,
                              name=name,
                              subname=subname,
                              contents=contents)

    def srg_create(self, group, host, name, description, display):
        """
        Create a Shared Roster Group

        If you want to specify several group identifiers in the Display argument,
        put \ " around the argument and separate the identifiers with \ \ n
        For example: ejabberdctl srg_create group3 myserver.com name desc \"group1\ngroup2\"

        :param group: Group identifier
        :type group: str
        :param host: Group server name
        :type host: str
        :param name: Group name
        :type name: str
        :param description: Group description
        :type description: str
        :param display: Groups to display
        :type display: str
        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.SrgCreate, group=group,
                              host=host,
                              name=name,
                              description=description,
                              display=display)

    def srg_delete(self, group, host):
        """
        Delete a Shared Roster Group

        :param group: Group identifier
        :type group: str
        :param host: Group server name
        :type host: str
        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.SrgDelete, group=group, host=host)

    def srg_get_info(self, group, host):
        """
        Get info of a Shared Roster Group

        :param group: Group identifier
        :type group: str
        :param host: Group server name
        :type host: str
        :return: List of group informations, as key and value
        :rtype: list
        """
        return self._call_api(methods.SrgGetInfo, group=group, host=host)

    def srg_get_members(self, group, host):
        """
        Get members of a Shared Roster Group

        :param group: Group identifier
        :type group: str
        :param host: Group server name
        :type host: str
        :return: List of group identifiers
        :rtype: list
        """
        return self._call_api(methods.SrgGetMembers, group=group, host=host)

    def srg_list(self, host):
        """
        List the Shared Roster Groups in Host

        :param host: Server name
        :type host: str
        :return:  List of group identifiers
        :rtype: list
        """
        return self._call_api(methods.SrgList, host=host)

    def srg_user_add(self, user, host, group, grouphost):
        """
        Add the JID user@host to the Shared Roster Group

        :param user: User name
        :type user: str
        :param host: User server name
        :type host: str
        :param group: Group identifier
        :type group: str
        :param grouphost: Group server name
        :type grouphost: str
        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.SrgUserAdd, user=user,
                              host=host,
                              group=group,
                              grouphost=grouphost)

    def srg_user_del(self, user, host, group, grouphost):
        """
        Delete this JID user@host from the Shared Roster Group

        :param user: User name
        :type user: str
        :param host: User server name
        :type host: str
        :param group: Group identifier
        :type group: str
        :param grouphost: Group server name
        :type grouphost: str
        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.SrgUserDel, user=user,
                              host=host,
                              group=group,
                              grouphost=grouphost)

    def stats(self, name):
        """
        Get statistical value

        :param name: Statistic name:
        * ``registeredusers``
        * ``onlineusers``
        * ``onlineusersnode``
        * ``uptimeseconds``
        * ``processes``
        :type name: str
        :return: Integer statistic value
        """
        return self._call_api(methods.Stats, name=name)

    def stats_host(self, name, host):
        """
        Get statistical value

        :param name: Statistic name:
        * ``registeredusers``
        * ``onlineusers``

        :type name: str
        :param host: Server JID
        :type host: str
        :return: Integer statistic value
        :rtype: int
        """
        return self._call_api(methods.StatsHost, name=name, host=host)

    def status(self):
        """
        Get status of the ejabberd server

        :return: Raw result string
        :rtype: str
        """
        return self._call_api(methods.Status)

    def status_list(self, status):
        """
        List of logged users with this status

        :param status: Status type to check
        :type status: str
        :return: List of users with this `status`
        :rtype: list
        """
        return self._call_api(methods.StatusList, status=status)

    def status_list_host(self, host, status):
        """
        List of users logged in host with their statuses

        :param host: Server name
        :type host: str
        :param status: Status type to check
        :type status: str
        :return: List of users with this `status` in `host`
        :rtype: list
        """
        return self._call_api(methods.StatusListHost, host=host, status=status)

    def status_num(self, status):
        """
         Number of logged users with this status

        :param status: Status type to check
        :type status: str
        :return: Number of connected sessions with given status type
        :rtype: list
        """
        return self._call_api(methods.StatusNum, status=status)

    def status_num_host(self, host, status):
        """
        Number of logged users with this status in host

        :param host: Server name
        :type host: str
        :param status: Status type to check
        :type status: str
        :return: Number of connected sessions with given status type
        :rtype: list
        """
        return self._call_api(methods.StatusNumHost, host=host, status=status)

    def stop(self):
        """
        Stop ejabberd gracefully

        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.Stop)

    def stop_kindly(self, delay, announcement):
        """
        Inform users and rooms, wait, and stop the server
        Provide the delay in seconds, and the announcement quoted,
        for example: ejabberdctl stop_kindly 60 \"The server will stop in one minute.\"

        :param delay: Seconds to wait
        :param announcement: Announcement to send, with quotes
        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.StopKindly,
                              delay=delay, announcement=announcement)

    def subscribe_room(self, user, nick, room, nodes=None):
        """
        Subscribe to a MUC conference
        
        :param user: User JID
        :type user: str
        :param nick: A user's nick
        :type nick: str
        :param room: The room to subscribe
        :type room: str
        :param nodes: List of nodes
        :type nodes: list
        :return: The list of nodes that has subscribed
        :rtype: list
        """
        return self._call_api(methods.SubscribeRoom, user=user, nick=nick, room=room, nodes=nodes)

    def unsubscribe_room(self, user, room):
        """
        Unsubscribe from a MUC conference

        :param user: User JID
        :type user: str
        :param room: The room to subscribe
        :type room: str
        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.UnSubscribeRoom, user=user, room=room)

    def update(self, module):
        """
        Update the given module, or use the keyword: all

        :param module: Module to update
        :return: Raw result string
        :rtype: str
        """
        return self._call_api(methods.Update, module=module)

    def update_list(self):
        """
        List modified modules that can be updated

        :return: List of modules
        :rtype: list
        """
        return self._call_api(methods.UpdateList)

    def update_sql(self):
        """
        Convert SQL DB to the new format

        :return: Status code (True if success, False otherwise)
        :rtype: bool
        """
        return self._call_api(methods.UpdateSql)

    def user_resources(self, user, host):
        """
        List user's connected resources

        :param user: User name
        :type user: str
        :param host: Server name
        :type host: str
        :return: List of resources
        :rtype: list
        """
        return self._call_api(methods.UserResources, user=user, host=host)

    def user_sessions_info(self, user, host):
        """
        Get information about all sessions of a user

        :param user: User name
        :type user: str
        :param host: Server name
        :type host: str
        :return: A List with user sessions
        :rtype: list
        """
        return self._call_api(methods.UserSessionInfo, user=user, host=host)
