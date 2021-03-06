from discord.ext import commands
from loguru import logger
from catnetbot import errors


# !!!!!!!!!Пока код не работает, потом если наймусь проектом - доделаю!!!!!!!!!!
class Bot(commands.AutoShardedBot):
    def __init__(self, token, prefix) -> None:

        ############ CLIENT SETTINGS ############
        intents = discord.Intents.all() #Discord 2020 Update: All Intentions
        allowed_mentions = discord.AllowedMentions(roles = False, everyone = False, users = False)
        super(SporeBot, self).__init__(command_prefix = prefix,
                                        intents = intents,
                                        allowed_mentions = allowed_mentions,
                                        case_insensitive = True,
                                        guild_subscriptions = True)


        self.MINUTE = 60


    async def on_ready(self):
        """
        Информация о запуске бота
        """
        logger.info(f"Бот вошёл в сеть. Аккаунт: {bot.user}, ID аккаунта: {bot.user.id}")

        import os
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                self.load_extension(f"cogs.{filename[:-3]}")



    async def on_command_completion(ctx):
        await ctx.message.delete()


    async def on_command_error(ctx, error):
        await errors.command_error_detection(ctx, error)





