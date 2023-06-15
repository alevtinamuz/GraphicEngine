from collections.abc import Callable


class EventSystem:
    def __init__(self, events: dict) -> None:
        self.events = events

    def add(self, name: str):
        self.events[name] = []

    def remove(self, name: str):
        self.events.pop(name)

    def handle(self, name: str, func: callable):
        self.events[name].append(func)

    def remove_handled(self, name: str, func: Callable):
        self.events[name].remove(func)

    def trigger(self, name: str, *args):
        for event in self.events[name]:
            event(*args)

    def get_handled(self, name: str):
        return self.events[name]

    def __getitem__(self, name: str):
        return self.events[name]