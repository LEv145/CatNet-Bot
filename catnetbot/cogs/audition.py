from datetime import datetime

import discord
from discord.ext import commands

import toml_config


conf = toml_config.load_config()


SUCCESS_LINE = conf["messages"]["errors"]["success_line"]["emoji"] * conf["messages"]["errors"]["success_line"]["repeat"] + "\n "
SUCCESS_COLOR = conf["messages"]["errors"]["success_line"]["color"]

STANDART_LINE = conf["messages"]["errors"]["standard_line"]["emoji"] * conf["messages"]["errors"]["standard_line"]["repeat"] + "\n "
STANDART_COLOR = conf["messages"]["errors"]["standard_line"]["color"]

ERROR_LINE = conf["messages"]["errors"]["error_line"]["emoji"] * conf["messages"]["errors"]["error_line"]["repeat"] + "\n "
ERROR_COLOR = conf["messages"]["errors"]["error_line"]["color"]

INVISIBLE_SYMBOL = conf["messages"]["errors"]["invisible_symbol"]

LOGS_CHANNEL_ID = conf["bot"]["logs_channel_id"]

class Audition(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        emb = discord.Embed(color = ERROR_COLOR, timestamp = datetime.now())
        emb.add_field(name = "Сообщение:", value = f"```{message.content[:1000]}```")
        emb.add_field(name = f"{INVISIBLE_SYMBOL}", value = f"{ERROR_LINE}", inline = False)
        emb.add_field(name = "ID сообщения:", value = f"{message.id}")
        emb.add_field(name = "Автор сообщения:", value = f"{message.author}", inline = False)
        emb.add_field(name = "Канал сообщения:", value = f"{message.channel}")
        logs_channel = message.guild.get_channel(LOGS_CHANNEL_ID)
        await logs_channel.send(embed = emb)

def setup(bot):
    bot.add_cog(Audition(bot))

    
