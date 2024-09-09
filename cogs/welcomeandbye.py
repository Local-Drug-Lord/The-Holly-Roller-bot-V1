import discord
from discord import app_commands, File
from discord.ext import commands
from datetime import datetime, timezone

#FIXME Convert to hex

#time
def current_time ():
    now = datetime.now(timezone.utc)
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time

async def get_welcome(guild_id, welcome, Type, member, guild_name):
    if Type == "channel":
        welcome_channel = await welcome.pool.fetchrow('SELECT wlc_id FROM info WHERE guild_id = $1', guild_id)
        try:
            wlc_id = welcome_channel["wlc_id"]
            welcome_channel = await welcome.bot.fetch_channel(wlc_id)
        except:
            welcome_channel = False
        return welcome_channel
    elif Type == "title":
        welcome_title = await welcome.pool.fetchrow('SELECT wlc_title FROM info WHERE guild_id = $1', guild_id)
        try:
            wlc_title = welcome_title["wlc_title"]
            welcome_title = wlc_title
        except:
            welcome_title = False
        return welcome_title
    elif Type == "rgb":
        welcome_rgb = await welcome.pool.fetchrow('SELECT wlc_rgb FROM info WHERE guild_id = $1', guild_id)
        wlc_rgb = welcome_rgb["wlc_rgb"]
        if wlc_rgb is None:
            welcome_rgb = discord.Color.from_rgb(1, 134, 0)
        else:
            rgb_string = welcome_rgb["wlc_rgb"]
            r, g, b = rgb_string.split(",")
            r = int(r)
            g = int(g)
            b = int(b)
            welcome_rgb = discord.Color.from_rgb(r, g, b)
        return welcome_rgb
    elif Type == "message":
        welcome_message = await welcome.pool.fetchrow('SELECT wlc_msg FROM info WHERE guild_id = $1', guild_id)
        try:
            wlc_msg = welcome_message["wlc_msg"]
            welcome_message = wlc_msg.format(user=member, mention=member.mention, server=guild_name)
        except:
            welcome_message = False
        return welcome_message
    elif Type == "image":
        welcome_image = await welcome.pool.fetchrow('SELECT wlc_pic FROM info WHERE guild_id = $1', guild_id)
        try:
            wlc_pic = welcome_image["wlc_pic"]
            welcome_image = wlc_pic
        except:
            welcome_image = False
        return welcome_image

async def get_goodbye(guild_id, goodbye, Type, member, guild_name):
    if Type == "channel":
        goodbye_channel = await goodbye.pool.fetchrow('SELECT bye_id FROM info WHERE guild_id = $1', guild_id)
        try:
            bye_id = goodbye_channel["bye_id"]
            goodbye_channel = await goodbye.bot.fetch_channel(bye_id)
        except:
            goodbye_channel = False
        return goodbye_channel
    elif Type == "title":
        goodbye_title = await goodbye.pool.fetchrow('SELECT bye_title FROM info WHERE guild_id = $1', guild_id)
        try:
            bye_title = goodbye_title["bye_title"]
            goodbye_title = bye_title
        except:
            goodbye_title = False
        return goodbye_title
    elif Type == "rgb":
        goodbye_rgb = await goodbye.pool.fetchrow('SELECT bye_rgb FROM info WHERE guild_id = $1', guild_id)
        bye_rgb = goodbye_rgb["bye_rgb"]
        if bye_rgb is None:
            goodbye_rgb = discord.Color.from_rgb(1, 134, 0)
        else:
            rgb_string = goodbye_rgb["bye_rgb"]
            r, g, b = rgb_string.split(",")
            r = int(r)
            g = int(g)
            b = int(b)
            goodbye_rgb = discord.Color.from_rgb(r, g, b)
        return goodbye_rgb
    elif Type == "message":
        goodbye_message = await goodbye.pool.fetchrow('SELECT bye_msg FROM info WHERE guild_id = $1', guild_id)
        try:
            bye_msg = goodbye_message["bye_msg"]
            goodbye_message = bye_msg.format(user=member, mention=member.mention, server=guild_name)
        except:
            goodbye_message = False
        return goodbye_message
    elif Type == "image":
        goodbye_image = await goodbye.pool.fetchrow('SELECT bye_pic FROM info WHERE guild_id = $1', guild_id)
        try:
            bye_pic = goodbye_image["bye_pic"]
            goodbye_image = bye_pic
        except:
            goodbye_image = False
        return goodbye_image
    
