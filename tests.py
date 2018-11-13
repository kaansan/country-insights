import unittest
import requests
import json

from src.constants import host, port
from elasticsearch import Elasticsearch


class TestMain(unittest.TestCase):

    def setUp(self):
        self.es = Elasticsearch()

    def test_country_endpoint(self):
        response = requests.get('http://%s:%s/country/tur/' % (host, port)).content
        response = json.loads(response)[0]

        body = {
            'query': {
                'match': {
                    'country_code': 'tur'
                }
            }
        }
        es_data = self.es.search(index='countries', doc_type='country', body=body)['hits']['hits'][0]
        self.assertEqual(response, es_data)

    def test_all_country_endpoint(self):
        response = requests.get('http://%s:%s/country/all/' % (host, port)).content
        response = json.loads(response)

        body = {
            'size': 10000,
            'query': {
                'match_all': {}
            }
        }

        es_data = self.es.search(index='countries', doc_type='country', body=body)['hits']['hits']
        self.assertEqual(response, es_data)

    def test_count_population(self):
        response = requests.get('http://%s:%s/country/tur/' % (host, port)).content
        response = json.loads(response)
        response_population = response[0]['_source']['data'][0]

        body = {
            'query': {
                'match': {
                    'country_code': 'tur',
                }
            }
        }

        es_data = self.es.search(index='countries', doc_type='country', body=body)['hits']['hits']

        data = es_data[0]['_source']['data']
        for serie in data:
            if serie.get('Population, total'):
                es_population = serie
                self.assertEqual(response_population, es_population)


if __name__ == '__main__':
    unittest.main()