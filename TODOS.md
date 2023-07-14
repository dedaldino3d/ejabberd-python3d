# METHODS TO IMPLEMENT
### TODO def backup(self, file): Store the database to backup file
### TODO def change_room_option(self, name, service, option, value)
### TODO def compile(self, file):
### TODO def convert_to_scram(self, host):
### TODO def convert_to_yaml(self, in, out):
### TODO def create_room(self, name, service, host):
### TODO def create_room_with_opts(self, name, service, host, options):
### TODO def create_rooms_file(self, file):
### TODO def delete_mnesia(self, host):
### TODO def delete_old_mam_messages(self, type, days):
### TODO def destroy_room(self, name, service):
### TODO def destroy_rooms_file(self, file):
### TODO def dump(self, file):
### TODO def dump_table(self, file, table):
### TODO def export2sql(self, host, file):
### TODO def export_piefxis(self, dir):
### TODO def export_piefxis_host(self, dir, host):
### TODO def gen_html_doc_for_commands(self, file, regexp, examples):
### TODO def gen_markdown_doc_for_commands(self, file, regexp, examples):
### TODO def get_offline_count(self):
### TODO def get_room_affiliations(self, name, service):
### TODO def get_room_occupants(self, name, service):
### TODO def get_room_occupants_number(self, name, service):
### TODO def get_room_options(self, name, service):
### TODO get_subscribers(self, name, service):
### TODO get_user_rooms(self, user, host):
### TODO def import_dir(self, file):
### TODO def import_file(self, file):
### TODO def import_piefxis(self, file):
### TODO def import_prosody(self, dir) Import data from Prosody
### TODO def install_fallback(self, file):
### TODO def join_cluster(self, node):
### TODO def leave_cluster(self, node):
### TODO def load(self, file):
### TODO def mnesia_change_nodename(self,
### TODO def module_check(self, module):
### TODO def module_install(self, module):
### TODO def module_uninstall(self, module):
### TODO def module_upgrade(self, module):
### TODO def modules_update_specs(self):
### TODO def muc_online_rooms(self, host):
### TODO def muc_unregister_nick(self, nick):
### TODO def privacy_set(self, user, host, xmlquery):
### TODO def private_get(self, user, host, element, ns):
### TODO def private_set(self, user, host, element):
### TODO def push_roster(self, file, user, host):
### TODO def push_roster_all(self, file):
### TODO def restore(self, file):
### TODO def rooms_unused_destroy(self, host, days):
### TODO def rooms_unused_list(self, host, days):
### TODO def rotate_log(self):
### TODO def send_direct_invitation(self,
### TODO def send_stanza(self, from, to, stanza):
### TODO def set_room_affiliation(self, name, service, jid, affiliation):
### TODO def subscribe_room(self, user, nick, room, nodes):
### TODO def unsubscribe_room(self, user, room):
### TODO: add argument options: [{name::string,value::string}]: List of options
### TODO: nodes must be separated by commas, so therefore you can use an array and before send transform arguments
### TODO: some arguments is not required
### TODO: name is between: registeredusers onlineusers onlineusersnode uptimeseconds processes
### TODO: name is between: registeredusers onlineusers
### TODO def backup(self, file): Store the database to backup file
### TODO def change_room_option(self, name, service, option, value)
### TODO def compile(self, file):
### TODO def convert_to_scram(self, host):
### TODO def convert_to_yaml(self, in, out):
### TODO def create_room(self, name, service, host):
### TODO def create_room_with_opts(self, name, service, host, options):
### TODO def create_rooms_file(self, file):
### TODO def delete_mnesia(self, host):
### TODO def delete_old_mam_messages(self, type, days):
### TODO def destroy_room(self, name, service):
### TODO def destroy_rooms_file(self, file):
### TODO def dump(self, file):
### TODO def dump_table(self, file, table):
### TODO def export2sql(self, host, file):
### TODO def export_piefxis(self, dir):
### TODO def export_piefxis_host(self, dir, host):
### TODO def gen_html_doc_for_commands(self, file, regexp, examples):
### TODO def gen_markdown_doc_for_commands(self, file, regexp, examples):
### TODO def get_offline_count(self):
### TODO def get_room_affiliations(self, name, service):
### TODO def get_room_occupants(self, name, service):
### TODO def get_room_occupants_number(self, name, service):
### TODO def get_room_options(self, name, service):
### TODO get_subscribers(self, name, service):
### TODO get_user_rooms(self, user, host):
### TODO def import_dir(self, file):
### TODO def import_file(self, file):
### TODO def import_piefxis(self, file):
### TODO def import_prosody(self, dir) Import data from Prosody
### TODO def install_fallback(self, file):
### TODO def join_cluster(self, node):
### TODO def leave_cluster(self, node):
### TODO def load(self, file):
### TODO def mnesia_change_nodename(self,
### TODO def module_check(self, module):
### TODO def module_install(self, module):
### TODO def module_uninstall(self, module):
### TODO def module_upgrade(self, module):
### TODO def modules_update_specs(self):
### TODO def muc_online_rooms(self, host):
### TODO def muc_unregister_nick(self, nick):
### TODO def privacy_set(self, user, host, xmlquery):
### TODO def private_get(self, user, host, element, ns):
### TODO def private_set(self, user, host, element):
### TODO def push_roster(self, file, user, host):
### TODO def push_roster_all(self, file):
### TODO def restore(self, file):
### TODO def rooms_unused_destroy(self, host, days):
### TODO def rooms_unused_list(self, host, days):
### TODO def rotate_log(self):
### TODO def send_direct_invitation(self,
### TODO def send_stanza(self, from, to, stanza):
### TODO def set_room_affiliation(self, name, service, jid, affiliation):
### TODO def subscribe_room(self, user, nick, room, nodes):
### TODO def unsubscribe_room(self, user, room):

## Generics TODOS
### TODO: add endpoint parameter
### TODO: add it to logger