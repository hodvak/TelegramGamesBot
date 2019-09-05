import random
from SecretHitler import fascistsBoard
from game import Game


class SecretHitlerGame(Game):
    cards_data = [{'name': 'hitler', "img": "hitler.png"},
                  {'name': 'liberal', "img": "liberal.png"},
                  {'name': 'fascist', "img": "fascist.png"}]
    CARDS = [1, 1, 0, 1, 2, 1, 2, 1, 2, 1]
    MIN_PLAYERS = 5
    MAX_PLAYERS = 10
    NAME = "Secret Hitler"

    def __init__(self, bot, chat_id, players):
        self.bot = bot
        self.chet_id = chat_id
        self.players = players
        self.fascist_board = fascistsBoard.select_board(len(players))

        self.dec = [[1] * 6, [0] * 9]
        random.shuffle(self.dec)

        # set players role
        new_cards = SecretHitlerGame.CARDS[:len(players)]
        random.shuffle(new_cards)
        hitler = ''
        fascists = []
        for player, card in zip(players, new_cards):
            player['card'] = card
            if card is 0:  # hitler
                hitler = player['name']
            elif card is 2:  # fascist
                fascists.append(player['name'])

        # send players there rule
        # send fascist how others fascists
        # send hitler how the fascist if 5-6 players
        for player in players:
            bot.send_message(chat_id=player['id'], text=SecretHitlerGame.cards_data[player['card']]['name'])
            if player['card'] is 0 and len(players) <= 6:  # hitler in 5-6 players game
                bot.send_message(chat_id=player['id'], text="fascist is " + fascists[0])
            elif player['card'] is 2 and len(players) <= 6:  # hitler in 5-6 players game
                bot.send_message(chat_id=player['id'], text="hitler is " + hitler)
            elif player['card'] is 2 and len(players) > 6:  # hitler in 5-6 players game
                bot.send_message(chat_id=player['id'],
                                 text="fascists are " + ", ".join(fascists) + " and Hitler is " + hitler)

        # random order of players
        random.shuffle(players)
        bot.send_message(
            chat_id=chat_id,
            text='the order of the players is : \n' + ', \n'.join([player['name'] for player in players])
        )

    def handle_btn(self, update):
        # todo: handle the buttons that players clicked
        pass
