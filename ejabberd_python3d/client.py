from __future__ import print_function

import copy
from urllib.parse import urlparse
from xmlrpc import client as xmlrpc_client

from ejabberd_python3d.abc import methods
from ejabberd_python3d.abc.api import API, APIArgument, EjabberdBaseAPI
from ejabberd_python3d.core.errors import MissingArguments
from ejabberd_python3d.defaults.constants import XMLRPC_API_PROTOCOL, XMLRPC_API_SERVER, \
    XMLRPC_API_PORT


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
        :return:
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
        :param arguments: A dictionary of arguments that will be passed to the method
        :type arguments: dict
        :rtype: dict
        :return: The serialized arguments
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
        :param method: The name oft hem method to call
        :type method: str|unicode
        :param arguments: A dictionary of arguments that will be passed to the method
        :type: arguments: dict
        :return:
        """
        if self.verbose:
            print("===> %s(%s)" % (method, ', '.join(['%s=%s' % (k, v) for k, v in arguments.items()])))

    def _call_api(self, api_class, **kwargs):
        """
        Internal method used to perform api calls
        :param api_class:
        :type api_class: py:class:API
        :param kwargs:
        :type kwargs: dict
        :rtype: object
        :return: Returns return value of the XMLRPC Method call
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
        List all registered users in the xmpp_host
        :param host: The XMPP_DOMAIN
        :type host: str|unicode
        :rtype: Iterable
        :return: A list of registered users in the xmpp_host
        """
        return self._call_api(methods.RegisteredUsers, host=host)

    def register(self, user, host, password):
        """
        Registers a user to the ejabberd server
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
        UnRegisters a user from the ejabberd server
        :param user: The username for the new user
        :type user: str|unicode
        :param host: The XMPP_DOMAIN
        :type host: str|unicode
        :rtype: bool
        :return: A boolean indicating if user unregistered has succeeded
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
        :rtype: bool
        :return: A boolean indicating if the given password matches the user's password
        """
        return self._call_api(methods.CheckPasswordHash, user=user, host=host, password=password)

    def add_rosteritem(self,
                       localuser, localserver,
                       user, server,
                       nick, group, subs):
        """
        Add an item to a user's roster (self,supports ODBC):
        """
        return self._call_api(methods.AddRosterItem, localuser=localuser,
                              localserver=localserver,
                              user=user,
                              server=server,
                              nick=nick,
                              group=group,
                              subs=subs)

    # TODO def backup(self, file): Store the database to backup file

    def ban_account(self, user, host, reason):
        """
        Ban an account: kick sessions and set random password
        """
        return self._call_api(methods.BanAccount, user=user,
                              host=host,
                              reason=reason)

    # TODO def change_room_option(self, name, service, option, value)
    # Change an option in a MUC room

    def check_account(self, user, host):
        """
        Check if an account exists or not
        """
        return self._call_api(methods.CheckAccount, user=user, host=host)

    def check_password(self, user, host, password):
        """
        Check if a password is correct
        """
        return self._call_api(methods.CheckPassword, user=user,
                              host=host,
                              password=password)

    # TODO def compile(self, file):
    # Recompile and reload Erlang source code file

    def connected_users(self):
        """
        List all established sessions
        """
        return self._call_api(methods.ConnectedUsers)

    def connected_users_info(self):
        """
        List all established sessions and their information
        """
        return self._call_api(methods.ConnectedUsersInfo)

    def connected_users_number(self):
        """
        Get the number of established sessions
        """
        return self._call_api(methods.ConnectedUsersNumber)

    def connected_users_vhost(self, host):
        """
        Get the list of established sessions in a vhost
        """
        return self._call_api(methods.ConnectedUsersVhost, host=host)

    # TODO def convert_to_scram(self, host):
    # Convert the passwords in ‘users’ SQL table to SCRAM

    # TODO def convert_to_yaml(self, in, out):
    # Convert the input file from Erlang to YAML format

    # TODO def create_room(self, name, service, host):
    # Create a MUC room name@service in host

    # TODO def create_room_with_opts(self, name, service, host, options):
    # Create a MUC room name@service in host with given options

    # TODO def create_rooms_file(self, file):
    # Create the rooms indicated in file

    def delete_expired_messages(self):
        """
        Delete expired offline messages from database
        """
        return self._call_api(methods.DeleteExpiredMessages)

    # TODO def delete_mnesia(self, host):
    # Export all tables as SQL queries to a file

    # TODO def delete_old_mam_messages(self, type, days):
    # Delete MAM messages older than DAYS

    def delete_old_messages(self, days):
        """
        Delete offline messages older than DAYS
        """
        return self._call_api(methods.DeleteOldMessages, days=days)

    def delete_old_users(self, days):
        """
        Delete users that didn't log in last days, or that never logged
        """
        return self._call_api(methods.DeleteOldUsers, days=days)

    def delete_old_users_vhost(self, host, days):
        """
        Delete users that didn't log in last days in vhost,
        or that never logged
        """
        return self._call_api(methods.DeleteOldUsersVhost,
                              host=host, days=days)

    def delete_rosteritem(self, localuser, localserver, user, server):
        """
        Delete an item from a user's roster (self,supports ODBC):
        """
        return self._call_api(methods.DeleteRosterItem, localuser=localuser,
                              localserver=localserver,
                              user=user,
                              server=server)

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

    def muc_online_rooms(self, host=None):
        pass

    def create_room(self, name, service, host):
        pass

    def destroy_room(self, name, service, host):
        pass

    def get_room_options(self, name, service):
        pass

    def change_room_option(self, name, service, option, value):
        pass

    def set_room_affiliation(self, name, service, jid, affiliation):
        pass

    def get_room_affiliations(self, name, service):
        pass

    def add_roster_item(self, localuser, localserver, user, server, nick, group, subs):
        pass

    def remove_rosteritem(self, localuser, localserver, user, server):
        pass

    def get_cookie(self):
        """
        Get the Erlang cookie of this node
        """
        return self._call_api(methods.GetCookie)

    def get_last(self, user, host):
        """
        Get last activity information (self,timestamp and status):
        """
        return self._call_api(methods.GetLast, user=user, host=host)

    def get_loglevel(self):
        """
        Get the current loglevel
        """
        return self._call_api(methods.GetLogLevel)

    # TODO def get_offline_count(self):
    # Get the number of unread offline messages

    # TODO def get_room_affiliations(self, name, service):
    # Get the list of affiliations of a MUC room

    # TODO def get_room_occupants(self, name, service):
    # Get the list of occupants of a MUC room

    # TODO def get_room_occupants_number(self, name, service):
    # Get the number of occupants of a MUC room

    # TODO def get_room_options(self, name, service):
    # Get options from a MUC room

    def get_roster(self, user, server):
        """
        Get roster of a local user.

        Note, parameters changed in 15.09
        from ``user, host``
        to ``user, server``.

        Arguments:

        user :: binary
        server :: binary

        Result:

        {contacts,{list,{contact,{tuple,[{jid,string},
                                         {nick,string},
                                         {subscription,string},
                                         {ask,string},
                                         {group,string}]}}}}

        """

        return self._call_api(methods.GetRoster, user=user, server=server)

    # TODO get_subscribers(self, name, service):
    # List subscribers of a MUC conference

    # TODO get_user_rooms(self, user, host):
    # Get the list of rooms where this user is occupant

    def get_vcard(self, user, host, name):
        """
        Get content from a vCard field
        """
        return self._call_api(methods.GetVcard, user=user,
                              host=host,
                              name=name)

    def get_vcard2(self, user, host, name, subname):
        """
        Get content from a vCard field
        """
        return self._call_api(methods.GetVcard2, user=user,
                              host=host,
                              name=name,
                              subname=subname)

    def get_vcard2_multi(self, user, host, name, subname):
        """
        Get multiple contents from a vCard field
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
        """
        return self._call_api(methods.KickUsers, user=user, host=host)

    # TODO def leave_cluster(self, node):
    # Remove node handled by Node from the cluster

    def list_cluster(self):
        """
        List nodes that are part of the cluster handled by Node

        Result:

        {nodes,{list,{node,atom}}}

        """
        try:
            return self._call_api(methods.ListCluster)
        except xmlrpc_client.Fault as e:
            msg = 'list_cluster is NOT available in your version of ejabberd'
            raise Exception('{}\n{}\n - code: {}'.format(msg, e.faultString, e.faultCode))

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
        List available modules
        """
        return self._call_api(methods.ModulesAvailable)

    def modules_installed(self):
        """
        List installed modules
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
        """
        return self._call_api(methods.NumResources, user=user, host=host)

    def outgoing_s2s_number(self):
        """
        Number of outgoing s2s connections on the node
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
        List or delete rosteritems that match filtering options
        """
        return self._call_api(methods.ProcessRosterItems, action=action,
                              subs=subs,
                              asks=asks,
                              users=users,
                              contacts=contacts)

    def push_alltoall(self, host, group):
        """
        Add all the users to all the users of Host in Group
        """
        return self._call_api(methods.PushAllToAll, host=host, group=group)

    # TODO def push_roster(self, file, user, host):
    # Push template roster from file to a user

    # TODO def push_roster_all(self, file):
    # Push template roster from file to all those users

    def registered_vhosts(self):
        """
        List all registered vhosts in SERVER
        """
        return self._call_api(methods.RegisteredVhosts)

    def reload_config(self):
        """
        Reload ejabberd configuration file into memory

        (only affects ACL and Access)
        """
        return self._call_api(methods.ReloadConfig)

    def reopen_log(self):
        """
        Reopen the log files
        """
        return self._call_api(methods.ReopenLog)

    def resource_num(self, user, host, num):
        """
        Resource string of a session number
        """
        return self._call_api(methods.ResourceNum, user=user,
                              host=host,
                              num=num)

    def restart(self):
        """
        Restart ejabberd
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
        """
        # noinspection PyTypeChecker
        return self._call_api(methods.SendMessage, type=type,
                              from_jid=from_jid, to=to,
                              subject=subject,
                              body=body)

    # TODO def send_stanza(self, from, to, stanza):
    # Send a stanza; provide From JID and valid To JID

    def send_stanza_c2s(self, user, host, resource, stanza):
        """
        Send a stanza as if sent from a c2s session
        """
        return self._call_api(methods.SendStanzaC2S, user=user,
                              host=host,
                              resource=resource,
                              stanza=stanza)

    def set_last(self, user, host, timestamp, status):
        """
        Set last activity information
        """
        return self._call_api(methods.SetLast, user=user,
                              host=host,
                              timestamp=timestamp,
                              status=status)

    def set_loglevel(self, loglevel):
        """
        Set the loglevel (0 to 5)

        Arguments:

            loglevel :: integer

        Result:

        {logger,atom}

        """
        try:
            return self._call_api(methods.SetLogLevel, loglevel=loglevel)
        except xmlrpc_client.Fault as e:
            msg = 'set_loglevel is NOT available in your version of ejabberd'
            raise Exception('{}\n{} - code: {}\n '.format(msg, e.faultString, e.faultCode))

    def set_master(self, nodename):
        """
        Set master node of the clustered Mnesia tables
        """
        return self._call_api(methods.SetMaster, nodename=nodename)

    def set_nickname(self, user, host, nickname):
        """
        Set nickname in a user's vCard
        """
        return self._call_api(methods.SetNickname, user=user,
                              host=host,
                              nickname=nickname)

    def set_presence(self, user, host, resource, type, show, status, priority):
        """
        Set presence of a session
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
        """
        return self._call_api(methods.SetVcard, user=user,
                              host=host,
                              name=name,
                              content=content)

    def set_vcard2(self, user, host, name, subname, content):
        """
        Set content in a vCard subfield
        """
        return self._call_api(methods.SetVcard2, user=user,
                              host=host,
                              name=name,
                              subname=subname,
                              content=content)

    def set_vcard2_multi(self, user, host, name, subname, contents):
        """
        *Set multiple contents in a vCard subfield
        """
        return self._call_api(methods.SetVcardMulti, user=user,
                              host=host,
                              name=name,
                              subname=subname,
                              contents=contents)

    def srg_create(self, group, host, name, description, display):
        """
        Create a Shared Roster Group
        """
        return self._call_api(methods.SrgCreate, group=group,
                              host=host,
                              name=name,
                              description=description,
                              display=display)

    def srg_delete(self, group, host):
        """
        Delete a Shared Roster Group
        """
        return self._call_api(methods.SrgDelete, group=group, host=host)

    def srg_get_info(self, group, host):
        """
        Get info of a Shared Roster Group
        """
        return self._call_api(methods.SrgGetInfo, group=group, host=host)

    def srg_get_members(self, group, host):
        """
        Get members of a Shared Roster Group
        """
        return self._call_api(methods.SrgGetMembers, group=group, host=host)

    def srg_list(self, host):
        """
        List the Shared Roster Groups in Host
        """
        return self._call_api(methods.SrgList, host=host)

    def srg_user_add(self, user, host, group, grouphost):
        """
        Add the JID user@host to the Shared Roster Group
        """
        return self._call_api(methods.SrgUserAdd, user=user,
                              host=host,
                              group=group,
                              grouphost=grouphost)

    def srg_user_del(self, user, host, group, grouphost):
        """
        Delete this JID user@host from the Shared Roster Group
        """
        return self._call_api(methods.SrgUserDel, user=user,
                              host=host,
                              group=group,
                              grouphost=grouphost)

    def stats(self, name):
        """
        Get statistical value:

        * ``registeredusers``
        * ``onlineusers``
        * ``onlineusersnode``
        * ``uptimeseconds``
        * ``processes`` - Introduced sometime after Ejabberd 15.07
        """
        try:
            return self._call_api(methods.Stats, name=name)
        except Exception as e:
            msg = 'processes stats NOT available in this version of Ejabberd'
            if e.message == self.errors['connect']:
                raise Exception('{}\n{}\n'.format(msg, e.message))
            raise Exception(e)

    def stats_host(self, name, host):
        """
        Get statistical value for this host:

        * ``registeredusers``
        * ``onlineusers``
        """
        return self._call_api(methods.StatsHost, name=name, host=host)

    def status(self):
        """
        Get ejabberd status
        """
        return self._call_api(methods.Status)

    def status_list(self, status):
        """
        List of logged users with this status
        """
        return self._call_api(methods.StatusList, status=status)

    def status_list_host(self, host, status):
        """
        List of users logged in host with their statuses
        """
        return self._call_api(methods.StatusListHost, host=host, status=status)

    def status_num(self, status):
        """
        Number of logged users with this status
        """
        return self._call_api(methods.StatusNum, status=status)

    def status_num_host(self, host, status):
        """
        Number of logged users with this status in host
        """
        return self._call_api(methods.StatusNumHost, host=host, status=status)

    def stop(self):
        """
        Stop ejabberd
        """
        return self._call_api(methods.Stop)

    def stop_kindly(self, delay, announcement):
        """
        Inform users and rooms, wait, and stop the server
        """
        return self._call_api(methods.StopKindly,
                              delay=delay, announcement=announcement)

    # TODO def subscribe_room(self, user, nick, room, nodes):
    # Subscribe to a MUC conference

    def unregister(self, user, host):
        """
        Unregister a user
        """
        return self._call_api(methods.Unregister, user=user, host=host)

    # TODO def unsubscribe_room(self, user, room):
    # Unsubscribe from a MUC conference

    def update(self, module):
        """
        Update the given module, or use the keyword: all
        """
        return self._call_api(methods.Update, module=module)

    def update_list(self):
        """
        List modified modules that can be updated
        """
        return self._call_api(methods.UpdateList)

    def user_resources(self, user, server):
        """
        List user's connected resources

        Note, parameters changed in 15.09
        from ``user, host``
        to ``user, server``.

        Arguments:

        user :: binary
        server :: binary

        Result:

        {resources,{list,{resource,string}}}

        """
        return self._call_api(methods.UserResources, user=user, server=server)

    def user_sessions_info(self, user, host):
        """
        Get information about all sessions of a user
        """
        return self._call_api(methods.UserSessionInfo, user=user, host=host)
