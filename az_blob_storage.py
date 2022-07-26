import os
import shutil
from time import sleep
from azure.storage.blob import BlobServiceClient, __version__
from dotenv import load_dotenv
from server_properties import get_game_type, initialise_property_file_folder


def create_blob_service_client():
    load_dotenv()
    print("Azure Blob Storage v" + __version__ + " - Python quickstart sample")
    connect_str = os.environ['AZURE_STORAGE_CONNECTION_STRING']
    
    return BlobServiceClient.from_connection_string(connect_str)

def create_container_storage_client(server_id):
    blob_service_client = create_blob_service_client()
    container_name = str(server_id)
    try:
        blob_service_client.create_container(container_name)
        print("Container " + container_name + " created")
    except:
        print("Container " + container_name + " already exists")

def get_container_storage_client(server_id):
    blob_service_client = create_blob_service_client()
    container_name = str(server_id)
    try:
        container_client = blob_service_client.get_container_client(container_name)
        print("Container " + container_name + " exists")
    except:
        print("Container " + container_name + " does not exist")
    return container_client

def get_total_number_blobs(server_id):
    blob_service_client = create_blob_service_client()
    container_name = str(server_id)
    try:
        container_client = blob_service_client.get_container_client(container_name)
        print("Container " + container_name + " exists")
    except:
        print("Container " + container_name + " does not exist")
    
    count = 0
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        count += 1
    return count

def upload_blob(server_id, blob_name, file_path):
    container_name = str(server_id)
    blob_service_client = create_blob_service_client()
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        
    with open(file_path + blob_name, "rb") as upload_file:
        blob_client.upload_blob(upload_file, overwrite=True)


def upload_save_state(server_id):
    try:
        initialise_property_file_folder(server_id)

        container_name = str(server_id)
        file_path = container_name + "/"

        game_type = get_game_type(server_id)

        #upload the server properties file
        upload_blob(container_name, container_name + ".properties", file_path)

        #upload the save state file
        upload_blob(container_name, game_type + ".state", file_path)

        #upload the gb ram file
        upload_blob(container_name, game_type + ".gb.ram", file_path)

        #upload the gb file
        upload_blob(container_name, game_type + ".gb", file_path)

        print("uploaded 4 files")
        #delete_temp_files(server_id, simpleServerName, file_path)

    except Exception as ex:
        print('Exception:')
        print(ex)

def upload_properties_file(server_id):
    container_name = str(server_id)
    file_path = container_name + "/"
    upload_blob(container_name, container_name + ".properties", file_path)

    
def download_save_state(server_id):
    load_dotenv()
    try:
        initialise_property_file_folder(server_id)
        
        blob_service_client = create_blob_service_client()

        container_name = str(server_id)
        file_path = container_name + "/"

        container_client = get_container_storage_client(server_id)
        # List the blobs in the container
        count = 0
        blob_list = container_client.list_blobs()

        blob_client = blob_service_client.get_container_client(container= container_name)

        for blob in blob_list:
            print("\t" + blob.name)
            with open(file_path + blob.name, "wb") as download_file:
                download_file.write(blob_client.download_blob(blob.name).readall())
            count += 1
        print("\nDownloaded " + str(count) + " blobs")

    except Exception as ex:
        print('Exception:')
        print(ex)

def download_blob(server_id, container_name, blob_name):
    file_path = str(server_id) + "/"
    blob_service_client = create_blob_service_client()
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    with open(file_path + blob_name, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())

def download_new_game_files(server_id):
    load_dotenv()
    try:
        initialise_property_file_folder(server_id)

        game_type = get_game_type(server_id)

        download_blob(server_id, "roms", game_type + ".gb")
        download_blob(server_id, "roms", game_type + ".gb.ram")
        download_blob(server_id, "roms", game_type + ".state")
    except Exception as ex:
        print('Exception:')
        print(ex)

def download_server_properties(server_id):
    load_dotenv()
    try:
        initialise_property_file_folder(server_id)
        
        blob_service_client = create_blob_service_client()

        container_name = str(server_id)
        file_path = container_name + "/"

        container_client = get_container_storage_client(server_id)
        # List the blobs in the container
        count = 0
        blob_list = container_client.list_blobs()

        blob_client = blob_service_client.get_container_client(container= container_name)

        for blob in blob_list:
            if blob.name == container_name + ".properties":
                with open(file_path + blob.name, "wb") as download_file:
                    download_file.write(blob_client.download_blob(blob.name).readall())
                count += 1
        print("\nDownloaded " + str(count) + " blobs")

    except Exception as ex:
        print('Exception:')
        print(ex)

def download_serverlist(server_id):
    initialise_property_file_folder(server_id)
    download_blob(server_id, "global", "serverlist.txt")


def upload_serverlist():
    upload_blob("global", "serverlist.txt", "serverlist.txt")