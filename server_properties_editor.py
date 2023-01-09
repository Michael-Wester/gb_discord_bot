import os
import shutil


def initialise_property_file(server_id, server_name, game_type):
    if not os.path.exists("servers/"):
        try:
            os.mkdir("servers/")
        except:
            print("directory already exists")
    try:
        os.mkdir("servers/" + str(server_id))

        os.mkdir("servers/" + str(server_id) + "/images")
    except:
        print("directory already exists")

    server_properties_file = open("servers/" + str(server_id) + "/" + str(server_id) + ".properties", "w")
    server_properties_file.write("server_id=" + str(server_id) + "\n")
    server_properties_file.write("server_name=" + str(server_name) + "\n")
    server_properties_file.write("game_type=" + game_type + "\n")
    server_properties_file.write("turn_count=0\n")
    server_properties_file.close()

def get_game_type(server_id):
    server_properties_file = open("servers/" + str(server_id) + "/" + str(server_id) + ".properties", "r")
    game_type = server_properties_file.read().split('\n')
    game_type = game_type[2].split('=')[1]
    server_properties_file.close()
    return game_type

def copy_emulator_files(server_id, game_type):
    shutil.copyfile("roms/" + game_type + '/' + game_type +  ".gb", "servers/" + str(server_id) + "/" + game_type + ".gb")
    shutil.copyfile("roms/" + game_type + '/' + game_type +  ".gb.ram", "servers/" + str(server_id) + "/" + game_type + ".gb.ram")
    shutil.copyfile("roms/" + game_type + '/' + game_type +  ".gb.state", "servers/" + str(server_id) + "/" + game_type + ".gb.state")

def server_exists(server_id):
    
    if os.path.exists(str(server_id)):
        return True
    else:
        return False

def delete_server_folder(server_id):
    shutil.rmtree("servers/" + str(server_id))
    

def increase_turn_count(server_id):
    server_properties_file = open("servers/" + str(server_id) + "/" + str(server_id) + ".properties", "r")
    server_properties = server_properties_file.read().split('\n')
    server_properties_file.close()
    turn_count = server_properties[3].split('=')[1]
    if turn_count == '':
        turn_count = 1
    else:
        turn_count = int(turn_count) + 1
    server_properties_file = open("servers/" + str(server_id) + "/" + str(server_id) + ".properties", "w")
    server_properties_file.write(server_properties[0] + "\n")
    server_properties_file.write(server_properties[1] + "\n")
    server_properties_file.write(server_properties[2] + "\n")
    server_properties_file.write("turn_count=" + str(turn_count) + "\n")
    server_properties_file.close()
    
def get_turn_count(server_id):
    server_properties_file = open("servers/" + str(server_id) + "/" + str(server_id) + ".properties", "r")
    server_properties = server_properties_file.read().split('\n')
    server_properties_file.close()
    turn_count = server_properties[3].split('=')[1]
    if turn_count == '':
        turn_count = 0
    else:
        turn_count = int(turn_count)
    return turn_count

def add_to_command_list(server_id, cmd, turn_count, author, time):
    with open("servers/" + str(server_id) + "/" + str(server_id) + ".data", "a") as f:
        f.write(cmd + "," + str(turn_count) + "," + author + "," + str(time) + "\n")