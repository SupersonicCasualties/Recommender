
import mongoengine


class Genre(mongoengine.EmbeddedDocument):
    genre = mongoengine.StringField()


class Keyword(mongoengine.EmbeddedDocument):
    Keyword = mongoengine.StringField()


class Movie(mongoengine.Document):
    titleType = mongoengine.StringField()
    primaryTitle = mongoengine.StringField()
    originalTitle = mongoengine.StringField()
    isAdult = mongoengine.BooleanField()
    startYear = mongoengine.IntField()
    endYear = mongoengine.IntField()
    runtimeMinutes = mongoengine.IntField()
    genres = mongoengine.EmbeddedDocumentField(Genre)
    averageRating = mongoengine.FloatField()
    numVotes = mongoengine.IntField()
    tconst = mongoengine.StringField()
    keywords = mongoengine.EmbeddedDocumentField(Keyword)
