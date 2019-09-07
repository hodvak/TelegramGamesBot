import random
from SecretHitler import fascistsBoard
from game import Game


class SecretHitlerGame(Game):
    LIBERAL_INDEX = 0
    FASCIST_INDEX = 1
    HITLER_INDEX = 2
    cards_data = [{'name': 'hitler', "img": "hitler.png"},
                  {'name': 'liberal', "img": "liberal.png"},
                  {'name': 'fascist', "img": "fascist.png"}]
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
        self.bot = bot
        self.chet_id = chat_id
        self.players = players
        board_index = fascistsBoard.select_index(len(players))
        self.fascist_board_methods = fascistsBoard.boards_method[board_index]
        self.fascist_board_stickers = fascistsBoard.board_files_id[board_index]
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
            elif player['card'] is SecretHitlerGame.FASCIST_INDEX and len(players) <= 6:  # fascist in 5-6 players game
                bot.send_message(chat_id=player['id'], text="hitler is " + hitler)
            elif player['card'] is SecretHitlerGame.FASCIST_INDEX and len(players) > 6:  # fascist in 7-10 players game
                bot.send_message(chat_id=player['id'],
                                 text="fascists are " + ", ".join(fascists) + " and Hitler is " + hitler)

        # Random order of players
        random.shuffle(players)
        bot.send_message(
            chat_id=chat_id,
            text='the order of the players is : \n' + ', \n'.join([player['name'] for player in players])
        )

        # Deck of rules
        self.deck = [SecretHitlerGame.LIBERAL_INDEX] * 6 + [SecretHitlerGame.FASCIST_INDEX] * 11
        random.shuffle(self.deck)

        # The boards message id
        self.boards_message_id = [bot.sendSticker(chat_id=chat_id, sticker=self.fascist_board_stickers[0]).message_id]

    def handle_btn(self, update):
        # todo: handle the buttons that players clicked
        pass
