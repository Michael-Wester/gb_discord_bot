import discord
from discord.ext import commands
import emulator as emulator
from pyboy import WindowEvent as we
import server_properties_editor as properties
import time
import image_helper as h
import constants as c
import os


class multi_movement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("multi_movement loaded")

    @commands.Cog.listener()
    async def on_message(self, message):
        client = self.bot
        print(message.content)
        if message.author == client.user:
            return

        server_id = message.guild.id
        server_name = message.guild.name
        server_folder_path = "servers/" + str(server_id) + "/"
        cmd = str(message.content)[1:]
        time_start = time.time()

        if os.path.exists(server_folder_path) == False:
            return

        if str(message.content)[0:2] == c.cmd_compound_prefix:

            def get_cmd_list(server_id):
                cmd_list_1 = ["w", "a", "s", "d", "e", "q", "r", "f"]
                cmd_list_2 = ["2", "1", "3", "4", "3", "4", "5", "6"]
                cmd_list_3 = ["2", "1", "3", "4", "a", "b", "z", "x"]
                cmd_set = properties.read_server_property_value(server_id, "cmd_set")
                if cmd_set == "1":
                    return cmd_list_1
                if cmd_set == "2":
                    return cmd_list_2
                if cmd_set == "3":
                    return cmd_list_3

            def append_image(server_id, image_array, image):
                image_array.append(h.save_image_frame(image, server_id))
                properties.increase_turn_count(server_id)
                properties.add_to_command_list(
                    server_id,
                    char,
                    properties.read_server_property_value(server_id, "turn_count"),
                    message.author.name,
                    time.time(),
                )
                return image_array

            def general(server_id, pyboy, images, press, release):
                emulator.movement(server_id, pyboy, press, release)
                img = emulator.save_screenshot(pyboy)
                images = append_image(server_id, images, img)

            images = []
            cmd_list = get_cmd_list(server_id)
            pyboy = emulator.load_game(server_id)

            for char in str(message.content)[2:]:
                if char == cmd_list[0]:
                    emulator.movement(
                        server_id, pyboy, we.PRESS_ARROW_UP, we.RELEASE_ARROW_UP
                    )
                    img = emulator.save_screenshot(pyboy)
                    images = append_image(server_id, images, img)
                if char == cmd_list[1]:
                    emulator.movement(
                        server_id, pyboy, we.PRESS_ARROW_LEFT, we.RELEASE_ARROW_LEFT
                    )
                    img = emulator.save_screenshot(pyboy)
                    images = append_image(server_id, images, img)
                if char == cmd_list[2]:
                    emulator.movement(
                        server_id, pyboy, we.PRESS_ARROW_DOWN, we.RELEASE_ARROW_DOWN
                    )
                    img = emulator.save_screenshot(pyboy)
                    images = append_image(server_id, images, img)
                if char == cmd_list[3]:
                    emulator.movement(
                        server_id, pyboy, we.PRESS_ARROW_RIGHT, we.RELEASE_ARROW_RIGHT
                    )
                    img = emulator.save_screenshot(pyboy)
                    images = append_image(server_id, images, img)
                if char == cmd_list[4]:
                    emulator.movement(
                        server_id, pyboy, we.PRESS_BUTTON_A, we.RELEASE_BUTTON_A
                    )
                    img = emulator.save_screenshot(pyboy)
                    images = append_image(server_id, images, img)
                if char == cmd_list[5]:
                    emulator.movement(
                        server_id, pyboy, we.PRESS_BUTTON_B, we.RELEASE_BUTTON_B
                    )
                    img = emulator.save_screenshot(pyboy)
                    images = append_image(server_id, images, img)
                if char == cmd_list[6]:
                    emulator.movement(
                        server_id, pyboy, we.PRESS_BUTTON_START, we.RELEASE_BUTTON_START
                    )
                    img = emulator.save_screenshot(pyboy)
                    images = append_image(server_id, images, img)
                if char == cmd_list[7]:
                    emulator.movement(
                        server_id,
                        pyboy,
                        we.PRESS_BUTTON_SELECT,
                        we.RELEASE_BUTTON_SELECT,
                    )
                    img = emulator.save_screenshot(pyboy)
                    images = append_image(server_id, images, img)

            emulator.save_and_stop(server_id, pyboy)
            h.make_gif(images, server_folder_path, "move.gif", server_id)
            time_end = time.time() - time_start
            await message.channel.send(
                file=discord.File(server_folder_path + c.gif_name)
            )
            await message.channel.send(
                "Time taken: " + str(time_end) + " seconds AFTER optimisation"
            )
            return


async def setup(bot):
    await bot.add_cog(multi_movement(bot))
