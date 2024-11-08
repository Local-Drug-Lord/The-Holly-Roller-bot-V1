import discord
import requests
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone

from links import Holly_Roller_pfp, LDL_pfp

#time
def current_time ():
    now = datetime.now(timezone.utc)
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time

class help(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
        print("---|Help       cog loaded!|---", current_time())

    @app_commands.command(name="help", description="command help list")
    async def help(self, interaction: discord.Integration):
        file1 = discord.File('Images/Holly_Roller_pfp.png')
        file2 = discord.File('Images/LDL_pfp.png')
        embed = discord.Embed(title="Help", description="This is a list of different commands and what they do.", color=660091)
        embed.set_author(name="Local Drug Lord", icon_url='attachment://LDL_pfp.png')
        embed.set_thumbnail(url='attachment://Holly_Roller_pfp.png')
        embed.add_field(name="**---| Moderation |---**", value= "", inline=False)
        embed.add_field(name="*/announce*", value="Sends an embedded message.", inline=True)
        embed.add_field(name="*/ban*", value="bans a member.", inline=True)
        embed.add_field(name="*/kick*", value="Kicks a member.", inline=True)
        embed.add_field(name="*/mute*", value="mutes a member.", inline=True)
        embed.add_field(name="*/unban*", value="unbans a member.", inline=True)
        embed.add_field(name="*/unmute*", value="unmutes a member.", inline=True)
        embed.add_field(name="**---| Config     |---**", value="", inline=False)
        embed.add_field(name="*/Settings channel*", value="Configure channels.", inline=True)
        embed.add_field(name="*/Settings messages*", value="Configure attachments.", inline=True)
        embed.add_field(name="*/Settings show*", value="Show the servers current config.", inline=True)
        embed.add_field(name="*/Settings help*", value="Show more in depth information about the /settings commands and related functions.", inline=True)
        embed.add_field(name="**---| Other      |---**", value="", inline=False)
        embed.add_field(name="*/help*", value="Shows this message.", inline=True)
        embed.add_field(name="*/ping*", value="Shows the response time of the bot.", inline=True)
        embed.set_footer(text=f"UTC: {current_time()}")
        await interaction.response.send_message(files=[file1, file2], embed=embed)

    @help.error
    async def help_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("There was an error executing this command, please contact developer")
        print("----!!!!----")
        raise error
        return

async def setup(bot):
  await bot.add_cog(help(bot))