import requests
import os
from tqdm import tqdm
from colorama import Fore, init

# Inicjalizacja kolorów
init(autoreset=True)

# ASCII Art i powitanie
def show_ascii_art():
    print(f"{Fore.CYAN}")
    print("  ______ _ _      _____ ____  ")
    print(" |  ____(_) |    |_   _/ __ \ ")
    print(" | |__   _| | ___  | || |  | |")
    print(" |  __| | | |/ _ \ | || |  | |")
    print(" | |    | | |  __/_| || |__| |")
    print(" |_|    |_|_|\___|_____\____/ ")
    print(f"{Fore.YELLOW}Created by Swir\n")

# Funkcja do logowania historii operacji
def log_history(action, file_name, link):
    with open('file_history.txt', 'a') as f:
        f.write(f"{action}: {file_name} - {link}\n")

# Funkcja do wysyłania pliku na File.io z paskiem postępu
def upload_file(file_path):
    if not os.path.exists(file_path):
        print(f"{Fore.RED}Error: File '{file_path}' does not exist.")
        return None

    url = 'https://file.io'
    file_size = os.path.getsize(file_path)
    print(f"{Fore.YELLOW}Uploading file: {file_path} ...")

    with open(file_path, 'rb') as f, tqdm(
        total=file_size, unit='B', unit_scale=True, unit_divisor=1024, desc=file_path
    ) as bar:
        files = {'file': (os.path.basename(file_path), f)}
        response = requests.post(url, files=files)
        bar.update(file_size)

    if response.status_code == 200:
        data = response.json()
        if data['success']:
            download_link = data['link']
            print(f"{Fore.GREEN}File uploaded successfully! Download link: {Fore.CYAN}{download_link}")
            log_history('UPLOAD', os.path.basename(file_path), download_link)
            return download_link
        else:
            print(f"{Fore.RED}Error during upload: {data.get('message', 'Unknown error')}")
            return None
    else:
        print(f"{Fore.RED}Upload failed with status code: {response.status_code}")
        return None

# Funkcja do pobrania pliku z wyświetleniem postępu
def download_file(download_link, save_path):
    print(f"{Fore.YELLOW}Downloading file from: {download_link} ...")
    response = requests.get(download_link, stream=True)

    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))
        with open(save_path, 'wb') as file, tqdm(
            desc=save_path,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                bar.update(len(chunk))
        print(f"{Fore.GREEN}File downloaded and saved as {save_path}")
        log_history('DOWNLOAD', os.path.basename(save_path), download_link)
    else:
        print(f"{Fore.RED}Download failed with status code: {response.status_code}")

# Menu główne
def main_menu():
    show_ascii_art()  # Pokazanie grafiki ASCII
    while True:
        print(f"\n{Fore.MAGENTA}Select option:")
        print(f"{Fore.CYAN}1. Upload file to File.io")
        print(f"{Fore.CYAN}2. Download file from File.io")
        print(f"{Fore.CYAN}3. Exit")
        
        choice = input(f"{Fore.YELLOW}Enter 1, 2, or 3: ")

        if choice == '1':
            upload_menu()
        elif choice == '2':
            download_menu()
        elif choice == '3':
            print(f"{Fore.GREEN}Exiting...")
            break
        else:
            print(f"{Fore.RED}Invalid option, please try again.")

# Menu do uploadu
def upload_menu():
    file_path = input(f"{Fore.YELLOW}Enter the path of the file to upload: ")
    download_link = upload_file(file_path)
    if download_link:
        print(f"{Fore.GREEN}Share this link to download the file: {Fore.CYAN}{download_link}")

# Menu do pobierania plików
def download_menu():
    download_link = input(f"{Fore.YELLOW}Enter the download link: ")
    save_path = input(f"{Fore.YELLOW}Enter the path to save the downloaded file: ")
    download_file(download_link, save_path)

if __name__ == "__main__":
    main_menu()
