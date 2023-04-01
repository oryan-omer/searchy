import abc


class BaseGracefulShutdown(abc.ABC):
    @abc.abstractmethod
    async def shutdown(self):
        raise NotImplemented("BASE CLASS")
