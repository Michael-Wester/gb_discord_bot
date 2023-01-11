from pyboy import PyBoy
from pyboy import WindowEvent
from pyboy import logger
import constants as c
from server_properties_editor import *
logger.log_level("ERROR")


def movement(press, release, server_id):
    server_folder_path = "servers/" + str(server_id) + "/"
    press_tick = int(read_server_property_value(server_id, "press_tick"))
    release_tick = int(read_server_property_value(server_id, "release_tick"))
    game_type = get_game_type(server_id)
    pyboy = PyBoy(server_folder_path + game_type + '.gb', window_type="headless")
    if(open(server_folder_path + game_type + '.gb.state', 'rb').read() != b''):
        pyboy.load_state(open(server_folder_path + game_type + '.gb.state', 'rb'))

    pyboy.send_input(press)
    for i in range(press_tick):
        pyboy.tick()

    pyboy.send_input(release)
    for i in range(release_tick):
        pyboy.tick()

    pyboy.save_state(open(server_folder_path + game_type + '.gb.state', 'wb'))
    pyboy.stop()
    return pyboy.screen_image()

def a_button(server_id):
    return movement(WindowEvent.PRESS_BUTTON_A, WindowEvent.RELEASE_BUTTON_A, server_id)

def b_button(server_id):
    return movement(WindowEvent.PRESS_BUTTON_B, WindowEvent.RELEASE_BUTTON_B, server_id)

def up_button(server_id):
    return movement(WindowEvent.PRESS_ARROW_UP, WindowEvent.RELEASE_ARROW_UP, server_id)

def down_button(server_id):
    return movement(WindowEvent.PRESS_ARROW_DOWN, WindowEvent.RELEASE_ARROW_DOWN, server_id)

def left_button(server_id):
    return movement(WindowEvent.PRESS_ARROW_LEFT, WindowEvent.RELEASE_ARROW_LEFT, server_id)

def right_button(server_id):
    return movement(WindowEvent.PRESS_ARROW_RIGHT, WindowEvent.RELEASE_ARROW_RIGHT, server_id)

def start_button(server_id):
    return movement(WindowEvent.PRESS_BUTTON_START, WindowEvent.RELEASE_BUTTON_START, server_id)

def select_button(server_id):
    return movement(WindowEvent.PRESS_BUTTON_SELECT, WindowEvent.RELEASE_BUTTON_SELECT, server_id)
