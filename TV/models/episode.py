from mongoengine import Document, IntField, StringField, FloatField, connect
from pymongo import UpdateOne

class Episode(Document):
    title = StringField(required=True)
    show = StringField(required=True)
    rating = FloatField(required=True)
    votes = IntField(required=True)


def bulk_upsert(episodes):
    bulk_operations = []
    for entity in episodes:
        try:
            entity.validate()
            filter = {
                'title': entity.title,
                'show': entity.show
            }
            bulk_operations.append(
                UpdateOne(filter, {'$set': entity.to_mongo().to_dict()}, upsert=True)
            )

        except ValidationError:
            pass

    if bulk_operations:
        with connect("tvdb") as c: 
            collection = Episode._get_collection().bulk_write(bulk_operations, ordered=False)