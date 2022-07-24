import os
import discord
from azblobstorage import create_container_storage_client, download_new_game_files, download_save_state, get_container_storage_client, upload_save_state
from emulator import *
from dotenv import load_dotenv
import constants as c
from emulator import *
import time
from az_containers import *


def run():
    
    load_dotenv()
    TOKEN = os.environ['DISCORD_TOKEN']
    CONTAINER_ID = os.environ['CONTAINER_ID']
    
    client = discord.Client()

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        start_time = time.time()
        server_id = message.guild.id
        server_name = message.guild.name
        #Create directory for server
        filepath = str(server_id) + "/"
        serverInFile = appendServer(server_id)

        if CONTAINER_ID == "0":
            if message.content == '!newgame':
                create_container_storage_client(server_id)
                await message.channel.send("Container created")
                download_new_game_files(server_id, "red")
                deploy_emulator(server_id)
            return


        if serverInFile == True and CONTAINER_ID == message.guild.id:
            if message.content == '!a':
                download_save_state(server_id, server_name)
                a_button(filepath)
                await message.channel.send(file=discord.File(filepath + c.screenshot_name))

                upload_save_state(server_id, server_name)
                return
            if message.content == '!b':
                download_save_state(server_id, server_name)
                b_button(filepath)
                await message.channel.send(file=discord.File(filepath + c.screenshot_name))

                upload_save_state(server_id, server_name)
                return
            if message.content == '!up':
                download_save_state(server_id, server_name)
                up(filepath)
                await message.channel.send(file=discord.File(filepath + c.screenshot_name))

                upload_save_state(server_id, server_name)
                return
            if message.content == '!down':
                download_save_state(server_id, server_name)
                down(filepath)
                await message.channel.send(file=discord.File(filepath + c.screenshot_name))

                upload_save_state(server_id, server_name)
                print("Sequential run time: %.2f seconds" % (time.time() - start_time))
                return
            if message.content == '!left':
                download_save_state(server_id, server_name)
                left(filepath)
                await message.channel.send(file=discord.File(filepath + c.screenshot_name))
                upload_save_state(server_id, server_name)

                print("Sequential run time: %.2f seconds" % (time.time() - start_time))
                return
            if message.content == '!right':
                download_save_state(server_id, server_name)
                right(filepath)
                await message.channel.send(file=discord.File(filepath + c.screenshot_name))

                upload_save_state(server_id, server_name)
                return
            if message.content == '!start':
                download_save_state(server_id, server_name)
                start(filepath)
                await message.channel.send(file=discord.File(filepath + c.screenshot_name))

                upload_save_state(server_id, server_name)
                return
            if message.content == '!select':
                download_save_state(server_id, server_name)
                select(filepath)
                await message.channel.send(file=discord.File(filepath + c.screenshot_name))

                upload_save_state(server_id, server_name)
                return
            # if message.content == '!download':
            #     count1 = download_save_state()
            #     await message.channel.send('downloading ' + str(count1) + ' blobs')
            #     return
            # if message.content == '!upload':
            #     count2 = upload_save_state()
            #     await message.channel.send('uploading ' + str(count2) + ' blobs')
            #     return
            if message.content == '!keycheck':
                AZURE_STORAGE_CONNECTION_STRING = os.environ['AZURE_STORAGE_CONNECTION_STRING'] # In Azure there needs to be quotes around the connection string in variables
                await message.channel.send('Token = ' + AZURE_STORAGE_CONNECTION_STRING)
                return
            if message.content == '!id':
                await message.channel.send("ID: " + str(message.guild.id) + "\n Name: " + str(message.guild.name))
                return
    

    client.run(TOKEN)





