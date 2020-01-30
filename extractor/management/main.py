import pymongo
from django.http import JsonResponse
from extractor.management.download_files import Downloader
from extractor.management.process_files import ProcessFiles
from extractor.models import models

"""
    Método chamado quando um ponto da API é atingido,
    primeiro instancia o objeto data para o retorno.
    cria um objeto da classe Extractor
    e manda ele fazer o download
"""


def start_extractor(request):
    data = {
        "data": [],
        "message": "success",
        "status": 200
    }

    ext = Extractor(request)

    response = ext.DownloadFiles()

    if response is False:
        data["message"] = "An error occured while processing the files"
        data["status"] = 400

    return JsonResponse(data)


class Extractor():

    __INTERFACE_URL__ = "https://datasets.imdbws.com/"

    request = {}

    def __init__(self, request):
        self.request = request

    def DownloadFiles(self):
        dwl_files = Downloader(self.__INTERFACE_URL__)

        processed = False

        downloaded = dwl_files.InitiateDownload()

        if downloaded:
            processed = ProcessFiles().Process()

        return processed
