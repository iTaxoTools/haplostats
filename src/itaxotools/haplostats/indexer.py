from __future__ import annotations


class StringIndexer:
    """Assign unique id to strings"""

    def __init__(self):
        self.string_to_id = {}
        self.id_to_string = {}
        self.current_id = 0

    def add(self, string: str) -> int:
        if string not in self.string_to_id:
            self.string_to_id[string] = self.current_id
            self.id_to_string[self.current_id] = string
            self.current_id += 1
        return self.string_to_id[string]

    def all(self) -> iter[tuple[int, str]]:
        return ((k, v) for k, v in self.id_to_string.items())

    def __len__(self) -> int:
        return self.current_id
