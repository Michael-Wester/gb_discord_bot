import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from cv2 import split
from dotenv import load_dotenv

def upload_save_state(server_id, server_name):
    load_dotenv()
    try:
        print("Azure Blob Storage v" + __version__ + " - Python quickstart sample")
        connect_str = os.environ['AZURE_STORAGE_CONNECTION_STRING']
        # Create server properties file
        
        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        old_server_name = server_name
        # Create a unique name for the container from server name and first 4 characters of server id
        server_name = ''.join(ch for ch in server_name if ch.isalnum())

        server_properties_file = open(server_name + ".properties", "w")
        server_properties_file.write("server_id=" + str(server_id) + "\n")
        server_properties_file.write("server_name=" + str(old_server_name) + "\n")
        server_properties_file.close()

        container_name = str(server_id)
        print(container_name)

        # Create container
        try:
            container_client = blob_service_client.create_container(container_name)
            print("Container " + container_name + " created")
        except:
            print("Container " + container_name + " already exists")
        
        # Check if container exists
        try:
            container_client = blob_service_client.get_container_client(container_name)
            print("Container " + container_name + " exists")
        except:
            print("Container " + container_name + " does not exist")
            
        # Create a local directory to hold blob data
        local_path = ""

        # Create a file in the local data directory to upload and download
        local_file_name = 'red.state'
        upload_file_path = os.path.join(local_path, local_file_name)

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

        print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

        # Upload the created file
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        
        with open(server_name + ".properties", "rb") as server_properties_file:
            blob_client.upload_blob(server_properties_file, overwrite=True)

        # Quick start code goes here
        print("\nListing blobs...")
        count = 0
        # List the blobs in the container
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            print("\t" + blob.name)
            count += 1

    except Exception as ex:
        print('Exception:')
        print(ex)

def download_save_state(server_id, server_name):
    load_dotenv()
    try:
        print("Azure Blob Storage v" + __version__ + " - Python quickstart sample")
        connect_str = os.environ['AZURE_STORAGE_CONNECTION_STRING']

        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        old_server_name = server_name
        server_name = ''.join(ch for ch in server_name if ch.isalnum())

        server_properties_file = open(server_name + ".properties", "w")
        server_properties_file.write("server_id=" + str(server_id) + "\n")
        server_properties_file.write("server_name=" + str(old_server_name) + "\n")
        server_properties_file.close()

        container_name = str(server_id)
        print(container_name)
        

        # Create a local directory to hold blob data
        local_path = ""

        # Create a file in the local data directory to upload and download
        local_file_name = 'red.state'

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)      

        download_file_path = os.path.join(local_path, local_file_name)
        blob_client = blob_service_client.get_container_client(container= container_name) 
        print("\nDownloading blob to \n\t" + download_file_path)
        
        print("\nListing blobs...")

        try:
            container_client = blob_service_client.create_container(container_name)
            print("Container " + container_name + " created")
        except:
            print("Container " + container_name + " already exists")

        try:
            container_client = blob_service_client.get_container_client(container_name)
            print("Container " + container_name + " exists")
        except:
            print("Container " + container_name + " does not exist")

        # List the blobs in the container
        count = 0
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            print("\t" + blob.name)
            count += 1
            
        with open(download_file_path, "wb") as download_file:
         download_file.write(blob_client.download_blob(blob.name).readall())

    except Exception as ex:
        print('Exception:')
        print(ex)
