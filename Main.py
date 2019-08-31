from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from SecretHitler import secretHitler

games = {}  # games that players play right now. key is chat id and value is GAME
before_start_games = {}  # games that not started yet. . key is chat id and value is array of users id
promo_keyboard = [InlineKeyboardButton(text="join game", callback_data="join")]
reply_markup = InlineKeyboardMarkup([promo_keyboard])


# the main function.
def main():
    # get the token from "token.txt" file...
    token = open('token.txt', 'r').readline()
    # setting up the bot.
    updater = Updater(token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start_secret_hitler", start_secret_hitler))
    dp.add_handler(CallbackQueryHandler(join_game, pattern='join'))
    dp.add_handler(CallbackQueryHandler(start_game, pattern='start'))
    updater.start_polling()
    updater.idle()


def init_game(bot, update, game, game_name):
    chat_id = update.message.chat_id
    before_start_games[chat_id] = {'game': game, 'players': []}
    bot.sendMessage(chat_id=chat_id, text=game_name, reply_markup=reply_markup)


def start_secret_hitler(bot, update):
    init_game(bot=bot,
              update=update,
              game=secretHitler.SecretHitlerGame,
              game_name="SecretHitler")


# when player click the join game button
def join_game(bot, update):
    chat_id = update.callback_query.message.chat.id
    user_id = update.callback_query.from_user.id
    user_name = update.callback_query.from_user.username

    player = {'name': user_name, 'id': user_id}
    before_start_games[chat_id]['players'].append(player)

    btns = []
    num_of_players = len(before_start_games[chat_id]['players'])
    print("level1")
    print(num_of_players)
    if num_of_players < before_start_games[chat_id]['game'].max_players:
        btns.append(
            InlineKeyboardButton(
                text="join game(" + str(num_of_players) + ")", callback_data="join")
        )
    if num_of_players >= before_start_games[chat_id]['game'].min_players:
        text = "start"
        if len(btns) is 0:
            text += "(" + str(num_of_players) + ")"
        btns.append(
            InlineKeyboardButton(text=text,
                                 callback_data="start"))

    new_markup = InlineKeyboardMarkup([btns])

    update.callback_query.edit_message_reply_markup(reply_markup=new_markup)


def start_game(bot, update):
    print('ok')
    chat_id = update.callback_query.message.chat.id
    print(chat_id)
    print(before_start_games[chat_id]['game'])
    games[chat_id] = before_start_games[chat_id]['game'](bot=bot,
                                                         chat_id=chat_id,
                                                         players=before_start_games[chat_id]['players'])


if __name__ == '__main__':
    main()
