import os
import requests
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, BarColumn, TextColumn, TransferSpeedColumn, TimeRemainingColumn
from rich.table import Table
from dotenv import load_dotenv
import random
import time

# Wczytanie konfiguracji z pliku .env
load_dotenv()

# Inicjalizacja konsoli rich
console = Console()

# Stałe
FILE_HISTORY = 'file_history.txt'
FILE_IO_URL = os.getenv('FILE_IO_URL', 'https://file.io')

# Określenie ścieżki do folderu Downloadsio
PROGRAM_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_FOLDER = os.path.join(PROGRAM_DIR, 'Downloadsio')

# URL do pobrania listy darmowych proxy z ProxyScrape
PROXY_LIST_URL = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=https&timeout=10000&country=all&ssl=all&anonymity=all'


class FileManager:
    """
    Klasa zarządzająca operacjami uploadu i downloadu plików.
    """

    @staticmethod
    def log_history(action: str, file_name: str, link: str):
        """
        Loguje historię operacji do pliku.
        """
        try:
            with open(FILE_HISTORY, 'a') as f:
                f.write(f"{action}: {file_name} - {link}\n")
        except Exception as e:
            console.print(f"[red]Failed to log history: {e}[/red]")

    @staticmethod
    def show_ascii_art():
        """
        Wyświetla grafikę ASCII oraz powitanie.
        """
        ascii_art = """
  ______ _ _      _____ ____
 |  ____(_) |    |_   _/ __ \
 | |__   _| | ___  | || |  | |
 |  __| | | |/ _ \ | || |  | |
 | |    | | |  __/_| || |__| |
 |_|    |_|_|\___|_____\____/
        """
        console.print(f"[cyan]{ascii_art}[/cyan]")
        console.print("[yellow]Created by Swir[/yellow]\n")

    @staticmethod
    def show_history():
        """
        Wyświetla historię operacji.
        """
        if not os.path.exists(FILE_HISTORY):
            console.print("[yellow]No history found.[/yellow]")
            return

        try:
            with open(FILE_HISTORY, 'r') as f:
                history = f.read()
                if history:
                    table = Table(title="Operation History")
                    table.add_column("Action", style="magenta")
                    table.add_column("File Name", style="cyan")
                    table.add_column("Link", style="green")
                    for line in history.strip().split('\n'):
                        if ": " not in line:
                            continue
                        action, rest = line.split(": ", 1)
                        if " - " not in rest:
                            continue
                        file_name, link = rest.split(" - ", 1)
                        table.add_row(action, file_name, link)
                    console.print(table)
                else:
                    console.print("[yellow]History is empty.[/yellow]")
        except Exception as e:
            console.print(f"[red]Failed to read history: {e}[/red]")


class ProxyManager:
    """
    Klasa odpowiedzialna za zarządzanie darmowymi proxy.
    """

    def __init__(self):
        self.proxies = self.fetch_proxies()

    def fetch_proxies(self):
        """
        Pobiera listę darmowych proxy z ProxyScrape API.
        """
        console.print("[yellow]Fetching free proxies from ProxyScrape...[/yellow]")
        try:
            response = requests.get(PROXY_LIST_URL, timeout=10)
            response.raise_for_status()

            proxy_list = response.text.split('\n')
            proxies = [proxy.strip() for proxy in proxy_list if proxy.strip()]
            console.print(f"[green]Fetched {len(proxies)} proxies from ProxyScrape.[/green]")
            return proxies
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Failed to fetch proxies from ProxyScrape: {e}[/red]")
            return []

    def is_proxy_working(self, proxy):
        """
        Sprawdza, czy proxy działa poprawnie.
        """
        test_url = 'https://httpbin.org/ip'
        proxies = {
            'http': proxy,
            'https': proxy,
        }
        try:
            response = requests.get(test_url, proxies=proxies, timeout=5)
            response.raise_for_status()
            return True
        except:
            return False

    def get_working_proxy(self):
        """
        Zwraca pierwsze działające proxy z listy.
        """
        random.shuffle(self.proxies)  # Losowe przetasowanie proxy
        for proxy in self.proxies:
            console.print(f"[yellow]Testing proxy: {proxy}[/yellow]")
            if self.is_proxy_working(proxy):
                console.print(f"[green]Proxy {proxy} is working.[/green]")
                return proxy
            else:
                console.print(f"[red]Proxy {proxy} failed. Removing from list.[/red]")
                self.proxies.remove(proxy)
        console.print("[red]No working proxies found.[/red]")
        return None


