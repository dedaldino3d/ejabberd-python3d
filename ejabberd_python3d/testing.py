from ejabberd_python3d import client

conn = client.EjabberdAPIClient("localhost", "dedaldino", "Dedaldino18", "localhost")
groups = conn.muc_online_rooms()

for g in groups:
    # TODO: add get_room_occupants in ejabberd_python3d lib
    room_name = g['room'].split('@')[0]
    subs = [u.split('@')[0] for u in
            conn.get_subscribers(room_name, 'groupchat.localhost')]
    print("subs: ", subs)
    options = conn.get_room_options(room_name, 'groupchat.localhost')
    print("muc options: ", options)

