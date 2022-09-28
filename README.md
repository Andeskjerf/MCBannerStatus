# MCBannerStatus

Generates an image containing various data about a running Minecraft server.

The program will use the first line of your servers MOTD as the name to display on image.

Intended to be run in combination with a web server to provide live updates to a served image.

## Familiar with Chunky and MCRcon?

Then you might be interested in this!

https://gist.github.com/VladTheSheep/92fd12273eb469ee184ebc639c00a20a

## Example outputs

![1](https://user-images.githubusercontent.com/6963524/192139657-cc096c36-b3c4-481e-b0bb-9e2470e02120.png)
![2](https://user-images.githubusercontent.com/6963524/192139697-6f392719-030d-44ec-a69c-3df56f2a758d.png)
![3](https://user-images.githubusercontent.com/6963524/192139741-918b4ce0-2745-4867-a299-3d908163f593.png)

## Dependencies

- Python 3.10>=

## Getting started

```Bash
git clone https://github.com/VladTheSheep/MCBannerStatus.git
cd MCBannerStatus
./setup.sh
```

The `setup.sh` script will setup the project for you.

- Checks for a valid Python version
- Creates a Python venv
- Installs required dependencies
- Adds `src/conf.py`
- Adds `run.sh`

## Configuring

Before running the program, `src/conf.py` needs to be configured.

Alternatively, you can pass the appropriate values via arguments instead.

```Python
# All of these can either be set here or via runtime arguments
# If arguments are given, they'll override the respective values set here

# Can be left as is unless you want the status for a remote server
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 25565

# Path to save the output image
TARGET_PATH = ""

# Image and font to use
IMAGE_PATH = ""
REGULAR_FONT_PATH = ""

# Use italic fonts in certain situations, optional
ITALIC_FONT_PATH = ""

# How often we should check for updates, in seconds
INTERVAL = 60

# Set to True to enable image rotation
# Make sure to add images to the images folder!
IMAGE_ROTATION = False

# How often should the image be rotated out, in seconds
# Only applies if image rotation is enabled
IMAGE_ROTATION_INTERVAL = 900

# The offset between the edge of the image and the text
X_OFFSET = 64

# The size to use for fonts
FONT_SIZE = 58

# The height of the text field drawed onto the image
# If not set, the height will be the image's height divided by 6
FIELD_HEIGHT = None

# The opacity of the field
FIELD_OPACITY = 0.6

# The text to show if the server is online
ONLINE_TEXT = "Online"

# The text to show if the server is unreachable / offline
OFFLINE_TEXT = "Offline"

# Text to show inplace of the player count if the server is unreachable / offline
PLAYER_COUNT_OFFLINE_TEXT = "Connection error"


```

## Running

The repo comes with a bash script to launch the program.

```Bash
#!/bin/bash

source env/bin/activate
python main.py "$@"
```

Invoke with `--help` or no arguments to learn more.

## Launching on boot

To run the program automatically on boot or after a crash (which hopefully shouldn't happen), you can use systemd or whatever you prefer. Example systemd service provided below.

### `mcbannerstatus.service`

```ini
[Unit]
Description="MCBannerStatus - Automatically update image with data from MC server"
After=network-online.target

[Service]
Type=simple
Restart=always
WorkingDirectory=/path/to/MCBannerStatus
ExecStart=bash /path/to/MCBannerStatus/run.sh

[Install]
WantedBy=multi-user.target
```

Place the file in either `/etc/systemd/system/` or in your users systemd config `~/.config/systemd/user/`

```Bash
# Ensure the daemon is reloaded first! Append --user if installed as a user service
systemctl daemon-reload

# If installed as a system service
systemctl enable --now mcbannerstatus

# If installed as a user service
systemctl enable --now --user mcbannerstatus
```
