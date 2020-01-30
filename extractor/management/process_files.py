import os
import pandas as pd
from extractor.management.insert_data import BulkInsert
from time import sleep
from extractor.management.get_access import AccessApi


class ProcessFiles:

    Directory = os.path.join("extractor", "management", "data")

    """
        Metodo de processamento dos arquivos, primeiramente
        se inicia pela busca no diretorio definido entao atraves da biblioteca pandas
        se le os arquivos do tsv então somente os do tipo filme (movie) e adicionado a
        lista de titulos que então é transformada em um data frame
    """

    def Process(self):

        titles_file = os.path.join(self.Directory, "title.basics.tsv.gz")
        ratings_file = os.path.join(self.Directory, "title.ratings.tsv.gz")

        titles = []
        for chunked in pd.read_csv(titles_file, sep="\t", header=0, low_memory=False, chunksize=5000):
            aux = chunked[(chunked.titleType == "movie")]
            titles.append(aux)

        titles = pd.concat(titles)
        ratings = pd.read_csv(ratings_file, sep="\t", header=0)

        movies = titles  # [(titles.titleType == "movie")].copy()

        del titles

        movies = movies[movies["startYear"].map(lambda x: str(x) != "\\N")]

        movies.set_index("tconst", inplace=True)
        ratings.set_index("tconst", inplace=True)

        join_movies = movies.join(ratings, how="inner")

        top_movies = join_movies.sort_values(
            by="numVotes", ascending=False)[:10000]

        return self.InsertData(top_movies)

    def InsertData(self, top_movies):
        data = top_movies.to_dict("index")
        bulkInsert = BulkInsert(500, "movies")

        for key in data:
            sleep(1)

            Api = AccessApi(key)
            movie = data[key]

            print("-- Start -- \nProcessing movie: " +
                  key + " - " + movie["originalTitle"])

            movie["tconst"] = key
            movie["titleType"] = movie["titleType"]
            movie["primaryTitle"] = movie["primaryTitle"]
            movie["originalTitle"] = movie["originalTitle"]
            movie["startYear"] = int(movie["startYear"])
            movie["endYear"] = (
                None if movie["endYear"] == "\\N" else int(movie["endYear"])
            )
            movie["runtimeMinutes"] = (
                0 if movie["runtimeMinutes"] == "\\N" else int(
                    movie["runtimeMinutes"])
            )
            movie["genres"] = movie["genres"].split(',')
            movie["isAdult"] = bool(movie["isAdult"])
            movie["averageRating"] = movie["averageRating"]
            movie["numVotes"] = int(movie["numVotes"])
            movie["keywords"] = Api.GetKeywords()
            movie["proc_keywords"] = ', '.join(
                str(item) for item in movie["keywords"])

            print("Movie Processed - Inserting to Queue")

            bulkInsert.AddToQueue(movie)

            print("Finished processing the Movie \n -- END -- ")

        bulkInsert.Done()

        return True
