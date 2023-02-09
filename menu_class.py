import discord
import constants as c
from pyboy_instance import pyboy_gb, pyboy_gbc
from emulator import Emulator
import server_properties_editor as p
import image_helper as h
from pyboy import WindowEvent as we

class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.pyboy_gb = pyboy_gb 
        self.pyboy_gbc = pyboy_gbc
        
    @discord.ui.button(label="UP", style=discord.ButtonStyle.gray)
    async def up_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("up button pressed")
        
        server_id = interaction.guild.id
        
        def save_emulator_image(emulator_img):
            p.record_cmd(server_id, "up", interaction.user.name)
            img_filepath = h.save_image(emulator_img, server_id)
            return img_filepath
        print("up button pressed3")


        if (p.read_value(server_id, "game_type") in ["red", "blue", "yellow"]):
            print("up button presse1d")
            
            self.pyboy = self.pyboy_gb
            
        else:
            print("up button presse2d")
            
            self.pyboy = self.pyboy_gbc
            
        print("up button pressed")
            
        emulator = Emulator(server_id, self.pyboy)
        emulator.load_game()
        print("up button pressed")
        
        emulator.movement(we.PRESS_BUTTON_A, we.RELEASE_BUTTON_A)
        
        
        img = emulator.save_screenshot()
        img_filepath = save_emulator_image(img)
        emulator.save()
        print("up button pressed")

        file = discord.File(img_filepath, filename="up.png")
        embed = discord.Embed()
        embed.set_image(url="attachment://up.png")
        print("up button pressed")
        
        
        await interaction.response.edit_message(embed=embed, attachments=[file])

    @discord.ui.button(label="DOWN", style=discord.ButtonStyle.gray)
    async def down_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You clicked the down button!")
        
    @discord.ui.button(label="LEFT", style=discord.ButtonStyle.gray)
    async def left_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You clicked the left button!")

    @discord.ui.button(label="RIGHT", style=discord.ButtonStyle.gray)
    async def right_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You clicked the right button!")