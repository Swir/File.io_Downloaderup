<div align="center">

# ☁️ File.io Uploader & Downloader

### Rich-Powered Python CLI for Temporary File Transfers

**Upload • Download • Progress Bars • History • Proxy Support • File.io**

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Rich](https://img.shields.io/badge/CLI-Rich-ff4fa3)
![Requests](https://img.shields.io/badge/HTTP-Requests-2ea44f)
![Platform](https://img.shields.io/badge/Platform-Cross--Platform-111111)
![Author](https://img.shields.io/badge/Author-Swir-8A2BE2)

</div>

---

## 🚀 About

**File.io Uploader & Downloader** is a Python command-line utility for uploading and downloading files through the File.io temporary file-sharing service.

The application uses the `rich` library for a cleaner terminal experience with progress bars, transfer information and history tables. It also includes optional proxy discovery/testing logic and keeps a local history of file-transfer operations.

It is designed for users searching for a **File.io uploader**, **File.io downloader**, **Python file transfer CLI**, **temporary file sharing tool**, **Rich progress downloader** or a lightweight terminal-based upload/download utility.

---

## ✨ Features

| Feature | Description |
|---|---|
| ☁️ File.io upload | Upload local files to File.io |
| 📥 File download | Download files from supported links |
| 📊 Progress display | Rich transfer bars, speed and remaining time |
| 📜 History | Stores and displays local transfer history |
| 📁 Download folder | Keeps downloads in a dedicated local directory |
| 🌐 Proxy helper | Can fetch and test HTTPS proxies |
| 🎨 Rich terminal UI | Tables, colored messages and interactive prompts |
| ⚙️ Environment config | Supports configuration through `.env` |
| 🪶 Lightweight | Runs as a straightforward Python CLI utility |

---

## 📋 Requirements

- Python 3.x
- Internet connection
- File.io service availability

Install dependencies:

```bash
pip install requests rich python-dotenv
```

---

## 📦 Installation

```bash
git clone https://github.com/Swir/File.io_Downloaderup.git
cd File.io_Downloaderup
pip install requests rich python-dotenv
python run.py
```

---

## 🧠 How It Works

```text
Local File
   │
   ▼
Python CLI
   │
   ├── requests
   ├── rich progress
   ▼
File.io
   │
   ▼
Temporary Download Link
```

Transfer history is stored locally in `file_history.txt`. Downloaded files are placed in the application's download directory.

---

## 🔧 Configuration

The program loads environment variables with `python-dotenv`. `FILE_IO_URL` can be configured externally, while the default target is:

```text
https://file.io
```

External proxy and hosting services can change independently of this project, so availability is not guaranteed.

---

## 🔍 Discoverability

`file.io uploader` • `file.io downloader` • `python file uploader` • `python download cli` • `temporary file sharing python` • `rich progress bar downloader` • `python file transfer tool` • `terminal uploader` • `requests upload progress` • `file sharing cli`

---

## ⚠️ Privacy & Service Note

Temporary file-sharing services are external services. Do not upload confidential, private or sensitive files unless you understand and accept the provider's current privacy and retention terms.

---

## 👨‍💻 Author

Developed by **Swir** — [@Swir](https://github.com/Swir)

<div align="center">

### ☁️ Simple file transfers with a terminal UI that actually looks good

⭐ **Star the repository if you find it useful!**

</div>
