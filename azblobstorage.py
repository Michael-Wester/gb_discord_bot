import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from dotenv import load_dotenv

def upload_save_state():
    load_dotenv()
    try:
        print("Azure Blob Storage v" + __version__ + " - Python quickstart sample")
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        # Create a unique name for the container
        container_name = 'botsavefile'
        print(container_name)

        # Create the container
        try:
            container_client = blob_service_client.get_container_client(container_name)
        except Exception as ex:
            print('Exception:')
            print(ex)

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

        # Quick start code goes here
        print("\nListing blobs...")

        # List the blobs in the container
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            print("\t" + blob.name)

    except Exception as ex:
        print('Exception:')
        print(ex)

def download_save_state():
    load_dotenv()
    try:
        print("Azure Blob Storage v" + __version__ + " - Python quickstart sample")
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        # Create a unique name for the container
        container_name = 'botsavefile'
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
            container_client = blob_service_client.get_container_client(container_name)
        except Exception as ex:
            print('Exception:')
            print(ex)

        # List the blobs in the container
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            print("\t" + blob.name)
            
        with open(download_file_path, "wb") as download_file:
         download_file.write(blob_client.download_blob(blob.name).readall())

    except Exception as ex:
        print('Exception:')
        print(ex)

download_save_state()