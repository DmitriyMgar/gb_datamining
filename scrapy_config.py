from pymongo import MongoClient
from gb_parse.settings import BOT_NAME

CLIENT_DB = MongoClient('localhost', 27017)[BOT_NAME]