# ShutdownHandler

## Usage
```python
from ShutdownHandler import ShutdownHandler, Signals

shutdown_handler = ShutdownHandler()

def listener_func(signal: Signals):
    print("Shutdown from signal number: ", signal)

shutdown_handler.add_listener(listener_func)

listener = shutdown_handler.add_listener(
    listener=lambda sig: print("Shutdown from signal number: ", sig),
    priority=5
)

assert shutdown_handler.has_listener(listener)

shutdown_handler.remove_listener(listener)

assert not shutdown_handler.has_listener(listener)

```