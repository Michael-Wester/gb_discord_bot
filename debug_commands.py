import os
import discord
from dotenv import load_dotenv
import server_csv as sc


def run():
    
    load_dotenv()
    TOKEN = os.environ['DISCORD_TOKEN']
    CONTAINER_ID = os.environ['CONTAINER_ID']
    
    client = discord.Client()

    @client.event
    async def on_ready():
        # SEnd a message to the server with id of 957136740173365320
        channel = client.get_channel(957136740173365320)
        await channel.send('hello server_id')

        
        print(f'{client.user} has connected to Discord!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        server_id = message.guild.id
        server_name = message.guild.name

        if message.content == '!container_id':
            await message.channel.send("Container ID: " + CONTAINER_ID)
            return
        if message.content == '!server_id':
            await message.channel.send("Server ID: " + str(server_id))
            return
        if message.content == '!server_name':
            await message.channel.send("Server Name: " + str(server_name))
            return
        if message.content == '!group':
            await message.channel.send("Group: " + str(sc.get_server_id_group(server_id)))
            return
        if message.content == '!serverlistsize':
            with open("serverlist.csv", 'r') as f:
                await message.channel.send("Serverlist Size: " + str(len(f.readlines())))
                return
        if message.content == '!channelid':
            await message.channel.send("Channel ID: " + str(message.channel.id))
            return
            
    client.run(TOKEN)

run()
