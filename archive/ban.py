import discord
import typing
from discord import app_commands, File
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, CheckFailure
from datetime import datetime, timezone

#time
def current_time ():
    now = datetime.now(timezone.utc)
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time

intents = discord.Intents.default()
intents.members = True

class ban(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.pool =bot.pool
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
        print("---|Ban       cog loaded!|---", current_time())

    @app_commands.command(name = "ban", description='Bans a member') 
    @app_commands.checks.has_permissions(ban_members = True)
    async def ban(self, interaction: discord.Interaction, user: discord.Member, reason: typing.Optional[str] = None):
        author_id = interaction.user.id
        user_id = user.id
        server = interaction.guild.name
        author_name = await interaction.client.fetch_user(int(author_id))
        Loggin_channel = await self.pool.fetchrow('SELECT log_id FROM info WHERE guild_id = $1', interaction.guild.id)
        try:
            log_id = Loggin_channel["log_id"]
            Loggin_channel = await interaction.client.fetch_channel(log_id)
            channel = Loggin_channel
        except:
            Loggin_channel = False

        if user_id == author_id:
            await interaction.response.send_message("Can't ban yourself dummy :)", ephemeral=True)
        else:
            if Loggin_channel == False:
                if reason == None:
                    reason = "None"
                    await interaction.response.send_message(f'User {user.mention} has been banned.\nPlease consider setting up the logging feature by running "/settings channels".')
                    await user.send(f"You've been banned from **{server}**", file=discord.File("Images/ban.gif"))
                else:
                    await interaction.response.send_message(f'User {user.mention} has been banned for **{reason}**.\nPlease consider setting up the logging feature by running "/settings channels".')
                    await user.send(f"You've been banned from **{server}** for **{reason}**", file=discord.File("Images/ban.gif"))                    
            else:
                image_file = File("Images/moderation_icon.png", filename="moderation_icon.png")
                Ban_embed = discord.Embed(title="Moderation action!", color=discord.Color.from_rgb(140,27,27))
                if reason == None:
                    reason = "None"
                    await interaction.response.send_message(f'User {user.mention} has been banned.')
                    await user.send(f"You've been banned from {server}", file=discord.File("Images/ban.gif"))
                    Ban_embed.add_field(name="", value= f"User {user} was banned by {author_name}.", inline=False)
                else:
                    await interaction.response.send_message(f'User {user.mention} has been banned for {reason}.')
                    await user.send(f"You've been banned from {server} for {reason}", file=discord.File("Images/ban.gif")) 
                    Ban_embed.add_field(name="", value= f"User {user} was banned for {reason} by {author_name}.", inline=False)

                Ban_embed.set_thumbnail(url="attachment://moderation_icon.png")    
                Ban_embed.add_field(name="", value= f"User ID: {user_id}")
                Ban_embed.set_footer(text=f"Action made by: {author_name} ({author_id}).\nUTC: {current_time()}")
                await channel.send(file=image_file, embed=Ban_embed) 
            await user.ban(reason=reason)

    @ban.error
    async def ban_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CommandInvokeError):
            await interaction.response.send_message("!!ERROR!! Please contact <@1184901953885585490>", ephemeral=True)
            print("----!!!!----")
            raise error
        if isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message("The bot is missing permissions.", ephemeral=True)
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("You don't have permissions to do that :)", ephemeral=True)

async def setup(bot):
  await bot.add_cog(ban(bot))