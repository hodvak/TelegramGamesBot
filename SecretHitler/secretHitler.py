import random
import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from SecretHitler import boards
from game import Game


class SecretHitlerGame(Game):
    LIBERAL_INDEX = 0
    FASCIST_INDEX = 1
    HITLER_INDEX = 2
    cards_data = [{'name': 'liberal', "img": "liberal.png"},
                  {'name': 'fascist', "img": "fascist.png"},
                  {'name': 'hitler', "img": "hitler.png"}]

    CARDS = [LIBERAL_INDEX,
             LIBERAL_INDEX,
             HITLER_INDEX,
             LIBERAL_INDEX,
             FASCIST_INDEX,
             LIBERAL_INDEX,
             FASCIST_INDEX,
             LIBERAL_INDEX,
             FASCIST_INDEX,
             LIBERAL_INDEX
             ]

    MIN_PLAYERS = 5
    MAX_PLAYERS = 10
    NAME = "Secret Hitler"

    def __init__(self, bot, chat_id, players):
        # the bot
        self.bot = bot
        # group chat id
        self.chat_id = chat_id
        # the players
        self.players = players
        self.alive = players.copy()
        self.state = 'pick canceler'  # /'vote'/'kill'/''
        self.president = 0
        self.cancler = -1
        # ya nain votes
        self.votes = []
        board_index = boards.fascist_select_index(len(players))
        self.fascist_board_methods = boards.fascist_board_methods[board_index]
        self.fascist_board_stickers = boards.fascist_board_files_id[board_index]
        self.liberals_board_stickers = boards.liberal_board_files_id
        self.rules = [0, 0]

        # set players role
        new_cards = SecretHitlerGame.CARDS[:len(players)]
        random.shuffle(new_cards)
        hitler = ''
        fascists = []
        for player, card in zip(players, new_cards):
            player['card'] = card
            if card is SecretHitlerGame.HITLER_INDEX:  # hitler
                hitler = player['name']
            elif card is SecretHitlerGame.FASCIST_INDEX:  # fascist
                fascists.append(player['name'])

        # Send to players there secret identity
        # Send fascist how others fascists
        # Send hitler how the fascist if 5-6 players
        for player in players:
            bot.send_message(chat_id=player['id'], text=SecretHitlerGame.cards_data[player['card']]['name'])
            if player['card'] is SecretHitlerGame.HITLER_INDEX and len(players) <= 6:  # hitler in 5-6 players game
                bot.send_message(chat_id=player['id'], text="fascist is " + fascists[0])
            elif player['card'] is SecretHitlerGame.FASCIST_INDEX and len(
                    players) <= 6:  # fascist in 5-6 players game
                bot.send_message(chat_id=player['id'], text="hitler is " + hitler)
            elif player['card'] is SecretHitlerGame.FASCIST_INDEX and len(
                    players) > 6:  # fascist in 7-10 players game
                bot.send_message(chat_id=player['id'],
                                 text="fascists are " + ", ".join(fascists) + " and Hitler is " + hitler)
        # Random order of players
        random.shuffle(players)
        buttons = [[{'text': player['name'], 'data': 'pickPlayer_' + str(player['id'])}] for player in players]
        buttons[0][0]['text'] += ' 👑'

        self.all_player_buttons = self.send_message(
            chat_id=chat_id,
            text='the order of the players is :',
            buttons=buttons
        ).message_id
        # self.render_name_buttons(bot)

        # Deck of rules
        self.deck = [SecretHitlerGame.LIBERAL_INDEX] * 6 + [SecretHitlerGame.FASCIST_INDEX] * 11
        random.shuffle(self.deck)

        # The boards message id
        self.boards_message_id = [bot.sendSticker(chat_id=chat_id, sticker=self.fascist_board_stickers[0]).message_id]
        self.boards_message_id.append(
            bot.sendSticker(chat_id=chat_id, sticker=self.liberals_board_stickers[0]).message_id)
        # self.send_message(chat_id=chat_id, text="president choose")

    def ja_nein_handler(self, update):
        try:
            # print(update.callback_query.__dict__)
            self.votes.append(
                {"id": update.callback_query.from_user.id, "data": update.callback_query.data.split('_')[1]})
            if len(self.votes) < len(self.alive):
                self.editMessageText(message_id=update.callback_query.message.message_id,
                                     text="agree?(" + str(len(self.votes)) + "/" + str(len(self.alive)) + ")",
                                     buttons=[[{'text': 'JA (YES)', 'data': 'jn_ja'}],
                                              [{'text': 'NEIN (NO)', 'data': 'jn_nein'}]])
            else:
                self.editMessageText(message_id=update.callback_query.message.message_id,
                                     text=",\n".join(
                                         [self.player_name_by_id(v['id']) + " : " + v['data'] for v in self.votes]),
                                     buttons=[])
                time.sleep(2.4)
                self.bot.deleteMessage(message_id=update.callback_query.message.message_id, chat_id=self.chat_id)
                if sorted(self.votes, key=lambda student: student['data'])[int(len(self.alive) / 2)]['data'] == 'nein':
                    self.president = (self.president + 1) % len(self.players)
                    self.cancler = -1
                    self.render_name_buttons(self.bot)
                    self.state = 'pick canceler'
                    self.votes = []
                else:
                    print(self.deck)
                    self.cards_to_pick = self.deck[:3]
                    self.deck = self.deck[3:]
                    self.state = 'president cards'
                    self.send_message(chat_id=int(self.players[self.president]['id']), text="pick one to remove",
                                      buttons=[
                                          [{"text": self.cards_data[card]['name'], "data": "president_" + str(card)}]
                                          for card in self.cards_to_pick])

                    # print(self.deck)
                    # print()
                    # print(self.deck[3:])

        except Exception as e:
            print(e)
            print(update)
        # print(self.votes)

    def president_pick(self, update):
        # self.cards_to_pick.remove()
        pass

    def handle_btn(self, update):
        print(self.state)
        if update.callback_query.data.startswith('pickPlayer_'):
            self.pickPlayer(update)
        if update.callback_query.data.startswith('jn_'):
            self.ja_nein_handler(update)
        if update.callback_query.data.startswith('president_'):
            self.president_pick(update)

    # elif update.callback_query.data.startswith('vote_'):
    #     self.vote(update)

    def pickPlayer(self, update):
        if update.callback_query.from_user.id == self.players[self.president]['id']:
            if self.state == 'pick canceler':
                self.cancler = self.player_index_by_id(int(update.callback_query.data.split('_')[1]))
                self.state = 'vote'
                self.render_name_buttons(self.bot)
                self.start_vote()

    def player_index_by_id(self, id):
        for index, player in enumerate(self.players):
            if player['id'] == id:
                return index
        return -1

    def player_name_by_id(self, id):
        for index, player in enumerate(self.players):
            if player['id'] == id:
                return player['name']
        return ""

    def start_vote(self):
        self.send_message(self.chat_id, text="agree?(0/" + str(len(self.alive)) + ")",
                          buttons=[[{'text': 'JA (YES)', 'data': 'jn_ja'}], [{'text': 'NEIN (NO)', 'data': 'jn_nein'}]])

    def render_name_buttons(self, bot):
        buttons = [[{'text': player['name'], 'data': 'pickPlayer_' + str(player['id'])}] for player in self.players]
        buttons[self.president][0]['text'] += ' 👑'
        if self.cancler != -1:
            buttons[self.cancler][0]['text'] += ' 🤵'  # 🗡️
        for index, temp_player in enumerate(self.players):
            if temp_player not in self.alive:
                print(index)
                buttons[index][0]['text'] += ' 🗡️'

        self.editMessageText(message_id=self.all_player_buttons, text="the order of the players is :", buttons=buttons)
