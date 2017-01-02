from telecatbot.telegram import TeleCatBot
from telecatbot.thecatapi import CatAPI


api = CatAPI()
bot = TeleCatBot(api)

if __name__ == '__main__':
    bot.serve()