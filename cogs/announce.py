import discord
import typing
import requests
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, CheckFailure
from datetime import datetime, timezone

#time
def current_time ():
    now = datetime.now(timezone.utc)
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time

class announce(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
    
        print("---|Announce   cog loaded!|---", current_time())
    
    @app_commands.command(name = "announce", description='Announce something!')
    @app_commands.checks.has_permissions(administrator = True)
    async def announce(self, interaction: discord.Interaction, title: str, content: str, attachment: typing.Optional[str], channel: discord.TextChannel, ping: discord.Role = None):
        author_id = interaction.user.id
        channel = self.bot.get_channel(channel.id)
        author_name = await interaction.client.fetch_user(int(author_id))

        if title == None:
            announce_embed = discord.Embed(title="", color=discord.Color.from_rgb(41,134,0))
        else:
            announce_embed = discord.Embed(title=title, color=discord.Color.from_rgb(41,134,0))
        if content == None:
            announce_embed.add_field(name="", value="")
        else:
            announce_embed.add_field(name=content, value="", inline=False)
        if not attachment == None:
            announce_embed.set_image(url=attachment)
        announce_embed.set_footer(text=f"Made by: \n{author_name} ({author_id}).\nUTC: {current_time()}")
        if ping == None:
            await channel.send(embed=announce_embed)
        else:
            await channel.send(ping.mention)
            await channel.send(embed=announce_embed)
        await interaction.response.send_message(f"Sent message in {channel}", ephemeral=True)
    
    @announce.error
    async def announce_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CommandInvokeError):
            await interaction.response.send_message("There was an error executing this command, please contact developer")
            print("----!!!!----")
            raise error
            return
        elif isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message("The bot is missing permissions.", ephemeral=True)
        elif isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("You don't have permissions to do that :)", ephemeral=True)
        else:
            await interaction.response.send_message("There was an error executing this command, please contact developer")
            print("----!!!!----")
            raise error
            return

async def setup(bot):
  await bot.add_cog(announce(bot))