import discord
from emulator import Emulator
import server_properties_editor as p
import image_helper as h
from pyboy import WindowEvent as we

def press_button(self, interaction, cmd):   
    server_id = interaction.guild.id
    
    if (p.read_value(server_id, "game_type") in ["red", "blue", "yellow"]):
        self.pyboy = self.pyboy_gb
    else:
        self.pyboy = self.pyboy_gbc
        
    emulator = Emulator(server_id, self.pyboy)
    emulator.load_game()
    
    if cmd == "up":
        emulator.movement(we.PRESS_ARROW_UP, we.RELEASE_ARROW_UP)
    elif cmd == "down":
        emulator.movement(we.PRESS_ARROW_DOWN, we.RELEASE_ARROW_DOWN)
    elif cmd == "left":
        emulator.movement(we.PRESS_ARROW_LEFT, we.RELEASE_ARROW_LEFT)
    elif cmd == "right":
        emulator.movement(we.PRESS_ARROW_RIGHT, we.RELEASE_ARROW_RIGHT)
    elif cmd == "a":
        emulator.movement(we.PRESS_BUTTON_A, we.RELEASE_BUTTON_A)
    elif cmd == "b":
        emulator.movement(we.PRESS_BUTTON_B, we.RELEASE_BUTTON_B)
    elif cmd == "start":
        emulator.movement(we.PRESS_BUTTON_START, we.RELEASE_BUTTON_START)
    elif cmd == "select":
        emulator.movement(we.PRESS_BUTTON_SELECT, we.RELEASE_BUTTON_SELECT)
    
    
    img = emulator.save_screenshot()
    p.record_cmd(server_id, cmd, interaction.user.name)
    img_filepath = h.save_image(img, server_id)
    
    emulator.save()
    file = discord.File(img_filepath, filename="cmd.png")
    embed = discord.Embed()
    embed.set_image(url="attachment://cmd.png")
    
    return embed, file
        