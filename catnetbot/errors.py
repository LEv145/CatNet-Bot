"""Ког с ошибками"""
import discord
from discord.ext import commands
import toml_config  # я не помню откуда питон ищет модули, вроде из места запуска

# На этом моменте может что ни будь сломаться т.к. не проверял, но должно работать

conf = toml_config.load_config()["messages"]["errors"]

permissions_config = toml_config.load_config()["discord"]

PREFIX = toml_config.load_config()["bot"]["prefix"]

SUCCESS_LINE = conf["success_line"]["emoji"] * conf["success_line"]["repeat"] + "\n "
SUCCESS_COLOR = conf["success_line"]["color"]

STANDART_LINE = conf["standard_line"]["emoji"] * conf["standard_line"]["repeat"] + "\n⠀"
STANDART_COLOR = conf["standard_line"]["color"]

ERROR_LINE = conf["error_line"]["emoji"] * conf["error_line"]["repeat"] + "\n⠀"
ERROR_COLOR = conf["error_line"]["color"]

INVISIBLE_SYMBOL = conf["invisible_symbol"]


async def command_error_detection(ctx, error):
    async def own_command_error_message(problem, solution):
        embed = discord.Embed(color = ERROR_COLOR)
        embed.add_field(name = "Проблема:", value = f"{problem}")
        embed.add_field(
                name = f"{INVISIBLE_SYMBOL}", value = f"{ERROR_LINE}", inline = False
        )
        embed.add_field(name = "Решение:", value = f"{solution}")
        await ctx.send(embed = embed)
        if ctx.message:
            try:
                await ctx.message.delete()
            except discord.errors.NotFound:
                pass

    if isinstance(error, commands.CommandNotFound):
        await own_command_error_message(
            "Команда не найдена!",
            "Используйте существующую команду,\nкоторая есть в списке `.help`",
        )
    elif isinstance(error, commands.DisabledCommand):
        await own_command_error_message(
            "Команда отключена!",
            "Используйте другую, активированную\n в данный момент команду",
        )
    elif isinstance(error, commands.CommandOnCooldown):

        def make_readable(seconds):
            hours, seconds = divmod(seconds, 60 ** 2)
            minutes, seconds = divmod(seconds, 60)
            return f"{round(hours)} ч, {round(minutes)} мин, {round(seconds)} сек"

        await own_command_error_message(
            "Команда с задержкой!",
            f"Используйте данную команду \nпосле `{make_readable(error.retry_after)}` ⏳",
        )
    elif isinstance(error, commands.MissingPermissions):
        await own_command_error_message(
                "У Вас недостаточно прав!",
                "Получите следующие права:\n" + "\n".join([permissions_config[f"{perm}"] for perm in error.missing_perms])
        )

    elif isinstance(error, commands.MissingRequiredArgument):

        await own_command_error_message(
                "Вы упустили аргументы при\nиспользовании команды!",
                f"Запишите команду по синтаксису:\n`{PREFIX}{ctx.command.usage}`"
        )

    elif isinstance(error, UserIsPunished):

        def make_readable(seconds):
            hours, seconds = divmod(seconds, 60 ** 2)
            minutes, seconds = divmod(seconds, 60)
            return f"{round(hours)} ч, {round(minutes)} мин, {round(seconds)} сек"

        await own_command_error_message(
                "Пользователь уже замьючен!",
                f"Замьютьте пользователя после размьюта!\n(через {make_readable(error.retry_after)})"
        )

    elif isinstance(error, UserIsNotPunished):

        await own_command_error_message(
                "Пользователь не замьючен!",
                f"Замьютьте пользователя {error.member}, чтобы\nразмьютить его!"
        )

class UserIsPunished(commands.CommandError):
    def __init__(self, retry_after):
        self.retry_after = retry_after

class UserIsNotPunished(commands.CommandError):
    def __init__(self, member):
        self.member = member