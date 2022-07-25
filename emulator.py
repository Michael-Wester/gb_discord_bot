from distutils.command.upload import upload
from pyboy import PyBoy
from pyboy import WindowEvent
from PIL import Image
import constants as c
from emulator import *
from server_properties import *


def double_size(img):
    new_img = img.resize((img.size[0]*2, img.size[1]*2), Image.ANTIALIAS)
    return new_img

def movement(a, b, server_id):
    server_id = str(server_id)
    game_type = get_game_type()
    pyboy = PyBoy(server_id + '/' + game_type + '.gb')
    pyboy.set_emulation_speed(4)
    if(open(server_id + '/' + game_type + '.state', 'rb').read() != b''):
        pyboy.load_state(open(server_id + '/' + game_type + '.state', 'rb'))
    pyboy.tick()
    pyboy.send_input(a)
    pyboy.tick()
    pyboy.tick()
    pyboy.send_input(b)
    for i in range(600):
        pyboy.tick()
    #pyboy.screen_image().save('ss.png')
    new_img = double_size(pyboy.screen_image())
    new_img.save(server_id + '/' + c.screenshot_name)
    pyboy.tick()
    pyboy.save_state(open(server_id + '/' + game_type + '.state', 'wb'))
    pyboy.stop()

def a_button(server_id):
    movement(WindowEvent.PRESS_BUTTON_A, WindowEvent.RELEASE_BUTTON_A, server_id)

def b_button(server_id):
    movement(WindowEvent.PRESS_BUTTON_B, WindowEvent.RELEASE_BUTTON_B, server_id)

def up(server_id):
    movement(WindowEvent.PRESS_ARROW_UP, WindowEvent.RELEASE_ARROW_UP, server_id)

def down(server_id):
    movement(WindowEvent.PRESS_ARROW_DOWN, WindowEvent.RELEASE_ARROW_DOWN, server_id)

def left(server_id):
    movement(WindowEvent.PRESS_ARROW_LEFT, WindowEvent.RELEASE_ARROW_LEFT, server_id)

def right(server_id):
    movement(WindowEvent.PRESS_ARROW_RIGHT, WindowEvent.RELEASE_ARROW_RIGHT, server_id)

def start(server_id):
    movement(WindowEvent.PRESS_BUTTON_START, WindowEvent.RELEASE_BUTTON_START, server_id)

def select(server_id):
    movement(WindowEvent.PRESS_BUTTON_SELECT, WindowEvent.RELEASE_BUTTON_SELECT, server_id)
