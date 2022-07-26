import os
import discord
from az_blob_storage import create_container_storage_client, download_new_game_files, download_save_state, download_server_properties, download_serverlist, upload_properties_file, upload_save_state, upload_serverlist
from server_properties import *
from emulator import *
from dotenv import load_dotenv
import constants as c
from emulator import *
from az_containers import *
import asyncio


def run():
    
    load_dotenv()
    TOKEN = os.environ['DISCORD_TOKEN']
    CONTAINER_ID = os.environ['CONTAINER_ID']
    
    client = discord.Client()

    @client.event
    async def on_ready():
        # If Container ID is not in the serverlist then download the game files and add the server to the serverlist
        download_serverlist(CONTAINER_ID)
        if CONTAINER_ID not in get_server_list(CONTAINER_ID):
            download_server_properties(CONTAINER_ID)
            download_new_game_files(CONTAINER_ID)
            append_server(CONTAINER_ID)
            upload_serverlist(CONTAINER_ID)

        
        print(f'{client.user} has connected to Discord!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        server_id = message.guild.id
        server_name = message.guild.name
        #Create directory for server

        if CONTAINER_ID == "0":
            def check(msg):
                return msg.author == message.author and msg.channel == message.channel and \
                msg.content.lower() in ["!red", "!green", "!blue", "!yellow", "red", "green", "blue", "yellow"]
            if message.content == '!newgame':
                try:
                    await message.channel.send("Which pokemon game would you like to play? (!red, !green, !blue or !yellow)")
                    msg = await client.wait_for("message", check=check, timeout=300) # 30 seconds to reply
                except asyncio.TimeoutError:
                    await message.send("Sorry, you didn't reply in time!")
                    return
                game_type = msg.content.lower().strip("!")
                create_container_storage_client(server_id)
                initialise_property_file(server_id, server_name, game_type)
                upload_properties_file(server_id)
                deploy_emulator(server_id)
                #delete_temp_files(server_id)
                await message.channel.send("Part 1 of the game has been deployed. Please wait for the game to start.")           
            return

        if CONTAINER_ID == message.guild.id:
            filepath = str(server_id) + "/"            
            if message.content == '!a':
                a_button(server_id)
                await message.channel.send(file=discord.File(filepath + c.screenshot_name))
                upload_save_state(server_id, server_name)
                return
            if message.content == '!b':
                b_button(server_id)
                await message.channel.send(file=discord.File(filepath + c.screenshot_name))
                upload_save_state(server_id, server_name)
                return
            if message.content == '!up':
                up(server_id)
                await message.channel.send(file=discord.File(filepath + c.screenshot_name))
                upload_save_state(server_id, server_name)
                return
            if message.content == '!down':
                down(server_id)
                await message.channel.send(file=discord.File(filepath + c.screenshot_name))
                upload_save_state(server_id, server_name)
                return
            if message.content == '!left':
                left(server_id)
                await message.channel.send(file=discord.File(filepath + c.screenshot_name))
                upload_save_state(server_id, server_name)
                return
            if message.content == '!right':
                right(server_id)
                await message.channel.send(file=discord.File(filepath + c.screenshot_name))
                upload_save_state(server_id, server_name)
                return
            if message.content == '!start':
                start(server_id)
                await message.channel.send(file=discord.File(filepath + c.screenshot_name))
                upload_save_state(server_id, server_name)
                return
            if message.content == '!select':
                select(server_id)
                await message.channel.send(file=discord.File(filepath + c.screenshot_name))
                upload_save_state(server_id, server_name)
                return
            if message.content == '!download':
                await message.channel.send('downloading blobs')
                download_save_state(server_id, server_name)
                return
            if message.content == '!upload':
                await message.channel.send('uploading blobs')
                upload_save_state(server_id, server_name)
                return
            if message.content == '!keycheck':
                AZURE_STORAGE_CONNECTION_STRING = os.environ['AZURE_STORAGE_CONNECTION_STRING'] # In Azure there needs to be quotes around the connection string in variables
                await message.channel.send('Token = ' + AZURE_STORAGE_CONNECTION_STRING)
                return
            if message.content == '!id':
                await message.channel.send("ID: " + str(message.guild.id) + "\n Name: " + str(message.guild.name))
                return
    
    client.run(TOKEN)





