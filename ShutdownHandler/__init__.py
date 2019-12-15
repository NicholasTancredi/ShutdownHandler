from typing import Optional, List, Callable, Any, Union, NamedTuple
import signal
import sys
import logging
from types import FrameType
from time import sleep
from enum import Enum


class Signals(int, Enum):
    SIGHUP: int = int(signal.SIGHUP)
    SIGINT: int = int(signal.SIGINT)
    SIGQUIT: int = int(signal.SIGQUIT)
    SIGABRT: int = int(signal.SIGABRT)
    SIGTERM: int = int(signal.SIGTERM)

    @staticmethod
    def get_name_by_value(value: int):
        for key, v in Signals.__members__.items():
            if value == v:
                return key
        raise ValueError("Invalid Signals value")


ShutdownListenerFunctionType = Callable[[], Any]


class ShutdownListener(NamedTuple):
    function: ShutdownListenerFunctionType
    priority: int


class ShutdownHandler:
    _listeners: List[ShutdownListener]

    def __init__(self, listeners: Optional[List[ShutdownListener]] = None):
        self._listeners = listeners if listeners else []

        for signal_enum in Signals.__members__.values():
            signal.signal(signal_enum, self._handler)

    def has_listener(self, listener: ShutdownListener) -> bool:
        for _listener in self._listeners:
            if listener == _listener:
                return True
        return False

    def add_listener(self,
                     listener: Union[ShutdownListener, ShutdownListenerFunctionType],
                     priority: int = 0) -> ShutdownListener:
        if not isinstance(listener, ShutdownListener):
            _listener = ShutdownListener(function=listener, priority=priority)
        else:
            _listener = listener
        if self.has_listener(_listener):
            logging.warning('Listener has already been added.')
            return _listener
        self._listeners.append(_listener)
        return _listener

    def remove_listener(self, listener: ShutdownListener):
        self._listeners.remove(listener)

    @staticmethod
    def _listener_sort(listener: ShutdownListener):
        return listener.priority

    def _handler(self, signal_enum: Signals, _: FrameType):
        self._listeners.sort(key=self._listener_sort, reverse=True)

        try:
            sig_info = Signals.get_name_by_value(signal_enum)
        except Exception as e:
            logging.error(e)
            sig_info = signal_enum

        logging.warning(f'Shutting signal: {sig_info}')

        for listener in self._listeners:
            try:
                listener.function()
            except Exception as e:
                logging.error(e)

        sys.exit(signal_enum)


if __name__ == '__main__':
    def main():
        shutdown_handler = ShutdownHandler()
        listener = shutdown_handler.add_listener(lambda: print("Shut down from signal: "), priority=5)
        assert shutdown_handler.has_listener(listener)
        shutdown_handler.remove_listener(listener)
        assert not shutdown_handler.has_listener(listener)

        listener = shutdown_handler.add_listener(ShutdownListener(lambda: print(2), 24))
        listener_remove = shutdown_handler.add_listener(ShutdownListener(lambda: print(1), 4))
        shutdown_handler.remove_listener(listener_remove)
        assert not shutdown_handler.has_listener(listener_remove)
        assert not shutdown_handler.has_listener(ShutdownListener(lambda: print(99), -1))
        assert shutdown_handler.has_listener(listener)
        while True:
            sleep(1)
    main()

