from pyboy import PyBoy
from pyboy import logger
from server_properties_editor import *

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


    def movement(self, press, release):
        pyboy = self.pyboy
        press_tick = self.press_tick
        release_tick = self.release_tick
        
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