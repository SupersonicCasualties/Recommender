import pymongo
from collections import defaultdict


class BulkInsert:

    queue = defaultdict(list)
    chunk_size = 0
    collection = ""

    def __init__(self, chunk_size, collection):
        self.chunk_size = chunk_size
        self.queue = defaultdict(list)
        self.collection = collection

    def AddToQueue(self, obj):
        model_key = self.collection

        self.queue[model_key].append(obj)
        print("Movie inserted on queue")
        if len(self.queue[model_key]) >= self.chunk_size:
            self.Commit()

        print("Queue size: ", len(
            self.queue[model_key]), " of ", self.chunk_size)

    def Commit(self):
        model_key = self.collection

        model_class = self.GetDbInstance()

        model_class.insert_many(self.queue[model_key])

        self.queue[model_key] = []

        print("Commiting movies to the collection")

    def Done(self):
        for objs in self.queue.items():
            if len(objs) > 0:
                self.Commit()

    def GetDbInstance(self):
        client = pymongo.MongoClient('localhost', 27017)

        db = client.Movies

        collection = db[self.collection]

        return collection

# def ProcessFiles(self):

#         dict = ProcessFiles().Process()

#         client = pymongo.MongoClient('localhost', 27017)

#         db = client.Movies

#         collection = db.movies

#         collection.insert_many(dict)
