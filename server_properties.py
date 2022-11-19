import os
import shutil

def initialise_property_file(server_id, server_name, game_type):

    try:
        os.mkdir(str(server_id))
    except:
        print("directory already exists")

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

def copy_emulator_files(server_id, game_type):
    shutil.copyfile("roms/" + game_type + '/' + game_type +  ".gb", str(server_id) + "/" + game_type + ".gb")
    shutil.copyfile("roms/" + game_type + '/' + game_type +  ".gb.ram", str(server_id) + "/" + game_type + ".gb.ram")
    shutil.copyfile("roms/" + game_type + '/' + game_type +  ".state", str(server_id) + "/" + game_type + ".state")

def server_exists(server_id):
    if os.path.exists(str(server_id)):
        return True
    else:
        return False

def get_server_list(server_id):
    try:
        serverlist = open(str(server_id) + "/serverlist.txt", "r")
        serverlist_list = serverlist.read().splitlines()
        serverlist.close()
    except:
        serverlist_list = []
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