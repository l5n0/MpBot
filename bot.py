import discord
from discord.ext import commands
import asyncio
import os
import re
from dotenv import load_dotenv

load_dotenv()  # Lädt Umgebungsvariablen aus .env

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
PREFIX = os.getenv("BOT_PREFIX", "!")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

def sanitize_filename(name: str) -> str:
    # Entfernt unzulässige Zeichen aus Dateinamen z.B. Windows ungültige
    return re.sub(r'[\\/*?:"<>|]', "", name)

def get_unique_filename(base_name, ext):
    filename = f"{base_name}.{ext}"
    counter = 1
    while os.path.exists(filename):
        filename = f"{base_name}({counter}).{ext}"
        counter += 1
    return filename

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

async def download_video(url, format):
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
    process = await asyncio.create_subprocess_exec(*cmd)
    await process.communicate()
    if process.returncode != 0:
        return None
    return filename

@bot.command()
async def mp4(ctx, url: str):
    await ctx.send("Downloading MP4... please wait")
    filename = await download_video(url, "mp4")
    if filename:
        await ctx.send(file=discord.File(filename))
        os.remove(filename)
    else:
        await ctx.send("Error: Could not download MP4.")

@bot.command()
async def mp3(ctx, url: str):
    await ctx.send("Downloading MP3... please wait")
    filename = await download_video(url, "mp3")
    if filename:
        await ctx.send(file=discord.File(filename))
        os.remove(filename)
    else:
        await ctx.send("Error: Could not download MP3.")

bot.run(TOKEN)
