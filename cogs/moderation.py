import discord
import typing
import asyncio
import asyncpg
import logging
from typing import Literal
from discord import app_commands, File
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, CheckFailure
from datetime import datetime, timezone
from datetime import timedelta

from links import Holly_Roller_pfp, LDL_pfp

#time

def current_time():
    now = datetime.now(timezone.utc)
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time

#Get logging channel

async def get_logging_channel(self, ctx):
    logging_channel = await self.pool.fetchrow('SELECT log_id FROM info WHERE guild_id = $1', ctx.guild.id)
    try:
        log_id = logging_channel["log_id"]
        logging_channel = await self.bot.fetch_channel(log_id)
    except:
        logging_channel = False
    return logging_channel

#Make log entry

async def log_entry(self, ctx, user, action, author_id, reason, time, channel):
    author_name = await self.bot.fetch_user(int(author_id))

    image_file = File("Images/moderation_icon.png", filename="moderation_icon.png")
    log_entry_embed = discord.Embed(title="Moderation action!", color=discord.Color.from_rgb(140,27,27))
    if reason == None:
        log_entry_embed.add_field(name="", value=f"User **{user}** was {action} by **{author_name}**.")
    else:
        log_entry_embed.add_field(name="", value=f"User **{user}** was {action} by **{author_name}** for **{reason}**.")
    log_entry_embed.set_thumbnail(url="attachment://moderation_icon.png") 
    if action == "muted":
        log_entry_embed.add_field(name="", value= f"Time: **{time}**")
    log_entry_embed.add_field(name="", value= f"User ID: **{user.id}**")
    log_entry_embed.set_footer(text=f"Action made by: {author_name} ({author_id}).\nUTC: {current_time()}")
    await channel.send(file=image_file, embed=log_entry_embed)
    
class moderation(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.pool =bot.pool

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
        print("---|moderation cog loaded!|---", current_time())
    
# kick #DONE

    @commands.hybrid_command(name = "kick", description='Kicks a member', aliases=["Kick"])
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx: commands.Context, user: discord.Member|discord.User, reason: typing.Optional[str] = None):

        try:
            user_id = user.id
        except:
            user_id = int(user)
            user = await self.bot.fetch_user(int(user_id))
        server = ctx.guild.name
        author_id = ctx.author.id

        try:
            await ctx.guild.fetch_member(user_id)
        except discord.NotFound:
            await ctx.send("Unable to kick a member who's not in the server.")
        else:

            if user_id == author_id:
                await ctx.send("Trying to give yourself the boot? I mean you do you and all but like no, just no...", ephemeral=True)
            else:

                Loggin_channel = await get_logging_channel(self, ctx)

                if Loggin_channel == False:

                    if reason == None:
                        reason = "None"
                        await user.send(f"You've been kicked from **{server}**", file=discord.File("Images/kick.gif"))
                        await ctx.send(f'User {user.mention} has been kicked.\nPlease consider setting up the logging feature by running "/settings channels".')

                    else:
                        reason = " ".join(ctx.message.content.split()[2:])
                        await user.send(f"You've been kicked from **{server}** for **{reason}**", file=discord.File("Images/kick.gif"))
                        await ctx.send(f'User {user.mention} has been kicked for **{reason}**.\nPlease consider setting up the logging feature by running "/settings channels".')
                        
                    await user.kick(reason=reason)
                else:

                    if reason == None:
                        reason = "None"
                        await user.send(f"You've been kicked from **{server}**", file=discord.File("Images/kick.gif"))
                        await ctx.send(f'User {user.mention} has been kicked.')

                    else:
                        reason = " ".join(ctx.message.content.split()[2:])
                        await user.send(f"You've been kicked from **{server}** for **{reason}**", file=discord.File("Images/kick.gif"))
                        await ctx.send(f'User {user.mention} has been kicked for **{reason}**.')

                    action = "kicked"
                    time = None
                    await log_entry(self, ctx, user, action, author_id, reason, time, Loggin_channel)
                    
                    await user.kick(reason=reason)

# Ban #DONE

    @commands.hybrid_command(name = "ban", description='Bans a member', aliases=["Ban"])
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx: commands.Context, user: discord.Member|discord.User, reason: typing.Optional[str] = None):

        try:
            user_id = user.id
        except:
            user_id = int(user)
            user = await self.bot.fetch_user(int(user_id))
        server = ctx.guild.name
        author_id = ctx.author.id

        try:
            await ctx.guild.fetch_ban(user)
        except discord.NotFound:

            if user_id == author_id:
                await ctx.send("Banning yourself? Nice one but sadly I'll have to say\n# NO!", ephemeral=True)
            else:

                Loggin_channel = await get_logging_channel(self, ctx)

                if Loggin_channel == False:

                    if reason == None:
                        reason = "None"
                        await user.send(f"You've been banned from **{server}**", file=discord.File("Images/ban.gif"))
                        await ctx.send(f'User {user.mention} has been banned.\nPlease consider setting up the logging feature by running "/settings channels".')

                    else:
                        reason = " ".join(ctx.message.content.split()[2:])
                        await user.send(f"You've been banned from **{server}** for **{reason}**", file=discord.File("Images/ban.gif"))
                        await ctx.send(f'User {user.mention} has been banned for **{reason}**.\nPlease consider setting up the logging feature by running "/settings channels".')
                        
                    await user.ban(reason=reason)
                else:

                    if reason == None:
                        reason = "None"
                        await user.send(f"You've been banned from **{server}**", file=discord.File("Images/ban.gif"))
                        await ctx.send(f'User {user.mention} has been banned.')

                    else:
                        reason = " ".join(ctx.message.content.split()[2:])
                        await user.send(f"You've been banned from **{server}** for **{reason}**", file=discord.File("Images/ban.gif"))
                        await ctx.send(f'User {user.mention} has been banned for **{reason}**.')

                    action = "banned"
                    time = None
                    await log_entry(self, ctx, user, action, author_id, reason, time, Loggin_channel)
                    
                    await user.ban(reason=reason)
        else:
            await ctx.send("Unable to ban a user who's already banned")
   
