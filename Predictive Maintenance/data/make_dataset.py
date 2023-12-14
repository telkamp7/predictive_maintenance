import os

from zipfile import ZipFile, BadZipFile
import requests
import io
import click

def download_url(url: str, save_path: str, file_name: str) -> None:
    """
    Download the data from the source.
    """

    # Ensure the save_path directory exists
    os.makedirs(save_path, exist_ok=True)

    # Join the 'save_path' and 'file_name' to give the full 'zip_path'
    zip_path = os.path.join(save_path, file_name)

    # Check if the file already exists
    if os.path.exists(zip_path):
        print(f"The file {zip_path} already exists. Skipping download.")
        return

    # Download the .zip file and write it to disk using requests
    response = requests.get(url, allow_redirects=True)

    if response.status_code == 200:
        with open(zip_path, 'wb') as out_file:
            out_file.write(response.content)
        print(f"Downloaded {url} to {zip_path}")
    else:
        print(f"Failed to download {url}. Status code: {response.status_code}")

def unzip_file(zip_path: str, extract_path: str):
    """
    Unzip the file at 'zip_path' to the 'extract_path'.
    """
    try:
        with ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        print(f"Unzipped {zip_path} to {extract_path}")
    except BadZipFile:
        print(f"Error: {zip_path} is not a valid zip file.")
    except Exception as e:
        print(f"An error occurred while unzipping {zip_path}: {str(e)}")

def cleanup_zip_file(zip_path: str) -> None:
    """
    Clean up and delete the zip file if it exists.
    """
    if os.path.exists(zip_path):
        os.remove(zip_path)
        print(f"Deleted {zip_path}")
    else:
        print(f"The file {zip_path} does not exist.")

@click.command()
@click.argument("url", type=click.Path())
@click.argument("save_path", type=click.Path())
@click.argument("file_name", type=click.Path())
def main(url: str, save_path: str, file_name: str):
    """
    Runs data processing scripts to download the data from source, extract the data from zip files, and process the data, so it is ready for analysis.
    """

    # Execute the 'download_url()' function
    download_url(url, save_path, file_name)

    # Join the 'save_path' and 'file_name' to give the full 'zip_path'
    zip_path = os.path.join(save_path, file_name)

    # Unzip the downloaded .zip file using the 'unzip_file()' function
    unzip_file(zip_path, save_path)
    # ... and remove the .zip file hereafter
    cleanup_zip_file(zip_path)

if __name__ == "__main__":
    main()
