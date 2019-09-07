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


boards_method = [
    [nothing, nothing, policy_peek, execution, execution],
    [nothing, investigate_loyalty, call_special_election, execution, execution],
    [investigate_loyalty, investigate_loyalty, call_special_election, execution, execution]
]

# stickers file id
board_files_id = [
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


def select_index(num_of_players):
    return int((num_of_players - 5) / 2)
