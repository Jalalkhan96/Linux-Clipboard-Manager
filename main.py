import signal
import sys
import threading
from storage import ClipboardStorage
from clipboard_monitor import ClipboardMonitor
from ui import ClipboardUI
from hotkey_manager import HotkeyManager

def main():
    print("Starting Linux Clipboard History Tool...")
    print("Press Win+V (Super+V) to open history.")
    print("Press Ctrl+C to exit (in terminal).")

    # 1. Init Storage
    storage = ClipboardStorage()

    # 2. Init UI (Creates root but doesn't start loop yet)
    ui = ClipboardUI(storage)

    # 3. Init Monitor (Background thread)
    monitor = ClipboardMonitor(storage)
    monitor.start()

    # 4. Init Hotkeys (Background thread/listener)
    hotkey_mgr = HotkeyManager(ui)
    hotkey_mgr.start()

    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\nExiting...")
        monitor.stop()
        hotkey_mgr.stop()
        # UI destroy is tricky if we are in mainloop, but sys.exit usually kills it
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # 5. Start UI Event Loop (Blocks main thread)
    try:
        ui.run()
    except KeyboardInterrupt:
        pass
    finally:
        monitor.stop()
        hotkey_mgr.stop()

if __name__ == "__main__":
    main()
