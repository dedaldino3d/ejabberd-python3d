from __future__ import print_function

import xmlrpc

from httplib import BadStatusLine


class EjabberdAPI(object):
    '''
    Python client for Ejabberd XML-RPC Administration API.
    '''
    def __init__(self,
                 host, username, password,
                 protocol='http', server='127.0.0.1', port=4560,
                 admin=True, verbose=False):
        '''
        Init XML-RPC server proxy.
        '''
        self.params = {'user': username,
                       'password': password,
                       'server': host,
                       'admin': admin}
        self.errors = {
            'connect': 'ERROR: cannot connect to the server/the call crashed',
            'access': 'ERROR: access denied, account unprivileged',
            'bad_arg': 'ERROR: call failed, bad input argument',
            'missing_arg': 'ERROR: call failed, missing input argument'
            }
        uri = '{}://{}:{}'.format(protocol, server, port)
        self.xmlrpc_server = xmlrpc.ServerProxy(uri, verbose=verbose)

    def _call_api(self, command, **kwargs):
        '''
        Run ejabberd command.
        '''
        fn = getattr(self.xmlrpc_server, command)
        try:
            if kwargs:
                return fn(self.params, **kwargs)
            return fn(self.params)
        except BadStatusLine, e:
            raise Exception('{}\n{}'.format(self.errors['connect'],
                                            e.message))
        except xmlrpc.Fault, e:
            if 'account_unprivileged' in e.message:
                raise Exception('{}\n{}'.format(self.errors['access'],
                                                e.message))
            if 'bad_argument' in e.message:
                raise Exception('{}\n{}'.format(self.errors['bad_arg'],
                                                e.message))
            if 'Required attribute' in e.message and 'not found' in e.message:
                raise Exception('{}\n{}'.format(self.errors['missing_arg'],
                                                e.message))
            raise Exception(e)

    def add_rosteritem(self,
                       localuser, localserver,
                       user, server,
                       nick, group, subs):
        '''
        Add an item to a user's roster (self,supports ODBC):
        '''
        return self._call_api('add_rosteritem', {'localuser': localuser,
                                           'localserver': localserver,
                                           'user': user,
                                           'server': server,
                                           'nick': nick,
                                           'group': group,
                                           'subs': subs})

    # TODO def backup(self, file): Store the database to backup file

    def ban_account(self, user, host, reason):
        '''
        Ban an account: kick sessions and set random password
        '''
        return self._call_api('ban_account', {'user': user,
                                        'host': host,
                                        'reason': reason})

    def change_password(self, user, host, newpass):
        '''
        Change the password of an account
        '''
        return self._call_api('change_password', {'user': user,
                                            'host': host,
                                            'newpass': newpass})

    # TODO def change_room_option(self, name, service, option, value)
    # Change an option in a MUC room

    def check_account(self, user, host):
        '''
        Check if an account exists or not
        '''
        return self._call_api('check_account', {'user': user, 'host': host})

    def check_password(self, user, host, password):
        '''
        Check if a password is correct
        '''
        return self._call_api('check_password', {'user': user,
                                           'host': host,
                                           'password': password})

    def check_password_hash(self, user, host, passwordhash, hashmethod):
        '''
        Check if the password hash is correct
        '''
        return self._call_api('check_password_hash', {'user': user,
                                                'host': host,
                                                'passwordhash': passwordhash,
                                                'hashmethod': hashmethod})

    # TODO def compile(self, file):
    # Recompile and reload Erlang source code file

    def connected_users(self):
        '''
        List all established sessions
        '''
        return self._call_api('connected_users')

    def connected_users_info(self):
        '''
        List all established sessions and their information
        '''
        return self._call_api('connected_users_info')

    def connected_users_number(self):
        '''
        Get the number of established sessions
        '''
        return self._call_api('connected_users_number')

    def connected_users_vhost(self, host):
        '''
        Get the list of established sessions in a vhost
        '''
        return self._call_api('connected_users_vhost', {'host': host})

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
        '''
        Delete expired offline messages from database
        '''
        return self._call_api('delete_expired_messages')

    # TODO def delete_mnesia(self, host):
    # Export all tables as SQL queries to a file

    # TODO def delete_old_mam_messages(self, type, days):
    # Delete MAM messages older than DAYS

    def delete_old_messages(self, days):
        '''
        Delete offline messages older than DAYS
        '''
        return self._call_api('delete_old_messages', {'days': days})

    def delete_old_users(self, days):
        '''
        Delete users that didn't log in last days, or that never logged
        '''
        return self._call_api('delete_old_users', {'days': days})

    def delete_old_users_vhost(self, host, days):
        '''
        Delete users that didn't log in last days in vhost,
        or that never logged
        '''
        return self._call_api('delete_old_users_vhost',
                        {'host': host, 'days': days})

    def delete_rosteritem(self, localuser, localserver, user, server):
        '''
        Delete an item from a user's roster (self,supports ODBC):
        '''
        return self._call_api('delete_rosteritem', {'localuser': localuser,
                                              'localserver': localserver,
                                              'user': user,
                                              'server': server})

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

    def get_cookie(self):
        '''
        Get the Erlang cookie of this node
        '''
        return self._call_api('get_cookie')

    def get_last(self, user, host):
        '''
        Get last activity information (self,timestamp and status):
        '''
        return self._call_api('get_last', {'user': user, 'host': host})

    def get_loglevel(self):
        '''
        Get the current loglevel
        '''
        return self._call_api('get_loglevel')

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
        '''
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

        '''
        try:
            return self._call_api('get_roster', {'user': user, 'server': server})
        except:
            return self._call_api('get_roster', {'user': user, 'host': server})

    # TODO get_subscribers(self, name, service):
    # List subscribers of a MUC conference

    # TODO get_user_rooms(self, user, host):
    # Get the list of rooms where this user is occupant

    def get_vcard(self, user, host, name):
        '''
        Get content from a vCard field
        '''
        return self._call_api('get_vcard', {'user': user,
                                      'host': host,
                                      'name': name})

    def get_vcard2(self, user, host, name, subname):
        '''
        Get content from a vCard field
        '''
        return self._call_api('get_vcard2', {'user': user,
                                       'host': host,
                                       'name': name,
                                       'subname': subname})

    def get_vcard2_multi(self, user, host, name, subname):
        '''
        Get multiple contents from a vCard field
        '''
        return self._call_api('get_vcard2_multi', {'user': user,
                                             'host': host,
                                             'name': name,
                                             'subname': subname})

    # TODO def import_dir(self, file):
    # Import users data from jabberd14 spool dir

    # TODO def import_file(self, file):
    # Import users data from jabberd14 spool file

    # TODO def import_piefxis(self, file):
    # Import users data from a PIEFXIS file (XEP-0227)

    # TODO def import_prosody(self, dir) Import data from Prosody

    def incoming_s2s_number(self):
        '''
        Number of incoming s2s connections on the node
        '''
        return self._call_api('incoming_s2s_number')

    # TODO def install_fallback(self, file):
    # Install the database from a fallback file

    # TODO def join_cluster(self, node):
    # Join this node into the cluster handled by Node

    def kick_session(self, user, host, resource, reason):
        '''
        Kick a user session
        '''
        return self._call_api('kick_session', {'user': user,
                                         'host': host,
                                         'resource': resource,
                                         'reason': reason})

    def kick_user(self, user, host):
        '''
        Disconnect user's active sessions
        '''
        return self._call_api('kick_user', {'user': user, 'host': host})

    # TODO def leave_cluster(self, node):
    # Remove node handled by Node from the cluster

    def list_cluster(self):
        '''
        List nodes that are part of the cluster handled by Node

        Result:

        {nodes,{list,{node,atom}}}

        '''
        try:
            return self._call_api('list_cluster')
        except xmlrpc.Fault, e:
            msg = 'list_cluster is NOT available in your version of ejabberd'
            raise Exception('{}\n{}\n'.format(msg, e.message))

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
        '''
        List available modules
        '''
        return self._call_api('modules_available')

    def modules_installed(self):
        '''
        List installed modules
        '''
        return self._call_api('modules_installed')

    # TODO def modules_update_specs(self):

    # TODO def muc_online_rooms(self, host):
    # List existing rooms (‘global’ to get all vhosts)

    # TODO def muc_unregister_nick(self, nick):
    # Unregister the nick in the MUC service

    def num_active_users(self, host, days):
        '''
        Get number of users active in the last days
        '''
        return self._call_api('num_active_users', {'host': host, 'days': days})

    def num_resources(self, user, host):
        '''
        Get the number of resources of a user
        '''
        return self._call_api('num_resources', {'user': user, 'host': host})

    def outgoing_s2s_number(self):
        '''
        Number of outgoing s2s connections on the node
        '''
        return self._call_api('outgoing_s2s_number')

    # TODO def privacy_set(self, user, host, xmlquery):
    # Send a IQ set privacy stanza for a local account

    # TODO def private_get(self, user, host, element, ns):
    # Get some information from a user private storage

    # TODO def private_set(self, user, host, element):
    # Set to the user private storage

    def process_rosteritems(self, action, subs, asks, users, contacts):
        '''
        List or delete rosteritems that match filtering options
        '''
        return self._call_api('process_rosteritems', {'action': action,
                                                'subs': subs,
                                                'asks': asks,
                                                'users': users,
                                                'contacts': contacts})

    def push_alltoall(self, host, group):
        '''
        Add all the users to all the users of Host in Group
        '''
        return self._call_api('push_alltoall', {'host': host, 'group': group})

    # TODO def push_roster(self, file, user, host):
    # Push template roster from file to a user

    # TODO def push_roster_all(self, file):
    # Push template roster from file to all those users

    def register(self, user, host, password):
        '''
        Register a user
        '''
        return self._call_api('register', {'user': user,
                                     'host': host,
                                     'password': password})

    def registered_users(self, host):
        '''
        List all registered users in HOST
        '''
        return self._call_api('registered_users', {'host': host})

    def registered_vhosts(self):
        '''
        List all registered vhosts in SERVER
        '''
        return self._call_api('registered_vhosts')

    def reload_config(self):
        '''
        Reload ejabberd configuration file into memory

        (only affects ACL and Access)
        '''
        return self._call_api('reload_config')

    def remove_node(self, node):
        '''
        Remove an ejabberd node from Mnesia clustering config
        '''
        return self._call_api('remove_node', {'node': node})

    def reopen_log(self):
        '''
        Reopen the log files
        '''
        return self._call_api('reopen_log')

    def resource_num(self, user, host, num):
        '''
        Resource string of a session number
        '''
        return self._call_api('resource_num', {'user': user,
                                         'host': host,
                                         'num': num})

    def restart(self):
        '''
        Restart ejabberd
        '''
        return self._call_api('restart')

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

    def send_message(self, type, from_jid, to, subject, body):
        '''
        Send a message to a local or remote bare of full JID
        '''
        return self._call_api('send_message', {'type': type,
                                         'from': from_jid,
                                         'to': to,
                                         'subject': subject,
                                         'body': body})

    # TODO def send_stanza(self, from, to, stanza):
    # Send a stanza; provide From JID and valid To JID

    def send_stanza_c2s(self, user, host, resource, stanza):
        '''
        Send a stanza as if sent from a c2s session
        '''
        return self._call_api('send_stanza_c2s', {'user': user,
                                            'host': host,
                                            'resource': resource,
                                            'stanza': stanza})

    def set_last(self, user, host, timestamp, status):
        '''
        Set last activity information
        '''
        return self._call_api('set_last', {'user': user,
                                     'host': host,
                                     'timestamp': timestamp,
                                     'status': status})

    def set_loglevel(self, loglevel):
        '''
        Set the loglevel (0 to 5)

        Arguments:

            loglevel :: integer

        Result:

        {logger,atom}

        '''
        try:
            return self._call_api('set_loglevel', {'loglevel': loglevel})
        except xmlrpc.Fault, e:
            msg = 'set_loglevel is NOT available in your version of ejabberd'
            raise Exception('{}\n{}\n'.format(msg, e.message))

    def set_master(self, nodename):
        '''
        Set master node of the clustered Mnesia tables
        '''
        return self._call_api('set_master', {'nodename': nodename})

    def set_nickname(self, user, host, nickname):
        '''
        Set nickname in a user's vCard
        '''
        return self._call_api('set_nickname', {'user': user,
                                         'host': host,
                                         'nickname': nickname})

    def set_presence(self, user, host, resource, type, show, status, priority):
        '''
        Set presence of a session
        '''
        return self._call_api('set_presence', {'user': user,
                                         'host': host,
                                         'resource': resource,
                                         'type': type,
                                         'show': show,
                                         'status': status,
                                         'priority': priority})

    # TODO def set_room_affiliation(self, name, service, jid, affiliation):
    # Change an affiliation in a MUC room

    def set_vcard(self, user, host, name, content):
        '''
        Set content in a vCard field
        '''
        return self._call_api('set_vcard', {'user': user,
                                      'host': host,
                                      'name': name,
                                      'content': content})

    def set_vcard2(self, user, host, name, subname, content):
        '''
        Set content in a vCard subfield
        '''
        return self._call_api('set_vcard2', {'user': user,
                                       'host': host,
                                       'name': name,
                                       'subname': subname,
                                       'content': content})

    def set_vcard2_multi(self, user, host, name, subname, contents):
        '''
        *Set multiple contents in a vCard subfield
        '''
        return self._call_api('set_vcard2_multi', {'user': user,
                                             'host': host,
                                             'name': name,
                                             'subname': subname,
                                             'contents': contents})

    def srg_create(self, group, host, name, description, display):
        '''
        Create a Shared Roster Group
        '''
        return self._call_api('srg_create', {'group': group,
                                       'host': host,
                                       'name': name,
                                       'description': description,
                                       'display': display})

    def srg_delete(self, group, host):
        '''
        Delete a Shared Roster Group
        '''
        return self._call_api('srg_delete', {'group': group, 'host': host})

    def srg_get_info(self, group, host):
        '''
        Get info of a Shared Roster Group
        '''
        return self._call_api('srg_get_info', {'group': group, 'host': host})

    def srg_get_members(self, group, host):
        '''
        Get members of a Shared Roster Group
        '''
        return self._call_api('srg_get_members', {'group': group, 'host': host})

    def srg_list(self, host):
        '''
        List the Shared Roster Groups in Host
        '''
        return self._call_api('srg_list', {'host': host})

    def srg_user_add(self, user, host, group, grouphost):
        '''
        Add the JID user@host to the Shared Roster Group
        '''
        return self._call_api('srg_user_add', {'user': user,
                                         'host': host,
                                         'group': group,
                                         'grouphost': grouphost})

    def srg_user_del(self, user, host, group, grouphost):
        '''
        Delete this JID user@host from the Shared Roster Group
        '''
        return self._call_api('srg_user_del', {'user': user,
                                         'host': host,
                                         'group': group,
                                         'grouphost': grouphost})

    def stats(self, name):
        '''
        Get statistical value:

        * ``registeredusers``
        * ``onlineusers``
        * ``onlineusersnode``
        * ``uptimeseconds``
        * ``processes`` - Introduced sometime after Ejabberd 15.07
        '''
        try:
            return self._call_api('stats', {'name': name})
        except Exception, e:
            msg = 'processes stats NOT available in this version of Ejabberd'
            if e.message == self.errors['connect']:
                raise Exception('{}\n{}\n'.format(msg, e.message))
            raise Exception(e)

    def stats_host(self, name, host):
        '''
        Get statistical value for this host:

        * ``registeredusers``
        * ``onlineusers``
        '''
        return self._call_api('stats_host', {'name': name, 'host': host})

    def status(self):
        '''
        Get ejabberd status
        '''
        return self._call_api('status')

    def status_list(self, status):
        '''
        List of logged users with this status
        '''
        return self._call_api('status_list', {'status': status})

    def status_list_host(self, host, status):
        '''
        List of users logged in host with their statuses
        '''
        return self._call_api('status_list_host', {'host': host, 'status': status})

    def status_num(self, status):
        '''
        Number of logged users with this status
        '''
        return self._call_api('status_num', {'status': status})

    def status_num_host(self, host, status):
        '''
        Number of logged users with this status in host
        '''
        return self._call_api('status_num_host', {'host': host, 'status': status})

    def stop(self):
        '''
        Stop ejabberd
        '''
        return self._call_api('stop')

    def stop_kindly(self, delay, announcement):
        '''
        Inform users and rooms, wait, and stop the server
        '''
        return self._call_api('stop_kindly',
                        {'delay': delay, 'announcement': announcement})

    # TODO def subscribe_room(self, user, nick, room, nodes):
    # Subscribe to a MUC conference

    def unregister(self, user, host):
        '''
        Unregister a user
        '''
        return self._call_api('unregister', {'user': user, 'host': host})

    # TODO def unsubscribe_room(self, user, room):
    # Unsubscribe from a MUC conference

    def update(self, module):
        '''
        Update the given module, or use the keyword: all
        '''
        return self._call_api('update', {'module': module})

    def update_list(self):
        '''
        List modified modules that can be updated
        '''
        return self._call_api('update_list')

    def user_resources(self, user, server):
        '''
        List user's connected resources

        Note, parameters changed in 15.09
        from ``user, host``
        to ``user, server``.

        Arguments:

        user :: binary
        server :: binary

        Result:

        {resources,{list,{resource,string}}}

        '''
        try:
            return self._call_api('user_resources', {'user': user, 'server': server})
        except:
            return self._call_api('user_resources', {'user': user, 'host': server})

    def user_sessions_info(self, user, host):
        '''
        Get information about all sessions of a user
        '''
        return self._call_api('user_sessions_info', {'user': user, 'host': host})
