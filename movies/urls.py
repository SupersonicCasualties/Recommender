from django.urls import path
from movies.analises.main import analise

urlpatterns = [
    path('movies', analise, name='analise')
]
