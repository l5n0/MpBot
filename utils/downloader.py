import asyncio
import os
import logging
from urllib.parse import urlparse
from utils.filename_utils import sanitize_filename, get_unique_filename

DOWNLOAD_TIMEOUT = 300  # Timeout in Sekunden (5 Minuten)

# Logging-Setup
logger = logging.getLogger('downloader')

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
    except Exception as e:
        logger.error(f"URL parsing error: {e}")
        return False

async def get_video_title(url: str) -> str:
    try:
        process = await asyncio.create_subprocess_exec(
            'yt-dlp', '--get-title', url,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await process.communicate()
        if process.returncode == 0:
            title = stdout.decode().strip()
            return sanitize_filename(title)
        else:
            logger.error(f"Failed to get video title for URL {url} with return code {process.returncode}")
            return "output"
    except Exception as e:
        logger.error(f"Exception during video title retrieval: {e}")
        return "output"

async def _download(cmd, msg, format):
    try:
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
    except Exception as e:
        logger.error(f"Exception during download: {e}")
        return -1

async def download_video(url, format, msg):
    ext = "mp3" if format == "mp3" else "mp4"
    title = await get_video_title(url)
    filename = get_unique_filename(title, ext)
    logger.info(f"Starting download: url={url}, format={format}, filename={filename}")

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
    else:
        cmd = [
            "yt-dlp",
            "-f",
            "mp4",
            "-o",
            filename,
            url,
        ]

    try:
        retcode = await asyncio.wait_for(_download(cmd, msg, format), timeout=DOWNLOAD_TIMEOUT)
    except asyncio.TimeoutError:
        logger.error(f"Download timeout for URL: {url}")
        await msg.edit(content="Error: Download took too long and was cancelled.")
        return None

    if retcode != 0:
        logger.error(f"Download failed for URL: {url} with return code: {retcode}")
        return None

    logger.info(f"Download finished successfully: {filename}")
    return filename
