from pymongo import MongoClient


class Storage:
    def __init__(self, db_name, *, clear=False):
        client = MongoClient()
        if clear:
            client.drop_database(db_name)
        self.db = client.get_database(db_name)
        self.chats = self.db.get_collection("chats")

    def add_item(self, chat_id: int, item: str):
        self.chats.update_one({"chat_id": chat_id}, {
            "$addToSet": {"items": item},
        }, upsert=True)
        return self.chats.find_one({"chat_id": chat_id})
