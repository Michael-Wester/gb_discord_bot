import os
import discord
import server_properties_editor as properties
import server_list_csv_editor as serverlist
import emulator as emulator
from pyboy import WindowEvent as we
import asyncio
import constants as c
import image_helper as h
import time
from PIL import Image


def run():

    TOKEN = os.environ["DISCORD_TOKEN"]
    client = discord.Client(intents=discord.Intents.all())

    @client.event
    async def on_ready():
        guild_count = 0
        for guild in client.guilds:
            print(f"- {guild.id} (name: {guild.name})")
            guild_count = guild_count + 1

        print(f"{client.user} has connected to Discord!")
        print("bot is in " + str(guild_count) + " guilds.")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        server_id = message.guild.id
        server_name = message.guild.name
        server_folder_path = "servers/" + str(server_id) + "/"
        cmd = str(message.content)[1:]
        time_start = time.time()
        
        try:
            prefix = properties.read_server_property_value(server_id, "prefix")
        except:
            print("Server properties not found.")
        if (
            os.path.exists(server_folder_path) and str(message.content)[0:1] == prefix
        ) or (
            os.path.exists(server_folder_path)
            and str(message.content)[0:2] == c.cmd_compound_prefix
        ):

            def save_emulator_image(emulator_img):
                properties.increase_turn_count(server_id)
                if cmd in c.cmd_list:
                    properties.add_to_command_list(
                        server_id,
                        cmd,
                        properties.read_server_property_value(server_id, "turn_count"),
                        message.author.name,
                        time.time(),
                    )
                img_file_path = h.save_image(emulator_img, server_id)
                return img_file_path

            def check(msg):
                return (
                    msg.author == message.author
                    and msg.channel == message.channel
                    and msg.content.lower() in c.list_of_games
                    or msg.content.lower() in [prefix + "y", prefix + "n"]
                )

            if cmd == "a":
                img_file_path = save_emulator_image(emulator.command(server_id, we.PRESS_BUTTON_A, we.RELEASE_BUTTON_A))
                await message.channel.send(file=discord.File(img_file_path))
                return
            if cmd == "b":
                img_file_path = save_emulator_image(emulator.command(server_id, we.PRESS_BUTTON_B, we.RELEASE_BUTTON_B))
                await message.channel.send(file=discord.File(img_file_path))
                return
            if cmd == "up":
                img_file_path = save_emulator_image(emulator.command(server_id, we.PRESS_ARROW_UP, we.RELEASE_ARROW_UP))
                await message.channel.send(file=discord.File(img_file_path))
                return
            if cmd == "down":
                img_file_path = save_emulator_image(emulator.command(server_id, we.PRESS_ARROW_DOWN, we.RELEASE_ARROW_DOWN))
                await message.channel.send(file=discord.File(img_file_path))
                return
            if cmd == "left":
                img_file_path = save_emulator_image(emulator.command(server_id, we.PRESS_ARROW_LEFT, we.RELEASE_ARROW_LEFT))
                await message.channel.send(file=discord.File(img_file_path))
                return
            if cmd == "right":
                img_file_path = save_emulator_image(emulator.command(server_id, we.PRESS_ARROW_RIGHT, we.RELEASE_ARROW_RIGHT))
                await message.channel.send(file=discord.File(img_file_path))
                return
            if cmd == "start":
                img_file_path = save_emulator_image(emulator.command(server_id, we.PRESS_BUTTON_START, we.RELEASE_BUTTON_START))
                await message.channel.send(file=discord.File(img_file_path))
                return
            if cmd == "select":
                img_file_path = save_emulator_image(emulator.command(server_id, we.PRESS_BUTTON_SELECT, we.RELEASE_BUTTON_SELECT))
                await message.channel.send(file=discord.File(img_file_path))
                return
                
            if cmd == "id":
                await message.channel.send(
                    "ID: "
                    + str(message.guild.id)
                    + "\n Name: "
                    + str(message.guild.name)
                )
                return
            if cmd == "help":
                cmd_list = []
                for cmd in c.cmd_list:
                    cmd_list.append(prefix + cmd)
                await message.channel.send(
                    "The following commands are available: " + str(cmd_list)
                )
                return
            if cmd == "games":
                games_list = []
                for cmd in c.list_of_games:
                    games_list.append(prefix + cmd)

                embed = discord.Embed(
                    title="Games list",
                    url=c.games_image,
                    description="Here is a list of supported Pokemon games",
                    color=0x004080,
                )
                embed.add_field(
                    name="Commands to use", value=str(games_list), inline=False
                )
                embed.set_image(url=c.games_gif)
                await message.channel.send(embed=embed)
                return
            if cmd == "reset":
                await message.channel.send(
                    "Are you sure you want to reset the server? (y/n)"
                )
                try:
                    msg = await client.wait_for("message", check=check, timeout=300)
                except asyncio.TimeoutError:
                    await message.send("Sorry, you didn't reply in time!")
                    return
                if msg.content.lower() == "n":
                    await message.channel.send("Server has not been reset")
                    return
                serverlist.delete_server(server_id)
                properties.delete_server_folder(server_id)
                await message.channel.send(
                    "Server has been reset. Server files are held for 7 days before being permanently deleted. Contact Michle#4142 if you need to restore them"
                )
                return
            if cmd == "newgame":
                await message.channel.send(
                    "Please reset the game using "
                    + prefix
                    + "reset before starting a new game"
                )
                return

            if cmd == "info":
                await message.channel.send(
                    "This bot is currently in beta. Please report any bugs to Michle#4142"
                )
            if cmd.startswith("recap"):
                cmd = cmd.split(" ")

                turn_number = int(
                    properties.read_server_property_value(server_id, "turn_count")
                )
                if len(cmd) == 1:
                    await message.channel.send(
                        "Please enter a turn number to recap from"
                    )
                    return
                if cmd[1] == "*":
                    await message.channel.send("Recapping from turn 1...")
                    images = []
                    i = 1
                    while i < turn_number:
                        image = Image.open(
                            server_folder_path
                            + "/images/"
                            + str(server_id)
                            + "_"
                            + str(i)
                            + ".png"
                        )
                        images.append(image)
                        i += 1
                    h.make_gif(images, server_folder_path + "/images/recap.gif")
                    await message.channel.send(
                        file=discord.File(server_folder_path + "/images/recap.gif")
                    )
                    return

                if not cmd[1].isdigit():
                    await message.channel.send("Please enter a valid turn number")
                    return
                if int(cmd[1]) > int(
                    properties.read_server_property_value(server_id, "turn_count")
                ):
                    await message.channel.send(
                        "Please enter a turn number that is less than the current turn number"
                    )
                    return
                if int(cmd[1]) < 1:
                    await message.channel.send(
                        "Please enter a turn number that is greater than 0"
                    )
                    return

                await message.channel.send("Recapping from turn " + cmd[1] + "...")
                images = []
                i = turn_number - int(cmd[1])
                while i < turn_number:
                    image = Image.open(
                        server_folder_path
                        + "/images/"
                        + str(server_id)
                        + "_"
                        + str(i)
                        + ".png"
                    )
                    images.append(image)
                    i += 1
                h.make_gif(images, server_folder_path, "/recap.gif", server_id)
                await message.channel.send(
                    file=discord.File(server_folder_path + "/recap.gif")
                )
                return
            if cmd.startswith("prefix"):
                cmd = cmd.split(" ")
                if len(cmd) == 1:
                    await message.channel.send("Please enter a prefix")
                    return
                if len(cmd[1]) > 1:
                    await message.channel.send(
                        "Please enter a prefix that is only 1 character long"
                    )
                    return
                properties.update_server_property_value(server_id, "prefix", cmd[1])
                await message.channel.send("Prefix has been set to " + cmd[1])
                return
            if cmd.startswith("press_tick"):
                cmd = cmd.split(" ")
                if not cmd[1].isdigit():
                    await message.channel.send("Please enter a number")
                    return
                if int(cmd[1]) < 1:
                    await message.channel.send(
                        "Please enter a tick value that is greater than 0"
                    )
                    return
                properties.update_server_property_value(server_id, "press_tick", cmd[1])
                await message.channel.send("Press tick has been set to " + cmd[1])
                return
            if cmd.startswith("release_tick"):
                cmd = cmd.split(" ")
                if len(cmd) == 1:
                    await message.channel.send("Please enter a tick value")
                    return
                if not cmd[1].isdigit():
                    await message.channel.send("Please enter a number")
                    return
                if int(cmd[1]) < 1:
                    await message.channel.send(
                        "Please enter a tick value that is greater than 0"
                    )
                    return
                properties.update_server_property_value(
                    server_id, "release_tick", cmd[1]
                )
                await message.channel.send("Release tick has been set to " + cmd[1])
                return
            if cmd.startswith("cmd_set"):
                cmd = cmd.split(" ")
                if len(cmd) == 1:
                    await message.channel.send("Please enter a command set")
                    return
                if not cmd[1].isdigit():
                    await message.channel.send("Please enter a number")
                    return
                properties.update_server_property_value(server_id, "cmd_set", cmd[1])
                await message.channel.send("Command set has been set to " + cmd[1])
                return
            if cmd.startswith("bar_colour"):
                cmd = cmd.split(" ")
                if cmd[1] not in [
                    "red",
                    "green",
                    "blue",
                    "yellow",
                    "orange",
                    "purple",
                    "pink",
                    "white",
                    "black",
                ]:
                    await message.channel.send("Please enter a valid colour")
                    return
                properties.update_server_property_value(server_id, "bar_colour", cmd[1])
                await message.channel.send("Bar colour has been set to " + cmd[1])
                return
            if cmd == 'reinit':
                properties.reinitialise_property_file(server_id)

            if str(message.content)[0:2] == c.cmd_compound_prefix:
                

                def get_cmd_list(server_id):
                    cmd_list_1 = ["w", "a", "s", "d", "e", "q", "r", "f"]
                    cmd_list_2 = ["2", "1", "3", "4", "3", "4", "5", "6"]
                    cmd_list_3 = ["2", "1", "3", "4", "a", "b", "z", "x"]
                    if (
                        properties.read_server_property_value(server_id, "cmd_set")
                        == "1"
                    ):
                        return cmd_list_1
                    if (
                        properties.read_server_property_value(server_id, "cmd_set")
                        == "2"
                    ):
                        return cmd_list_2
                    if (
                        properties.read_server_property_value(server_id, "cmd_set")
                        == "3"
                    ):
                        return cmd_list_3
                    return cmd_list_1

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

                images = []
                cmd_list = get_cmd_list(server_id)
                pyboy = emulator.load_game(server_id)
                guild = client.get_guild(957136739632295966)
                channel = guild.get_channel(1063468447415160904)

                for char in str(message.content)[2:]:
                    if char == cmd_list[0]:
                        emulator.movement(server_id, pyboy, we.PRESS_ARROW_UP, we.RELEASE_ARROW_UP)
                        img = emulator.save_screenshot(pyboy)
                        images = append_image(server_id, images, img)                        
                    if char == cmd_list[1]:
                        emulator.movement(server_id, pyboy, we.PRESS_ARROW_LEFT, we.RELEASE_ARROW_LEFT)
                        img = emulator.save_screenshot(pyboy)
                        images = append_image(server_id, images, img)
                    if char == cmd_list[2]:
                        emulator.movement(server_id, pyboy, we.PRESS_ARROW_DOWN, we.RELEASE_ARROW_DOWN)
                        img = emulator.save_screenshot(pyboy)
                        images = append_image(server_id, images, img)
                    if char == cmd_list[3]:
                        emulator.movement(server_id, pyboy, we.PRESS_ARROW_RIGHT, we.RELEASE_ARROW_RIGHT)
                        img = emulator.save_screenshot(pyboy)
                        images = append_image(server_id, images, img)
                    if char == cmd_list[4]:
                        emulator.movement(server_id, pyboy, we.PRESS_BUTTON_A, we.RELEASE_BUTTON_A)
                        img = emulator.save_screenshot(pyboy)
                        images = append_image(server_id, images, img)
                    if char == cmd_list[5]:
                        emulator.movement(server_id, pyboy, we.PRESS_BUTTON_B, we.RELEASE_BUTTON_B)
                        img = emulator.save_screenshot(pyboy)
                        images = append_image(server_id, images, img)
                    if char == cmd_list[6]:
                        emulator.movement(server_id, pyboy, we.PRESS_BUTTON_START, we.RELEASE_BUTTON_START)
                        img = emulator.save_screenshot(pyboy)
                        images = append_image(server_id, images, img)
                    if char == cmd_list[7]:
                        emulator.movement(server_id, pyboy, we.PRESS_BUTTON_SELECT, we.RELEASE_BUTTON_SELECT)
                        img = emulator.save_screenshot(pyboy)
                        images = append_image(server_id, images, img)
                emulator.save_and_stop(server_id, pyboy)
                h.make_gif(images, server_folder_path, "move.gif", server_id)
                time_end = time.time() - time_start
                await message.channel.send(
                    file=discord.File(server_folder_path + c.gif_name)
                )
                await message.channel.send( "Time taken: " + str(time_end) + " seconds AFTER optimisation")
                return
            print("Unrecognised command")
            return
        elif (
            os.path.exists(str(server_id)) == False
            and str(message.content)[0:1] == c.cmd_prefix
        ) or (
            os.path.exists(str(server_id)) == False
            and str(message.content)[0:2] != c.cmd_compound_prefix
        ):
            if cmd == "newgame":

                def check(msg):
                    games_list = []
                    for cmd in c.list_of_games:
                        games_list.append(c.cmd_prefix + cmd)
                    return (
                        msg.author == message.author
                        and msg.channel == message.channel
                        and msg.content.lower() in c.list_of_games
                        or msg.content.lower() in games_list
                    )

                try:
                    await message.channel.send(
                        "Which pokemon game would you like to play? Use "
                        + c.cmd_prefix
                        + "games to see a list of games"
                    )
                    games_list = []
                    for cmd in c.list_of_games:
                        games_list.append(c.cmd_prefix + cmd)
                    embed = discord.Embed(
                        title="Games list",
                        url=c.games_image,
                        description="Here is a list of supported Pokemon games",
                        color=0x004080,
                    )
                    embed.add_field(
                        name="Commands to use", value=str(games_list), inline=False
                    )
                    embed.set_image(url=c.games_gif)
                    await message.channel.send(embed=embed)
                    msg = await client.wait_for(
                        "message", check=check, timeout=15
                    )  # 30 seconds to reply
                except asyncio.TimeoutError:
                    await message.channel.send(
                        c.octagonal_sign
                        + "**Sorry "
                        + str(message.author)
                        + ", either you didn't reply in time or you didn't reply with a valid game type**"
                        + c.octagonal_sign
                    )
                    return

                game_type = msg.content.lower().strip(c.cmd_prefix)
                serverlist.create_serverlist()
                serverlist.add_rows(server_id, server_name, game_type)
                properties.initialise_property_file(server_id, server_name, game_type)
                properties.copy_emulator_files(server_id, game_type)
                await message.channel.send(
                    "Game has initiated! Use "
                    + c.cmd_prefix
                    + "a to start the game and "
                    + c.cmd_prefix
                    + "help for a list of commands"
                )
                return
            if cmd == "games":
                await message.channel.send(
                    "The following games are available: " + str(c.list_of_games)
                )
                return
            return

        else:
            return

    client.run(TOKEN)
