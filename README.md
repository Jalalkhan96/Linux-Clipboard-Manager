# 📋 Linux Clipboard Manager

A lightweight, Windows 11-style clipboard history manager for Linux.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux-orange.svg)

## ✨ Features

- **🖼️ Windows 11 Style UI** - Modern Fluent Design with frosted glass effect
- **📋 Clipboard History** - Stores last 15 text items and images
- **😀 Emoji Picker** - Hundreds of emojis organized by category
- **;) Kaomoji** - Japanese emoticons collection
- **Ω Symbols** - Math, arrows, currency, and more
- **⌨️ Global Hotkey** - Press `Win+V` (Super+V) to open anywhere
- **📌 Pin Items** - Keep important items at the top
- **🚀 Auto-paste** - Click an item to paste it instantly
- **💾 Low Memory** - Uses under 30MB RAM
- **🔄 Auto-start** - Runs automatically on system boot

## 📦 Installation

### Quick Install (Ubuntu/Debian/Mint)

```bash
# Clone the repository
git clone https://github.com/Jalalkhan96/Linux-Clipboard-Manager.git
cd linux-clipboard-manager

# Run the setup script
chmod +x setup.sh
./setup.sh

# Enable autostart
./install-autostart.sh
```

### Manual Installation

```bash
# Install system dependencies
sudo apt install python3-dev python3-tk python3-venv xdotool xclip

# Create virtual environment
python3 -m venv .venv

# Install Python dependencies
./.venv/bin/pip install -r requirements.txt

# Run
./.venv/bin/python main.py
```

## 🚀 Usage

### Running Manually
```bash
./.venv/bin/python main.py
```

### Keyboard Shortcuts
| Shortcut | Action |
|----------|--------|
| `Win + V` | Open clipboard history |
| `Escape` | Close clipboard |
| `↑` / `↓` | Navigate items |
| `Enter` | Paste selected item |

### Features
- **Click** any item to paste it
- **Pin** 📌 items to keep them
- **Delete** 🗑️ items you don't need
- **Clear all** removes entire history
- Click outside window to close

## 🔧 Auto-start on Boot

The setup script creates an autostart entry. To manually enable:

```bash
cp clipboard-history.desktop ~/.config/autostart/
```

To disable autostart:
```bash
rm ~/.config/autostart/clipboard-history.desktop
```

## 📁 Project Structure

```
linux-clipboard-manager/
├── main.py              # Entry point
├── ui.py                # Windows 11 style UI
├── clipboard_monitor.py # Clipboard watcher
├── hotkey_manager.py    # Global hotkey handler
├── storage.py           # History storage
├── setup.sh             # Installation script
├── install-autostart.sh # Autostart installer
├── requirements.txt     # Python dependencies
└── clipboard-history.desktop  # Desktop entry
```

## 🔧 Requirements

- **OS**: Linux (X11) - Ubuntu, Debian, Mint, Fedora, etc.
- **Python**: 3.8+
- **Dependencies**: 
  - `python3-tk` (Tkinter)
  - `xdotool` (for auto-paste)
  - `xclip` (for image clipboard)

## ⚠️ Known Limitations

- **Wayland**: Global hotkeys may not work on Wayland. Switch to X11/Xorg session if needed.
- **Images**: Image history is not persisted across restarts.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

MIT License - feel free to use and modify!

## 🙏 Credits

Inspired by Windows 11 Clipboard (Win+V)
