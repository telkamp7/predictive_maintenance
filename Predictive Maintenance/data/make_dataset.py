import urllib.request
import click

def download_url(url: str, save_path: str) -> None:
    """
    Download the data from the source.
    """
    with urllib.request.urlopen(url) as dl_file:
        with open(save_path, 'wb') as out_file:
            out_file.write(dl_file.read())


@click.command()
@click.argument("url", type=click.Path())
@click.argument("save_path", type=click.Path())
def main(url: str, save_path: str):
    """
    Runs data processing scripts to download the data from source, extract the data from zip files, and process the data, so it is ready for analysis.
    """
    download_url(url, save_path)

    if __name__ == "__main__":
        main()
