from datetime import datetime

import discord
from discord.ext import commands

import toml_config


conf = toml_config.load_config()
permissions_config = toml_config.load_config()["discord"]
on_off_dict = conf["on_off_dict"]

SUCCESS_LINE = conf["messages"]["errors"]["success_line"]["emoji"] * conf["messages"]["errors"]["success_line"]["repeat"] + "\n "
SUCCESS_COLOR = conf["messages"]["errors"]["success_line"]["color"]

STANDART_LINE = conf["messages"]["errors"]["standard_line"]["emoji"] * conf["messages"]["errors"]["standard_line"]["repeat"] + "\n "
STANDART_COLOR = conf["messages"]["errors"]["standard_line"]["color"]

ERROR_LINE = conf["messages"]["errors"]["error_line"]["emoji"] * conf["messages"]["errors"]["error_line"]["repeat"] + "\n "
ERROR_COLOR = conf["messages"]["errors"]["error_line"]["color"]

INVISIBLE_SYMBOL = conf["messages"]["errors"]["invisible_symbol"]

LOGS_CHANNEL_ID = conf["bot"]["logs_channel_id"]


async def role_audition_info(role, type_of_audition_color, type_of_audition_line):
    """
    функция для оповещения об удалении/создании роли на сервере

    :param role: роль о которой сообщается
    :param type_of_audition_color: цвет эмбеда
    :param type_of_audition_line: линии для эмбеда
    :return: информация о роли
    """
    emb = discord.Embed(color = type_of_audition_color, timestamp = datetime.now())
    emb.add_field(name = "Роль:", value = f"{role.mention}")
    emb.add_field(name = "Имя роли:", value = f"{role.name}", inline = False)
    emb.add_field(name = "ID роли:", value = f"{role.id}")
    emb.add_field(name = "Цвет роли:", value = f"{role.color}", inline = False)
    emb.add_field(name = f"{INVISIBLE_SYMBOL}", value = f"{type_of_audition_line}", inline = False)
    emb.add_field(name = "Права роли:", value = "\n".join(
            permissions_config[f"{perm}"] for perm, boolean in role.permissions if boolean is True))
    emb.add_field(name = f"{INVISIBLE_SYMBOL}", value = f"{type_of_audition_line}", inline = False)
    emb.add_field(name = "Позиция роли:", value = f"{role.position} позиция")
    emb.add_field(name = "Возможность упоминания для всех:", value = f"{on_off_dict[f'{role.mentionable}']}",
                  inline = False)
    emb.add_field(name = "Управление интеграциями:", value = f"{on_off_dict[f'{role.managed}']}")
    emb.add_field(name = "Отдельное отображение:", value = f"{on_off_dict[f'{role.hoist}']}", inline = False)
    logs_channel = role.guild.get_channel(LOGS_CHANNEL_ID)
    await logs_channel.send(embed = emb)


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

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.bot:
            return
        emb = discord.Embed(color = STANDART_COLOR, timestamp = datetime.now())
        emb.add_field(name = "Сообщение до:", value = f"```{before.content[:1000]}```", inline = False)
        emb.add_field(name = "Сообщение после:", value = f"```{after.content[:1000]}```")
        emb.add_field(name = f"{INVISIBLE_SYMBOL}", value = f"{STANDART_LINE}", inline = False)
        emb.add_field(name = "ID сообщения:", value = f"{after.id}")
        emb.add_field(name = "Автор сообщения:", value = f"{after.author}", inline = False)
        emb.add_field(name = "Канал сообщения:", value = f"[{after.channel}]({after.jump_url})")
        logs_channel = after.guild.get_channel(LOGS_CHANNEL_ID)
        await logs_channel.send(embed = emb)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        await role_audition_info(role, SUCCESS_COLOR, SUCCESS_LINE)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        await role_audition_info(role, ERROR_COLOR, ERROR_LINE)


def setup(bot):
    bot.add_cog(Audition(bot))

