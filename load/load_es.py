from elasticsearch import Elasticsearch
import pandas as pd
from elasticsearch import helpers


def create_es_index_for_netflix_movies_data(es_client, index_name):
    request_body = {
        "settings": {"number_of_shards": 1, "number_of_replicas": 1},
        "mappings": {
            "properties": {
                "director": {"type": "text"},
                "duration": {"type": "text"},
            }
        },
    }
    es_client.indices.create(index=index_name, body=request_body, ignore=[400, 404])


def prepare_bulk_data(index_name):
    df = pd.read_csv("netflix_titles.csv")
    df = df.dropna()
    records = df.to_dict(orient="records")
    for record in records:
        yield {
            "_index": index_name,
            "_type": "_doc",
            "_id": record.get("show_id", None),
            "_source": {
                "title": record.get("title", ""),
                "director": record.get("director", ""),
                "description": record.get("description", ""),
                "duration": record.get("duration", ""),
                "cast": record.get("cast", ""),
            },
        }


def main(elastic_host, index_name):
    es_client = Elasticsearch(elastic_host)
    create_es_index_for_netflix_movies_data(es_client, index_name)
    bulk_data = prepare_bulk_data(index_name)
    res = helpers.bulk(es_client, bulk_data)


if __name__ == "__main__":
    elastic_host = "http://0.0.0.0:9200"
    index_name = "netflix_movies"
    main(elastic_host, index_name)
