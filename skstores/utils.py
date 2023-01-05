import requests


# https://dsbuck.blob.core.windows.net/praprimus/laptop_price/final_df_laptop_price .pkl

def download_file_from_azure_container(filename, destination):
    full_url = f'https://dsbuck.blob.core.windows.net/praprimus/{filename}'
    print(full_url)
    download = requests.get(full_url)
    chunk_size = 32768
    #
    with open(destination, "wb") as f:
        for chunk in download.iter_content(chunk_size):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
