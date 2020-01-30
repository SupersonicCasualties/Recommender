import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RecomendMovie():

    title = ""

    movies = {}

    general_vector = []

    def __init__(self, title, movies):
        self.title = title
        self.movies = movies

    def make_vector(self):
        keyword_list = self.movies['proc_keywords'].tolist()
        vector = CountVectorizer(keyword_list)
        general = vector.fit_transform(keyword_list).toarray()

        self.general_vector = general

    def recommend_me(self):
        index = self.movies[self.movies.primaryTitle ==
                            self.title].index.values[0]
        result = []

        vectors = self.general_vector
        coseno_list = []

        for i in range(len(vectors)):
            list = [vectors[index], vectors[i]]
            coseno_list.append(cosine_similarity(list)[0, 1])

        coseno_list = pd.Series(coseno_list)
        index = coseno_list.nlargest(11).index

        matches = self.movies.iloc[index]
        for mov, tconst, score in zip(matches['primaryTitle'][1:], matches['tconst'][1:], coseno_list[index][1:]):
            dic = {}
            dic["tconst"] = tconst
            dic["movie"] = mov
            dic["score"] = score
            result.append(dic)

        return result
