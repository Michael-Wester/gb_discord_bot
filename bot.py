import os
import discord
from azblobstorage import download_save_state, upload_save_state
from emulator import *
from dotenv import load_dotenv
import constants as c
from emulator import *
import time


def run():
    
    load_dotenv()
    TOKEN = os.environ['DISCORD_TOKEN']
    
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

        if message.content == '!help':
            await message.channel.send('Commands are: !up, !down, !left, !right, !start, !select, !a, !b, !quit, !help')
            return
        if message.content == '!quit':
            await message.channel.send('Quitting...')
            return
        if message.content == '!a':
            download_save_state(server_id, server_name)
            a_button(filepath)
            upload_save_state(server_id, server_name)
            await message.channel.send(file=discord.File(c.screenshot_name))
            return
        if message.content == '!b':
            download_save_state(server_id, server_name)
            b_button(filepath)
            upload_save_state(server_id, server_name)
            await message.channel.send(file=discord.File(c.screenshot_name))
            return
        if message.content == '!up':
            download_save_state(server_id, server_name)
            up(filepath)
            upload_save_state(server_id, server_name)
            await message.channel.send(file=discord.File(c.screenshot_name))
            return
        if message.content == '!down':
            download_save_state(server_id, server_name)
            down(filepath)
            upload_save_state(server_id, server_name)
            await message.channel.send(file=discord.File(c.screenshot_name))
            print("Sequential run time: %.2f seconds" % (time.time() - start_time))
            return
        if message.content == '!left':
            download_save_state(server_id, server_name)
            left(filepath)
            upload_save_state(server_id, server_name)
            await message.channel.send(file=discord.File(c.screenshot_name))
            print("Sequential run time: %.2f seconds" % (time.time() - start_time))
            return
        if message.content == '!right':
            download_save_state(server_id, server_name)
            right(filepath)
            upload_save_state(server_id, server_name)
            await message.channel.send(file=discord.File(c.screenshot_name))
            return
        if message.content == '!start':
            download_save_state(server_id, server_name)
            start(filepath)
            upload_save_state(server_id, server_name)
            await message.channel.send(file=discord.File(c.screenshot_name))
            return
        if message.content == '!select':
            download_save_state(server_id, server_name)
            select(filepath)
            upload_save_state(server_id, server_name)
            await message.channel.send(file=discord.File(c.screenshot_name))
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
        if message.content.startswith('!'):
            await message.channel.send('Command not found. Type !help for a list of commands.')
            return



    client.run(TOKEN)





