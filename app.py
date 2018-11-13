from flask import Flask, jsonify
from elasticsearch import Elasticsearch
from src.constants import host, port
from src import parse_data

app = Flask(__name__)

es = Elasticsearch()

@app.route('/country/<code>/')
def get_country_data(code):
    """ Get a specific country's data. """
    body = {
        'query':{
            'match':{
                'country_code': code
            }
        }
    }
    country_data = es.search(index='countries', doc_type='country', body=body)['hits']['hits']
    return jsonify(country_data)

@app.route('/country/all/')
def get_all_country_data():
    """ Get all countries data. """
    body = {
        'size': 10000,
        'query': {
            'match_all': {}
        }
    }

    all_countries = es.search(index='countries', doc_type='country', body=body)['hits']['hits']
    return jsonify(all_countries)

@app.route('/country/<code>/population/')
def get_country_population(code):
    """ Get a country's population. """
    body = {
        'query': {
            'match': {
                'country_code': code,
            }
        }
    }

    country_data = es.search(index='countries', doc_type='country', body=body)['hits']['hits']

    data = country_data[0]['_source']['data']
    for serie in data:
        if serie.get('Population, total'):
            population_data = serie
            return jsonify(population_data)
        else:
            return 404


if __name__ == '__main__':
    print("Loading ...")
    parse_data.main()
    app.run(host=host, port=port)