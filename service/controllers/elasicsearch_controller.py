from typing import Union, List, Dict

from elasticsearch import Elasticsearch

from service.utils.logger import get_logger
from service.utils.settings import settings

logger = get_logger()


class ElasticsearchController:
    def __init__(self, elastic_host=settings.ELASTICSEARCH_URL):
        self.es_client = Elasticsearch(elastic_host)

    def search(self, query: str) -> (Dict, Union[str, None]):
        try:
            search_body = {
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["title^3", "description^2", "content"],
                        "type": "best_fields",
                        "operator": "and",
                    }
                }
            }

            search_result = self.es_client.search(
                index=settings.ELASTICSEARCH_INDEX, body=search_body
            )

            if search_result.get("error"):
                return [], search_result["error"]["root_cause"][0]["reason"]

            total = search_result["hits"]["total"]["value"]
            hits = [hit["_source"] for hit in search_result["hits"]["hits"]]
            return dict(total=total, hits=hits), None

        except Exception as e:
            return [], e

    def autocomplete(self, query) -> (List[dict], Union[str, None]):
        try:
            search_body = {
                "suggest": {
                    "text": query,
                    "completion": {
                        "field": "suggest",
                        "skip_duplicates": True,
                        "size": settings.AUTO_COMPLETION_SIZE,
                    },
                }
            }

            search_result = self.es_client.search(
                index=settings.ELASTICSEARCH_INDEX, body=search_body
            )

            if search_result.get("error"):
                return [], search_result["error"]["root_cause"][0]["reason"]

            return [
                hit["text"]
                for hit in search_result["suggest"]["completion"][0]["options"]
            ], None
        except Exception as e:
            return [], e

    def healthcheck(self):
        try:
            self.es_client.cluster.health()
        except Exception as e:
            logger.error(f"elasticsearch is not healthy and not available, error={e}")
            raise Exception("elasticsearch is not healthy and not available")
