import time


def nothing(game):
    print("nothing function")


def execution(game):
    print("execution")
    message = game.send_message(text="president must kill player").message_id
    last_handle_btn = game.handle_btn
    game.president -= 1
    game.handle_btn = lambda update: execution_btn_handler(game, update, last_handle_btn, message)


def execution_btn_handler(game, update, btn_handler, message_to_delete):
    # todo : check if its hitler
    if update.callback_query.from_user.id == game.players[game.president]['id']:
        player_index = game.player_index_by_id(int(update.callback_query.data.split('_')[1]))
        if game.players[player_index] in game.alive and player_index != game.president:
            game.alive.remove(game.players[player_index])
            game.president = (game.president + 1) % len(game.players)
            while game.players[game.president] not in game.alive:
                game.president = (game.president + 1) % len(game.players)
            game.handle_btn = btn_handler
            game.bot.deleteMessage(message_id=message_to_delete, chat_id=game.chat_id)
            game.render_name_buttons(game.bot)


def policy_peek(game):
    from SecretHitler.secretHitler import SecretHitlerGame
    message_id = game.send_message(
        int(game.players[game.president]['id']),
        "the 3 next cards will be :\n" + ", ".join(
            [SecretHitlerGame.cards_data[card]['name'] for card in game.deck[:3]])
    ).message_id

    time.sleep(10)

    game.bot.deleteMessage(message_id=message_id, chat_id=game.chat_id)


def call_special_election(game):
    print("call_special_election")
    message = game.send_message(text="president must choose the next president").message_id
    last_handle_btn = game.handle_btn
    game.president -= 1
    game.handle_btn = lambda update: call_special_election_btn_handler(game, update, last_handle_btn, message)


def call_special_election_btn_handler(game, update, btn_handler, message_to_delete):
    if update.callback_query.from_user.id == game.players[game.president]['id']:
        player_index = game.player_index_by_id(int(update.callback_query.data.split('_')[1]))
        if game.players[player_index] in game.alive and player_index != game.president:
            game.president = player_index
            game.handle_btn = btn_handler
            game.bot.deleteMessage(message_id=message_to_delete, chat_id=game.chat_id)
            game.render_name_buttons(game.bot)


def investigate_loyalty(game):
    print("investigate_loyalty")
    message = game.send_message(
        text="president must choose alive player and see his party membership (hitler is a fascist)"
    ).message_id
    last_handle_btn = game.handle_btn
    game.president -= 1
    game.handle_btn = lambda update: investigate_loyalty_btn_handler(game, update, last_handle_btn, message)


def investigate_loyalty_btn_handler(game, update, btn_handler, message_to_delete):
    if update.callback_query.from_user.id == game.players[game.president]['id']:
        player_index = game.player_index_by_id(int(update.callback_query.data.split('_')[1]))
        if game.players[player_index] in game.alive and player_index != game.president:

            membership = 'liberal' if game.players[player_index]['card'] == 0 else "fascist"
            game.send_message(
                chat_id=game.players[game.president]['id'],
                text=f"{game.players[player_index]['name']} is a {membership}"
            )

            game.president = (game.president + 1) % len(game.players)
            while game.players[game.president] not in game.alive:
                game.president = (game.president + 1) % len(game.players)
            game.handle_btn = btn_handler
            game.bot.deleteMessage(message_id=message_to_delete, chat_id=game.chat_id)
            game.render_name_buttons(game.bot)


fascist_board_methods = [
    [nothing, nothing, policy_peek, execution, execution],
    [nothing, investigate_loyalty, call_special_election, execution, execution],
    [investigate_loyalty, investigate_loyalty, call_special_election, execution, execution]
]

# stickers file id
fascist_board_files_id = [
    [
        'CAADAQADJQADPUHDFCRQ9EDgHRPxFgQ',
        'CAADAQADJgADPUHDFLV8q4IVus-8FgQ',
        'CAADAQADJwADPUHDFGla0jnVKphMFgQ',
        'CAADAQADGQADPUHDFCKw4iRvMvIvFgQ',
        'CAADAQADGgADPUHDFDYugNYIb5bCFgQ',
        'CAADAQADGwADPUHDFP7fQtQ71GZ0FgQ',
        'CAADAQADHAADPUHDFOebUvLwygmCFgQ'
    ],
    [
        'CAADAQADFQADPUHDFDdurFz2mQABehYE',
        'CAADAQADFwADPUHDFFlFpXlVcaH5FgQ',
        'CAADAQADGAADPUHDFAT0BrzxaShsFgQ',
        'CAADAQADGQADPUHDFCKw4iRvMvIvFgQ',
        'CAADAQADGgADPUHDFDYugNYIb5bCFgQ',
        'CAADAQADGwADPUHDFP7fQtQ71GZ0FgQ',
        'CAADAQADHAADPUHDFOebUvLwygmCFgQ'
    ],
    [
        'CAADAQADKAADPUHDFPP50DW3s8UCFgQ',
        'CAADAQADFwADPUHDFFlFpXlVcaH5FgQ',
        'CAADAQADGAADPUHDFAT0BrzxaShsFgQ',
        'CAADAQADGQADPUHDFCKw4iRvMvIvFgQ',
        'CAADAQADGgADPUHDFDYugNYIb5bCFgQ',
        'CAADAQADGwADPUHDFP7fQtQ71GZ0FgQ',
        'CAADAQADHAADPUHDFOebUvLwygmCFgQ'
    ]
]
liberal_board_files_id = ['CAADAQADHQADPUHDFGdPOhESIavXFgQ',
                          'CAADAQADHgADPUHDFDp-GuXHRak4FgQ',
                          'CAADAQADHwADPUHDFFc3YX2A1z8nFgQ',
                          'CAADAQADIAADPUHDFLXq6zVC0uI6FgQ',
                          'CAADAQADIQADPUHDFKMU6C1u1f0_FgQ',
                          'CAADAQADIgADPUHDFKDPYU6jlO-cFgQ']
nein_board_files_id = [
    "CAACAgEAAxkBAAIW019ahQoaeBVFqsUhoLAr7IhsSG6kAAINAAM9QcMUMckZigXYTswbBA",
    "CAACAgEAAxkBAAIW1F9ahRC8vYP3davE-94PWmhihWWLAAIOAAM9QcMUb_Hvk71c974bBA",
    "CAACAgEAAxkBAAIW1V9ahRYJBThP1zweTBzM6zhO1aBbAAIPAAM9QcMUwoncgcZQf9MbBA",
    "CAACAgEAAxkBAAIW1l9ahRnpqypyw_zp44a8ao-BfhezAAIQAAM9QcMUflRR3ijB6H4bBA"
]


def fascist_select_index(num_of_players):
    return int((num_of_players - 5) / 2)
