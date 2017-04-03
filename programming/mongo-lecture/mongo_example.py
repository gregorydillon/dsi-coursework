import pymongo
MONGODB_URI = ''  # IT'S A SECRET (look in env if you want to run this...)

mc = pymongo.MongoClient(MONGODB_URI)
collection_name = 'mongodb_lecture'
database_name = pymongo.uri_parser.parse_uri(MONGODB_URI)['database']
db = mc[database_name]

coll = db[collection_name]
