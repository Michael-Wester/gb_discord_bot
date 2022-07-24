

def appendServer(server_id):
    serverlist = open("serverlist.txt", "r")
    # For each server in the serverlist
    for server in serverlist:
        serverlist_list = serverlist.read().splitlines()
        
    if str(server_id) not in serverlist_list:
        serverlist.close()
        # x = list(chunks(range(0, serverlist_list.length), 2))
        serverlist = open("serverlist.txt", "a")
        serverlist.write(str(server_id) + "\n")
        serverlist.close()

