import discord
from discord.ext import commands
import emulator as emulator
from pyboy import WindowEvent as we
import server_properties_editor as p
import time
import image_helper as h
import constants as c
import os
from pyboy_instance import pyboy
import gc
from emulator import Emulator


class multi_movement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pyboy = pyboy 

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

        if cmd == c.cmd_compound_prefix:

            def get_cmd_list(server_id):
                cmd_list_1 = ["w", "a", "s", "d", "e", "q", "r", "f"]
                cmd_list_2 = ["2", "1", "3", "4", "3", "4", "5", "6"]
                cmd_list_3 = ["2", "1", "3", "4", "a", "b", "z", "x"]
                cmd_set = p.read_value(server_id, "cmd_set")
                if cmd_set == "1":
                    return cmd_list_1
                if cmd_set == "2":
                    return cmd_list_2
                if cmd_set == "3":
                    return cmd_list_3
            
            
            def append_image(server_id, image_array, emulator, press, release):
                emulator.movement(press, release)
                image = emulator.save_screenshot()
                image_array.append(h.save_image_frame(image, server_id))
                p.record_cmd(server_id, char, message.author.name)
                return image_array

            emulator = Emulator(server_id, self.pyboy)
            emulator.load_game()
            
            images = []
            cmd_list = get_cmd_list(server_id)
            for char in cmd:
                if char == cmd_list[4]:
                    images = append_image(server_id, images, emulator, we.PRESS_BUTTON_A, we.RELEASE_BUTTON_A)
                if char == cmd_list[5]:
                    images = append_image(server_id, images, emulator, we.PRESS_BUTTON_B, we.RELEASE_BUTTON_B)                        
                if char == cmd_list[0]:
                    images = append_image(server_id, images, emulator, we.PRESS_ARROW_UP, we.RELEASE_ARROW_UP)
                if char == cmd_list[1]:
                    images = append_image(server_id, images, emulator, we.PRESS_ARROW_LEFT, we.RELEASE_ARROW_LEFT)
                if char == cmd_list[2]:
                    images = append_image(server_id, images, emulator, we.PRESS_ARROW_DOWN, we.RELEASE_ARROW_DOWN)
                if char == cmd_list[3]:
                    images = append_image(server_id, images, emulator, we.PRESS_ARROW_RIGHT, we.RELEASE_ARROW_RIGHT)
                if char == cmd_list[6]:
                    images = append_image(server_id, images, emulator, we.PRESS_BUTTON_SELECT, we.RELEASE_BUTTON_SELECT)
                if char == cmd_list[7]:
                    images = append_image(server_id, images, emulator, we.PRESS_BUTTON_START, we.RELEASE_BUTTON_START)


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
