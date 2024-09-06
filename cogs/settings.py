import discord
import typing
from typing import Literal
from discord import app_commands, File
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, CheckFailure
from datetime import datetime, timezone

#TODO Make a it so you can't update a DB value to the thing it already is

#time
def current_time():
    now = datetime.now(timezone.utc)
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time

#rgb > list (R,G,B)
def Convert(string):
    print(string)
    string = string.replace(',', '')
    print(string)
    li = list(string.split(" "))
    print(li)
    return li

#Logging channel
async def get_logging_channel(interaction, self):
    logging_channel = await self.pool.fetchrow('SELECT log_id FROM info WHERE guild_id = $1', interaction.guild.id)
    try:
        log_id = logging_channel["log_id"]
        logging_channel = await interaction.client.fetch_channel(log_id)
    except:
        logging_channel = False
    return logging_channel

#Log entry
async def log_entry(self, interaction, What, Type, To):
    author_id = interaction.user.id
    author_name = await interaction.client.fetch_user(int(author_id))
    channel = await get_logging_channel(interaction, self)
    if channel:
        image_file = File("Images/settings_icon.png", filename="settings_icon.png")
        log_entry_embed = discord.Embed(title="Server config action!", description="Someone has made a changed a server config setting for The Holly Roller!", color=discord.Color.from_rgb(140,27,27))
        log_entry_embed.add_field(name="", value=f"**{What}** **{Type}** was changed to **{To}**")
        log_entry_embed.set_thumbnail(url="attachment://settings_icon.png") 
        if Type == "attachment":
            log_entry_embed.set_image(url=To)
        log_entry_embed.set_footer(text=f"Action made by: {author_name} ({author_id}).\nUTC: {current_time()}")
        await channel.send(file=image_file, embed=log_entry_embed)
    else:
        return

