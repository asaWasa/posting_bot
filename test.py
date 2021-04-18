from database.mongodb.mongodriver import MongoDriver

db = MongoDriver('posting_bot', 'invite_keys')

db.push({'invite_key': '1'})
