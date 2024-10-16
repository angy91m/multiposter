# Multiposter

## Requirements
- libmagic

## Python requirements
- asyncio
- aiohttp
- aiohttp-index
- python-magic
- tkinter (only if required)
- python-libmagic (maybe for windows)
- python-magic-bin (maybe for windows)

## Usage

### Create your venv and activate
Linux/MacOS:
```sh
python3 -m venv venv
source venv/bin/activate
```

Windows:
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### Install packages
Linux/MacOS:
```sh
pip install asyncio aiohttp aiohttp-index python-magic
```

### Configure
Create a `config.json` file like the example.
Create a `main.py` file like the example.

## Compile to exe
pyinstaller -F --add-data="config.json:." --add-data="public_html:." main.py