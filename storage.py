from collections import deque
from typing import List, Optional
import threading

class ClipboardStorage:
    """
    Manages the history of clipboard items.
    Stores up to `max_items` distinct text entries.
    Thread-safe.
    """
    def __init__(self, max_items: int = 15):
        self.max_items = max_items
        # deque is efficient for appends and pops from both ends
        self.history: deque = deque(maxlen=max_items)
        self.lock = threading.Lock()
        # Items to skip (emojis, symbols that shouldn't be in history)
        self.skip_items: set = set()

    def add_item(self, item: str) -> None:
        """
        Add an item to history if it's not the same as the most recent item.
        Move item to top if it already exists elsewhere.
        """
        if not item or not isinstance(item, str):
            return
        
        # Check if this item should be skipped
        if item in self.skip_items:
            self.skip_items.discard(item)  # Remove from skip list
            return

        with self.lock:
            if not self.history:
                self.history.append(item)
                return

            # Check most recent item (last in deque)
            if self.history[-1] == item:
                return

            # If it exists elsewhere, remove it so we can re-add it as fresh
            try:
                self.history.remove(item)
            except ValueError:
                pass # Item not in list

            self.history.append(item)

    def get_history(self) -> List[str]:
        """
        Returns history as a list, most recent last.
        """
        with self.lock:
            return list(reversed(self.history))

    def get_item(self, index: int) -> Optional[str]:
        """Gets item by index (0 is most recent)."""
        rev_hist = self.get_history() # already locks
        if 0 <= index < len(rev_hist):
            return rev_hist[index]
        return None

    def clear(self):
        with self.lock:
            self.history.clear()
