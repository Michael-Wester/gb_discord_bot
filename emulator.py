from pyboy import PyBoy
from pyboy import logger
from server_properties_editor import *

logger.log_level("ERROR")


def load_game(server_id):
    server_folder_path = "servers/" + str(server_id) + "/"

    game_type = read_server_property_value(server_id, "game_type")
    pyboy = PyBoy(server_folder_path + game_type + ".gb", window_type="headless")
    if open(server_folder_path + game_type + ".gb.state", "rb").read() != b"":
        pyboy.load_state(open(server_folder_path + game_type + ".gb.state", "rb"))
    return pyboy


def movement(server_id, pyboy, press, release):
    press_tick = int(read_server_property_value(server_id, "press_tick"))
    release_tick = int(read_server_property_value(server_id, "release_tick"))

    pyboy.send_input(press)
    for i in range(press_tick):
        pyboy.tick()

    pyboy.send_input(release)
    for i in range(release_tick):
        pyboy.tick()

    return pyboy


def save_screenshot(pyboy):
    return pyboy.screen_image()


def save_and_stop(server_id, pyboy):
    server_folder_path = "servers/" + str(server_id) + "/"
    game_type = read_server_property_value(server_id, "game_type")
    pyboy.save_state(open(server_folder_path + game_type + ".gb.state", "wb"))
    pyboy.stop()


def command(server_id, press, release):
    pyboy = load_game(server_id)
    pyboy = movement(server_id, pyboy, press, release)
    img = save_screenshot(pyboy)
    save_and_stop(server_id, pyboy)
    return img
