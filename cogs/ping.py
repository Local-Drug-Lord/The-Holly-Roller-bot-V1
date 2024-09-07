import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone

#time
def current_time ():
    now = datetime.now(timezone.utc)
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time

class ping(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.pool =bot.pool
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
        print("---|Ping       cog loaded!|---", current_time())

    @commands.hybrid_command(name="ping", description="you ping i pong! ;)") #TODO General appearance modifications
    async def ping(self, ctx: commands.Context):
        bot_latency = round(self.bot.latency * 1000)
        Ping_embed = discord.Embed(title="Pong! :ping_pong:", color=discord.Color.from_rgb(41,134,0))
        Ping_embed.add_field(name="", value= "", inline=False)
        Ping_embed.add_field(name=":satellite: API:", value= f"**{bot_latency} ms.**", inline=True)
        Ping_embed.add_field(name="", value= "", inline=True)
        try:
            await self.pool.fetchrow('SELECT guild_id FROM info WHERE guild_id = $1', ctx.guild.id )
            Ping_embed.add_field(name=":file_cabinet: Database:", value= "**DB connection: __Normal__**", inline=True)
        except:
            Ping_embed.add_field(name=":file_cabinet: Database:", value= "**DB connection: __Dead__**", inline=True)
        Ping_embed.set_footer(text=f"UTC: {current_time()}")
        await ctx.send(embed=Ping_embed)

    @ping.error
    async def ping_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("There was an error executing this command, please contact developer")
            print("----!!!!----")
            raise error
            return
        else:
            await ctx.send("There was an error executing this command, please contact developer")
            print("----!!!!----")
            raise error
            return

async def setup(bot):
  await bot.add_cog(ping(bot))