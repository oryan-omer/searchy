from typing import Union, List, Dict

from elasticsearch import AsyncElasticsearch

from service.controllers.base import BaseGracefulShutdown, BaseSingleton
from service.utils.logger import get_logger
from service.utils.settings import settings

logger = get_logger()


class ElasticsearchController(BaseGracefulShutdown, BaseSingleton):
    instance = None

    def __init__(self, elastic_host=settings.ELASTICSEARCH_URL):
        logger.info("Starting elasticsearch...")
        self.es_client = AsyncElasticsearch(elastic_host)

    @classmethod
    async def get_instance(cls):
        if cls.instance is None:
            cls.instance = ElasticsearchController()

        return cls.instance

    async def search(self, query: str) -> (Dict, Union[str, None]):
        try:
            logger.debug(f"Searching request for query {query}")
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

            search_result = await self.es_client.search(
                index=settings.ELASTICSEARCH_INDEX, body=search_body
            )

            if search_result.get("error"):
                return [], search_result["error"]["root_cause"][0]["reason"]

            total = search_result["hits"]["total"]["value"]
            hits = [hit["_source"] for hit in search_result["hits"]["hits"]]
            return dict(total=total, hits=hits), None

        except Exception as e:
            return [], e

    async def autocomplete(self, query) -> (List[dict], Union[str, None]):
        try:
            logger.debug(f"Autocomplete request for query {query}")
            search_body = {
                "suggest": {
                    "movie-suggest": {
                        "prefix": query,
                        "completion": {
                            "field": "description",
                            "size": settings.AUTO_COMPLETION_SIZE,
                        },
                    }
                }
            }

            search_result = await self.es_client.search(
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

    async def healthcheck(self):
        try:
            await self.es_client.cluster.health()
        except Exception as e:
            logger.error(f"elasticsearch is not healthy and not available, error={e}")
            raise Exception("elasticsearch is not healthy and not available")

    async def shutdown(self):
        await self.es_client.close()


async def get_elasticsearch_controller():
    elasticsearch_controller = await ElasticsearchController.get_instance()
    await elasticsearch_controller.healthcheck()
    return elasticsearch_controller
