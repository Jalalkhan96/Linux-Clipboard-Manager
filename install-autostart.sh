#!/bin/bash
# Install autostart for Linux Clipboard Manager

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTOSTART_DIR="$HOME/.config/autostart"
DESKTOP_FILE="$SCRIPT_DIR/clipboard-history.desktop"

# Create autostart directory if it doesn't exist
mkdir -p "$AUTOSTART_DIR"

# Update desktop file with correct paths
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Type=Application
Name=Clipboard History
Comment=Linux Clipboard History Manager (Win+V)
Exec=$SCRIPT_DIR/.venv/bin/python $SCRIPT_DIR/main.py
Icon=edit-paste
Terminal=false
Categories=Utility;
StartupNotify=false
X-GNOME-Autostart-enabled=true
EOF

# Copy to autostart
cp "$DESKTOP_FILE" "$AUTOSTART_DIR/"

echo "✅ Autostart installed!"
echo "   Clipboard Manager will start automatically on next login."
echo ""
echo "   To start now, run:"
echo "   $SCRIPT_DIR/.venv/bin/python $SCRIPT_DIR/main.py &"
