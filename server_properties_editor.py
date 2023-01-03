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
