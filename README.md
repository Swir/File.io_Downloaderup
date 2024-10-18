# File.IO Uploader & Downloader

This project provides a simple command-line tool to upload and download files using [File.io](https://file.io) – a temporary file sharing service. The program offers a user-friendly interface, utilizing **ASCII art** for a welcoming introduction, with easy-to-use features for uploading and downloading files with progress bars to track the status.

## Features
- **Upload files** to File.io with a progress bar.
- **Download files** from File.io with a progress bar showing download progress.
- **Log operations**: The program logs each upload and download operation with a file name and corresponding link.
- **ASCII Art**: Display a stylish "File.IO" ASCII art banner at startup.
- **Created by**: Swir.

## How to Use

### 1. Uploading a File:
   - After starting the program, select the option to upload a file.
   - Enter the path to the file you want to upload.
   - Once the upload is complete, the program will return a download link.

### 2. Downloading a File:
   - Enter the download link provided by File.io.
   - Specify the path where you want to save the downloaded file.
   - The file will be downloaded with a progress bar indicating the download status.

### 3. Exit:
   - To exit the program, choose the "Exit" option from the menu.

## Requirements

- Python 3.x
- Install the required libraries:
  ```bash
  pip install requests tqdm colorama
