from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from service.controllers import ElasticsearchController
from service.utils.logger import get_logger
from service.utils.limiter import limiter

router = APIRouter()
logger = get_logger()
elasticsearch_controller = ElasticsearchController()


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
@limiter.limit("2/minute")
async def autocomplete(
    request: Request,
    autocomplete_request: AutocompleteRequest,
    _=Depends(elasticsearch_controller.healthcheck),
):
    """
    Endpoint to perform autocomplete on Elasticsearch for the given query.
    """
    suggestions, error = elasticsearch_controller.autocomplete(
        autocomplete_request.query
    )
    if error is not None:
        logger.error(f"Error auto complete query with error={error}")
        return Response(
            "Error auto complete query",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return AutocompleteResponse(suggestions=suggestions)


@router.post("/search", response_model=SearchResult)
@limiter.limit("2/minute")
async def search(
    request: Request,
    search_request: SearchRequest,
    _=Depends(elasticsearch_controller.healthcheck),
):
    """
    Endpoint to perform a search on Elasticsearch for the given query.
    """

    res, error = elasticsearch_controller.search(search_request.query)
    if error is not None:
        logger.error(f"Error to search, query={search_request.query},error={error}")
        return Response(
            "Error to search, query", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return SearchResult(total=res["total"], hits=res["hits"])
