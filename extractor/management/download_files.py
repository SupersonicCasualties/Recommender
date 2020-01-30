import requests
import os
import urllib
from bs4 import BeautifulSoup


class Downloader():

    URL = None

    Folder = os.path.join('extractor', 'management', 'data')

    def __init__(self, url):
        self.URL = url

    """
        Processo de download, utilizando a biblioteca Requests do Python
        para pegar o conteudo da pagina de interfaces
        procurar todas as tags a retirar o conteudo do atributo href
        para os links title.basics e ratings
    """

    def InitiateDownload(self):

        if self.URL is None:
            raise Exception("Null URL!")
            return

        req = requests.get(self.URL)

        soup = BeautifulSoup(req.content, 'html.parser')

        links = soup.findAll('a')

        links = [link['href'] for link in links if 'title.basics' in link['href']
                 or 'ratings' in link['href']]

        return self.DownloadFiles(links)

    """
        Metodo que faz o download dos arquivos e os armazenas em uma pasta.
    """

    def DownloadFiles(self, links):

        if not os.path.isdir(self.Folder):
            os.mkdir(self.Folder)

        for link in links:

            file_name = link.split('/')[-1]

            file = os.path.join(self.Folder, file_name)

            if os.path.exists(file):
                continue

            urllib.request.urlretrieve(link, file)

        return True
