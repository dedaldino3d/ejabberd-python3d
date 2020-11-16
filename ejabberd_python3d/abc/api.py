from __future__ import unicode_literals

from abc import ABC, abstractmethod
from enum import Enum as BaseClassEnum


class APIArgumentSerializer(ABC):
    @abstractmethod
    def to_api(self, value):
        pass

    @abstractmethod
    def to_builtin(self, value):
        pass


class APIArgument(ABC):
    def __init__(self, name, description=None, required=True, **kwargs):
        self.name = name
        self.description = description
        self.required = required

    @abstractmethod
    def serializer_class(self):
        pass


class Enum(BaseClassEnum):
    @classmethod
    def get_by_name(cls, name):
        return getattr(cls, name, None)

    @classmethod
    def get_by_value(cls, value):
        return cls(value)


class API(ABC):
    @abstractmethod
    def method(self):
        """
        Return the exact name of the XML-RPC API method to call
        """
        pass

    @abstractmethod
    def arguments(self):
        """
        Return an (ordered) list of APIArgument objects
        """
        pass

    @property
    def authenticate(self):
        """
        Defines whether or not we should authenticate when calling API
        """
        return True

    def transform_arguments(self, **kwargs):
        """
        Handler methods to transform an argument before processing
        :param kwargs: Named argument dictionary
        """
        return kwargs

    def validate_response(self, api, arguments, response):
        """
        Handler to validate the API response, Can be used 
        to raise an Exception to indicate fail, the pipeline will continue with the
        'transform_response' method
        :param arguments: The dictionary containing the arguments that have been used to perform the call
        :param response: object
        """
        pass

    def transform_response(self, api, arguments, response):
        """
        Handler method to process the response, The output of this method
        will be return as the output of the API
        :param response:
        :param api: The api object that has been used fot the call
        :param arguments: The dictionary containing the arguments
        """
        return response


