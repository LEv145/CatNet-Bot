import datetime

import discord
from discord.ext import commands, tasks
import peewee

import toml_config
import models
from errors import UserIsPunished, UserIsNotPunished

db = peewee.SqliteDatabase('catnet.db')

models.Punishment.create_table()

conf = toml_config.load_config()

SUCCESS_LINE = conf["messages"]["errors"]["success_line"]["emoji"] * conf["messages"]["errors"]["success_line"]["repeat"] + "\n "
SUCCESS_COLOR = conf["messages"]["errors"]["success_line"]["color"]

STANDART_LINE = conf["messages"]["errors"]["standard_line"]["emoji"] * conf["messages"]["errors"]["standard_line"]["repeat"] + "\n "
STANDART_COLOR = conf["messages"]["errors"]["standard_line"]["color"]

ERROR_LINE = conf["messages"]["errors"]["error_line"]["emoji"] * conf["messages"]["errors"]["error_line"]["repeat"] + "\n "
ERROR_COLOR = conf["messages"]["errors"]["error_line"]["color"]

INVISIBLE_SYMBOL = conf["messages"]["errors"]["invisible_symbol"]

HOUR_FORMAT_TUPLE = ("hours", "hour", "h", "часов", "час", "ч")
MINUTE_FORMAT_TUPLE = ("minutes", "minute", "min", "m", "минуты", "минут", "мин", "м")
HOUR = 60

MUTE_ROLE_ID = conf["discord"]["mute_role_id"]

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mute_expiry.start()
        
    @commands.command(
            name = "кик",
            aliases = ["kick", "выгнать", "кикнуть"],
            brief = "Выгнать участника с сервера",
            description = "Команда для того, чтобы выгнать участника с сервера",
            usage = "кик [участник] (причина)",
    )
    @commands.has_permissions(kick_members = True)
    async def moderation_command_kick(self, ctx, member: discord.Member, reason = "Не указана"):

        await member.kick()
        emb = discord.Embed(color = SUCCESS_COLOR)
        emb.add_field(name = "Выгнан:", value = f"{member}")
        emb.add_field(name = "Выгнал:", value = f"{ctx.author.mention}")
        emb.add_field(name = f"{INVISIBLE_SYMBOL}", value = f"{SUCCESS_LINE}", inline = False)
        emb.add_field(name = "Причина:", value = f"{reason}")
        await ctx.send(embed = emb)

    @commands.command(
            name = "бан",
            aliases = ["ban", "блокировать", "забанить"],
            brief = "Забанить участника на сервере",
            description = "Команда для того, чтобы участник был заблокирован на сервере",
            usage = "бан [участник] (причина)",
    )
    @commands.has_permissions(ban_members = True)
    async def moderation_command_ban(self, ctx, member: discord.Member, reason = "Не указана"):

        await member.ban(reason = reason + f" ({ctx.author.name})")
        emb = discord.Embed(color = SUCCESS_COLOR)
        emb.add_field(name = "Забанен:", value = f"{member}")
        emb.add_field(name = "Забанил:", value = f"{ctx.author.mention}")
        emb.add_field(name = f"{INVISIBLE_SYMBOL}", value = f"{SUCCESS_LINE}", inline = False)
        emb.add_field(name = "Причина:", value = f"{reason}")
        await ctx.send(embed = emb)

    @commands.command(
            name = "мьют",
            aliases = ["мут", "mute", "молчанка"],
            brief = "Замьютить участника сервера",
            description = "Команда для того, чтобы участник не мог писать и говорить на сервере",
            usage = "мьют [участник] [время] [формат времени] (причина)",
    )
    @commands.has_permissions(manage_messages = True)
    async def moderation_command_mute(self, ctx, member: discord.Member, duration: int, duration_format: str, *, reason: str = "Не указана"):
        if models.Punishment.select().where(models.Punishment.punished_id == member.id):
            punishment_info = models.Punishment.get(models.Punishment.punished_id == member.id)
            punishment_timedelta = punishment_info.punishment_until - datetime.datetime.now()
            raise UserIsPunished(punishment_timedelta.total_seconds())
        else:
            MUTE_ROLE = discord.utils.get(ctx.guild.roles, id=MUTE_ROLE_ID)
            now = datetime.datetime.now()

            if duration_format.lower() in HOUR_FORMAT_TUPLE:
                until = now.replace(hour = now.hour + duration)
            elif duration_format.lower() in MINUTE_FORMAT_TUPLE:
                until = now.replace(minute = now.minute + duration)


            await member.add_roles(MUTE_ROLE)
            models.Punishment(punished_id = member.id, moderator_id = ctx.author.id, punishment_until = until, punishment_reason = reason).save()
            emb = discord.Embed(color = SUCCESS_COLOR)
            emb.add_field(name = "Замьючен:", value = f"{member}")
            emb.add_field(name = "Замьютил:", value = f"{ctx.author.mention}")
            emb.add_field(name = f"{INVISIBLE_SYMBOL}", value = f"{SUCCESS_LINE}", inline = False)
            emb.add_field(name = "Причина:", value = f"{reason}")
            emb.add_field(name = "Время:", value = f"{duration} {duration_format}")
            await ctx.send(embed = emb)


    @tasks.loop(minutes = 1)
    async def mute_expiry(self):
        catnet = self.bot.get_guild(636658861209813000)
        MUTE_ROLE = discord.utils.get(catnet.roles, id = MUTE_ROLE_ID)
        for punishment in models.Punishment.select().where(models.Punishment.punishment_until <= datetime.datetime.now()):
            punishment_info = catnet.get_member(punishment.punished_id)
            await punishment_info.remove_roles(MUTE_ROLE)
            punishment.delete_instance()

    @commands.command(
            name = "размьют",
            aliases = ["unmute", "размут"],
            description = "Снять с человека мьют",
            usage = "размьют [участник] (причина)"
    )
    async def moderation_command_unmute(self, ctx, member: discord.Member, *, reason: str = "Не указана"):
        if models.Punishment.select().where(models.Punishment.punished_id == member.id):
            punishment_info = models.Punishment.get(models.Punishment.punished_id == member.id)
            MUTE_ROLE = discord.utils.get(ctx.guild.roles, id = MUTE_ROLE_ID)

            await member.remove_roles(MUTE_ROLE)
            punishment_info.delete_instance()

            emb = discord.Embed(color = SUCCESS_COLOR)
            emb.add_field(name = "Размьючен:", value = f"{member}")
            emb.add_field(name = "Размьютил:", value = f"{ctx.author.mention}")
            emb.add_field(name = f"{INVISIBLE_SYMBOL}", value = f"{SUCCESS_LINE}", inline = False)
            emb.add_field(name = "Причина:", value = f"{reason}")
            await ctx.send(embed = emb)

        else:
            if member in ctx.guild.members:
                raise UserIsNotPunished(member)
            else:
                raise commands.BadArgument()

def setup(bot):
    bot.add_cog(Moderation(bot))
