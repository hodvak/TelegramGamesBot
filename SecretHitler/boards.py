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


def fascist_select_index(num_of_players):
    return int((num_of_players - 5) / 2)
