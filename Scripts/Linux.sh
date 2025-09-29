#!/bin/bash
set -e

echo \"Installing ffmpeg on Linux...\"

# Update Paketliste und installiere ffmpeg
sudo apt update
sudo apt install -y ffmpeg

# Prüfe Installation
if command -v ffmpeg &> /dev/null
then
    echo \"ffmpeg wurde erfolgreich installiert.\"
else
    echo \"Fehler: ffmpeg konnte nicht installiert werden.\"
    exit 1
fi
