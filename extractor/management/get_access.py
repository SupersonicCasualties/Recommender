from imdb import IMDb


class AccessApi:

    Key = ""

    def __init__(self, key):
        self.key = key[2:]

    def GetKeywords(self):
        api = IMDb()

        keywords = []

        try:
            keywords = api.get_movie_keywords(self.key)["data"]["keywords"]
        except:
            keywords = []

        return keywords
