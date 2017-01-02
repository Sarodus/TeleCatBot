import requests
import xml.etree.ElementTree as ET

from .config import THECATAPI_KEY


class CatAPI:
    """Cat api implementation
    http://thecatapi.com/docs.html
    """

    def __init__(self):
        self.token = THECATAPI_KEY

        api_base = 'http://thecatapi.com/api/images/'

        self.url_get     = api_base + 'get?format=xml'
        self.url_like    = api_base + 'vote?api_key=%s&sub_id={id_user}&image_id={id_image}&score=10' % self.token
        self.url_dislike = api_base + 'vote?api_key=%s&sub_id={id_user}&image_id={id_image}&score=1' % self.token
        self.url_report  = api_base + 'report?api_key=%s&sub_id={id_user}&image_id={id_image}' % self.token

    def get(self):
        req = requests.get(self.url_get)
        tree = ET.ElementTree(ET.fromstring(req.text))
        image = tree.find('./data/images/image')

        return {
            'id': image.find('id').text,
            'url': image.find('url').text,
        }

    def like(self, id_image, id_user):
        url = self.url_like.format(id_image=id_image, id_user=id_user)
        requests.get(url)

    def dislike(self, id_image, id_user):
        url = self.url_dislike.format(id_image=id_image, id_user=id_user)
        requests.get(url)

    def report(self, id_image, id_user):
        url = self.url_report.format(id_image=id_image, id_user=id_user)
        requests.get(url)
