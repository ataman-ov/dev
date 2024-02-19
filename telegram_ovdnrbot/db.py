from pymongo import MongoClient
import constants

db = MongoClient(constants.MONGO_LINK)[constants.MONGO_DB]

def get_or_create_user(db, effective_user, message):
        user = db.users.find_one({"user_id": effective_user.id, "userName": "{}".format(effective_user.username)})
        if not user:
            user = {
                "user_id": effective_user.id,
                "first_name": effective_user.first_name,
                "last_name": effective_user.last_name,
                "username": effective_user.username,
                "chat_id": message.chat_id,
            }
            db.users.insert_one(user)
        return user