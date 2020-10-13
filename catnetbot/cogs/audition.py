from datetime import datetime

import discord
from discord.ext import commands

import toml_config


conf = toml_config.load_config()
permissions_config = toml_config.load_config()["discord"]
on_off_dict = conf["on_off_dict"]
channels_type_dict = conf["channels_type_dict"]

SUCCESS_LINE = conf["messages"]["errors"]["success_line"]["emoji"] * conf["messages"]["errors"]["success_line"]["repeat"] + "\n "
SUCCESS_COLOR = conf["messages"]["errors"]["success_line"]["color"]

STANDART_LINE = conf["messages"]["errors"]["standard_line"]["emoji"] * conf["messages"]["errors"]["standard_line"]["repeat"] + "\n "
STANDART_COLOR = conf["messages"]["errors"]["standard_line"]["color"]

ERROR_LINE = conf["messages"]["errors"]["error_line"]["emoji"] * conf["messages"]["errors"]["error_line"]["repeat"] + "\n "
ERROR_COLOR = conf["messages"]["errors"]["error_line"]["color"]

INVISIBLE_SYMBOL = conf["messages"]["errors"]["invisible_symbol"]

LOGS_CHANNEL_ID = conf["bot"]["logs_channel_id"]


async def role_audition_info(role, type_of_audition_color, type_of_audition_line) -> None:
    """
    функция для оповещения об удалении или создании роли на сервере

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
    emb.add_field(name = "Дополнительно:", value = f"""Позиция: {role.position} в списке
                                                    Возможность упоминания для всех: {on_off_dict[f'{role.mentionable}']}
                                                    Управление интеграциями: {on_off_dict[f'{role.managed}']}
                                                    Отдельное отображение : {on_off_dict[f'{role.hoist}']}
                                                    """)
    logs_channel = role.guild.get_channel(LOGS_CHANNEL_ID)
    await logs_channel.send(embed = emb)


async def role_updating_info(before: discord.Role, after: discord.Role) -> None:
    """
    функция для оповещения об обновлении роли на сервере

    :param before: роль паньше
    :param after: роль после
    :return: информация об обновлённой роли
    """

    emb = discord.Embed(color = STANDART_COLOR, timestamp = datetime.now())
    emb.add_field(name = "Роль:", value = f"{after.mention}", inline = False)
    emb.add_field(name = "ID роли:", value = f"{after.id}", inline = False)
    emb.add_field(name = f"{INVISIBLE_SYMBOL}", value = f"{STANDART_LINE}", inline = False)

    before_permissions = [perm for perm, boolean in before.permissions if boolean]
    after_permissions = [perm for perm, boolean in after.permissions if boolean]

    added_permissions = [permissions_config[f'{perm}'] for perm in after_permissions if perm not in before_permissions]
    deleted_permissions = [permissions_config[f'{perm}'] for perm in before_permissions if perm not in after_permissions]

    if added_permissions or deleted_permissions:
        if added_permissions:
            emb.add_field(name = "Добавленные права:", value = "\n".join(added_permissions), inline = False)
        if deleted_permissions:
            emb.add_field(name = "Удалённые права:", value = "\n".join(deleted_permissions), inline = False)
        emb.add_field(name = f"{INVISIBLE_SYMBOL}", value = f"{STANDART_LINE}", inline = False)

    emb.add_field(name = "Дополнительно (раньше):", value = f"""
                                                        Название: {before.name}
                                                        Цвет: {before.color}
                                                        Позиция: {before.position} в списке
                                                        Возможность упоминания для всех: {on_off_dict[f'{before.mentionable}']}
                                                        Управление интеграциями: {on_off_dict[f'{before.managed}']}
                                                        Отдельное отображение: {on_off_dict[f'{before.hoist}']}
                                                        """, inline = False)
    emb.add_field(name = "Дополнительно (сейчас):", value = f"""
                                                        Название: {after.name}
                                                        Цвет: {after.color}
                                                        Позиция: {after.position} в списке 
                                                        Возможность упоминания для всех: {on_off_dict[f'{after.mentionable}']}
                                                        Управление интеграциями: {on_off_dict[f'{after.managed}']}
                                                        Отдельное отображение : {on_off_dict[f'{after.hoist}']}
                                                        """, inline = False)
    logs_channel = after.guild.get_channel(LOGS_CHANNEL_ID)
    await logs_channel.send(embed = emb)


async def channel_audition_info(channel, type_of_audition_color, type_of_audition_line) -> None:
    """
    функция для оповещения об удалении/создании канала на сервере

    :param channel: канал о котором сообщается
    :param type_of_audition_color: цвет эмбеда
    :param type_of_audition_line: линии для эмбеда
    :return: информация о канале
    """

    emb = discord.Embed(color = type_of_audition_color, timestamp = datetime.now())

    if isinstance(channel, discord.TextChannel):
        emb.add_field(name = f"{channels_type_dict[f'{channel.type}']} Канал:", value = f"{channel.name}")
        emb.add_field(name = "ID канала:", value = f"{channel.id}", inline = False)
        emb.add_field(name = f"{INVISIBLE_SYMBOL}", value = f"{type_of_audition_line}", inline = False)
        if channel.category:
            emb.add_field(name = f"Категория:", value = f"{channel.category}")
        emb.add_field(name = f"Дополнительно:", value = f"Позиция: {channel.position}", inline = False)
        logs_channel = channel.guild.get_channel(LOGS_CHANNEL_ID)
        await logs_channel.send(embed = emb)

    elif isinstance(channel, discord.VoiceChannel):
        emb.add_field(name = f"{channels_type_dict[f'{channel.type}']} Канал:", value = f"{channel.name}")
        emb.add_field(name = "ID канала:", value = f"{channel.id}", inline = False)
        emb.add_field(name = f"{INVISIBLE_SYMBOL}", value = f"{type_of_audition_line}", inline = False)
        if channel.category:
            emb.add_field(name = "Категория:", value = f"{channel.category}")
        emb.add_field(name = f"Дополнительно:", value = f"""Позиция: {channel.position}
                                                            Битрейт: {channel.bitrate}
                                                            Лимит участников: {channel.user_limit}""", inline = False)
        logs_channel = channel.guild.get_channel(LOGS_CHANNEL_ID)
        await logs_channel.send(embed = emb)


async def emoji_audition_info(emoji, type_of_audition_color, type_of_audition_line) -> None:

    emb = discord.Embed(color = type_of_audition_color, timestamp = datetime.now())
    emb.add_field(name = "Эмодзи:", value = f"{emoji}")
    emb.add_field(name = "Название эмодзи:", value = f"{emoji.name}")
    emb.add_field(name = "ID эмодзи:", value = f"{emoji.id}")
    emb.add_field(name = f"{INVISIBLE_SYMBOL}", value = f"{type_of_audition_line}", inline = False)
    emb.add_field(name = "Дополнительно:", value = f"""Создал: {emoji.user}
                                                       Управление интеграцией: {on_off_dict[f'{emoji.managed}']} 
                                                        Анимация: {on_off_dict[f'{emoji.animated}']}
                                                        [URL эмодзи]({emoji.url})    
                                                    """)
    logs_channel = emoji.guild.get_channel(LOGS_CHANNEL_ID)
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
    async def on_guild_role_update(self, before, after):
        await role_updating_info(before, after)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        await role_audition_info(role, ERROR_COLOR, ERROR_LINE)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        await channel_audition_info(channel, SUCCESS_COLOR, SUCCESS_LINE)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        await channel_audition_info(channel, ERROR_COLOR, ERROR_LINE)


def setup(bot):
    bot.add_cog(Audition(bot))

