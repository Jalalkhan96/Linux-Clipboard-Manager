from pynput import keyboard
from ui import ClipboardUI
import threading

class HotkeyManager:
    """
    Listens for global hotkeys to trigger the UI.
    Default: <ctrl>+<alt>+v
    """
    def __init__(self, ui: ClipboardUI):
        self.ui = ui
        self.listener = None

    def start(self):
        # We need to run pynput in a non-blocking way for the main thread, 
        # but pynput.keyboard.GlobalHotKeys runs in its own thread usually.
        # We'll use the GlobalHotKeys helper.
        
        self.listener = keyboard.GlobalHotKeys({
            '<cmd>+v': self._on_activate  # Super/Win + V
        })
        self.listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()

    def _on_activate(self):
        # The hotkey callback runs in a separate thread.
        # We need to signal the UI thread to toggle visibility.
        # Direct calls to Tkinter from other threads can be unsafe, but simple 
        # operations often work. Ideally, we would use a thread-safe queue.
        # For now, we attempt to call the UI toggle method which handles queueing 
        # or state updates safely.
        
        print("Hotkey detected!") 
        # We need to signal the UI thread.
        # We will assume we can call a method on UI that handles thread safety if needed
        # OR we rely on the fact that we'll design Main to poll or UI to be robust.
        
        # For now, let's just callback.
        if hasattr(self.ui, 'toggle'):
            self.ui.toggle()
        else:
            self.ui.show()
