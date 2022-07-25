import os
from re import L

def initialise_property_file_folder(server_id):
    try:
        os.mkdir(str(server_id))
    except:
        print("directory already exists")


def initialise_property_file(server_id, server_name, game_type):
    # create server properties file
    initialise_property_file_folder(server_id)
    server_properties_file = open(str(server_id) + "/" + str(server_id) + ".properties", "w")
    server_properties_file.write("server_id=" + str(server_id) + "\n")
    server_properties_file.write("server_name=" + str(server_name) + "\n")
    server_properties_file.write("game_type=" + game_type + "\n")
    server_properties_file.close()

initialise_property_file(1, "Test Server", "test")

def get_game_type(server_id):
    server_properties_file = open(str(server_id) + "/" + str(server_id) + ".properties", "r")
    # get game_type from server properties file
    game_type = server_properties_file.readline().split("=")[2]
    server_properties_file.close()
    return game_type

def append_server(server_id):
    serverlist = open("serverlist.txt", "r")
    # For each server in the serverlist
    for server in serverlist:
        serverlist_list = serverlist.read().splitlines()
        print(serverlist_list)
        
    if str(server_id) not in serverlist_list:
        serverlist.close()
        serverlist = open("serverlist.txt", "a")
        serverlist.write(str(server_id) + "\n")
        serverlist.close()
        return False
    return True

def remove_server(server_id):
    with open("serverlist.txt", "r") as input:
        with open("temp.txt", "w") as output:
            for line in input:
                if line.strip("\n") != str(server_id):
                    output.write(line)

    os.replace('temp.txt', 'serverlist.txt')