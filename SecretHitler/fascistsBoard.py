def nothing(peek, president, players, chat_id):
    pass


def execution(peek, president, players, chat_id):
    # todo: do it
    pass


def policy_peek(bot, peek, president, players, chat_id):
    # todo: do it
    pass


def call_special_election(bot, peek, president, players, chat_id):
    # todo: do it
    pass


def investigate_loyalty(bot, peek, president, players, chat_id):
    # todo: do it
    pass


def handle_btn(data, bot):
    # todo: do it
    pass


boards = [
    [nothing, nothing, policy_peek, execution, execution],
    [nothing, investigate_loyalty, call_special_election, execution, execution],
    [investigate_loyalty, investigate_loyalty, call_special_election, execution, execution]
]


def select_board(num_of_players):
    return boards[int((num_of_players - 5) / 2)]
