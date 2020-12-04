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
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def registered_users(self, host):
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def register(self, user, host, password):
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def unregister(self, user, host):
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def change_password(self, user, host, password, newpass):
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def check_password_hash(self, user, host, password):
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def connected_users(self):
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def connected_users_info(self):
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def connected_users_number(self):
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def user_sessions_info(self, user, host):
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def muc_online_rooms(self, service=None):
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def create_room(self, name, service, host):
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def destroy_room(self, name, service):
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def get_room_options(self, name, service):
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def change_room_option(self, name, service, option, value):
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def set_room_affiliation(self, name, service, jid, affiliation):
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def get_room_affiliations(self, name, service):
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def add_rosteritem(self,
                       localuser, localhost,
                       user, host,
                       nick, group, subs):
        """
        Add an item to a user's roster (self,supports ODBC):
        """
        raise NotImplementedError("subclass must implement this method")

    # TODO def backup(self, file): Store the database to backup file

    @abstractmethod
    def ban_account(self, user, host, reason):
        """
        Ban an account: kick sessions and set random password
        """
        raise NotImplementedError("subclass must implement this method")

    # TODO def change_room_option(self, name, service, option, value)
    # Change an option in a MUC room

    @abstractmethod
    def check_account(self, user, host):
        """
        Check if an account exists or not
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def check_password(self, user, host, password):
        """
        Check if a password is correct
        """
        raise NotImplementedError("subclass must implement this method")

    # TODO def compile(self, file):
    # Recompile and reload Erlang source code file

    @abstractmethod
    def connected_users_vhost(self, host):
        """
        Get the list of established sessions in a vhost
        """
        raise NotImplementedError("subclass must implement this method")

    # TODO def convert_to_scram(self, host):
    # Convert the passwords in ‘users’ SQL table to SCRAM

    # TODO def convert_to_yaml(self, in, out):
    # Convert the input file from Erlang to YAML format

    @abstractmethod
    def create_room_with_opts(self, name, service, host, options):
        """
        Create a MUC room name@service in host with given options
        """
        raise NotImplementedError("subclass must implement this method")

    # TODO def create_rooms_file(self, file):
    # Create the rooms indicated in file

    @abstractmethod
    def delete_expired_messages(self):
        """
        Delete expired offline messages from database
        """
        raise NotImplementedError("subclass must implement this method")

    # TODO def delete_mnesia(self, host):
    # Export all tables as SQL queries to a file

    # TODO def delete_old_mam_messages(self, type, days):
    # Delete MAM messages older than DAYS

    @abstractmethod
    def delete_old_messages(self, days):
        """
        Delete offline messages older than DAYS
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def delete_old_users(self, days):
        """
        Delete users that didn't log in last days, or that never logged
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def delete_old_users_vhost(self, host, days):
        """
        Delete users that didn't log in last days in vhost,
        or that never logged
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def delete_rosteritem(self, localuser, localserver, user, server):
        """
        Delete an item from a user's roster (self,supports ODBC):
        """
        raise NotImplementedError("subclass must implement this method")

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
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def get_last(self, user, host):
        """
        Get last activity information (self,timestamp and status):
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def get_loglevel(self):
        """
        Get the current loglevel
        """
        raise NotImplementedError("subclass must implement this method")

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
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def get_subscribers(self, name, service):
        """
        List subscribers of a MUC conference
        """
        raise NotImplementedError("subclass must implement this method")

    def get_user_rooms(self, user, host):
        """
        Get the list of rooms where this user is occupant
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def get_vcard(self, user, host, name):
        """
        Get content from a vCard field
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def get_vcard2(self, user, host, name, subname):
        """
        Get content from a vCard field
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def get_vcard2_multi(self, user, host, name, subname):
        """
        Get multiple contents from a vCard field
        """
        raise NotImplementedError("subclass must implement this method")

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
        raise NotImplementedError("subclass must implement this method")

    # TODO def install_fallback(self, file):
    # Install the database from a fallback file

    # TODO def join_cluster(self, node):
    # Join this node into the cluster handled by Node
    @abstractmethod
    def kick_session(self, user, host, resource, reason):
        """
        Kick a user session
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def kick_user(self, user, host):
        """
        Disconnect user's active sessions
        """
        raise NotImplementedError("subclass must implement this method")

    # TODO def leave_cluster(self, node):
    # Remove node handled by Node from the cluster
    @abstractmethod
    def list_cluster(self):
        """
        List nodes that are part of the cluster handled by Node
        """
        raise NotImplementedError("subclass must implement this method")

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
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def modules_installed(self):
        """
        List installed modules
        """
        raise NotImplementedError("subclass must implement this method")

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
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def outgoing_s2s_number(self):
        """
        Number of outgoing s2s connections on the node
        """
        raise NotImplementedError("subclass must implement this method")

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
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def push_alltoall(self, host, group):
        """
        Add all the users to all the users of Host in Group
        """
        raise NotImplementedError("subclass must implement this method")

    # TODO def push_roster(self, file, user, host):
    # Push template roster from file to a user

    # TODO def push_roster_all(self, file):
    # Push template roster from file to all those users
    @abstractmethod
    def registered_vhosts(self):
        """
        List all registered vhosts in SERVER
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def reload_config(self):
        """
        Reload ejabberd configuration file into memory
        (only affects ACL and Access)
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def reopen_log(self):
        """
        Reopen the log files
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def resource_num(self, user, host, num):
        """
        Resource string of a session number
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def restart(self):
        """
        Restart ejabberd
        """
        raise NotImplementedError("subclass must implement this method")

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
        raise NotImplementedError("subclass must implement this method")

    # TODO def send_stanza(self, from, to, stanza):
    # Send a stanza; provide From JID and valid To JID
    @abstractmethod
    def send_stanza_c2s(self, user, host, resource, stanza):
        """
        Send a stanza as if sent from a c2s session
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def set_last(self, user, host, timestamp, status):
        """
        Set last activity information
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def set_loglevel(self, loglevel):
        """
        Set the loglevel (0 to 5)
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def set_master(self, nodename):
        """
        Set master node of the clustered Mnesia tables
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def set_nickname(self, user, host, nickname):
        """
        Set nickname in a user's vCard
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def set_presence(self, user, host, resource, type, show, status, priority):
        """
        Set presence of a session
        """
        raise NotImplementedError("subclass must implement this method")

    # TODO def set_room_affiliation(self, name, service, jid, affiliation):
    # Change an affiliation in a MUC room

    @abstractmethod
    def set_vcard(self, user, host, name, content):
        """
        Set content in a vCard field
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def set_vcard2(self, user, host, name, subname, content):
        """
        Set content in a vCard subfield
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def set_vcard2_multi(self, user, host, name, subname, contents):
        """
        *Set multiple contents in a vCard subfield
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def srg_create(self, group, host, name, description, display):
        """
        Create a Shared Roster Group
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def srg_delete(self, group, host):
        """
        Delete a Shared Roster Group
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def srg_get_info(self, group, host):
        """
        Get info of a Shared Roster Group
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def srg_get_members(self, group, host):
        """
        Get members of a Shared Roster Group
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def srg_list(self, host):
        """
        List the Shared Roster Groups in Host
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def srg_user_add(self, user, host, group, grouphost):
        """
        Add the JID user@host to the Shared Roster Group
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def srg_user_del(self, user, host, group, grouphost):
        """
        Delete this JID user@host from the Shared Roster Group
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def stats(self, name):
        """
        Get statistical value:
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def stats_host(self, name, host):
        """
        Get statistical value for this host:
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def status(self):
        """
        Get ejabberd status
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def status_list(self, status):
        """
        List of logged users with this status
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def status_list_host(self, host, status):
        """
        List of users logged in host with their statuses
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def status_num(self, status):
        """
        Number of logged users with this status
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def status_num_host(self, host, status):
        """
        Number of logged users with this status in host
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def stop(self):
        """
        Stop ejabberd
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def stop_kindly(self, delay, announcement):
        """
        Inform users and rooms, wait, and stop the server
        """
        raise NotImplementedError("subclass must implement this method")

    def subscribe_room(self, user, nick, room, nodes):
        """
        Subscribe to a MUC conference
        """
        raise NotImplementedError("subclass must implement this method")

    def unsubscribe_room(self, user, room):
        """
        Unsubscribe from a MUC conference
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def update(self, module):
        """
        Update the given module, or use the keyword: all
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def update_list(self):
        """
        List modified modules that can be updated
        """
        raise NotImplementedError("subclass must implement this method")

    @abstractmethod
    def user_resources(self, user, host):
        """
        List user's connected resources
        """
        raise NotImplementedError("subclass must implement this method")
