from pyboy import PyBoy
from pyboy import logger
from server_properties_editor import *
from pyboy import WindowEvent as we

logger.log_level("ERROR")


class Emulator:
    def __init__(self, server_id, pyboy):
        self.pyboy = pyboy
        self.server_id = server_id
        self.server_folder_path = "servers/" + str(server_id) + "/"
        self.game_type = read_value(server_id, "game_type")
        self.press_tick = int(read_value(server_id, "press_tick"))
        self.release_tick = int(read_value(server_id, "release_tick"))
        

    def load_game(self):
        pyboy = self.pyboy
        server_folder_path = self.server_folder_path
        game_type = self.game_type

        if open(server_folder_path + game_type + ".gb.state", "rb").read() != b"":
            pyboy.load_state(open(server_folder_path + game_type + ".gb.state", "rb"))
            
        return pyboy


    def movement(self, cmd):
        pyboy = self.pyboy
        press_tick = self.press_tick
        release_tick = self.release_tick
        if cmd == "a":
            press, release = we.PRESS_BUTTON_A, we.RELEASE_BUTTON_A
        elif cmd == "b":
            press, release = we.PRESS_BUTTON_B, we.RELEASE_BUTTON_B
        elif cmd == "up":
            press, release = we.PRESS_ARROW_UP, we.RELEASE_ARROW_UP
        elif cmd == "down":
            press, release = we.PRESS_ARROW_DOWN, we.RELEASE_ARROW_DOWN
        elif cmd == "left":
            press, release = we.PRESS_ARROW_LEFT, we.RELEASE_ARROW_LEFT
        elif cmd == "right":
            press, release = we.PRESS_ARROW_RIGHT, we.RELEASE_ARROW_RIGHT
        elif cmd == "start":
            press, release = we.PRESS_BUTTON_START, we.RELEASE_BUTTON_START
        elif cmd == "select":
            press, release = we.PRESS_BUTTON_SELECT, we.RELEASE_BUTTON_SELECT
        else:
            print("Not a movement command")
            return

        pyboy.send_input(press)
        for i in range(press_tick):
            pyboy.tick()

        pyboy.send_input(release)
        for i in range(release_tick):
            pyboy.tick()

        return pyboy

    def save_screenshot(self):
        pyboy = self.pyboy
        return pyboy.screen_image()


    def save(self):
        pyboy = self.pyboy
        server_folder_path = self.server_folder_path
        game_type = self.game_type
        pyboy.save_state(open(server_folder_path + game_type + ".gb.state", "wb"))
        return True
    
    
    def stop(self):
        self.pyboy.stop()
        return True