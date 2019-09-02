from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from SecretHitler import secretHitler
from collections import namedtuple
from .game import Game

UnstartedGame = namedtuple('Unstarted Game', ['game', 'players'])

games: dict[str: Game] = {}  # Games in play right now. The key is the chat ID
unstarted_games: dict[str: UnstartedGame] = {}  # Games that haven't started yet. The key is the chat ID
promo_keyboard = [InlineKeyboardButton(text="join game", callback_data="join")]
reply_markup = InlineKeyboardMarkup([promo_keyboard])

TOKEN_FILE = 'token.txt'


def main():
    # Get the token from "token.txt" file
    with open(TOKEN_FILE, 'r') as f:
        token = f.readline()

    # Set up the bot
    updater = Updater(token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start_secret_hitler", start_secret_hitler))
    dp.add_handler(CallbackQueryHandler(join_game, pattern='join'))
    dp.add_handler(CallbackQueryHandler(start_game, pattern='start'))
    updater.start_polling()
    updater.idle()


def init_game(bot, update, game, game_name):
    chat_id = update.message.chat_id
    unstarted_games[chat_id] = UnstartedGame(game, [])
    bot.sendMessage(chat_id=chat_id, text=game_name, reply_markup=reply_markup)


def start_secret_hitler(bot, update):
    init_game(bot=bot,
              update=update,
              game=secretHitler.SecretHitlerGame,
              game_name="SecretHitler")


def join_game(bot, update):
    """
    Runs when the player clicks the 'join game' button
    """
    chat_id = update.callback_query.message.chat.id
    user_id = update.callback_query.from_user.id
    user_name = update.callback_query.from_user.username

    player = {'name': user_name, 'id': user_id}
    unstarted_games[chat_id]['players'].append(player)

    new_markup = InlineKeyboardMarkup([_get_new_buttons(chat_id)])
    update.callback_query.edit_message_reply_markup(reply_markup=new_markup)


def _get_new_buttons(chat_id):
    buttons = []

    num_of_players = len(unstarted_games[chat_id].players)

    if num_of_players < unstarted_games[chat_id].game.max_players:
        buttons.append(InlineKeyboardButton(text=f'join game({num_of_players})', callback_data='join'))
    else:
        buttons.append(InlineKeyboardButton(text=f'start ({num_of_players})', callback_data='start'))

    return buttons


def start_game(bot, update):
    chat_id = update.callback_query.message.chat.id
    games[chat_id] = unstarted_games[chat_id].game(bot=bot,
                                                   chat_id=chat_id,
                                                   players=unstarted_games[chat_id].players)


if __name__ == '__main__':
    main()