class Uploader:
    """
    Klasa odpowiedzialna za upload plików.
    """

    def __init__(self, proxy_manager: ProxyManager):
        self.proxy_manager = proxy_manager

    def upload_file(self, file_path: str) -> str:
        """
        Uploaduje plik na File.io i zwraca link do pobrania.
        """
        if not os.path.exists(file_path):
            console.print(f"[red]Error: File '{file_path}' does not exist.[/red]")
            return ""

        url = FILE_IO_URL
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)

        console.print(f"[yellow]Uploading file: {file_path}...[/yellow]")

        try:
            with open(file_path, 'rb') as f:
                with Progress(
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    "[progress.percentage]{task.percentage:>3.1f}%",
                    "•",
                    TransferSpeedColumn(),
                    "•",
                    TimeRemainingColumn(),
                    console=console,
                ) as progress:
                    task = progress.add_task("Uploading...", total=file_size)
                    for chunk in iter(lambda: f.read(8192), b''):
                        if chunk:
                            progress.update(task, advance=len(chunk))
                response = requests.post(url, files={'file': (file_name, open(file_path, 'rb'), 'application/octet-stream')})

        except requests.exceptions.RequestException as e:
            console.print(f"[red]An error occurred during upload: {e}[/red]")
            return ""
        except Exception as e:
            console.print(f"[red]Unexpected error: {e}[/red]")
            return ""

        if response.status_code == 200:
            try:
                data = response.json()
                if data.get('success'):
                    download_link = data.get('link', '')
                    console.print(f"[green]File uploaded successfully![/green]")
                    console.print(f"[cyan]Download link: {download_link}[/cyan]")
                    FileManager.log_history('UPLOAD', file_name, download_link)
                    return download_link
                else:
                    console.print(f"[red]Error during upload: {data.get('message', 'Unknown error')}[/red]")
            except ValueError:
                console.print("[red]Failed to parse response JSON.[/red]")
        else:
            console.print(f"[red]Upload failed with status code: {response.status_code}[/red]")

        return ""


