import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from utils.downloader import download_video

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
PREFIX = os.getenv("BOT_PREFIX", "!")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

DISCORD_UPLOAD_LIMIT = 8 * 1024 * 1024  # 8 MB

@bot.command()
async def mp4(ctx, url: str):
    msg = await ctx.send("Starting MP4 download...")
    filename = await download_video(url, "mp4", msg)
    if filename:
        filesize = os.path.getsize(filename)
        if filesize > DISCORD_UPLOAD_LIMIT:
            await msg.edit(content=f"Error: The MP4 file is too large to upload ({filesize/1_048_576:.2f} MB). Max size is 8 MB.")
            os.remove(filename)
            return

        await msg.edit(content=f"Uploading {filename}...")
        await ctx.send(file=discord.File(filename))
        os.remove(filename)
        await msg.delete()
    else:
        await msg.edit(content="Error: Could not download MP4.")

@bot.command()
async def mp3(ctx, url: str):
    msg = await ctx.send("Starting MP3 download...")
    filename = await download_video(url, "mp3", msg)
    if filename:
        filesize = os.path.getsize(filename)
        if filesize > DISCORD_UPLOAD_LIMIT:
            await msg.edit(content=f"Error: The MP3 file is too large to upload ({filesize/1_048_576:.2f} MB). Max size is 8 MB.")
            os.remove(filename)
            return

        await msg.edit(content=f"Uploading {filename}...")
        await ctx.send(file=discord.File(filename))
        os.remove(filename)
        await msg.delete()
    else:
        await msg.edit(content="Error: Could not download MP3.")

bot.run(TOKEN)
