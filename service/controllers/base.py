import abc


class BaseGracefulShutdown(abc.ABC):
    @abc.abstractmethod
    async def shutdown(self):
        raise NotImplemented("BASE CLASS")


class BaseSingleton(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_instance(self):
        raise NotImplemented("BASE CLASS")
