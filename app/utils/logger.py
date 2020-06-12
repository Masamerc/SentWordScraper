import logging

mylogger = logging.getLogger(__name__)
mylogger.setLevel(logging.DEBUG)

file_format = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s: %(message)s')
file_handler = logging.FileHandler('app/utils/app.log')
file_handler.setFormatter(file_format)

mylogger.addHandler(file_handler)