class EjabberdBaseAPI(ABC):
    @abstractmethod
    def echo(self, sentence):
        pass

    @abstractmethod
    def registered_users(self, host):
        pass

    @abstractmethod
    def register(self, user, host, password):
        pass

    @abstractmethod
    def unregister(self, user, host):
        pass

    @abstractmethod
    def change_password(self, user, host, password, newpass):
        pass

    @abstractmethod
    def check_password_hash(self, user, host, password):
        pass

    @abstractmethod
    def connected_users(self):
        pass

    @abstractmethod
    def connected_users_info(self):
        pass

    @abstractmethod
    def connected_users_number(self):
        pass

    @abstractmethod
    def user_sessions_info(self):
        pass

    @abstractmethod
    def muc_online_rooms(self, host=None):
        pass

    @abstractmethod
    def create_room(self, name, service, host):
        pass

    @abstractmethod
    def destroy_room(self, name, service, host):
        pass

    @abstractmethod
    def get_room_options(self, name, service):
        pass

    @abstractmethod
    def change_room_option(self, name, service, option, value):
        pass

    @abstractmethod
    def set_room_affiliation(self, name, service, jid, affiliation):
        pass

    @abstractmethod
    def get_room_affiliations(self, name, service):
        pass

    @abstractmethod
    def add_roster_item(self, localuser, localserver, user, server, nick, group, subs):
        pass

    @abstractmethod
    def remove_rosteritem(self, localuser, localserver, user, server):
        pass

    @abstractmethod
    def add_rosteritem(self,
                       localuser, localserver,
                       user, server,
                       nick, group, subs):
        """
        Add an item to a user's roster (self,supports ODBC):
        """
        pass

    # TODO def backup(self, file): Store the database to backup file

    @abstractmethod
    def ban_account(self, user, host, reason):
        """
        Ban an account: kick sessions and set random password
        """
        pass

    # TODO def change_room_option(self, name, service, option, value)
    # Change an option in a MUC room

    @abstractmethod
    def check_account(self, user, host):
        """
        Check if an account exists or not
        """
        pass

    @abstractmethod
    def check_password(self, user, host, password):
        """
        Check if a password is correct
        """
        pass

    # TODO def compile(self, file):
    # Recompile and reload Erlang source code file

    @abstractmethod
    def connected_users_vhost(self, host):
        """
        Get the list of established sessions in a vhost
        """
        pass

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

    @abstractmethod
    def delete_expired_messages(self):
        """
        Delete expired offline messages from database
        """
        pass

    # TODO def delete_mnesia(self, host):
    # Export all tables as SQL queries to a file

    # TODO def delete_old_mam_messages(self, type, days):
    # Delete MAM messages older than DAYS

    @abstractmethod
    def delete_old_messages(self, days):
        """
        Delete offline messages older than DAYS
        """
        pass

    @abstractmethod
    def delete_old_users(self, days):
        """
        Delete users that didn't log in last days, or that never logged
        """
        pass

    @abstractmethod
    def delete_old_users_vhost(self, host, days):
        """
        Delete users that didn't log in last days in vhost,
        or that never logged
        """
        pass

    @abstractmethod
    def delete_rosteritem(self, localuser, localserver, user, server):
        """
        Delete an item from a user's roster (self,supports ODBC):
        """
        pass

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
    @abstractmethod
    def get_cookie(self):
        """
        Get the Erlang cookie of this node
        """
        pass

    @abstractmethod
    def get_last(self, user, host):
        """
        Get last activity information (self,timestamp and status):
        """
        pass

    @abstractmethod
    def get_loglevel(self):
        """
        Get the current loglevel
        """
        pass

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
    @abstractmethod
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
        pass

    # TODO get_subscribers(self, name, service):
    # List subscribers of a MUC conference

    # TODO get_user_rooms(self, user, host):
    # Get the list of rooms where this user is occupant
    @abstractmethod
    def get_vcard(self, user, host, name):
        """
        Get content from a vCard field
        """
        pass

    @abstractmethod
    def get_vcard2(self, user, host, name, subname):
        """
        Get content from a vCard field
        """
        pass

    @abstractmethod
    def get_vcard2_multi(self, user, host, name, subname):
        """
        Get multiple contents from a vCard field
        """
        pass

    # TODO def import_dir(self, file):
    # Import users data from jabberd14 spool dir

    # TODO def import_file(self, file):
    # Import users data from jabberd14 spool file

    # TODO def import_piefxis(self, file):
    # Import users data from a PIEFXIS file (XEP-0227)

    # TODO def import_prosody(self, dir) Import data from Prosody
    @abstractmethod
    def incoming_s2s_number(self):
        """
        Number of incoming s2s connections on the node
        """
        pass

    # TODO def install_fallback(self, file):
    # Install the database from a fallback file

    # TODO def join_cluster(self, node):
    # Join this node into the cluster handled by Node
    @abstractmethod
    def kick_session(self, user, host, resource, reason):
        """
        Kick a user session
        """
        pass

    @abstractmethod
    def kick_user(self, user, host):
        """
        Disconnect user's active sessions
        """
        pass

    # TODO def leave_cluster(self, node):
    # Remove node handled by Node from the cluster
    @abstractmethod
    def list_cluster(self):
        """
        List nodes that are part of the cluster handled by Node

        Result:

        {nodes,{list,{node,atom}}}

        """
        pass

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
    @abstractmethod
    def modules_available(self):
        """
        List available modules
        """
        pass

    @abstractmethod
    def modules_installed(self):
        """
        List installed modules
        """
        pass

    # TODO def modules_update_specs(self):

    # TODO def muc_online_rooms(self, host):
    # List existing rooms (‘global’ to get all vhosts)

    # TODO def muc_unregister_nick(self, nick):
    # Unregister the nick in the MUC service

    @abstractmethod
    def num_resources(self, user, host):
        """
        Get the number of resources of a user
        """
        pass

    @abstractmethod
    def outgoing_s2s_number(self):
        """
        Number of outgoing s2s connections on the node
        """
        pass

    # TODO def privacy_set(self, user, host, xmlquery):
    # Send a IQ set privacy stanza for a local account

    # TODO def private_get(self, user, host, element, ns):
    # Get some information from a user private storage

    # TODO def private_set(self, user, host, element):
    # Set to the user private storage
    @abstractmethod
    def process_rosteritems(self, action, subs, asks, users, contacts):
        """
        List or delete rosteritems that match filtering options
        """
        pass

    @abstractmethod
    def push_alltoall(self, host, group):
        """
        Add all the users to all the users of Host in Group
        """
        pass

    # TODO def push_roster(self, file, user, host):
    # Push template roster from file to a user

    # TODO def push_roster_all(self, file):
    # Push template roster from file to all those users
    @abstractmethod
    def registered_vhosts(self):
        """
        List all registered vhosts in SERVER
        """
        pass

    @abstractmethod
    def reload_config(self):
        """
        Reload ejabberd configuration file into memory

        (only affects ACL and Access)
        """
        pass

    @abstractmethod
    def reopen_log(self):
        """
        Reopen the log files
        """
        pass

    @abstractmethod
    def resource_num(self, user, host, num):
        """
        Resource string of a session number
        """
        pass

    @abstractmethod
    def restart(self):
        """
        Restart ejabberd
        """
        pass

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
    @abstractmethod
    def send_message(self, type, from_jid, to, subject, body):
        """
        Send a message to a local or remote bare of full JID
        """
        pass

    # TODO def send_stanza(self, from, to, stanza):
    # Send a stanza; provide From JID and valid To JID
    @abstractmethod
    def send_stanza_c2s(self, user, host, resource, stanza):
        """
        Send a stanza as if sent from a c2s session
        """
        pass

    @abstractmethod
    def set_last(self, user, host, timestamp, status):
        """
        Set last activity information
        """
        pass

    @abstractmethod
    def set_loglevel(self, loglevel):
        """
        Set the loglevel (0 to 5)

        Arguments:

            loglevel :: integer

        Result:

        {logger,atom}

        """
        pass

    @abstractmethod
    def set_master(self, nodename):
        """
        Set master node of the clustered Mnesia tables
        """
        pass

    @abstractmethod
    def set_nickname(self, user, host, nickname):
        """
        Set nickname in a user's vCard
        """
        pass

    @abstractmethod
    def set_presence(self, user, host, resource, type, show, status, priority):
        """
        Set presence of a session
        """
        pass

    # TODO def set_room_affiliation(self, name, service, jid, affiliation):
    # Change an affiliation in a MUC room

    @abstractmethod
    def set_vcard(self, user, host, name, content):
        """
        Set content in a vCard field
        """
        pass

    @abstractmethod
    def set_vcard2(self, user, host, name, subname, content):
        """
        Set content in a vCard subfield
        """
        pass

    @abstractmethod
    def set_vcard2_multi(self, user, host, name, subname, contents):
        """
        *Set multiple contents in a vCard subfield
        """
        pass

    @abstractmethod
    def srg_create(self, group, host, name, description, display):
        """
        Create a Shared Roster Group
        """
        pass

    @abstractmethod
    def srg_delete(self, group, host):
        """
        Delete a Shared Roster Group
        """
        pass

    @abstractmethod
    def srg_get_info(self, group, host):
        """
        Get info of a Shared Roster Group
        """
        pass

    @abstractmethod
    def srg_get_members(self, group, host):
        """
        Get members of a Shared Roster Group
        """
        pass

    @abstractmethod
    def srg_list(self, host):
        """
        List the Shared Roster Groups in Host
        """
        pass

    @abstractmethod
    def srg_user_add(self, user, host, group, grouphost):
        """
        Add the JID user@host to the Shared Roster Group
        """
        pass

    @abstractmethod
    def srg_user_del(self, user, host, group, grouphost):
        """
        Delete this JID user@host from the Shared Roster Group
        """
        pass

    @abstractmethod
    def stats(self, name):
        """
        Get statistical value:

        * ``registeredusers``
        * ``onlineusers``
        * ``onlineusersnode``
        * ``uptimeseconds``
        * ``processes`` - Introduced sometime after Ejabberd 15.07
        """
        pass

    @abstractmethod
    def stats_host(self, name, host):
        """
        Get statistical value for this host:

        * ``registeredusers``
        * ``onlineusers``
        """
        pass

    @abstractmethod
    def status(self):
        """
        Get ejabberd status
        """
        pass

    @abstractmethod
    def status_list(self, status):
        """
        List of logged users with this status
        """
        pass

    @abstractmethod
    def status_list_host(self, host, status):
        """
        List of users logged in host with their statuses
        """
        pass

    @abstractmethod
    def status_num(self, status):
        """
        Number of logged users with this status
        """
        pass

    @abstractmethod
    def status_num_host(self, host, status):
        """
        Number of logged users with this status in host
        """
        pass

    @abstractmethod
    def stop(self):
        """
        Stop ejabberd
        """
        pass

    @abstractmethod
    def stop_kindly(self, delay, announcement):
        """
        Inform users and rooms, wait, and stop the server
        """
        pass

    # TODO def subscribe_room(self, user, nick, room, nodes):
    # Subscribe to a MUC conference

    # TODO def unsubscribe_room(self, user, room):
    # Unsubscribe from a MUC conference

    @abstractmethod
    def update(self, module):
        """
        Update the given module, or use the keyword: all
        """
        pass

    @abstractmethod
    def update_list(self):
        """
        List modified modules that can be updated
        """
        pass

    @abstractmethod
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
        pass
