import os
import shutil

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

def get_game_type(server_id):
    server_properties_file = open(str(server_id) + "/" + str(server_id) + ".properties", "r")
    # get game_type from server properties file
    game_type = server_properties_file.read().split('\n')
    game_type = game_type[2].split('=')[1]
    server_properties_file.close()
    return game_type

def get_server_list(server_id):
    serverlist = open(str(server_id) + "/serverlist.txt", "r")
    serverlist_list = serverlist.read().splitlines()
    serverlist.close()
    return serverlist_list

def append_server(server_id):
    with open(str(server_id) + "/serverlist.txt", "a") as f:
        f.write(str(server_id) + "\n")
    return True

def remove_server(server_id):
    with open("serverlist.txt", "r") as input:
        with open("temp.txt", "w") as output:
            for line in input:
                if line.strip("\n") != str(server_id):
                    output.write(line)

    os.replace('temp.txt', 'serverlist.txt')

def delete_temp_files(server_id):
    try:      
        shutil.rmtree(str(server_id))
        print("deleted temp files")
    except:
        print("temp files not found")