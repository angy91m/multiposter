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

Your callback (`post_data` in `main_example.py`) will receive a post representation as a dict with this properties:
- `content`: a non-empty string
- `socials`: a non-empty list of non-empty strings

If an image was uploaded the post dict will have also:
- `image`: a bytestring with the content of the image
- `image_path`: a string with the full local path of the image file
- `image_url`: a string with the url of the remote image file
- `image_name`: a string with the temporary generated image filename
- `image_original_name`: a string with the original image filename
- `image_type`: a string with the detected image mime type
- `image_b64`: a string with the data URL representation of the image file

## Compile to exe
```powershell
pyinstaller -F --add-data="config.json:." --add-data="public_html:." main.py
```