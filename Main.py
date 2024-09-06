import discord
from discord import app_commands
from discord.ext import commands
import os
import asyncio
import time
import asyncpg
from datetime import datetime, timezone
from time import perf_counter
from asyncpg.pool import create_pool

from apikeys import Token, Database_Name, Host_IP, Host_Port, User_Name, User_Pass

DEFAULT_PREFIX = "!"

#time
def current_time ():
    now = datetime.now(timezone.utc)
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time

async def get_server_prefix(bot, message):
    prefix = await bot.pool.fetchrow('SELECT prefix FROM info WHERE guild_id = $1', message.guild.id)
    return prefix

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix= get_server_prefix, intents=intents)

##  Events
    #  on_guild_join
@bot.event
async def on_guild_join(guild):
    owner = guild.owner
    server = guild.name
    await owner.send(f"Thank you for adding The Holy Roller to **{server}**")
    await bot.pool.execute('INSERT INTO info (guild_id, prefix) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET prefix = $2', guild.id, DEFAULT_PREFIX)

    #  on_guild_remove
@bot.event
async def on_guild_remove(guild):
    await bot.pool.execute('DELETE FROM info WHERE guild_id = $1', guild.id)
    
##  Commands
@bot.command()
async def setprefix(ctx, new_prefix: str):
    try:
        await bot.pool.execute('UPDATE info SET prefix = $2 WHERE guild_id = $1', ctx.guild.id, new_prefix)
        await ctx.send(f"Changed prefix to {new_prefix}")
    except:
        await ctx.send("Could not change prefix, please try again")

##  Core

    #  on_ready
@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f"synced {len(synced)} command(s)")
    await bot.change_presence(activity=discord.activity.Game(name="Church service simulator 2024"))
    print("The Holly Roller is awake and high as a fucking kite just like always     ", "UTC:",current_time())
    print("---------------------------------------------------------------------")
    
    #  Load cogs
async def load():
    start = perf_counter()
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
    end = perf_counter()
    print(f"Loading took {(end-start)*1000} ms")

    #  Main
async def main():

    #startup debug
    discord.utils.setup_logging()

    #DB connection
    try:
        bot.pool = await asyncpg.create_pool(database=Database_Name, host=Host_IP, port=Host_Port, user=User_Name, password=User_Pass)
        print("Connection to DB was successfully established.")
    except:
        print("Connection to DB failed to establish.")
        exit()

    #Start
    try:
        await load()
        await bot.start(Token)
    finally:
        await bot.pool.close()

asyncio.run(main())