class Downloader:
    """
    Klasa odpowiedzialna za pobieranie plików.
    """

    def __init__(self, proxy_manager: ProxyManager):
        self.proxy_manager = proxy_manager

    def download_file(self, download_link: str, use_proxy: bool):
        """
        Pobiera plik z podanego linku i zapisuje go w folderze Downloadsio.
        """
        console.print(f"[yellow]Downloading file from: {download_link}...[/yellow]")

        # Maksymalna liczba prób
        max_attempts = 5
        attempt = 0

        proxies = None
        if use_proxy:
            proxies = self.proxy_manager.get_working_proxy()
            if not proxies:
                console.print("[red]Unable to find a working proxy. Aborting download.[/red]")
                return
            proxies = {
                'http': proxies,
                'https': proxies,
            }

        while attempt < max_attempts:
            try:
                response = requests.get(download_link, stream=True, proxies=proxies, timeout=10)
                response.raise_for_status()

                total_size = int(response.headers.get('content-length', 0))
                os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

                # Automatyczne określenie nazwy pliku z nagłówków lub linku
                if 'Content-Disposition' in response.headers:
                    # Próbujemy wyciągnąć nazwę pliku z nagłówka
                    content_disp = response.headers.get('Content-Disposition')
                    if 'filename=' in content_disp:
                        file_name = content_disp.split('filename=')[1].strip('"')
                    else:
                        file_name = download_link.split('/')[-1]
                else:
                    file_name = download_link.split('/')[-1]

                save_path = os.path.join(DOWNLOADS_FOLDER, file_name)

                with open(save_path, 'wb') as file:
                    with Progress(
                        TextColumn("[progress.description]{task.description}"),
                        BarColumn(),
                        "[progress.percentage]{task.percentage:>3.1f}%",
                        "•",
                        TransferSpeedColumn(),
                        "•",
                        TimeRemainingColumn(),
                        console=console,
                    ) as progress:
                        task = progress.add_task("Downloading...", total=total_size)
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                file.write(chunk)
                                progress.update(task, advance=len(chunk))

                console.print(f"[green]File downloaded and saved as {save_path}[/green]")
                FileManager.log_history('DOWNLOAD', file_name, download_link)
                return

            except requests.exceptions.ProxyError:
                if use_proxy:
                    console.print(f"[red]Proxy error with proxy {proxies['https']}. Removing proxy and trying without proxy.[/red]")
                    self.proxy_manager.proxies.remove(proxies['https'])
                    proxies = self.proxy_manager.get_working_proxy()
                    if not proxies:
                        console.print("[red]No more working proxies available. Aborting download.[/red]")
                        return
                    proxies = {
                        'http': proxies,
                        'https': proxies,
                    }
                else:
                    console.print(f"[red]Proxy error occurred: {e}[/red]")
                    return
            except requests.exceptions.ConnectTimeout:
                console.print(f"[red]Connection timed out. Retrying...[/red]")
            except requests.exceptions.HTTPError as e:
                if response.status_code == 404:
                    console.print(f"[red]Download link not found (404). It might have expired.[/red]")
                    return
                else:
                    console.print(f"[red]HTTP error occurred: {e}[/red]")
            except requests.exceptions.RequestException as e:
                console.print(f"[red]An error occurred during download: {e}[/red]")
            except Exception as e:
                console.print(f"[red]Unexpected error: {e}[/red]")

            attempt += 1
            console.print(f"[yellow]Attempt {attempt} of {max_attempts} failed. Retrying...[/yellow]")
            time.sleep(2)  # Krótka przerwa przed następną próbą

        console.print("[red]All attempts to download the file have failed.[/red]")


class FileIOApp:
    """
    Główna klasa aplikacji zarządzająca interfejsem użytkownika.
    """

    def __init__(self):
        self.proxy_manager = ProxyManager()
        self.uploader = Uploader(self.proxy_manager)
        self.downloader = Downloader(self.proxy_manager)

    def main_menu(self):
        """
        Wyświetla główne menu i obsługuje wybór użytkownika.
        """
        FileManager.show_ascii_art()
        while True:
            console.print("\n[magenta]Select an option:[/magenta]")
            console.print("[cyan]1. Upload file to File.io[/cyan]")
            console.print("[cyan]2. Download file from File.io[/cyan]")
            console.print("[cyan]3. View operation history[/cyan]")
            console.print("[cyan]4. Exit[/cyan]")

            choice = Prompt.ask("[yellow]Enter 1, 2, 3, or 4[/yellow]")

            if choice == '1':
                self.upload_menu()
            elif choice == '2':
                self.download_menu()
            elif choice == '3':
                FileManager.show_history()
            elif choice == '4':
                console.print("[green]Exiting...[/green]")
                break
            else:
                console.print("[red]Invalid option, please try again.[/red]")

    def upload_menu(self):
        """
        Obsługuje menu uploadu plików.
        """
        file_path = Prompt.ask("[yellow]Enter the path of the file to upload[/yellow]")
        if file_path:
            download_link = self.uploader.upload_file(file_path)
            if download_link:
                console.print(f"[green]Share this link to download the file:[/green] [cyan]{download_link}[/cyan]")

    def download_menu(self):
        """
        Obsługuje menu pobierania plików.
        """
        download_link = Prompt.ask("[yellow]Enter the download link[/yellow]")
        if not download_link:
            console.print("[red]Download link cannot be empty.[/red]")
            return

        use_proxy = Prompt.ask("[yellow]Do you want to download using a proxy? (yes/no)[/yellow]", choices=["yes", "no"], default="no")
        use_proxy = use_proxy.lower() == "yes"

        self.downloader.download_file(download_link, use_proxy)


def main():
    """
    Główna funkcja uruchamiająca aplikację.
    """
    app = FileIOApp()
    app.main_menu()


if __name__ == "__main__":
    main()
