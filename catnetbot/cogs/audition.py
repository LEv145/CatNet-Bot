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


class Audition(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



def setup(bot):
    bot.add_cog(Audition(bot))

    
