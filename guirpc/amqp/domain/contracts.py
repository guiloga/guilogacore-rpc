from abc import ABC, abstractmethod
from typing import TypeVar, Callable

from .exceptions import OpeningChannelError
from .mixins import AMQPMixin
from .objects import ProxyObject

BlockingConnection = TypeVar("BlockingConnection")
Channel = TypeVar("Channel")


def channel_is_open(func) -> Callable:
    """
    Checks if he Producer channel is opened, else opens a new one.

    func (Callable): wrapped function.
    returns (Callable): the decorated function.
    """

    def wrapper(ins):
        if not ins.channel.is_open:
            new_ch = ins.open_new_channel()
            ins.channel = new_ch
        return func(ins)

    return wrapper


class ConsumerInterface(AMQPMixin, ABC):
    def __init__(
        self,
        amqp_url: str,
        max_workers: int = 4,
        prefetch_count: int = 1,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._amqp_url = amqp_url
        self._max_workers = max_workers
        self._prefetch_count = prefetch_count

    @property
    def amqp_url(self):
        return self._amqp_url

    @property
    def max_workers(self):
        return self._max_workers

    @property
    def prefetch_count(self):
        return self._prefetch_count

    @abstractmethod
    def run(self):
        pass


class ProducerInterface(AMQPMixin, ABC):
    __connection: BlockingConnection = None
    __channel: Channel = None

    def __init__(self, bk_con: BlockingConnection, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__connection = bk_con
        self.channel = self.open_new_channel()

    def __del__(self):
        try:
            self.channel.close()
        except Exception:
            pass

    @property
    def connection(self) -> BlockingConnection:
        return self.__connection

    @property
    def channel(self) -> Channel:
        return self.__channel

    @channel.setter
    def channel(self, ch_):
        self.__channel = ch_

    def open_new_channel(self) -> Channel:
        if not self.connection or not self.connection.is_open:
            raise OpeningChannelError(self.connection)

        return self.connection.channel()

    @abstractmethod
    @channel_is_open
    def publish(self, x_request: ProxyObject) -> ProxyObject:
        pass


class BaseSerializer(ABC):
    CONTENT_TYPE: str = None
    ENCODING: str = None

    @classmethod
    @abstractmethod
    def serialize(cls, obj: ProxyObject) -> str:
        pass

    @classmethod
    @abstractmethod
    def deserialize(cls, obj_str: str) -> ProxyObject:
        pass
