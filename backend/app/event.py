"""Module providing a class that wraps event persistence access."""

import dataclasses
import uuid


@dataclasses.dataclass
class Event:
    """Class representing a calendar event."""

    title: str
    date: str
    event_id: str


class EventMapper:
    """Class representing an event mapper."""

    def __init__(self, cache=None) -> None:
        if cache is None:
            cache = []
        self._cache = cache

    def get_all_events(self) -> list:
        """Gets all events.

        Returns:
            A list of all events.
        """
        return self._cache

    def insert(self, title: str, date: str) -> None:
        """Creates a new event with the provided parameters and
        persists the event.

        Args:
            title: The title of the event.
            date: The date of the event.
        """
        self._cache.append(
            {
                "id": uuid.uuid4().hex,
                "title": title,
                "start": date,
            }
        )

    def update(self, event_id: str, title: str, date: str) -> None:
        """Updates the event with given id.

        Args:
            id: The id of the event.
            title: The title of the event.
            date: The date of the event.
        """
        for event in self._cache:
            if event["id"] == event_id:
                event["title"] = title
                event["start"] = date
            break

    def delete(self, event_id: str) -> None:
        """Deletes event that has provided id.

        Args:
            id: The id of event to be deleted.
        """

        # TODO: This sucks and a better solution exists.
        for event in self._cache:
            if event["id"] == event_id:
                self._cache.remove(event)
                break
