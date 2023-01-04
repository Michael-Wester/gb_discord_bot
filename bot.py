import os
import discord
import server_properties_editor as properties
import server_list_csv_editor as serverlist
import emulator as emulator
import dotenv
import asyncio
import constants as c
import image_helper as h


def run():
    
    dotenv.load_dotenv()
    TOKEN = os.environ['DISCORD_TOKEN']
    client = discord.Client(intents=discord.Intents.all())

    @client.event
    async def on_ready():          
        print(f'{client.user} has connected to Discord!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        server_id = message.guild.id
        server_name = message.guild.name
        filepath = str(server_id) + "/"
        cmd = str(message.content)[1:]
                  
        if str(message.content)[0:1] == c.cmd_prefix:

            def check(msg, list):
                return msg.author == message.author and msg.channel == message.channel and \
                msg.content.lower() in list   

            if cmd == 'newgame':
                try:
                    await message.channel.send("Which pokemon game would you like to play? Use " + c.cmd_prefix + "games" + "to see a list of games")
                    msg = await client.wait_for("message", check=check(list=c.list_of_games), timeout=300) # 30 seconds to reply
                except asyncio.TimeoutError:
                    await message.send("Sorry, either you didn't reply in time or you didn't reply with a valid game type.")
                    return
                game_type = msg.content.lower().strip(c.cmd_prefix)
                serverlist.create_serverlist()
                serverlist.add_rows(server_id, server_name, game_type)
                properties.initialise_property_file(server_id, server_name, game_type)
                properties.copy_emulator_files(server_id, game_type)
                await message.channel.send("Game has started! Use" + c.cmd_prefix + "help for a list of commands") 
                return 

            if properties.server_exists(server_id) == False:
                print("Use " + c.cmd_prefix + " newgame to start a new game")
                return

            if cmd == 'a':
                h.double_size(emulator.a_button(server_id)).save(filepath + c.screenshot_name)
                await message.channel.send(file=discord.File(filepath + c.screenshot_name))
                return
            if cmd == 'b':
                h.double_size(emulator.b_button(server_id)).save(filepath + c.screenshot_name)
                await message.channel.send(file=discord.File(filepath + c.screenshot_name))
                return
            if cmd == 'up':
                h.double_size(emulator.up_button(server_id)).save(filepath + c.screenshot_name)
                await message.channel.send(file=discord.File(filepath + c.screenshot_name))
                return
            if cmd == 'down':
                h.double_size(emulator.down_button(server_id)).save(filepath + c.screenshot_name)
                await message.channel.send(file=discord.File(filepath + c.screenshot_name))
                return
            if cmd == 'left':
                h.double_size(emulator.left_button(server_id)).save(filepath + c.screenshot_name)
                await message.channel.send(file=discord.File(filepath + c.screenshot_name))
                return
            if cmd == 'right':
                h.double_size(emulator.right_button(server_id)).save(filepath + c.screenshot_name)
                await message.channel.send(file=discord.File(filepath + c.screenshot_name))
                return
            if cmd == 'start':
                h.double_size(emulator.start_button(server_id)).save(filepath + c.screenshot_name)
                await message.channel.send(file=discord.File(filepath + c.screenshot_name))
                return
            if cmd == 'select':
                h.double_size(emulator.select_button(server_id)).save(filepath + c.screenshot_name)
                await message.channel.send(file=discord.File(filepath + c.screenshot_name))
                return
            if cmd == 'id':
                await message.channel.send("ID: " + str(message.guild.id) + "\n Name: " + str(message.guild.name))
                return
            if cmd == 'help':
                await message.channel.send("The following commands are available: newgame, a, b, up, down, left, right, start, select, id, help")
                return
            if cmd == 'games':
                await message.channel.send("The following games are available: " + str(c.list_of_games))
                return 
            if cmd == 'reset':
                await message.channel.send("Are you sure you want to reset the server? (y/n)")
                try:
                    msg = await client.wait_for("message", check=check(list=["y", "n"]), timeout=300) 
                except asyncio.TimeoutError:
                    await message.send("Sorry, you didn't reply in time!")
                    return
                if msg.content.lower() == "n":
                    await message.channel.send("Server has not been reset")
                    return
                serverlist.delete_server(server_id)
                properties.delete_server_folder(server_id)
                await message.channel.send("Server has been reset")
                return
            return

        if str(message.content)[0:2] == c.cmd_compound_prefix:
            images = []
            for char in str(message.content)[2:]:
                if char == "w":
                    images.append(h.double_size(emulator.up(server_id)))
                if char == "a":
                    images.append(h.double_size(emulator.left(server_id)))
                if char == "s":
                    images.append(h.double_size(emulator.down(server_id)))
                if char == "d":
                    images.append(h.double_size(emulator.right(server_id)))
                if char == "e":
                    images.append(h.double_size(emulator.a_button(server_id)))
                if char == "q":
                    images.append(h.double_size(emulator.b_button(server_id)))
                if char == "r":
                    images.append(h.double_size(emulator.start(server_id)))
                if char == "f":
                    images.append(h.double_size(emulator.select(server_id)))
            h.make_gif(images, filepath)
            await message.channel.send(file=discord.File(filepath + c.gif_name))
            return


    client.run(TOKEN)





