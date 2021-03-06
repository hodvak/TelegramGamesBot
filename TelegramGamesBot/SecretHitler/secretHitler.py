import random
import time

from . import boards
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

    def __init__(self, bot, chat_id, players: list):
        super().__init__(bot, chat_id, players)
        # the bot
        self.bot = bot
        # group chat id
        self.chat_id = chat_id
        # the players
        self.players = players
        self.alive = players.copy()
        self.nein_in_a_row = 0
        self.state = 'pick canceler'  # /'vote'/'kill'/''
        self.president = 0
        self.chancellor = -1
        self.cards_to_pick = None
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
        self.burn_deck = []
        random.shuffle(self.deck)
        self.deck_status = self.send_message(text="17 cards in the deck\n0 cards burned").message_id
        # The boards message id
        self.boards_message_id = [
            bot.sendSticker(chat_id=chat_id, sticker=self.fascist_board_stickers[0]).message_id,
            bot.sendSticker(chat_id=chat_id, sticker=self.liberals_board_stickers[0]).message_id,
            bot.sendSticker(chat_id=chat_id, sticker=boards.nein_board_files_id[0]).message_id
        ]

    def ja_nein_handler(self, update):
        if self.state == 'vote':
            try:
                user_id = update.callback_query.from_user.id
                if not any(vote['id'] == user_id for vote in self.votes) and self.player_index_by_id(user_id) != -1:
                    self.votes.append(
                        {"id": update.callback_query.from_user.id, "data": update.callback_query.data.split('_')[1]})
                    if len(self.votes) < len(self.alive):
                        self.edit_message_text(message_id=update.callback_query.message.message_id,
                                               text="agree?(" + str(len(self.votes)) + "/" + str(len(self.alive)) + ")",
                                               buttons=[[{'text': 'JA (YES)', 'data': 'jn_ja'}],
                                                        [{'text': 'NEIN (NO)', 'data': 'jn_nein'}]])
                    else:
                        self.edit_message_text(message_id=update.callback_query.message.message_id,
                                               text=",\n".join(
                                                   [self.player_name_by_id(v['id']) + " : " + v['data'] for v in
                                                    self.votes]),
                                               buttons=[])
                        time.sleep(2.4)
                        self.bot.deleteMessage(
                            message_id=update.callback_query.message.message_id, chat_id=self.chat_id
                        )

                        if sorted(self.votes,
                                  key=lambda student: student['data'])[int(len(self.alive) / 2)]['data'] == 'nein':
                            self.nein_in_a_row += 1
                            if self.nein_in_a_row == 3:
                                self.nein_in_a_row = 0
                                self.rules[self.deck.pop(0)] += 1
                                if len(self.deck) < 3:
                                    self.deck += self.burn_deck
                                    self.burn_deck = []
                                    random.shuffle(self.deck)
                                self.render_cards_status()

                            self.president = (self.president + 1) % len(self.players)
                            while self.players[self.president] not in self.alive:
                                self.president = (self.president + 1) % len(self.players)
                            self.chancellor = -1

                            self.render_name_buttons()
                            self.render_new_boards()
                            self.state = 'pick canceler'
                        else:
                            if self.players[self.chancellor]['card'] == SecretHitlerGame.HITLER_INDEX and \
                                    len(self.votes[SecretHitlerGame.FASCIST_INDEX]) >= 3:
                                self.state = "gameOver"
                                self.send_message("FASCISTS win \n hitler chosen as chancellor after 3 FASCISTS rules")
                            else:
                                self.cards_to_pick = self.deck[:3]
                                self.deck = self.deck[3:]
                                self.nein_in_a_row = 0
                                self.state = 'president cards'
                                self.send_message(chat_id=self.players[self.president]['id'], text="pick one to remove",
                                                  buttons=[
                                                      [{"text": self.cards_data[card]['name'],
                                                        "data": "president_" + str(card)}]
                                                      for card in self.cards_to_pick])
                        self.votes = []

            except Exception as e:
                print(e)
                print(update)

    def president_pick(self, update):
        if self.state == 'president cards':
            if update.callback_query.message.chat.id == self.players[self.president]['id']:
                card_type = int(update.callback_query.data.split("_")[1])
                self.bot.deleteMessage(
                    message_id=update.callback_query.message.message_id,
                    chat_id=self.players[self.president]['id']
                )
                if card_type in self.cards_to_pick:
                    self.cards_to_pick.remove(card_type)
                    self.burn_deck.append(card_type)
                    self.state = "chancellor cards"
                    buttons = [
                        [
                            {
                                "text": self.cards_data[card]['name'],
                                "data": "chancellor_" + str(card)
                            }
                        ] for card in self.cards_to_pick]
                    if self.rules[SecretHitlerGame.FASCIST_INDEX] == 5:
                        buttons.append([{"text": "ask for veto", "data": "chancellor_veto"}])
                    self.send_message(chat_id=int(self.players[self.chancellor]['id']), text="pick one to remove",
                                      buttons=buttons)

    def chancellor_pick(self, update):
        if self.state == "chancellor cards":
            if update.callback_query.message.chat.id == self.players[self.chancellor]['id']:
                if update.callback_query.data.split("_")[1] == 'veto':
                    if self.rules[SecretHitlerGame.FASCIST_INDEX] == 5:
                        self.bot.deleteMessage(
                            message_id=update.callback_query.message.message_id,
                            chat_id=self.players[self.chancellor]['id']
                        )
                        self.state = "aks_for_veto"
                        self.send_message(
                            text="chancellor asking the president to call veto",
                            buttons=[[{"text": "yes", "data": "veto_yes"}, {"text": "no", "data": "veto_no"}]]
                        )
                        buttons = [
                            [
                                {
                                    "text": self.cards_data[card]['name'],
                                    "data": "chancellor_" + str(card)
                                }
                            ] for card in self.cards_to_pick]
                        self.edit_message_text(
                            update.callback_query.message.message_id,
                            text="pick one to remove",
                            buttons=buttons

                        )
                    return
                card_type = int(update.callback_query.data.split("_")[1])
                self.bot.deleteMessage(
                    message_id=update.callback_query.message.message_id,
                    chat_id=self.players[self.chancellor]['id']
                )
                if card_type in self.cards_to_pick:
                    self.cards_to_pick.remove(card_type)
                    self.burn_deck.append(card_type)
                    self.rules[self.cards_to_pick[0]] += 1

                    if self.rules[SecretHitlerGame.FASCIST_INDEX] == 6:
                        self.state = "gameOver"
                        self.send_message("FASCISTS win after getting 6 FASCISTS rules")
                        self.render_new_boards()
                        return
                    if self.rules[SecretHitlerGame.LIBERAL_INDEX] == 5:
                        self.state = "gameOver"
                        self.send_message("LIBERALS win after getting 5 FASCISTS rules")
                        self.render_new_boards()
                        return

                    self.state = 'pick canceler'
                    self.chancellor = -1

                    self.render_new_boards()

                    if len(self.deck) < 3:
                        self.deck += self.burn_deck
                        self.burn_deck = []
                        random.shuffle(self.deck)

                    if self.cards_to_pick[0] == SecretHitlerGame.FASCIST_INDEX:
                        self.fascist_board_methods[self.rules[SecretHitlerGame.FASCIST_INDEX] - 1](self)

                    self.president = (self.president + 1) % len(self.players)
                    while self.players[self.president] not in self.alive:
                        self.president = (self.president + 1) % len(self.players)

                    self.render_name_buttons()
                    self.render_cards_status()

    def veto_pick(self, update):
        print(self.state)
        print(self.players[self.president]['id'])
        if self.state == 'aks_for_veto' and update.callback_query.from_user.id == self.players[self.president]['id']:
            self.bot.deleteMessage(
                message_id=update.callback_query.message.message_id, chat_id=self.chat_id
            )
            if update.callback_query.data == "veto_no":
                my_m = self.send_message(text="president not agree to veto").message_id
                time.sleep(3)
                self.bot.deleteMessage(message_id=my_m, chat_id=self.chat_id)
                self.state = 'chancellor cards'
                buttons = [
                    [
                        {
                            "text": self.cards_data[card]['name'],
                            "data": "chancellor_" + str(card)
                        }
                    ] for card in self.cards_to_pick]
                self.send_message(chat_id=int(self.players[self.chancellor]['id']), text="pick one to remove",
                                  buttons=buttons)
            else:
                self.state = 'president cards'
                my_m = self.send_message(text="president agree to veto").message_id
                time.sleep(3)
                self.bot.deleteMessage(message_id=my_m, chat_id=self.chat_id)

                self.burn_deck.extend(self.cards_to_pick)
                self.cards_to_pick = []
                if len(self.deck) < 3:
                    self.deck += self.burn_deck
                    self.burn_deck = []
                    random.shuffle(self.deck)
                self.render_cards_status()
                self.cards_to_pick = self.deck[:3]
                self.deck = self.deck[3:]
                self.state = 'president cards'
                self.send_message(chat_id=self.players[self.president]['id'], text="pick one to remove",
                                  buttons=[
                                      [{"text": self.cards_data[card]['name'],
                                        "data": "president_" + str(card)}]
                                      for card in self.cards_to_pick])

    def handle_btn(self, update):
        print(self.state)
        if update.callback_query.data.startswith('pickPlayer_'):
            self.pick_player(update)
        if update.callback_query.data.startswith('jn_'):
            self.ja_nein_handler(update)
        if update.callback_query.data.startswith('president_'):
            self.president_pick(update)
        if update.callback_query.data.startswith('chancellor_'):
            self.chancellor_pick(update)
        if update.callback_query.data.startswith('veto_'):
            self.veto_pick(update)

    def pick_player(self, update):
        if self.state == 'pick canceler':
            if update.callback_query.from_user.id == self.players[self.president]['id']:
                self.chancellor = self.player_index_by_id(int(update.callback_query.data.split('_')[1]))
                self.state = 'vote'
                self.render_name_buttons()
                self.start_vote()

    def player_index_by_id(self, user_id):
        for index, player in enumerate(self.players):
            if player['id'] == user_id:
                return index
        return -1

    def player_name_by_id(self, user_id):
        for index, player in enumerate(self.players):
            if player['id'] == user_id:
                return player['name']
        return ""

    def start_vote(self):
        self.send_message(self.chat_id, text="agree?(0/" + str(len(self.alive)) + ")",
                          buttons=[[{'text': 'JA (YES)', 'data': 'jn_ja'}], [{'text': 'NEIN (NO)', 'data': 'jn_nein'}]])

    def render_name_buttons(self):
        buttons = [[{'text': player['name'], 'data': 'pickPlayer_' + str(player['id'])}] for player in self.players]
        buttons[self.president][0]['text'] += ' 👑'
        if self.chancellor != -1:
            buttons[self.chancellor][0]['text'] += ' 🤵'
        for index, temp_player in enumerate(self.players):
            if temp_player not in self.alive:
                buttons[index][0]['text'] += ' 🗡️'

        self.edit_message_text(message_id=self.all_player_buttons, text="the order of the players is :",
                               buttons=buttons)

    def render_cards_status(self):
        self.edit_message_text(self.deck_status,
                               text=f"{len(self.deck)} cards in deck\n{len(self.burn_deck)} cards burned")

    def render_new_boards(self):
        # The boards message id
        [self.bot.deleteMessage(message_id=message, chat_id=self.chat_id) for message in self.boards_message_id]
        self.boards_message_id = [
            self.bot.sendSticker(
                chat_id=self.chat_id, sticker=self.fascist_board_stickers[self.rules[SecretHitlerGame.FASCIST_INDEX]]
            ).message_id,
            self.bot.sendSticker(
                chat_id=self.chat_id, sticker=self.liberals_board_stickers[self.rules[SecretHitlerGame.LIBERAL_INDEX]]
            ).message_id,
            self.bot.sendSticker(
                chat_id=self.chat_id, sticker=boards.nein_board_files_id[self.nein_in_a_row]
            ).message_id
        ]
