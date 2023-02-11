import discord
from discord.ext import commands
import emulator as emulator
from pyboy import WindowEvent as we
import server_properties_editor as p
import time
import image_helper as h
import constants as c
import os
from pyboy_instance import pyboy_gb, pyboy_gbc
import gc
from emulator import Emulator
import logging


class multi_movement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pyboy_gb = pyboy_gb 
        self.pyboy_gbc = pyboy_gbc

    @commands.Cog.listener()
    async def on_ready(self):
        print("multi_movement loaded")

    @commands.Cog.listener()
    async def on_message(self, message):
        client = self.bot
        if message.author == client.user:
            return

        server_id = message.guild.id
        server_folder_path = "servers/" + str(server_id) + "/"
        time_start = time.time()
        cmd = str(message.content)[2:]

        if os.path.exists(server_folder_path) == False:
            return

        try:
            prefix = p.read_value(server_id, "cmp_prefix")
        except:
            print("Server properties not found.")        
        
        if str(message.content)[0:2] != prefix:
            return

        def get_cmd_list(server_id):
            cmd_list_1 = ["w", "a", "s", "d", "e", "q", "r", "f"]
            cmd_list_2 = ["2", "1", "3", "4", "3", "4", "5", "6"]
            cmd_list_3 = ["2", "1", "3", "4", "a", "b", "z", "x"]
            cmd_set = p.read_value(server_id, "cmd_set")
            if cmd_set == "1":
                return cmd_list_1
            elif cmd_set == "2":
                return cmd_list_2
            elif cmd_set == "3":
                return cmd_list_3
            else:
                logging.error("Invalid cmd_set value in server properties.")
            

        def append_image(server_id, image_array, emulator, cmd):
            emulator.movement(cmd)
            image = emulator.save_screenshot()
            image_array.append(h.save_image_frame(image, server_id))
            p.record_cmd(server_id, char, message.author.name)
            return image_array

        if (p.read_value(server_id, "game_type") in ["red", "blue", "yellow"]):
            self.pyboy = self.pyboy_gb
        else:
            self.pyboy = self.pyboy_gbc
            
        emulator = Emulator(server_id, self.pyboy)
        emulator.load_game()
        
        images = []
        cmd_list = get_cmd_list(server_id)
        for char in cmd:                          
            if char == cmd_list[0]:
                images = append_image(server_id, images, emulator, "up")
            if char == cmd_list[1]:
                images = append_image(server_id, images, emulator, "left")
            if char == cmd_list[2]:
                images = append_image(server_id, images, emulator, "down")
            if char == cmd_list[3]:
                images = append_image(server_id, images, emulator, "right")
            if char == cmd_list[4]:
                images = append_image(server_id, images, emulator, "a")
            if char == cmd_list[5]:
                images = append_image(server_id, images, emulator, "b")         
            if char == cmd_list[6]:
                images = append_image(server_id, images, emulator, "select")
            if char == cmd_list[7]:
                images = append_image(server_id, images, emulator, "start")

        emulator.save()
        h.make_gif(images, server_folder_path, "move.gif", server_id)

        await message.channel.send(
            file=discord.File(server_folder_path + c.gif_name)
        )
        time_end = time.time() - time_start
        #await message.channel.send( "Time taken: " + str(time_end) + " seconds for an average of " + str(time_end / len(cmd)) + " seconds per command")
        gc.collect
        return


async def setup(bot):
    await bot.add_cog(multi_movement(bot))
