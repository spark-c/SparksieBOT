import logging


logger: logging.Logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler: logging.FileHandler = logging.FileHandler(
    filename='discord.log',
    encoding='utf-8',
    mode='w'
    )
handler.setFormatter(
    logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(message)s'
        )
    )
logger.addHandler(handler)