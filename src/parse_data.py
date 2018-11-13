from elasticsearch import Elasticsearch
import requests
import json
from collections import OrderedDict
import pandas as pd


def main():
    """ Read, Parse data index to the elasticsearch. """

    es = Elasticsearch()

    if not es.indices.exists(index="countries"):

        df = pd.read_csv('src/world_data.csv')
        df = df.fillna(0)

        results = []

        for (country_name, country_code), bag in df.groupby(["Country Name", "Country Code"]):
            contents_df = bag.drop(["Country Name", "Country Code", "Series Name"], axis=1)
            others = [dict(row) for i,row in contents_df.iterrows()]
            series_names = bag.drop(['Country Name', 'Country Code', 'Series Code',
                               'Scale (Precision)', '1990 [YR1990]', '2000 [YR2000]', '2010 [YR2010]',
                               '2017 [YR2017]'], axis=1)
            series = [dict(row)['Series Name'] for i, row in series_names.iterrows()]

            for i, serie in enumerate(series):
                series[i] = dict([(serie, others[i])])

            results.append(OrderedDict([("country_name", country_name),
                                        ("country_code", country_code),
                                        ("data", series)]))


        countries_json = json.loads(json.dumps(results))

        for i, country in enumerate(countries_json):
            es.index(index='countries', doc_type='country', id=i, body=country)
            print("_____-_-____ Indexing, %s ______-_-__" % country['country_name'])

        es.indices.refresh('countries')

if __name__ == '__main__':
    main()