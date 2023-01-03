import os
import discord
import server_properties_editor as properties
import emulator as emulator
import dotenv
import asyncio
import server_list_csv_editor as serverlist
import constants as c
intents = discord.Intents.all()

def run():
    
    dotenv.load_dotenv()
    TOKEN = os.environ['DISCORD_TOKEN']

    client = discord.Client(intents=intents)

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
            
        def check(msg):
            return msg.author == message.author and msg.channel == message.channel and \
            msg.content.lower() in ["!red", "!green", "!blue", "!yellow", "!silver", "!gold", "!crystal", "!coral"]

        if message.content == '!newgame':
            try:
                await message.channel.send("Which pokemon game would you like to play? (!red, !green, !blue or !yellow)")
                msg = await client.wait_for("message", check=check, timeout=300) # 30 seconds to reply
            except asyncio.TimeoutError:
                await message.send("Sorry, you didn't reply in time!")
                return
            game_type = msg.content.lower().strip("!")
            serverlist.create_serverlist()
            serverlist.add_rows(server_id, server_name, game_type)
            properties.initialise_property_file(server_id, server_name, game_type)
            properties.copy_emulator_files(server_id, game_type)

            await message.channel.send("Part 1 of the game has been deployed. Please wait for the game to start.") 
            return  
        
        if properties.server_exists(server_id) == False:
            print("server not in list")
            await message.channel.send("Please start a new game with !newgame")
            return
        if message.content == '!a':
            emulator.a_button(server_id)
            await message.channel.send(file=discord.File(filepath + c.screenshot_name))
            return
        if message.content == '!b':
            emulator.b_button(server_id)
            await message.channel.send(file=discord.File(filepath + c.screenshot_name))
            return
        if message.content == '!up':
            emulator.up(server_id)
            await message.channel.send(file=discord.File(filepath + c.screenshot_name))
            return
        if message.content == '!down':
            emulator.down(server_id)
            await message.channel.send(file=discord.File(filepath + c.screenshot_name))
            return
        if message.content == '!left':
            emulator.left(server_id)
            await message.channel.send(file=discord.File(filepath + c.screenshot_name))
            return
        if message.content == '!right':
            emulator.right(server_id)
            await message.channel.send(file=discord.File(filepath + c.screenshot_name))
            return
        if message.content == '!start':
            emulator.start(server_id)
            await message.channel.send(file=discord.File(filepath + c.screenshot_name))
            return
        if message.content == '!select':
            emulator.select(server_id)
            await message.channel.send(file=discord.File(filepath + c.screenshot_name))
            return
        if message.content == '!id':
            await message.channel.send("ID: " + str(message.guild.id) + "\n Name: " + str(message.guild.name))
            return
        if message.content == '!help':
            await message.channel.send("The following commands are available: !newgame !a !b !up !down !left !right !start !select !id !help")
            return
        if message.content == '!reset':
            # Confirm reset
            await message.channel.send("Are you sure you want to reset the server? (y/n)")
            def check(msg):
                return msg.author == message.author and msg.channel == message.channel and \
                msg.content.lower() in ["y", "n"]
            try:
                msg = await client.wait_for("message", check=check, timeout=300) # 30 seconds to reply
            except asyncio.TimeoutError:
                await message.send("Sorry, you didn't reply in time!")
                return
            if msg.content.lower() == "n":
                await message.channel.send("Server has not been reset")
                return
            # Reset server
            properties.delete_server_folder(server_id)
            serverlist.delete_server(server_id)
            await message.channel.send("Server has been reset")
            return

    client.run(TOKEN)





