from pyboy import PyBoy
from pyboy import WindowEvent
from PIL import Image
import constants as c


def double_size(img):
    new_img = img.resize((img.size[0]*2, img.size[1]*2), Image.ANTIALIAS)
    new_img.save(c.screenshot_name)
    return new_img

def movement(a, b):
    pyboy = PyBoy('red.gb')
    pyboy.set_emulation_speed(4)
    if(open('red.state', 'rb').read() != b''):
        pyboy.load_state(open('red.state', 'rb'))
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
    pyboy.save_state(open('red.state', 'wb'))
    pyboy.stop()

def a_button():
    movement(WindowEvent.PRESS_BUTTON_A, WindowEvent.RELEASE_BUTTON_A)

def b_button():
    movement(WindowEvent.PRESS_BUTTON_B, WindowEvent.RELEASE_BUTTON_B)

def up():
    movement(WindowEvent.PRESS_ARROW_UP, WindowEvent.RELEASE_ARROW_UP)

def down():
    movement(WindowEvent.PRESS_ARROW_DOWN, WindowEvent.RELEASE_ARROW_DOWN)

def left():
    movement(WindowEvent.PRESS_ARROW_LEFT, WindowEvent.RELEASE_ARROW_LEFT)

def right():
    movement(WindowEvent.PRESS_ARROW_RIGHT, WindowEvent.RELEASE_ARROW_RIGHT)

def start():
    movement(WindowEvent.PRESS_BUTTON_START, WindowEvent.RELEASE_BUTTON_START)

def select():
    movement(WindowEvent.PRESS_BUTTON_SELECT, WindowEvent.RELEASE_BUTTON_SELECT)


    




        

