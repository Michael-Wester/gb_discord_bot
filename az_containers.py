import os
from dotenv import load_dotenv
from server_properties import remove_server

def deploy_emulator(server_id):
    load_dotenv()
    
    REGISTRY_LOGIN_SERVER = os.environ['REGISTRY_LOGIN_SERVER']
    REGISTRY_USERNAME = os.environ['REGISTRY_USERNAME']
    REGISTRY_PASSWORD = os.environ['REGISTRY_PASSWORD']

    container_name = str(server_id)

    image_tag = ":99"

    image_name = REGISTRY_LOGIN_SERVER + "/michael-wester/gbdiscordbot" + image_tag
    
    AZURE_STORAGE_CONNECTION_STRING = os.environ['AZURE_STORAGE_CONNECTION_STRING']
    TOKEN = os.environ['DISCORD_TOKEN']
    environment_variables = "CONTAINER_ID=" + container_name + " AZURE_STORAGE_CONNECTION_STRING=" + AZURE_STORAGE_CONNECTION_STRING + " DISCORD_TOKEN=" + TOKEN

    create_container_cmd1 = "az container create -g Discordbot --name " + container_name + " --image " + image_name + " --cpu 1 --memory 1 "
    create_container_cmd2 = "--registry-login-server " + REGISTRY_LOGIN_SERVER + " --registry-username " + REGISTRY_USERNAME + " --registry-password " + REGISTRY_PASSWORD + " "
    create_container_cmd3 = "--environment-variables " + environment_variables
    full_create_container = create_container_cmd1 + create_container_cmd2 + create_container_cmd3

    os.system(full_create_container)

def delete_container(server_id):
    container_name = str(server_id)
    delete_container_cmd = "az container delete -g Discordbot --name " + container_name + " --yes"
    os.system(delete_container_cmd)
    remove_server(server_id)

#delete_container(957136739632295966)
#deploy_emulator(957136739632295966)
