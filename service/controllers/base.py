import abc


class BaseGracefulShutdown(abc.ABC):
    @abc.abstractmethod
    async def shutdown(self):
        raise NotImplementedError("BASE CLASS")


class BaseSingleton(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_instance(self):
        raise NotImplementedError("BASE CLASS")
