import os
import discord
import server_properties_editor as properties
import server_list_csv_editor as serverlist
import emulator as emulator
import asyncio
import constants as c
import image_helper as h
import time

def run():
    
    TOKEN = os.environ['DISCORD_TOKEN']
    client = discord.Client(intents=discord.Intents.all())

    @client.event
    async def on_ready():
        guild_count = 0
        for guild in client.guilds:
            print(f"- {guild.id} (name: {guild.name})")
            guild_count = guild_count + 1

        print(f'{client.user} has connected to Discord!')
        print("bot is in " + str(guild_count) + " guilds.")

    @client.event
    async def on_join(member):
        print("joined")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        server_id = message.guild.id
        server_name = message.guild.name
        server_folder_path = "servers/" + str(server_id) + "/"
        cmd = str(message.content)[1:]

                  
        if (os.path.exists(server_folder_path) and str(message.content)[0:1] == c.cmd_prefix) or (properties.server_exists and str(message.content)[0:2] == c.cmd_compound_prefix):
            def save_emulator_image(emulator_img):
                properties.increase_turn_count(server_id)
                if cmd in c.cmd_list:
                    properties.add_to_command_list(server_id, cmd, properties.get_turn_count(server_id), message.author.name, time.time())
                img_file_path = h.save_image(emulator_img, server_id)
                return img_file_path

            def check(msg):
                return msg.author == message.author and msg.channel == message.channel and \
                msg.content.lower() in c.list_of_games or msg.content.lower() in [c.cmd_prefix + "y", c.cmd_prefix + "n"]
                
            if cmd == 'a':
                img_file_path = save_emulator_image(emulator.a_button(server_id))
                await message.channel.send(file=discord.File(img_file_path))
                return
            if cmd == 'b':
                img_file_path = save_emulator_image(emulator.b_button(server_id))
                await message.channel.send(file=discord.File(img_file_path))
                return
            if cmd == 'up':
                img_file_path = save_emulator_image(emulator.up_button(server_id))
                await message.channel.send(file=discord.File(img_file_path))
                return
            if cmd == 'down':
                img_file_path = save_emulator_image(emulator.down_button(server_id))
                await message.channel.send(file=discord.File(img_file_path))
                return
            if cmd == 'left':
                img_file_path = save_emulator_image(emulator.left_button(server_id))
                await message.channel.send(file=discord.File(img_file_path))
                return
            if cmd == 'right':
                img_file_path = save_emulator_image(emulator.right_button(server_id))
                await message.channel.send(file=discord.File(img_file_path))
                return
            if cmd == 'start':
                img_file_path = save_emulator_image(emulator.start_button(server_id))
                await message.channel.send(file=discord.File(img_file_path))
                return
            if cmd == 'select':
                img_file_path = save_emulator_image(emulator.select_button(server_id))
                await message.channel.send(file=discord.File(img_file_path))
                return
            if cmd == 'id':
                await message.channel.send("ID: " + str(message.guild.id) + "\n Name: " + str(message.guild.name))
                return
            if cmd == 'help':
                cmd_list = []
                for cmd in c.cmd_list:
                    cmd_list.append(c.cmd_prefix + cmd)
                await message.channel.send("The following commands are available: " + str(cmd_list))
                return
            if cmd == 'games':
                games_list = []
                for cmd in c.list_of_games:
                    games_list.append(c.cmd_prefix + cmd)

                embed=discord.Embed(title="Games list", url="https://cdn.discordapp.com/attachments/957136740173365320/1061631724372643920/gameslist.png", description="Here is a list of supported Pokemon games", color=0x004080)
                embed.add_field(name="Commands to use", value=str(games_list), inline=False)
                embed.set_image(url="https://cdn.discordapp.com/attachments/957136740173365320/1061555438124027974/games.gif")
                await message.channel.send(embed=embed)
                return 
            if cmd == 'reset':
                await message.channel.send("Are you sure you want to reset the server? (y/n)")
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
                await message.channel.send("Server has been reset. Server files are held for 7 days before being permanently deleted. Contact Michle#4142 before the need to restore it") 
                return
            if cmd == 'newgame':
                await message.channel.send("Please reset the game using " + c.cmd_prefix + "reset before starting a new game")
                return
            
            if str(message.content)[0:2] == c.cmd_compound_prefix:
                images = []
                for char in str(message.content)[2:]:
                    if char == "w":
                        images.append(h.save_image_frame(emulator.up_button(server_id), server_id))
                        properties.increase_turn_count(server_id)
                        properties.add_to_command_list(server_id, char, properties.get_turn_count(server_id), message.author.name, time.time())
                    if char == "a":
                        images.append(h.save_image_frame(emulator.left_button(server_id), server_id))
                        properties.increase_turn_count(server_id)
                        properties.add_to_command_list(server_id, "A", properties.get_turn_count(server_id), message.author.name, time.time())
                    if char == "s":
                        images.append(h.save_image_frame(emulator.down_button(server_id), server_id))
                        properties.increase_turn_count(server_id)
                        properties.add_to_command_list(server_id, char, properties.get_turn_count(server_id), message.author.name, time.time())
                    if char == "d":
                        images.append(h.save_image_frame(emulator.right_button(server_id), server_id))
                        properties.increase_turn_count(server_id)
                        properties.add_to_command_list(server_id, char, properties.get_turn_count(server_id), message.author.name, time.time())
                    if char == "e":
                        images.append(h.save_image_frame(emulator.a_button(server_id), server_id))
                        properties.increase_turn_count(server_id)
                        properties.add_to_command_list(server_id, char, properties.get_turn_count(server_id), message.author.name, time.time())
                    if char == "q":
                        images.append(h.save_image_frame(emulator.b_button(server_id), server_id))
                        properties.increase_turn_count(server_id)
                        properties.add_to_command_list(server_id, char, properties.get_turn_count(server_id), message.author.name, time.time())
                    if char == "r":
                        images.append(h.save_image_frame(emulator.start_button(server_id), server_id))
                        properties.increase_turn_count(server_id)
                        properties.add_to_command_list(server_id, char, properties.get_turn_count(server_id), message.author.name, time.time())
                    if char == "f":
                        images.append(h.save_image_frame(emulator.select_button(server_id), server_id))
                        properties.increase_turn_count(server_id)
                        properties.add_to_command_list(server_id, cmd, properties.get_turn_count(server_id), message.author.name, time.time())
                h.make_gif(images, server_folder_path)
                await message.channel.send(file=discord.File(server_folder_path + c.gif_name))
                return

            print("Unrecognised command")
            return
        elif (os.path.exists(str(server_id)) == False and str(message.content)[0:1] == c.cmd_prefix) or (os.path.exists(str(server_id)) == False and str(message.content)[0:2] != c.cmd_compound_prefix):
            if cmd == 'newgame':
                def check(msg):
                    games_list = []
                    for cmd in c.list_of_games:
                        games_list.append(c.cmd_prefix + cmd)
                    return msg.author == message.author and msg.channel == message.channel and \
                    msg.content.lower() in c.list_of_games or msg.content.lower() in games_list
                try:
                    await message.channel.send("Which pokemon game would you like to play? Use " + c.cmd_prefix + "games to see a list of games")
                    games_list = []
                    for cmd in c.list_of_games:
                        games_list.append(c.cmd_prefix + cmd)
                    
                    embed=discord.Embed(title="Games list", url="https://cdn.discordapp.com/attachments/957136740173365320/1061631724372643920/gameslist.png", description="Here is a list of supported Pokemon games", color=0x004080)
                    embed.add_field(name="Commands to use", value=str(games_list), inline=False)
                    embed.set_image(url="https://cdn.discordapp.com/attachments/957136740173365320/1061555438124027974/games.gif")
                    await message.channel.send(embed=embed)
                    msg = await client.wait_for("message", check=check, timeout=15) # 30 seconds to reply
                except asyncio.TimeoutError:
                    await message.channel.send("<:octagonal_sign:1061655413151498340> **Sorry " + str(message.author) + ", either you didn't reply in time or you didn't reply with a valid game type** <:octagonal_sign:1061655413151498340>")
                    return
                
                game_type = msg.content.lower().strip(c.cmd_prefix)
                serverlist.create_serverlist()
                serverlist.add_rows(server_id, server_name, game_type)
                properties.initialise_property_file(server_id, server_name, game_type)
                properties.copy_emulator_files(server_id, game_type)
                await message.channel.send("Game has initiated! Use " + c.cmd_prefix + "a to start the game and " + c.cmd_prefix + "help for a list of commands")
                return 
            if cmd == 'games':
                await message.channel.send("The following games are available: " + str(c.list_of_games))
                return 
            return
            
        else:
            return

    client.run(TOKEN)





