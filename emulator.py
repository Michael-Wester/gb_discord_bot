from distutils.command.upload import upload
from pyboy import PyBoy
from pyboy import WindowEvent
from PIL import Image
import constants as c
from emulator import *


def double_size(img):
    new_img = img.resize((img.size[0]*2, img.size[1]*2), Image.ANTIALIAS)
    new_img.save(c.screenshot_name)
    return new_img

def movement(a, b, filepath):
    pyboy = PyBoy(filepath + 'red.gb')
    pyboy.set_emulation_speed(4)
    if(open(filepath + 'red.state', 'rb').read() != b''):
        pyboy.load_state(open(filepath + 'red.state', 'rb'))
    pyboy.tick()
    pyboy.send_input(a)
    pyboy.tick()
    pyboy.tick()
    pyboy.send_input(b)
    for i in range(600):
        pyboy.tick()
    #pyboy.screen_image().save('ss.png')
    double_size(pyboy.screen_image())
    pyboy.tick()
    pyboy.save_state(open(filepath + 'red.state', 'wb'))
    pyboy.stop()

def a_button(filepath):
    movement(WindowEvent.PRESS_BUTTON_A, WindowEvent.RELEASE_BUTTON_A, filepath)

def b_button(filepath):
    movement(WindowEvent.PRESS_BUTTON_B, WindowEvent.RELEASE_BUTTON_B, filepath)

def up(filepath):
    movement(WindowEvent.PRESS_ARROW_UP, WindowEvent.RELEASE_ARROW_UP, filepath)

def down(filepath):
    movement(WindowEvent.PRESS_ARROW_DOWN, WindowEvent.RELEASE_ARROW_DOWN, filepath)

def left(filepath):
    movement(WindowEvent.PRESS_ARROW_LEFT, WindowEvent.RELEASE_ARROW_LEFT, filepath)

def right(filepath):
    movement(WindowEvent.PRESS_ARROW_RIGHT, WindowEvent.RELEASE_ARROW_RIGHT, filepath)

def start(filepath):
    movement(WindowEvent.PRESS_BUTTON_START, WindowEvent.RELEASE_BUTTON_START, filepath)

def select(filepath):
    movement(WindowEvent.PRESS_BUTTON_SELECT, WindowEvent.RELEASE_BUTTON_SELECT, filepath)
