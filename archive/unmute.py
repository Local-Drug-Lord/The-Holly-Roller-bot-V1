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

class unmute(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.pool =bot.pool
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
        print("---|Unmute    cog loaded!|---", current_time())

    @app_commands.command(name = "unmute", description='Unmutes a member')
    @app_commands.checks.has_permissions(mute_members = True)
    async def unmute(self, interaction: discord.Interaction, user: discord.Member, reason: typing.Optional[str] = None):
                
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

        if Loggin_channel == False:
                if reason == None:
                    await interaction.response.send_message(f'User **{user}** has been unmuted.\nPlease consider setting up the logging feature by running "/settings channels".')
                else:
                    await interaction.response.send_message(f'User **{user}** has been unmuted for **{reason}**.\nPlease consider setting up the logging feature by running "/settings channels".')
        else:
            image_file = File("Images/moderation_icon.png", filename="moderation_icon.png")
            Unmute_embed = discord.Embed(title="Moderation action!", color=discord.Color.from_rgb(140,27,27))    
            if reason == None:
                await interaction.response.send_message(f'User **{user}** has been unmuted.')
                Unmute_embed.add_field(name="", value= f"User **{user}** was unmuted by {author_name}.", inline=False)
            else:
                await interaction.response.send_message(f'User **{user}** has been unmuted for **{reason}**.')
                Unmute_embed.add_field(name="", value= f"User **{user}** was unmuted for **{reason}** by **{author_name}**.", inline=False)

            Unmute_embed.set_thumbnail(url="attachment://moderation_icon.png")  
            Unmute_embed.add_field(name="", value= f"User ID: **{user_id}**")
            Unmute_embed.set_footer(text=f"Action made by: {author_name} ({author_id}).\nUTC: {current_time()}")
            await channel.send(file=image_file, embed=Unmute_embed)
        await user.edit(timed_out_until=None)
    
    @unmute.error
    async def unmute_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CommandInvokeError):
            await interaction.response.send_message("!!ERROR!! Please contact <@1184901953885585490>", ephemeral=True)
            print("----!!!!----")
            raise error
        if isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message("The bot is missing permissions.", ephemeral=True)
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("You don't have permissions to do that :)", ephemeral=True)       

async def setup(bot):
  await bot.add_cog(unmute(bot))