import asyncio
import os
from urllib.parse import urlparse
from utils.filename_utils import sanitize_filename, get_unique_filename

DOWNLOAD_TIMEOUT = 300  # Timeout in Sekunden (5 Minuten)

# Unterstützte Plattformen (Domains)
SUPPORTED_DOMAINS = [
    "youtube.com", "youtu.be",
    "vimeo.com",
    "soundcloud.com",
    "facebook.com",
    "twitch.tv",
    "dailymotion.com",
    "bilibili.com",
    "twitter.com",
    "tiktok.com",
    "instagram.com",
]

def is_supported_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        for d in SUPPORTED_DOMAINS:
            if d in domain:
                return True
        return False
    except Exception:
        return False

async def get_video_title(url: str) -> str:
    process = await asyncio.create_subprocess_exec(
        'yt-dlp', '--get-title', url,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, _ = await process.communicate()
    if process.returncode == 0:
        title = stdout.decode().strip()
        return sanitize_filename(title)
    return "output"

async def _download(cmd, msg, format):
    process = await asyncio.create_subprocess_exec(*cmd,
                                                   stdout=asyncio.subprocess.PIPE,
                                                   stderr=asyncio.subprocess.STDOUT)
    while True:
        line = await process.stdout.readline()
        if not line:
            break
        line_str = line.decode('utf-8').strip()
        if "%" in line_str:
            try:
                percent = line_str.split("%")[0].split()[-1]
                await msg.edit(content=f"Downloading {format.upper()}... {percent}%")
            except Exception:
                pass
    await process.wait()
    return process.returncode

async def download_video(url, format, msg):
    ext = "mp3" if format == "mp3" else ("gif" if format == "gif" else "mp4")
    title = await get_video_title(url)
    filename = get_unique_filename(title, ext)

    if format == "mp3":
        cmd = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format",
            "mp3",
            "-o",
            filename,
            url,
        ]
        retcode = await asyncio.wait_for(_download(cmd, msg, format), timeout=DOWNLOAD_TIMEOUT)
        if retcode != 0:
            return None
        return filename

    elif format == "gif":
        # Download video zuerst als MP4
        video_temp = get_unique_filename(title, "mp4")
        cmd_download = [
            "yt-dlp",
            "-f",
            "mp4",
            "-o",
            video_temp,
            url,
        ]
        retcode = await asyncio.wait_for(_download(cmd_download, msg, "mp4"), timeout=DOWNLOAD_TIMEOUT)
        if retcode != 0:
            return None

        # Palette für GIF erstellen
        palette_cmd = [
            "ffmpeg",
            "-y",
            "-i",
            video_temp,
            "-t", "10",
            "-vf", "fps=10,scale=320:-1:flags=lanczos,palettegen",
            "palette.png"
        ]
        process_palette = await asyncio.create_subprocess_exec(*palette_cmd)
        await process_palette.communicate()
        if process_palette.returncode != 0:
            os.remove(video_temp)
            return None

        # GIF erstellen mit Palette
        ffmpeg_gif_cmd = [
            "ffmpeg",
            "-y",
            "-i",
            video_temp,
            "-i",
            "palette.png",
            "-t", "10",
            "-lavfi",
            "fps=10,scale=320:-1:flags=lanczos[x];[x][1:v]paletteuse",
            filename
        ]
        process_gif = await asyncio.create_subprocess_exec(*ffmpeg_gif_cmd)
        await process_gif.communicate()

        os.remove(video_temp)
        os.remove("palette.png")

        if process_gif.returncode != 0:
            return None

        return filename

    else:
        # mp4 Standarddownload
        cmd = [
            "yt-dlp",
            "-f",
            "mp4",
            "-o",
            filename,
            url,
        ]
        retcode = await asyncio.wait_for(_download(cmd, msg, format), timeout=DOWNLOAD_TIMEOUT)
        if retcode != 0:
            return None
        return filename
