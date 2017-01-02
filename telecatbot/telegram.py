import logging

from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram.ext import InlineQueryHandler
from .config import TELEGRAM_TOKEN
from .cache import cache


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


# http://apps.timwhitlock.info/emoji/tables/unicode  -  Unicode Field
emoji_heart_eyes_cat = chr(int('1F63B', 16))
emoji_crying_cat_face = chr(int('1F63F', 16))


class TeleCatBot:
    """TeleCatBot! a Telegram bot fully of cats! =^_^="""

    def __init__(self, api):
        self.updater = Updater(token=TELEGRAM_TOKEN)
        self.dispatcher = self.updater.dispatcher
        self.api = api
        self.register_handlers()

    @property
    def keyboard_initial(self):
        """The initial keyboard layout when /start is hit"""
        return ReplyKeyboardMarkup(
        [
                [
                    KeyboardButton("/next"),
                    KeyboardButton("/help")
                ]
        ]
        )

    @property
    def keyboard_rating(self):
        """Rating keyboard layout"""
        return ReplyKeyboardMarkup(
        [
                [
                    KeyboardButton("/like"),
                    KeyboardButton("/dislike"),
                    KeyboardButton("/report")
                ],
                [
                    KeyboardButton("/next")
                ]
        ]
        )

    def register_handlers(self):
        """Register all handlers"""
        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)

        help_handler = CommandHandler('help', self.help)
        self.dispatcher.add_handler(help_handler)

        get_handler = CommandHandler('next', self.next)
        self.dispatcher.add_handler(get_handler)

        like_handler = CommandHandler('like', self.like)
        self.dispatcher.add_handler(like_handler)

        dislike_handler = CommandHandler('dislike', self.dislike)
        self.dispatcher.add_handler(dislike_handler)

        report_handler = CommandHandler('report', self.report)
        self.dispatcher.add_handler(report_handler)

        unknown_handler = MessageHandler(Filters.command, self.unknown)
        self.dispatcher.add_handler(unknown_handler)

    def serve(self):
        """Serve the bot, this function is blocking!"""
        self.updater.start_polling()

    def start(self, bot, update):
        """/start command"""
        bot.send_message(chat_id=update.message.chat_id, text="Welcome to TeleCatBot!", reply_markup=self.keyboard_initial)

    def help(self, bot, update):
        """/help command"""
        bot.send_message(chat_id=update.message.chat_id, text="""Welcome to TeleCatBot!
Commands:
/next command for next image!
/like command for like last image seen!
/dislike command for dislike last image seen!
/report command for report last image seen!
""")

    def next(self, bot, update):
        """/next command"""
        image = self.api.get()
        bot.send_photo(chat_id=update.message.chat_id, photo=image['url'], reply_markup=self.keyboard_rating)
        # TODO: set cache, last image seed for this chat_id

        cache.set(update.message.chat_id, image['id'])

    def like(self, bot, update):
        """/like command"""

        id_image = self._last_image_seen(update)
        if id_image:
            bot.send_message(chat_id=update.message.chat_id, text=emoji_heart_eyes_cat)
            self.api.like(id_image, update.message.from_user.id)

    def dislike(self, bot, update):
        """/dislike command"""

        id_image = self._last_image_seen(update)
        if id_image:
            bot.send_message(chat_id=update.message.chat_id, text=emoji_crying_cat_face)
            self.api.dislike(id_image, update.message.from_user.id)

    def report(self, bot, update):
        """/report command"""
        id_image = self._last_image_seen(update)
        if id_image:
            bot.send_message(chat_id=update.message.chat_id, text='Image reported!')
            self.api.report(id_image, update.message.from_user.id)

    def unknown(self, bot, update):
        """Any unknown command handler!"""
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")


    def _last_image_seen(self, update):
        return cache.get(update.message.chat_id).decode('utf-8')