# Unban #DONE

    @commands.hybrid_command(name = "unban", description='unbans a member', aliases = ["Unban","uban","Uban"])
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx: commands.Context, user: discord.Member|discord.User, reason: typing.Optional[str] = None):

        try:
            user_id = user.id
        except:
            user_id = int(user)
            user = await self.bot.fetch_user(int(user_id))

        author_id = ctx.author.id

        try:
            await ctx.guild.fetch_ban(user)
        except discord.NotFound:
            await ctx.send("That user is not banned in this server")
        else:

            if user_id == author_id:
                await ctx.send("Ok, let's think this over...\nYou're in the server you want to be unbanned from... right?\n-# (Buddy ain't the smartest :cold_face:)")
            else:

                Loggin_channel = await get_logging_channel(self, ctx)

                if Loggin_channel == False:

                    if reason == None:
                        reason = "None"
                        await ctx.send(f'User {user.mention} has been unbanned.')

                    else:
                        reason = " ".join(ctx.message.content.split()[2:])
                        await ctx.send(f'User {user.mention} has been unbanned for **{reason}**.')
                        
                    await user.ban(reason=reason)
                else:

                    if reason == None:
                        reason = "None"
                        await ctx.send(f'User {user.mention} has been unbanned.')

                    else:
                        reason = " ".join(ctx.message.content.split()[2:])
                        await ctx.send(f'User {user.mention} has been unbanned for **{reason}**.')

                    action = "unbanned"
                    time = None
                    await log_entry(self, ctx, user, action, author_id, reason, time, Loggin_channel)
                    
                    await ctx.guild.unban(discord.Object(int(user_id)))

# Mute #FIXME

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
        valid_units = {"S", "M", "H", "D"}
        unit = time[-1].lower()
        duration = int(time[:-1])  

        if duration == 0 or None:
            await interaction.response.send_message(f"Please insert a time greater than 0", ephemeral=True)
            return
        if unit == "s":
            tdelta = timedelta(seconds=duration)
        elif unit == "m":
            tdelta = timedelta(minutes=duration)
        elif unit == "h":
            tdelta = timedelta(hours=duration)
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

# Unmute #FIXME

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

# Errors #FIXME

    @kick.error
    async def kick_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CommandInvokeError):
            await interaction.response.send_message("!!ERROR!! Please contact <@1184901953885585490>", ephemeral=True)
            print("----!!!!----")
            raise error
        elif isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message("The bot is missing permissions.", ephemeral=True)
        elif isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("You don't have permissions to do that :)", ephemeral=True)   
        else:
            raise error

    @ban.error
    async def ban_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CommandInvokeError):
            await interaction.response.send_message("!!ERROR!! Please contact <@1184901953885585490>", ephemeral=True)
            print("----!!!!----")
            raise error
        elif isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message("The bot is missing permissions.", ephemeral=True)
        elif isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("You don't have permissions to do that :)", ephemeral=True)   
        else:
            raise error

    @unban.error
    async def unban_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CommandInvokeError):
            await interaction.response.send_message("!!ERROR!! Please contact <@1184901953885585490>", ephemeral=True)
            print("----!!!!----")
            raise error
        elif isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message("The bot is missing permissions.", ephemeral=True)
        elif isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("You don't have permissions to do that :)", ephemeral=True)   
        else:
            raise error
    
    @mute.error
    async def mute_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CommandInvokeError):
            await interaction.response.send_message("!!ERROR!! Please contact <@1184901953885585490>", ephemeral=True)
            print("----!!!!----")
            raise error
        elif isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message("The bot is missing permissions.", ephemeral=True)
        elif isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("You don't have permissions to do that :)", ephemeral=True)   
        else:
            raise error
    
    @unmute.error
    async def unmute_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CommandInvokeError):
            await interaction.response.send_message("!!ERROR!! Please contact <@1184901953885585490>", ephemeral=True)
            print("----!!!!----")
            raise error
        elif isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message("The bot is missing permissions.", ephemeral=True)
        elif isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("You don't have permissions to do that :)", ephemeral=True)   
        else:
            raise error

async def setup(bot):
  await bot.add_cog(moderation(bot))