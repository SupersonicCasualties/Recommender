import pymongo
from recommender.settings import DB


class Query():

    instance = {}

    def __init__(self, collection):

        client = pymongo.MongoClient(DB["HOST"], DB["PORT"])

        instance = client.Movies

        self.instance = instance[collection]

    def Find(self, arguments):
        return self.instance.find(arguments)

    def All(self):
        return self.instance.find()
