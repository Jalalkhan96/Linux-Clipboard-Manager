import time
import threading
import pyperclip
from storage import ClipboardStorage

class ClipboardMonitor:
    """
    Monitors system clipboard for changes and updates storage.
    Run in a separate thread.
    """
    def __init__(self, storage: ClipboardStorage, interval: float = 0.5):
        self.storage = storage
        self.interval = interval
        self.running = False
        self.thread = None
        self._last_clip = ""

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)

    def _monitor_loop(self):
        # Initialize with current clipboard content
        try:
            self._last_clip = pyperclip.paste()
        except Exception as e:
            print(f"Error accessing clipboard: {e}")

        while self.running:
            try:
                current_clip = pyperclip.paste()
                if current_clip != self._last_clip:
                    self._last_clip = current_clip
                    self.storage.add_item(current_clip)
                    
                    # Print 3-line preview to terminal
                    self._print_preview(current_clip)
            except Exception as e:
                print(f"Clipboard monitor error: {e}")
            
            time.sleep(self.interval)

    def _print_preview(self, text: str):
        """Print a 3-line preview of the copied content to terminal."""
        lines = text.split('\n')
        preview_lines = []
        
        for line in lines[:3]:
            line = line.strip()
            if len(line) > 60:
                line = line[:57] + "..."
            preview_lines.append(line)
        
        # Build preview string
        preview = '\n'.join(preview_lines)
        if len(lines) > 3:
            preview += f"\n  ... ({len(lines)} total lines)"
        
        # Print with formatting
        print(f"\n{'─' * 50}")
        print(f"📋 New clipboard content:")
        print(f"{'─' * 50}")
        for line in preview_lines:
            print(f"  {line}")
        if len(lines) > 3:
            print(f"  ... ({len(lines)} total lines)")
        print(f"{'─' * 50}")
