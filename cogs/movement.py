import discord
from discord.ext import commands
import emulator as emulator
from pyboy import WindowEvent as we
import server_properties_editor as p
import time
import image_helper as h
import os
import constants as c
from emulator import Emulator
from pyboy_instance import pyboy
import gc

class movement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pyboy = pyboy 

    @commands.Cog.listener()
    async def on_ready(self):
        print("movement loaded")

    @commands.Cog.listener()
    async def on_message(self, message):
        client = self.bot
        if message.author == client.user:
            return
        server_id = message.guild.id
        server_folder_path = "servers/" + str(server_id) + "/"
        cmd = str(message.content)[1:]
        time_start = time.time()
        
        if os.path.exists(server_folder_path) == False:
            return
        try:
            prefix = p.read_value(server_id, "prefix")
        except:
            print("Server properties not found.")
        if str(message.content)[0:1] != prefix:
            return
        
        if cmd not in c.cmd_list:
            return
        def save_emulator_image(emulator_img):
            if cmd in c.cmd_list:
                p.record_cmd(server_id, cmd, message.author.name)
            img_filepath = h.save_image(emulator_img, server_id)
            return img_filepath
        
        emulator = Emulator(server_id, self.pyboy)
        emulator.load_game()

        if cmd == "a":
            emulator.movement(we.PRESS_BUTTON_A, we.RELEASE_BUTTON_A)
        elif cmd == "b":
            emulator.movement(we.PRESS_BUTTON_B, we.RELEASE_BUTTON_B)
        elif cmd == "up":
            emulator.movement(we.PRESS_ARROW_UP, we.RELEASE_ARROW_UP)
        elif cmd == "down":
            emulator.movement(we.PRESS_ARROW_DOWN, we.RELEASE_ARROW_DOWN)
        elif cmd == "left":
            emulator.movement(we.PRESS_ARROW_LEFT, we.RELEASE_ARROW_LEFT)
        elif cmd == "right":
            emulator.movement(we.PRESS_ARROW_RIGHT, we.RELEASE_ARROW_RIGHT)
        elif cmd == "start":
            emulator.movement(we.PRESS_BUTTON_START, we.RELEASE_BUTTON_START)
        elif cmd == "select":
            emulator.movement(we.PRESS_BUTTON_SELECT, we.RELEASE_BUTTON_SELECT)
        else:
            print("Not a movement command")
            return

        img = emulator.save_screenshot()
        img_filepath = save_emulator_image(img)
        emulator.save()
        
        await message.channel.send(file=discord.File(img_filepath))
        #await message.channel.send( "Command executed in " + str(round(time.time() - time_start, 2)) + " seconds.")
        return
        

async def setup(bot):
    await bot.add_cog(movement(bot))
