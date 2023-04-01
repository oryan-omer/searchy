from starlette.requests import Request
from starlette.responses import Response

from service.controllers import get_redis_controller, get_elasticsearch_controller
from service.routers import router as app_router
from service.utils.limiter import limiter
from service.utils.logger import get_logger, LOGGING_FORMAT
from service.utils.settings import settings
from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

logger = get_logger()


@limiter.limit("80/minute")
def _health_check(request: Request):
    return Response("Searchy service is strong and healthy!")


class Searchy:
    def __init__(self):
        self.app = FastAPI()
        self.app.logger = logger
        self.app.state.limiter = limiter
        self.controllers_to_terminate = []
        self.app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
        self.app.add_event_handler("startup", self._init_controllers)
        self.app.add_event_handler("shutdown", self._terminate_controllers)
        self.app.add_api_route(f"{settings.URL_PREFIX}/health_check", _health_check)
        self._include_routers_middleware()
        self._register_routers()

    def run(self):
        logger.info(f"Starting Searchy on port {settings.APP_PORT}...")
        log_config = uvicorn.config.LOGGING_CONFIG
        log_config["formatters"]["access"]["fmt"] = LOGGING_FORMAT
        log_config["formatters"]["default"]["fmt"] = LOGGING_FORMAT
        uvicorn.run(self.app, host=settings.APP_HOST, port=settings.APP_PORT)

    def _register_routers(self):
        self.app.include_router(app_router, prefix=settings.URL_PREFIX)

    def _include_routers_middleware(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    async def _init_controllers(self):
        logger.info("Init Controllers..")
        redis_controller = await get_redis_controller()
        await redis_controller.init_async_client()
        elasticsearch_controllers = await get_elasticsearch_controller()
        self.controllers_to_terminate.append(redis_controller)
        self.controllers_to_terminate.append(elasticsearch_controllers)

    async def _terminate_controllers(self):
        logger.info("Terminating controllers safely...")
        for controller in self.controllers_to_terminate:
            await controller.shutdown()
