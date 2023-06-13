from collections.abc import Callable


class EventSystem:
    def __init__(self, events: dict):
        self.events = events

    def add(self, name: str):
        self.events[name] = []

    def remove(self, name: str):
        self.events.pop(name)

    def handle(self, name: str, function: Callable):
        self.events[name].append(function)

    def remove_handled(self, name: str, function: Callable):
        self.events[name].remove(function)

    def trigger(self, name: str, *args):
        for event in self.events[name]:
            event(*args)

    def get_handled(self, name: str):
        return self.events.get(name)

    def __getitem__(self, name: str):
        return self.get_handled()
