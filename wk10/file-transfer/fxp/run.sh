#!/bin/bash

# Create FTP directories if not exist
mkdir -p ftp1
mkdir -p ftp2

# Path to virtualenv activate script
VENV="p3net"

# Launch server 1 (port 2121) in ftp1
gnome-terminal -- bash -ic "cd ftp1 && workon p3net && python3 ../fxp-ftp-server.py 2121; echo 'Press enter to exit...'; read"

# Launch server 2 (port 2122) in ftp2
gnome-terminal -- bash -ic "cd ftp2 && workon p3net && python3 ../fxp-ftp-server.py 2122; echo 'Press enter to exit...'; read"

echo "Launched two FXP servers inside virtualenv p3net."
