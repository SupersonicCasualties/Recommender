from django.urls import path
from extractor.management.main import start_extractor

urlpatterns = [
    path('extractData', start_extractor, name='extract_data')
]
