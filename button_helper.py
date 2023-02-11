import discord
from emulator import Emulator
import server_properties_editor as p
import image_helper as h
from pyboy import WindowEvent as we
from pyboy_instance import pyboy_gb, pyboy_gbc

def press_button(interaction, cmd):   
    server_id = interaction.guild.id
    
    if (p.read_value(server_id, "game_type") in ["red", "blue", "yellow"]):
        pyboy = pyboy_gb
    else:
        pyboy = pyboy_gbc
        
    emulator = Emulator(server_id, pyboy)
    emulator.load_game()
    emulator.movement(cmd)
    
    img = emulator.save_screenshot()
    p.record_cmd(server_id, cmd, interaction.user.name)
    img_filepath = h.save_image(img, server_id)
    
    emulator.save()
    file = discord.File(img_filepath, filename="cmd.png")
    embed = discord.Embed()
    embed.title = interaction.user.name + ": " + cmd
    embed.set_image(url="attachment://cmd.png")
    
    return embed, file
        