from discord import utils
from discord.ext import commands
from loguru import logger
import toml_config
import os
import peewee
import errors

db = peewee.SqliteDatabase('catnet.db')

config = toml_config.load_config()
bot = commands.Bot(command_prefix = f'{config["bot"]["prefix"]}', case_insensitive = True)

MINUTE = 60

MUTE_ROLE_ID = config["discord"]["mute_role_id"]


@bot.event
async def on_ready():
    """
    Информация о запуске бота
    """
    logger.info(f"Бот вошёл в сеть. Аккаунт: {bot.user}, ID аккаунта: {bot.user.id}")

    @bot.event
    async def on_command(ctx):
        await ctx.message.delete()

    @bot.event
    async def on_command_error(ctx, error):
        await errors.command_error_detection(ctx, error)

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

if __name__ == "__main__":  # если запускаем именно этот файл то входим в бота

    bot.run(f'{config["discord"]["token"]}')





