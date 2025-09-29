import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
from utils.downloader import download_video, is_supported_url

LOG_FILE = 'bot.log'
MAX_LOG_LINES = 1000
TRIM_LINES = 500  # Anzahl der Zeilen, die gelöscht werden, wenn Limit erreicht ist

def trim_log_file():
    if not os.path.isfile(LOG_FILE):
        return
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if len(lines) >= MAX_LOG_LINES:
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.writelines(lines[TRIM_LINES:])

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
PREFIX = os.getenv("BOT_PREFIX", "!")

intents = discord.Intents.default()
intents.message_content = True

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('bot')

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

DISCORD_UPLOAD_LIMIT = 8 * 1024 * 1024  # 8 MB

@bot.event
async def on_ready():
    logger.info(f"Bot logged in as {bot.user} (ID: {bot.user.id})")

async def check_and_trim_log():
    trim_log_file()

@bot.command()
async def mp4(ctx, url: str):
    await check_and_trim_log()
    logger.info(f"MP4 command received from user {ctx.author} with url: {url}")
    if not is_supported_url(url):
        msg = "Error: The URL platform is not supported."
        logger.warning(msg + f" URL: {url}")
        await ctx.send(msg)
        return

    msg = await ctx.send("Starting MP4 download...")
    filename = await download_video(url, "mp4", msg)
    if filename:
        filesize = os.path.getsize(filename)
        if filesize > DISCORD_UPLOAD_LIMIT:
            msg_error = f"Error: The MP4 file is too large to upload ({filesize/1_048_576:.2f} MB). Max size is 8 MB."
            logger.warning(msg_error + f" Filename: {filename}, User: {ctx.author}")
            await msg.edit(content=msg_error)
            os.remove(filename)
            return

        await msg.edit(content=f"Uploading {filename}...")
        await ctx.send(file=discord.File(filename))
        os.remove(filename)
        await msg.delete()
        logger.info(f"Uploaded MP4 file {filename} for user {ctx.author}")
    else:
        err_msg = "Error: Could not download MP4."
        logger.error(f"{err_msg} URL: {url} User: {ctx.author}")
        await msg.edit(content=err_msg)

@bot.command()
async def mp3(ctx, url: str):
    await check_and_trim_log()
    logger.info(f"MP3 command received from user {ctx.author} with url: {url}")
    if not is_supported_url(url):
        msg = "Error: The URL platform is not supported."
        logger.warning(msg + f" URL: {url}")
        await ctx.send(msg)
        return

    msg = await ctx.send("Starting MP3 download...")
    filename = await download_video(url, "mp3", msg)
    if filename:
        filesize = os.path.getsize(filename)
        if filesize > DISCORD_UPLOAD_LIMIT:
            msg_error = f"Error: The MP3 file is too large to upload ({filesize/1_048_576:.2f} MB). Max size is 8 MB."
            logger.warning(msg_error + f" Filename: {filename}, User: {ctx.author}")
            await msg.edit(content=msg_error)
            os.remove(filename)
            return

        await msg.edit(content=f"Uploading {filename}...")
        await ctx.send(file=discord.File(filename))
        os.remove(filename)
        await msg.delete()
        logger.info(f"Uploaded MP3 file {filename} for user {ctx.author}")
    else:
        err_msg = "Error: Could not download MP3."
        logger.error(f"{err_msg} URL: {url} User: {ctx.author}")
        await msg.edit(content=err_msg)

@bot.command()
async def gif(ctx, url: str):
    await check_and_trim_log()
    logger.info(f"GIF command received from user {ctx.author} with url: {url}")
    if not is_supported_url(url):
        msg = "Error: The URL platform is not supported."
        logger.warning(msg + f" URL: {url}")
        await ctx.send(msg)
        return

    msg = await ctx.send("Starting GIF download...")
    filename = await download_video(url, "gif", msg)
    if filename:
        filesize = os.path.getsize(filename)
        if filesize > DISCORD_UPLOAD_LIMIT:
            msg_error = f"Error: The GIF file is too large to upload ({filesize/1_048_576:.2f} MB). Max size is 8 MB."
            logger.warning(msg_error + f" Filename: {filename}, User: {ctx.author}")
            await msg.edit(content=msg_error)
            os.remove(filename)
            return

        await msg.edit(content=f"Uploading {filename}...")
        await ctx.send(file=discord.File(filename))
        os.remove(filename)
        await msg.delete()
        logger.info(f"Uploaded GIF file {filename} for user {ctx.author}")
    else:
        err_msg = "Error: Could not download GIF."
        logger.error(f"{err_msg} URL: {url} User: {ctx.author}")
        await msg.edit(content=err_msg)

bot.run(TOKEN)
