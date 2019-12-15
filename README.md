# ShutdownHandler

## Usage
```python
from ShutdownHandler import ShutdownHandler

shutdown_handler = ShutdownHandler()

def listener_func():
    print("Shutdown from signal number: ")

shutdown_handler.add_listener(listener_func)

listener = shutdown_handler.add_listener(
    listener=lambda: print("Shutdown from signal number: "),
    priority=5
)

assert shutdown_handler.has_listener(listener)

shutdown_handler.remove_listener(listener)

assert not shutdown_handler.has_listener(listener)

```