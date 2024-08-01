# bot.py：
# 主要提供 load、unload、reload 的指令，
# 可以讓 Bot 不掉線，也能修改程式，並讓 Bot 收到最新的指令。

import os
from dotenv import load_dotenv, find_dotenv
import asyncio
import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

load_dotenv(find_dotenv())
# CHANNEL_ID = os.getenv("CHANNEL_ID")
TOKEN = os.getenv("DISCORD_TOKEN")


@bot.event
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")


# 用於將新的程式檔案載入，或是之前未載入的檔案載入。
@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")


# 用於若程式碼有問題，可以先卸載避免機器人出錯
@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"UnLoaded {extension} done.")


# 用於更新了某個指令檔案
@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"ReLoaded {extension} done.")


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


if __name__ == "__main__":
    # print({CHANNEL_ID})
    asyncio.run(main())
