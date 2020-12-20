from bot import Bot
from catnetbot import toml_config #import bot settings


if __name__ == '__main__':
    bot = Bot()
    config = toml_config.load_config()
    bot.run(prefix = config["bot"]["prefix"], token = config["discord"]["token"])
