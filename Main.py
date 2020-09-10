from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from SecretHitler import secretHitler
from collections import namedtuple
from typing import Dict
from game import Game

Unstarted_game = namedtuple("unstarted_game",
                            ['game', 'players'])

games: Dict[int, Game] = {}  # Dict[int, Game]  # Games in play right now. The key is the chat ID
unstarted_games: Dict[int, Unstarted_game] = {}  # Games that haven't started yet. The key is the chat ID
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
    dp.add_handler(CallbackQueryHandler(handle_game_buttons))
    updater.start_polling()
    updater.idle()


def init_game(bot, update, game):
    chat_id = update.message.chat_id
    unstarted_games[chat_id] = Unstarted_game(game=game, players=[])

    bot.sendMessage(chat_id=chat_id, text=game.NAME, reply_markup=reply_markup)


def start_secret_hitler(bot, update):
    init_game(bot=bot,
              update=update,
              game=secretHitler.SecretHitlerGame)


def join_game(bot, update):
    """
    Runs when the player clicks the 'join game' button
    """
    chat_id = update.callback_query.message.chat.id
    user_id = update.callback_query.from_user.id
    user_name = update.callback_query.from_user.username

    new_player = {'name': user_name + str(len(unstarted_games[chat_id].players)), 'id': user_id}
    # add player only if there no more than max players and player not in the array
    # todo: when done testing remove 'or true'
    if chat_id in unstarted_games \
            and len(unstarted_games[chat_id].players) < unstarted_games[chat_id].game.MAX_PLAYERS \
            and (not any(player['id'] == user_id for player in unstarted_games[chat_id].players) or True):
        unstarted_games[chat_id].players.append(new_player)
    new_markup = InlineKeyboardMarkup(get_new_buttons(chat_id))
    update.callback_query.edit_message_reply_markup(reply_markup=new_markup)


def get_new_buttons(chat_id):
    if chat_id not in unstarted_games:
        return [[]]
    buttons = []
    num_of_players = len(unstarted_games[chat_id].players)

    start_text = "start"
    if num_of_players == unstarted_games[chat_id].game.MAX_PLAYERS:
        start_text = "start(" + str(num_of_players) + ")"

    if num_of_players < unstarted_games[chat_id].game.MAX_PLAYERS:
        buttons.append([InlineKeyboardButton(text=f'join game({num_of_players})', callback_data='join')])
    if num_of_players >= unstarted_games[chat_id].game.MIN_PLAYERS:
        buttons.append([InlineKeyboardButton(text=start_text, callback_data='start')])

    return buttons


def start_game(bot, update):
    chat_id = update.callback_query.message.chat.id
    if chat_id in unstarted_games \
            and len(unstarted_games[chat_id].players) >= unstarted_games[chat_id].game.MIN_PLAYERS:
        games[chat_id] = unstarted_games[chat_id].game(bot=bot,
                                                       chat_id=chat_id,
                                                       players=unstarted_games[chat_id].players)
        update.callback_query.message.edit_text(text=unstarted_games[chat_id].game.NAME + " has began")
    else:
        update.callback_query.message.delete()


def handle_game_buttons(bot, update):
    data = update.callback_query.data
    chat_id = int(update.callback_query.data.split('_')[0])
    update.callback_query.data = data[data.index('_') + 1:]
    # chat_id = update.callback_query.message.chat.id
    if chat_id in games:
        games[chat_id].handle_btn(update)


if __name__ == '__main__':
    main()
