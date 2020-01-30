import pandas as pd
from movies.analises.query import Query
from mongoengine import connect
from django.http import JsonResponse
from movies.analises.similarity import RecomendMovie


def analise(request):

    result = {
        "data": [],
        "message": "Sucess!",
        "status": 200
    }

    data = []

    movie = request.GET.get('movie', '')

    if movie != '':
        data = recommend(movie)

    result["data"] = data

    return JsonResponse(result)


def recommend(movie):
    query = Query("movies")

    movies = query.All()

    movies = pd.DataFrame(list(movies))[:1000]

    recommendation = RecomendMovie(movie, movies)

    recommendation.make_vector()

    result = recommendation.recommend_me()

    return result
