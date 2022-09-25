# MCBannerStatus
Generates an image containing various data about a running Minecraft server.

Intended to be run in combination with a web server to provide live updates to a served image.

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
 - Creates `images`
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

# Image and font to use
IMAGE_PATH = ""
REGULAR_FONT_PATH = ""

# Set to true to enable image rotation
# Make sure to add images to the images folder!
IMAGE_ROTATION = False

# How often should the image be rotated out, in seconds
# Only applies if image rotation is enabled
IMAGE_ROTATION_INTERVAL = 900

# Path to save the output image
TARGET_PATH = ""

# Use italic fonts in certain situations, optional
ITALIC_FONT_PATH = ""

# The offset between the edge of the image and the text
X_OFFSET = 64

# The size to use for fonts
FONT_SIZE = 64

# The height of the text field drawed onto the image
# If not set, the height will be the image's height divided by 6
FIELD_HEIGHT = None

# The opacity of the field
FIELD_OPACITY = 0.5

# The text to show if the server is online
ONLINE_TEXT = "Online"

# The text to show if the server is unreachable / offline
OFFLINE_TEXT = "Offline"

# Text to show inplace of the player count if the server is unreachable / offline
PLAYER_COUNT_OFFLINE_TEXT = "Unable to establish connection"
```

## Running

The repo comes with a bash script to launch the program.

```Bash
#!/bin/bash

source env/bin/activate
python main.py "$@"
```

Invoke with `--help` or no arguments to learn more.

## Automatically updating the banner

To run the program automatically, you can use systemd or whatever you prefer. Example systemd service and timer is provided below.

#### `mcbannerstatus.service`

```
[Unit]
Description="Updates Minecraft banner"
After=network-online.target

[Service]
Type=simple
WorkingDirectory=/path/to/MCBannerStatus
ExecStart=bash /path/to/MCBannerStatus/run.sh
```

#### `mcbannerstatus.timer`

```
[Unit]
Description=Timer for MCBannerStatus

[Timer]
OnBootSec=0min
OnUnitActiveSec=5min

[Install]
WantedBy=multi-user.target
```

You can set how often you want to update the banner by changing `OnUnitActiveSec=5min`.

Place both of these files in either `/etc/systemd/system/` or in your users systemd config `~/.config/systemd/user/`

You can enable it by enabling and starting the timer.

```Bash
# Ensure the daemon is reloaded first! Append --user if installed as a user service
systemctl daemon-reload

# If installed as a system service
systemctl enable --now mcbannerstatus.timer

# If installed as a user service
systemctl enable --now --user mcbannerstatus.timer
```
