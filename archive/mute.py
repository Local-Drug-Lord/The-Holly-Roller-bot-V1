import discord
import typing
from discord import app_commands, File
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, CheckFailure
from datetime import datetime, timezone
from datetime import timedelta

#time
def current_time ():
    now = datetime.now(timezone.utc)
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time

intents = discord.Intents.default()
intents.members = True

class mute(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.pool =bot.pool
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
        print("---|Mute      cog loaded!|---", current_time())

    @app_commands.command(name = "mute", description='Mutes a member')
    @app_commands.checks.has_permissions(mute_members = True)
    async def mute(self, interaction: discord.Interaction, user: discord.Member, time: str, reason: typing.Optional[str] = None):
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

        # Validate time input
        valid_units = {"h", "H", "m", "M", "s","S", "d", "D"}
        unit = time[-1].lower()
        duration = int(time[:-1])  

        if unit == "h":
          tdelta = timedelta(hours=duration)
        elif unit == "m":
            tdelta = timedelta(minutes=duration)
        elif unit == "s":
            tdelta = timedelta(seconds=duration)
        elif unit == "d":
            tdelta = timedelta(days=duration)
        else:
            await interaction.response.send_message(f"Invalid time format: **{unit}**! \nValid units are: **{valid_units}**.", ephemeral=True)
            return
            
        if user_id == author_id:
            await interaction.response.send_message("Can't mute yourself dummy :)", ephemeral=True)
        else:
            if Loggin_channel == False:
                if reason == None:
                    await user.send(f"You've been muted in **{server}**", file=discord.File("Images/mute.gif"))
                    await interaction.response.send_message(f'User {user.mention} has been muted.\nPlease consider setting up the logging feature by running "/settings channels".')
                else:
                    await user.send(f"You've been muted in **{server}** for **{reason}**", file=discord.File("Images/mute.gif"))
                    await interaction.response.send_message(f'User {user.mention} has been muted for **{reason}**.\nPlease consider setting up the logging feature by running "/settings channels".')
            else:
                image_file = File("Images/moderation_icon.png", filename="moderation_icon.png")
                Mute_embed = discord.Embed(title="Moderation action!", color=discord.Color.from_rgb(140,27,27))
                if reason == None:
                    await user.send(f"You've been muted in **{server}**", file=discord.File("Images/mute.gif"))
                    await interaction.response.send_message(f'User {user.mention} has been muted.')
                    Mute_embed.add_field(name="", value= f"User **{user}** was muted by **{author_name}**.", inline=False)
                else:
                    await user.send(f"You've been muted in **{server}** for **{reason}**", file=discord.File("Images/mute.gif"))
                    await interaction.response.send_message(f'User {user.mention} has been muted for **{reason}**.')
                    Mute_embed.add_field(name="", value= f"User **{user}** was muted for **{reason}** by **{author_name}**.", inline=False)
            
                Mute_embed.set_thumbnail(url="attachment://moderation_icon.png")  
                Mute_embed.add_field(name="", value= f"Time: **{tdelta}**")
                Mute_embed.add_field(name="", value= f"User ID: **{user_id}**", inline=False)
                Mute_embed.set_footer(text=f"Action made by: {author_name} ({author_id}).\nUTC: {current_time()}")
                await channel.send(file=image_file, embed=Mute_embed)
            await user.timeout(tdelta)
    
    @mute.error
    async def mute_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CommandInvokeError):
            await interaction.response.send_message("!!ERROR!! Please contact <@1184901953885585490>", ephemeral=True)
            print("----!!!!----")
            raise error
        if isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message("The bot is missing permissions.", ephemeral=True)
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("You don't have permissions to do that :)", ephemeral=True)       

async def setup(bot):
  await bot.add_cog(mute(bot))