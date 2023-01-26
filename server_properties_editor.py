import os
import shutil
import time


def initialise_property_file(server_id, server_name, game_type):
    if not os.path.exists("servers/"):
        os.mkdir("servers/")
    if not os.path.exists("servers_bin/"):
        os.mkdir("servers_bin/")
    try:
        os.mkdir("servers/" + str(server_id))
        os.mkdir("servers/" + str(server_id) + "/images")
    except:
        print("directory already exists")

    server_properties_file = open(
        "servers/" + str(server_id) + "/" + str(server_id) + ".properties", "w"
    )
    server_properties_file.write("date_created=0\n")
    server_properties_file.write("owner_id=0\n")
    server_properties_file.write("server_id=" + str(server_id) + "\n")
    server_properties_file.write("server_name=" + str(server_name) + "\n")
    server_properties_file.write("game_type=" + game_type + "\n")
    server_properties_file.write("turn_count=0\n")
    server_properties_file.write("prefix=!\n")
    server_properties_file.write("cmp_prefix=!!\n")
    server_properties_file.write("press_tick=4\n")
    server_properties_file.write("release_tick=120\n")
    server_properties_file.write("progress_bar=0\n")
    server_properties_file.write("progress_bar_height=3\n")
    server_properties_file.write("progress_bar_colour=red\n")
    server_properties_file.write("cmd_set=1\n")

    server_properties_file.close()


def get_server_properties(server_id):
    server_properties_file = open(
        "servers/" + str(server_id) + "/" + str(server_id) + ".properties", "r"
    )
    server_properties = server_properties_file.read().split("\n")
    server_properties_file.close()
    return server_properties


def reinitialise_property_file(server_id):
    property_list = [
        ("date_created", "0"),
        ("owner_id", "0"),
        ("server_id", "id"),
        ("server_name", "name"),
        ("game_type", "red"),
        ("turn_count", "0"),
        ("prefix", "!"),
        ("cmp_prefix", "!!"),
        ("press_tick", "4"),
        ("release_tick", "120"),
        ("progress_bar", "0"),
        ("progress_bar_height", "3"),
        ("progress_bar_colour", "red"),
        ("cmd_set", "1"),
    ]
    for property, default_value in property_list:
        if read_property(server_id, property) == None:
            with open(
                "servers/" + str(server_id) + "/" + str(server_id) + ".properties", "a"
            ) as f:
                f.write(str(property) + "=" + str(default_value) + "\n")


def get_game_type(server_id):
    game_type = read_value(server_id, "game_type")
    return game_type


def copy_emulator_files(server_id, game_type):
    roms_folder = "roms/" + game_type + "/"
    server_folder = "servers/" + str(server_id) + "/"
    shutil.copyfile(
        roms_folder + game_type + ".gb",
        server_folder + game_type + ".gb",
    )
    shutil.copyfile(
        roms_folder + game_type + ".gb.ram",
        server_folder + game_type + ".gb.ram",
    )
    shutil.copyfile(
        roms_folder + game_type + ".gb.state",
        server_folder + game_type + ".gb.state",
    )


def delete_server_folder(server_id):   
    if os.path.exists("server_bin/" + str(server_id)):
        shutil.rmtree("server_bin/" + str(server_id))
        
    shutil.move("servers/" + str(server_id), "server_bin")
    return
        


def update_server_property_value(server_id, property, value):
    server_properties = get_server_properties(server_id)
    server_properties_file = open(
        "servers/" + str(server_id) + "/" + str(server_id) + ".properties", "w"
    )
    for i in range(len(server_properties)):
        if server_properties[i].split("=")[0] == property:
            server_properties[i] = property + "=" + value
        if server_properties[i] != "":
            server_properties_file.write(server_properties[i] + "\n")
    server_properties_file.close()


def read_value(server_id, property):
    server_properties = get_server_properties(server_id)
    for i in range(len(server_properties)):
        if server_properties[i].split("=")[0] == property:
            return server_properties[i].split("=")[1]
        
#print(read_value(957136739632295966, "prefix"))


def read_property(server_id, property):
    server_properties = get_server_properties(server_id)
    for i in range(len(server_properties)):
        if server_properties[i].split("=")[0] == property:
            return server_properties[i].split("=")[0]
    return None


def increase_turn_count(server_id):
    turn_count = read_value(server_id, "turn_count")
    turn_count = int(turn_count) + 1
    update_server_property_value(server_id, "turn_count", str(turn_count))
    return turn_count


def record_cmd(server_id, cmd, author):
    turn_count = increase_turn_count(server_id)
    current_time = str(time.time())
    with open("servers/" + str(server_id) + "/" + str(server_id) + ".data", "a") as f:
        f.write(cmd + "," + str(turn_count) + "," + author + "," + current_time + "\n")
    return

