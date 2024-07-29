#!/bin/bash

pip3 install curses
pip3 install random
pip3 install time
PYTHON_FILE="$HOME/NukeInvaders/main.py"
DESKTOP_FILE="$HOME/.local/share/applications/NukeInvaders.desktop"
LOGO_PATH="$HOME/NukeInvaders/Logo.png"

cat > "$DESKTOP_FILE" <<EOL
[Desktop Entry]
Name=Nuke Invaders
Exec=gnome-terminal --title="Nuke Invaders" -- python3 "$PYTHON_FILE" 
Icon=$LOGO_PATH
Type=Application
Categories=Games;
Terminal=>True
EOL




