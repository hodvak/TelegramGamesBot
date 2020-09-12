from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class Game:
    MIN_PLAYERS = 5
    MAX_PLAYERS = 10

    def __init__(self, bot, chat_id, players):
        self.bot = bot
        self.chat_id = chat_id
        # init get the bot, the group chat id and the players id and names that playing that game

    def handle_btn(self, data):
        print(data)

    def send_message(self, chat_id=None, text=None, buttons=None):
        """
        :param chat_id: chat to write in
        :param text: the text to write
        :param buttons: list(rows) of list(cols) of dict with 'text' and 'data'
        :return: nothing
        """
        if chat_id is None:
            chat_id = self.chat_id
        reply_markup = []
        if buttons is not None:
            reply_markup = []
            for line in buttons:
                line_buttons = []
                for button in line:
                    line_buttons.append(InlineKeyboardButton(
                        text=button['text'],
                        callback_data=str(self.chat_id) + '_' + button['data'])
                    )
                reply_markup.append(line_buttons)

        return self.bot.sendMessage(chat_id=chat_id, text=text, reply_markup=InlineKeyboardMarkup(reply_markup))

    def send_sticker(self, char, sticker):
        pass

    def edit_message_text(self, message_id, chat_id=None, text="", buttons=None):
        if chat_id is None:
            chat_id = self.chat_id
        reply_markup = None
        if buttons is not None:
            reply_markup = []
            for line in buttons:
                linebuttons = []
                for button in line:
                    linebuttons.append(InlineKeyboardButton(text=button['text'],
                                                            callback_data=str(self.chat_id) + '_' + button['data']))
                reply_markup.append(linebuttons)

        self.bot.edit_message_text(message_id=message_id, chat_id=chat_id, text=text,
                                   reply_markup=InlineKeyboardMarkup(
                                       reply_markup) if reply_markup is not None else None)
