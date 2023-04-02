from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from service.controllers import get_redis_controller, get_elasticsearch_controller
from service.utils.logger import get_logger
from service.utils.limiter import limiter
from service.utils.utils import is_in_cache

router = APIRouter()
logger = get_logger()


class AutocompleteRequest(BaseModel):
    query: str


class AutocompleteResponse(BaseModel):
    suggestions: List[str]


class SearchRequest(BaseModel):
    query: str


class SearchResult(BaseModel):
    total: int
    hits: List[dict]


@router.post("/autocomplete", response_model=AutocompleteResponse)
@limiter.limit("10/minute")
async def autocomplete(
    request: Request,
    autocomplete_request: AutocompleteRequest,
    redis_controller=Depends(get_redis_controller),
    elasticsearch_controller=Depends(get_elasticsearch_controller),
):
    """
    Endpoint to perform autocomplete on Elasticsearch for the given query.
    """
    if not (
        suggestions := await is_in_cache(redis_controller, autocomplete_request.query)
    ):
        suggestions, error = elasticsearch_controller.autocomplete(
            autocomplete_request.query
        )
        if error is not None:
            logger.error(f"Error auto complete query with error={error}")
            return Response(
                "Error auto complete query",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        await redis_controller.set(autocomplete_request.query, suggestions)

    return AutocompleteResponse(suggestions=suggestions)


@router.post("/search", response_model=SearchResult)
@limiter.limit("10/minute")
async def search(
    request: Request,
    search_request: SearchRequest,
    redis_controller=Depends(get_redis_controller),
    elasticsearch_controller=Depends(get_elasticsearch_controller),
):
    """
    Endpoint to perform a search on Elasticsearch for the given query.
    """
    if not (res := await is_in_cache(redis_controller, search_request.query)):
        res, error = await elasticsearch_controller.search(search_request.query)
        if error is not None:
            logger.error(f"Error to search, query={search_request.query},error={error}")
            return Response(
                "Error to search, query",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        await redis_controller.set(search_request.query, res)
    return SearchResult(total=res["total"], hits=res["hits"])