class settings(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.pool = bot.pool

    group = app_commands.Group(name="settings", description="configure settings")
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
        print("---|settings   cog loaded!|---", current_time())

# settings channels #FIXME
    
    @group.command(name="channels", description="Configure channels")
    @app_commands.checks.has_permissions(administrator = True)
    async def channels(self, interaction: discord.Interaction, channel_type: typing.Literal["Logging/Logs","Welcome","Goodbye"], channel: discord.TextChannel):
        if channel_type == "Logging/Logs":
            await self.pool.execute('INSERT INTO info (guild_id, log_id) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET log_id = $2', interaction.guild.id, channel.id)
            await interaction.response.send_message(f"**Logging channel** was changed to {channel.mention}")
            What = "Logging/Logs" 
            Type = "channel"
            To = channel.mention
            await log_entry(self, interaction, What, Type, To)

        elif channel_type == "Welcome":
            await self.pool.execute('INSERT INTO info (guild_id, wlc_id) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET wlc_id = $2', interaction.guild.id, channel.id)
            await interaction.response.send_message(f"**Welcome channel** was changed to {channel.mention}")
            What = "Welcome"
            Type = "channel"
            To = channel.mention
            await log_entry(self, interaction, What, Type, To)

        elif channel_type == "Goodbye":
            await self.pool.execute('INSERT INTO info (guild_id, bye_id) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET bye_id = $2', interaction.guild.id, channel.id)
            await interaction.response.send_message(f"**Goodbye channel** was changed to {channel.mention}")
            What = "Goodbye"
            Type = "channel"
            To = channel.mention
            await log_entry(self, interaction, What, Type, To)

# settings message #FIXME

    @group.command(name="messages", description="Configure your welcome and goodbye messages")
    @app_commands.checks.has_permissions(administrator = True)
    async def messages(self, interaction: discord.Interaction, message: typing.Literal["Welcome","Goodbye"], setting: typing.Literal["Attachment", "Title", "Message", "Color"], input: str):
        if message == "Welcome":
            media_link = input
            text = input
            rgb = input
            if setting == "Attachment":
                await self.pool.execute('INSERT INTO info (guild_id, wlc_pic) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET wlc_pic = $2', interaction.guild.id, media_link)  
                await interaction.response.send_message(f"**Welcome image** was changed to {media_link}")
                What = "Welcome" 
                Type = "attachment"
                To = media_link
                await log_entry(self, interaction, What, Type, To)
            elif setting == "Title":
                await self.pool.execute('INSERT INTO info (guild_id, wlc_title) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET wlc_title = $2', interaction.guild.id, text)
                await interaction.response.send_message(f"**Welcome image** was changed to {text}")
                What = "Welcome" 
                Type = "title"
                To = text
                await log_entry(self, interaction, What, Type, To)
            elif setting == "Message":
                await self.pool.execute('INSERT INTO info (guild_id, wlc_msg) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET wlc_msg = $2', interaction.guild.id, media_link)
                await interaction.response.send_message(f"**Welcome message** was changed to {text}")
                What = "Welcome" 
                Type = "message"
                To = text
                await log_entry(self, interaction, What, Type, To)
            elif setting == "Color": #TODO Make hex compatible
                await self.pool.execute('INSERT INTO info (guild_id, wlc_rgb) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET wlc_rgb = $2', interaction.guild.id, rgb)
                await interaction.response.send_message(f"**Welcome embed color** was changed to {rgb}")
                What = "Welcome" 
                Type = "embed color"
                To = rgb
                await log_entry(self, interaction, What, Type, To)

        elif message == "Goodbye":
            media_link = input
            text = input
            rgb = input
            if setting == "Attachment":
                await self.pool.execute('INSERT INTO info (guild_id, bye_pic) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET bye_pic = $2', interaction.guild.id, media_link)
                await interaction.response.send_message(f"**Goodbye image** was changed to {media_link}")
                What = "Goodbye" 
                Type = "attachment"
                To = media_link
                await log_entry(self, interaction, What, Type, To)
            elif setting == "Title":
                await self.pool.execute('INSERT INTO info (guild_id, bye_title) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET bye_title = $2', interaction.guild.id, text)
                await interaction.response.send_message(f"**Goodbye image** was changed to {text}")
                What = "Goodbye" 
                Type = "title"
                To = text
                await log_entry(self, interaction, What, Type, To)
            elif setting == "Message":
                await self.pool.execute('INSERT INTO info (guild_id, bye_msg) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET bye_msg = $2', interaction.guild.id, media_link)
                await interaction.response.send_message(f"**Goodbye message** was changed to {text}")
                What = "Goodbye" 
                Type = "message"
                To = text
                await log_entry(self, interaction, What, Type, To)
            elif setting == "Color":
                await self.pool.execute('INSERT INTO info (guild_id, bye_rgb) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET bye_rgb = $2', interaction.guild.id, rgb)
                await interaction.response.send_message(f"**Goodbye embed color** was changed to {rgb}")
                What = "Goodbye" 
                Type = "embed color"
                To = rgb
                await log_entry(self, interaction, What, Type, To)

# settings show #FIXME

    @group.command(name="show", description="Show current settings for the server")
    @app_commands.checks.has_permissions(administrator = True)
    async def show(self, interaction: discord.Interaction):
        setup_channels = 0
        setup_pics = 0
        #Log channel
        log_id_record = await self.pool.fetchrow('SELECT log_id FROM info WHERE guild_id = $1', interaction.guild.id)
        try:
            log_id = log_id_record["log_id"]
            log_channel = await interaction.client.fetch_channel(log_id)
            setup_channels += 1
        except:
            log_channel = False
        #Welcome channel
        wlc_id_record = await self.pool.fetchrow('SELECT wlc_id FROM info WHERE guild_id = $1', interaction.guild.id)
        try:
            wlc_id = wlc_id_record["wlc_id"]
            wlc_channel = await interaction.client.fetch_channel(wlc_id)
            setup_channels += 1
        except:
            wlc_channel = False
        #Goodbye channel
        bye_id_record = await self.pool.fetchrow('SELECT bye_id FROM info WHERE guild_id = $1', interaction.guild.id)
        try:
            bye_id = bye_id_record["bye_id"]
            bye_channel = await interaction.client.fetch_channel(bye_id)
            setup_channels += 1
        except:
            bye_channel = False
        #Welcome attachment
        wlc_pic_record = await self.pool.fetchrow('SELECT wlc_pic FROM info WHERE guild_id = $1', interaction.guild.id)
        try:
            wlc_pic = wlc_pic_record["wlc_pic"]
            setup_pics += 1
        except:
            wlc_pic = False
        #Goodbye attachment
        bye_pic_record = await self.pool.fetchrow('SELECT bye_pic FROM info WHERE guild_id = $1', interaction.guild.id)
        try:
            bye_pic = bye_pic_record["bye_pic"]
            setup_pics += 1
        except:
            bye_pic = False
        #Embed
        show_embed = discord.Embed(title="Server settings", color=discord.Color.from_rgb(41,134,0))
        if setup_channels > 0:
            if log_channel == False:
                show_embed.add_field(name="Logging channel:", value="**Not set**", inline=False)
            else:
                show_embed.add_field(name="Logging channel:", value=log_channel.mention, inline=False)

            if wlc_channel == False:
                show_embed.add_field(name="Welcome channel:", value="**Not set**", inline=False)
            else:
                show_embed.add_field(name="Welcome channel:", value=wlc_channel.mention, inline=False)

            if bye_channel == False:
                show_embed.add_field(name="Goodbye channel:", value="**Not set**", inline=False)
            else:
                show_embed.add_field(name="Goodbye channel:", value=bye_channel.mention, inline=False)
        else:
            show_embed.add_field(name="No channels have been set", value='Please run "/settings channels" to finish setting up your channels', inline=False)

        if setup_pics > 0:           
            if wlc_pic == False:
                show_embed.add_field(name="Welcome attachment:", value="**Not set**", inline=False)
            else:
                show_embed.add_field(name="Welcome attachment:", value=wlc_pic, inline=False)

            if bye_pic == False:
                show_embed.add_field(name="Goodbye attachment:", value="**Not set**", inline=False)
            else:
                show_embed.add_field(name="Goodbye attachment:", value=bye_pic, inline=False)
        else:
            show_embed.add_field(name="No attachments have been set", value='Please run "/settings attachments" to finish setting up your attachments.', inline=False)
        #Embed send
        show_embed.set_footer(text=f"{setup_channels}/3 channels set\n{setup_pics}/2 attachments set\nUTC: {current_time()}")
        await interaction.response.send_message(embed=show_embed)

# settings help #FIXME

    @group.command(name="help", description="Instructions on how to use the /settings commands.")
    async def settings_help(self, interaction: discord.Interaction):
        file1 = discord.File('Images/Holly_Roller_pfp.png')
        file2 = discord.File('Images/LDL_pfp.png')
        embed = discord.Embed(title="Help", description="This is a list of different commands and what they do.\n**Note that all settings except the RGB values has to be set up for the welcome/goodbye messages to send.**", color=660091)
        embed.set_author(name="Local Drug Lord", icon_url='attachment://LDL_pfp.png')
        embed.set_thumbnail(url='attachment://Holly_Roller_pfp.png')
        embed.add_field(name="**---| channel    |---**", value= "", inline=False)
        embed.add_field(name="*/Settings channel*", value="This command is used to change what channels does what. \nCurrent options are:", inline=False)
        embed.add_field(name="*/Settings show*", value="Show the servers current channel config", inline=False)
        embed.add_field(name="*Logging/Logs*", value= "This is what channel to use for keeping logs.", inline=False)
        embed.add_field(name="*Welcome*", value= "This is what channel to use for the welcome message.", inline=False)
        embed.add_field(name="*Goodbye*", value= "This is what channel to use for the goodbye message.", inline=False)

        embed.add_field(name="**---| messages   |---**", value= "", inline=False)
        embed.add_field(name="*/Settings messages*", value="Configure the welcome and goodbye embed messages. \nCurrent settings are:", inline=False)
        embed.add_field(name="*Attachment*", value= "This is the image you want to send in the message.\n(This should be in the form of a url/media link)", inline=False)
        embed.add_field(name="*Title*", value= "This is the title for your embed message.", inline=False)
        embed.add_field(name="*Message*", value= 'This is the content of the message, for help with formatting look at "Formatting" section.', inline=False)
        embed.add_field(name="*Color*", value= "This is what color should be used for the embed.\n**Note: This should be in the rgb format, please ensure that you separate the values with a comma.(R,G,B)**", inline=True)

        embed.add_field(name="**---| Formatting |---**", value= "", inline=False)
        embed.add_field(name="*This is a small tutorial on how to format your messages*", value="", inline=False)
        embed.add_field(name="", value='**{user}** or **{member}**:\nThese placeholders insert the username of the person joining/leaving\n(e.g., "Hello {user}!" becomes "Hello discord_user123!").', inline=False)
        embed.add_field(name="", value='**{mention}**:\nThis inserts a mention of the user, including the "@" symbol\n(e.g., "Hello {mention}!" becomes "Hello @discord_user123!").', inline=False)
        embed.add_field(name="", value='**{server}**:\nThis inserts the name of the server the user joined/left\n(e.g., "Welcome to {server}!" becomes "Welcome to Cool Chat").', inline=False)

        embed.set_footer(text=f"UTC: {current_time()}")
        await interaction.response.send_message(files=[file1, file2], embed=embed)

# Errors #FIXME

    @channels.error
    async def channels_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CommandInvokeError):
            await interaction.response.send_message("!!ERROR!! Please contact <@1184901953885585490>", ephemeral=True)
            print("----!!!!----")
            raise error
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("You don't have permissions to do that :)", ephemeral=True)    
    
    @messages.error
    async def messages_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CommandInvokeError):
            await interaction.response.send_message("!!ERROR!! Please contact <@1184901953885585490>", ephemeral=True)
            print("----!!!!----")
            raise error
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("You don't have permissions to do that :)", ephemeral=True)   

    @show.error
    async def show_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CommandInvokeError):
            await interaction.response.send_message("!!ERROR!! Please contact <@1184901953885585490>", ephemeral=True)
            print("----!!!!----")
            raise error

async def setup(bot):
  await bot.add_cog(settings(bot))