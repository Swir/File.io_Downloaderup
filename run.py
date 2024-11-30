import os
import requests
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, BarColumn, DownloadColumn, TextColumn, TransferSpeedColumn, TimeRemainingColumn
from rich.table import Table
from dotenv import load_dotenv

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
                        action, rest = line.split(": ", 1)
                        file_name, link = rest.split(" - ", 1)
                        table.add_row(action, file_name, link)
                    console.print(table)
                else:
                    console.print("[yellow]History is empty.[/yellow]")
        except Exception as e:
            console.print(f"[red]Failed to read history: {e}[/red]")


class Uploader:
    """
    Klasa odpowiedzialna za upload plików.
    """

    @staticmethod
    def upload_file(file_path: str) -> str:
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
                    DownloadColumn(),
                    "•",
                    TransferSpeedColumn(),
                    "•",
                    TimeRemainingColumn(),
                    console=console,
                ) as progress:
                    task = progress.add_task("Uploading...", total=file_size)
                    files = {
                        'file': (file_name, f, 'application/octet-stream')
                    }

                    def progress_monitor(monitor):
                        progress.update(task, advance=monitor.bytes_read - progress.tasks[0].completed)

                    response = requests.post(url, files=files)

        except requests.exceptions.RequestException as e:
            console.print(f"[red]An error occurred during upload: {e}[/red]")
            return ""
        except Exception as e:
            console.print(f"[red]Unexpected error: {e}[/red]")
            return ""

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                download_link = data.get('link', '')
                console.print(f"[green]File uploaded successfully![/green]")
                console.print(f"[cyan]Download link: {download_link}[/cyan]")
                FileManager.log_history('UPLOAD', file_name, download_link)
                return download_link
            else:
                console.print(f"[red]Error during upload: {data.get('message', 'Unknown error')}[/red]")
        else:
            console.print(f"[red]Upload failed with status code: {response.status_code}[/red]")

        return ""


class Downloader:
    """
    Klasa odpowiedzialna za pobieranie plików.
    """

    @staticmethod
    def download_file(download_link: str):
        """
        Pobiera plik z podanego linku i zapisuje go w folderze Downloadsio.
        """
        console.print(f"[yellow]Downloading file from: {download_link}...[/yellow]")

        try:
            response = requests.get(download_link, stream=True)
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
                    DownloadColumn(),
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
            file_name = os.path.basename(save_path)
            FileManager.log_history('DOWNLOAD', file_name, download_link)
        except requests.exceptions.RequestException as e:
            console.print(f"[red]An error occurred during download: {e}[/red]")
        except Exception as e:
            console.print(f"[red]Unexpected error: {e}[/red]")


class FileIOApp:
    """
    Główna klasa aplikacji zarządzająca interfejsem użytkownika.
    """

    def __init__(self):
        self.uploader = Uploader()
        self.downloader = Downloader()

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

        self.downloader.download_file(download_link)


def main():
    """
    Główna funkcja uruchamiająca aplikację.
    """
    app = FileIOApp()
    app.main_menu()


if __name__ == "__main__":
    main()
