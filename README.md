# MpBot

A handy Discord bot that downloads videos as MP4 files or extracts audio as MP3 from any shared link, delivering media quickly and easily.

---

## Features

- Download MP3, MP4, and GIF files using simple commands (`!mp3 <URL>`, `!mp4 <URL>`, `!gif <URL>`)
- Progress updates shown during downloading
- Automatic filename generation with conflict avoidance
- Supports many platforms thanks to yt-dlp (YouTube, Vimeo, TikTok, Instagram, and more)
- File size checks with upload limit (default 8 MB) before sending
- Error and event logging to `bot.log` with automatic log size management
- GIF downloads are optimized automatically (max 10 seconds, 10 fps, 320px width)

---

## Requirements

- Python 3.8 or higher
- yt-dlp (called internally by the bot, must be installed)
- ffmpeg (required for GIF conversion and media processing)

---

## Installing ffmpeg

For the bot to properly convert videos to GIFs and process media files, **ffmpeg** needs to be installed.

### Linux

Run the included script `Scripts/Linux.sh` in the terminal to install ffmpeg automatically:

```bash
bash Scripts/Linux.sh
```

### Windows

Run the prepared PowerShell script `Scripts/Windows.ps1` with administrator privileges to download and add ffmpeg to the system path:

```cmd
.\Scripts\Windows.ps1
```


A system restart is recommended afterward to activate the new path.

---

## Starting the Bot

1. Create a `.env` file in the root folder with the following content:

```env
DISCORD_BOT_TOKEN=your_discord_bot_token
BOT_PREFIX=!
```


2. Install the required Python packages:

```
pip install -r requirements.txt
```


3. Start the bot:

```
python bot.py
```


---

## Usage

- `!mp3 <URL>`: Downloads the audio track as an MP3 and sends it.
- `!mp4 <URL>`: Downloads the video as an MP4 and sends it.
- `!gif <URL>`: Creates a GIF up to 10 seconds long and sends it.

---

## Logs

The bot logs important events in the `bot.log` file. This file is automatically limited to 1000 lines to keep its size manageable.

---

## License

This bot is open source. Contributions and modifications are welcome!

---

If you encounter questions or issues, feel free to reach out. Enjoy using the Media Downloader Bot!