async def kick_on_join(join, member, guild_name):
    channel = await join.bot.fetch_channel(1246495926173040671)
    channel_2 = await join.bot.fetch_channel(1064732487231737896)
    reason = "being blackberry or being related to him"
    await member.kick(reason="User was flagged as being blackberry or being related to him")
    image_file = File("Images/moderation_icon.png", filename="moderation_icon.png")
    ban_embed = discord.Embed(title="Moderation action!", color=discord.Color.from_rgb(140,27,27))
    ban_embed.add_field(name="", value= f'User **{member}** was banned for **{reason}** by **"Anti Jackson Filter"**.', inline=False)
    ban_embed.set_thumbnail(url="attachment://moderation_icon.png")
    ban_embed.add_field(name="", value= f"User ID: **{member.id}**")
    ban_embed.set_footer(text=f"UTC: {current_time()}")
    await channel.send(file=image_file, embed=ban_embed)
    await channel_2.send("@everyone\n:rotating_light: Jackson/Blackberry or James has tried to join the server")

class greetings(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.pool = bot.pool
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
        print("---|greetings cog loaded!|---", current_time())

    @commands.Cog.listener()
    async def on_member_join(self, member):
        positive_return = 0
        guild_id = member.guild.id
        guild_name = member.guild
        Type = "channel"
        channel = await get_welcome(guild_id, self, Type, member, guild_name)
        join = self
        #if member.id == 751126644412121258 or 1225093203989106773 or 1139355142152532059:
        #    await kick_on_join(join, member, guild_name)
        #elif member == "blackberry001" or "blackberry08596" or "james340134":
        #    await kick_on_join(join, member, guild_name)
        #else:
        if channel:
            Type = "title"
            title = await get_welcome(guild_id, self, Type, member, guild_name)

            Type = "rgb"
            rgb = await get_welcome(guild_id, self, Type, member, guild_name)

            Type = "message"
            message = await get_welcome(guild_id, self, Type, member, guild_name)

            Type = "image"
            image = await get_welcome(guild_id, self, Type, member, guild_name)

            if message or title or image:
                if title:
                    welcome_embed = discord.Embed(title=title, color=rgb)
                else:
                    welcome_embed = discord.Embed(title="", color=rgb)      
                if message:
                    welcome_embed.add_field(name="", value=message, inline=True)
                if image:
                    welcome_embed.set_image(url=image)
                welcome_embed.set_footer(text=f"{member} ({member.id})\nUTC: {current_time()}")
                await channel.send(embed=welcome_embed)
                await channel.send(member.mention, delete_after=0)
            
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        positive_return = 0
        guild_id = member.guild.id
        guild_name = member.guild
        Type = "channel"
        channel = await get_goodbye(guild_id, self, Type, member, guild_name)
        if channel == False:
            return  
        else:
            Type = "title"
            title = await get_goodbye(guild_id, self, Type, member, guild_name)

            Type = "rgb"
            rgb = await get_goodbye(guild_id, self, Type, member, guild_name)

            Type = "message"
            message = await get_goodbye(guild_id, self, Type, member, guild_name)

            Type = "image"
            image = await get_goodbye(guild_id, self, Type, member, guild_name)

            if message or title or image:
                if title:
                    goodbye_embed = discord.Embed(title=title, color=rgb)
                else:
                    goodbye_embed = discord.Embed(title="", color=rgb)
                if message:
                    goodbye_embed.add_field(name="", value=f"" + message, inline=True)
                if image:
                    goodbye_embed.set_image(url=image)
                goodbye_embed.set_footer(text=f"{member} ({member.id})\nUTC: {current_time()}")
                await channel.send(embed=goodbye_embed)
                await channel.send(member.mention, delete_after=0)

async def setup(bot):
  await bot.add_cog(greetings(bot))