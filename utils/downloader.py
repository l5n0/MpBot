import asyncio
from utils.filename_utils import sanitize_filename, get_unique_filename

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

async def download_video(url, format, msg):
    ext = "mp3" if format == "mp3" else "mp4"
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
    else:
        cmd = [
            "yt-dlp",
            "-f",
            "mp4",
            "-o",
            filename,
            url,
        ]

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
    if process.returncode != 0:
        return None
    return filename
