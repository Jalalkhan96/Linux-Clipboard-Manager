import tkinter as tk
from tkinter import ttk
import pyperclip
import queue
import subprocess
import time
import tempfile
from PIL import Image, ImageTk, ImageGrab
from pynput import mouse
from storage import ClipboardStorage

class ClipboardUI:
    """
    Windows 11 Fluent Design clipboard manager.
    Features frosted glass effect, rounded cards, and smooth interactions.
    """
    
    # Windows 11 Fluent Design - Light Theme
    COLORS = {
        # Acrylic/Mica backgrounds
        'acrylic_bg': '#f5f5f5',          # Main frosted background
        'acrylic_tint': '#ffffff',         # Card background
        'surface': '#fafafa',              # Content surface
        
        # Semantic colors
        'accent': '#0067c0',               # Windows blue
        'accent_light': '#0078d4',
        'accent_hover': '#1a86d9',
        
        # Text hierarchy
        'text_primary': '#202020',
        'text_secondary': '#5d5d5d',
        'text_tertiary': '#868686',
        'text_disabled': '#a0a0a0',
        
        # Borders and dividers
        'border': '#e5e5e5',
        'border_strong': '#d1d1d1',
        'divider': '#ebebeb',
        
        # States
        'hover': '#f0f0f0',
        'pressed': '#e8e8e8',
        'selected': '#e6f2fb',
        'card_hover': '#fafafa',
        
        # Semantic
        'danger': '#c42b1c',
        'success': '#0f7b0f',
    }
    
    # Tab configuration
    TABS = [
        {'id': 'clipboard', 'icon': '📋', 'label': 'Clipboard'},
        {'id': 'emoji', 'icon': '😊', 'label': 'Emoji'},
        {'id': 'gif', 'icon': 'GIF', 'label': 'GIF'},
        {'id': 'kaomoji', 'icon': ';)', 'label': 'Kaomoji'},
        {'id': 'symbols', 'icon': 'Ω', 'label': 'Symbols'},
    ]
    
    EMOJIS = {
        'Smileys': '😀😃😄😁😅😂🤣😊😇🙂🙃😉😌😍🥰😘😗😙😚😋😛😜🤪😝🤑🤗🤭🤫🤔🤐🤨😐😑😶😏😒🙄😬😮‍💨🤥😌😔😪🤤😴😷🤒🤕🤢🤮🤧🥵🥶🥴😵🤯🤠🥳🥸😎🤓🧐😕😟🙁☹️😮😯😲😳🥺😦😧😨😰😥😢😭😱😖😣😞😓😩😫🥱😤😡😠🤬',
        'Gestures': '👋🤚🖐️✋🖖👌🤌🤏✌️🤞🫰🤟🤘🤙👈👉👆🖕👇☝️🫵👍👎✊👊🤛🤜👏🙌🫶👐🤲🤝🙏✍️💅🤳💪🦾',
        'Hearts': '❤️🧡💛💚💙💜🖤🤍🤎💔❤️‍🔥❤️‍🩹❣️💕💞💓💗💖💘💝',
        'Animals': '🐶🐱🐭🐹🐰🦊🐻🐼🐻‍❄️🐨🐯🦁🐮🐷🐸🐵🐔🐧🐦🐤🦆🦅🦉🦇🐺🐗🐴🦄🐝🐛🦋🐌🐞🐜',
        'Objects': '⌚📱💻⌨️🖥️🖨️🖱️💽💾💿📀🎥📷📸📹📼🔍🔎💡🔦🏮📔📕📖📗📘📙📚📓📒📃📜📄📰',
        'Symbols': '❤️💯✅❌⭕🔴🟠🟡🟢🔵🟣⚫⚪🟤▪️▫️◾◽◼️◻️⬛⬜🔶🔷🔸🔹🔺🔻💠🔲🔳⚠️🚫♻️✔️☑️➡️⬅️⬆️⬇️↗️↘️↙️↖️↕️↔️🔄',
    }
    
    KAOMOJI = [
        '(◕‿◕)', '(◠‿◠)', '(◕ᴗ◕✿)', '╰(*°▽°*)╯', '(っ◔◡◔)っ',
        '(◕‿◕)♡', '(♡´▽`♡)', '(*˘︶˘*).｡.:*♡', '(灬♥ω♥灬)',
        '¯\\_(ツ)_/¯', '(ಠ_ಠ)', '(；一_一)', '(-_-) zzZ',
        '(╯°□°）╯︵ ┻━┻', '┬─┬ノ( º _ ºノ)', '(ノಠ益ಠ)ノ彡┻━┻',
        '(´;ω;`)', '(T_T)', '(ಥ﹏ಥ)', '(つ﹏⊂)',
        '٩(◕‿◕｡)۶', '(ノ◕ヮ◕)ノ*:・゚✧', 'ヽ(>∀<☆)☆',
        '( •_•)>⌐■-■', '(⌐■_■)', '(•ω•)', '(◕‿◕)',
    ]
    
    SYMBOLS = '±×÷≠≈≤≥∞∑π√∫∮αβγδεθλμσφω←→↑↓↔↕⇐⇒⇔$€£¥₹₿©®™•…†‡§¶°′″'
    
    def __init__(self, storage: ClipboardStorage):
        self.storage = storage
        self.root = tk.Tk()
        self.root.title("Clipboard")
        self.root.withdraw()
        
        # Window configuration
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        
        # Frosted glass transparency
        try:
            self.root.attributes('-alpha', 0.92)
        except:
            pass
        
        self.queue = queue.Queue()
        self.current_tab = 'clipboard'
        self.is_pinned = False
        self.pinned_items = set()
        self.image_history = []
        self.is_visible = False
        
        self._drag_x = 0
        self._drag_y = 0
        
        # Typography
        self.fonts = {
            'header': ('Segoe UI', 13, 'bold'),
            'title': ('Segoe UI', 11),
            'body': ('Segoe UI', 10),
            'small': ('Segoe UI', 9),
            'caption': ('Segoe UI', 8),
            'icon': ('Segoe UI', 12),
            'emoji': ('Segoe UI Emoji', 18),
            'emoji_small': ('Segoe UI Emoji', 14),
            'tab_icon': ('Segoe UI Emoji', 12),
        }
        
        # Global mouse listener for click-outside detection
        self.mouse_listener = mouse.Listener(on_click=self._on_global_click)
        self.mouse_listener.start()

    def _on_global_click(self, x, y, button, pressed):
        """Handle global mouse clicks to close window when clicking outside."""
        if pressed and self.is_visible and not self.is_pinned:
            try:
                # Get window bounds
                win_x = self.root.winfo_rootx()
                win_y = self.root.winfo_rooty()
                win_w = self.root.winfo_width()
                win_h = self.root.winfo_height()
                
                # Check if click is outside window
                if x < win_x or x > win_x + win_w or y < win_y or y > win_y + win_h:
                    # Schedule hide on main thread
                    self.root.after(10, self._hide_window)
            except:
                pass

    def _hide_window(self):
        """Hide the window."""
        self.is_visible = False
        self.root.withdraw()

    def run(self):
        self._check_queue()
        self._check_image_clipboard()
        self.root.mainloop()

    def _check_queue(self):
        try:
            while True:
                msg = self.queue.get_nowait()
                if msg == 'show':
                    self._show_window()
        except queue.Empty:
            pass
        self.root.after(100, self._check_queue)

    def _check_image_clipboard(self):
        try:
            img = ImageGrab.grabclipboard()
            if img and isinstance(img, Image.Image):
                img_hash = hash(img.tobytes())
                if not hasattr(self, '_last_img_hash') or self._last_img_hash != img_hash:
                    self._last_img_hash = img_hash
                    thumb = img.copy()
                    thumb.thumbnail((80, 80))
                    self.image_history.insert(0, {'image': img, 'thumbnail': thumb})
                    self.image_history = self.image_history[:10]
        except:
            pass
        self.root.after(500, self._check_image_clipboard)

    def toggle(self):
        self.queue.put('show')

    def _show_window(self):
        self._build_layout()
        
        # Dimensions
        width = 380
        height = 440
        
        # Center on screen
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - width) // 2
        y = (sh - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.is_visible = True
        
        # Escape to close
        self.root.bind("<Escape>", lambda e: self._hide_window())

    def _start_drag(self, e):
        self._drag_x = e.x
        self._drag_y = e.y

    def _do_drag(self, e):
        x = self.root.winfo_x() + e.x - self._drag_x
        y = self.root.winfo_y() + e.y - self._drag_y
        self.root.geometry(f"+{x}+{y}")

    def _build_layout(self):
        for w in self.root.winfo_children():
            w.destroy()
        
        # Main container with rounded appearance simulation
        main = tk.Frame(self.root, bg=self.COLORS['acrylic_bg'])
        main.pack(fill=tk.BOTH, expand=True)
        
        # Outer border for glass effect
        border = tk.Frame(main, bg=self.COLORS['border'], padx=1, pady=1)
        border.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        inner = tk.Frame(border, bg=self.COLORS['acrylic_bg'])
        inner.pack(fill=tk.BOTH, expand=True)
        
        # === DRAG HANDLE ===
        handle = tk.Frame(inner, bg=self.COLORS['acrylic_bg'], height=12, cursor='fleur')
        handle.pack(fill=tk.X)
        handle.bind("<Button-1>", self._start_drag)
        handle.bind("<B1-Motion>", self._do_drag)
        
        # Handle indicator
        handle_line = tk.Frame(handle, bg=self.COLORS['border_strong'], width=36, height=4)
        handle_line.place(relx=0.5, rely=0.5, anchor='center')
        
        # === TAB BAR ===
        tab_frame = tk.Frame(inner, bg=self.COLORS['acrylic_bg'])
        tab_frame.pack(fill=tk.X, padx=16, pady=(4, 12))
        
        for tab in self.TABS:
            is_active = self.current_tab == tab['id']
            
            tab_btn = tk.Frame(tab_frame, bg=self.COLORS['acrylic_bg'], cursor='hand2')
            tab_btn.pack(side=tk.LEFT, padx=2)
            
            # Icon
            icon_color = self.COLORS['accent'] if is_active else self.COLORS['text_tertiary']
            icon_label = tk.Label(
                tab_btn,
                text=tab['icon'],
                bg=self.COLORS['acrylic_bg'],
                fg=icon_color,
                font=self.fonts['tab_icon'] if tab['icon'] in ['📋', '😊'] else self.fonts['small'],
                padx=8,
                pady=6
            )
            icon_label.pack()
            
            # Active indicator
            if is_active:
                indicator = tk.Frame(tab_btn, bg=self.COLORS['accent'], height=2, width=20)
                indicator.pack()
            
            # Bindings
            for widget in [tab_btn, icon_label]:
                widget.bind("<Button-1>", lambda e, t=tab['id']: self._switch_tab(t))
                widget.bind("<Enter>", lambda e, f=tab_btn: self._tab_hover(f, True))
                widget.bind("<Leave>", lambda e, f=tab_btn: self._tab_hover(f, False))
        
        # === HEADER ===
        header = tk.Frame(inner, bg=self.COLORS['acrylic_bg'])
        header.pack(fill=tk.X, padx=16, pady=(0, 8))
        
        # Title
        title_text = next((t['label'] for t in self.TABS if t['id'] == self.current_tab), 'Clipboard')
        
        title = tk.Label(
            header,
            text=title_text,
            bg=self.COLORS['acrylic_bg'],
            fg=self.COLORS['text_primary'],
            font=self.fonts['header']
        )
        title.pack(side=tk.LEFT)
        
        # Actions
        if self.current_tab == 'clipboard':
            # Clear all button
            clear_btn = tk.Label(
                header,
                text="Clear all",
                bg=self.COLORS['acrylic_bg'],
                fg=self.COLORS['accent'],
                font=self.fonts['small'],
                cursor='hand2',
                padx=10,
                pady=4
            )
            clear_btn.pack(side=tk.RIGHT)
            clear_btn.bind("<Button-1>", lambda e: self._clear_all())
            clear_btn.bind("<Enter>", lambda e: clear_btn.configure(fg=self.COLORS['accent_hover']))
            clear_btn.bind("<Leave>", lambda e: clear_btn.configure(fg=self.COLORS['accent']))
        
        # Pin toggle
        pin_color = self.COLORS['accent'] if self.is_pinned else self.COLORS['text_tertiary']
        self.pin_btn = tk.Label(
            header,
            text="📌" if self.is_pinned else "📍",
            bg=self.COLORS['acrylic_bg'],
            fg=pin_color,
            font=self.fonts['emoji_small'],
            cursor='hand2'
        )
        self.pin_btn.pack(side=tk.RIGHT, padx=8)
        self.pin_btn.bind("<Button-1>", lambda e: self._toggle_pin())
        
        # === CONTENT ===
        content = tk.Frame(inner, bg=self.COLORS['surface'])
        content.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))
        
        # Route to content builder
        if self.current_tab == 'clipboard':
            self._build_clipboard(content)
        elif self.current_tab == 'emoji':
            self._build_emoji(content)
        elif self.current_tab == 'kaomoji':
            self._build_kaomoji(content)
        elif self.current_tab == 'symbols':
            self._build_symbols(content)
        else:
            self._build_placeholder(content, self.current_tab)

    def _tab_hover(self, frame, hover):
        bg = self.COLORS['hover'] if hover else self.COLORS['acrylic_bg']
        frame.configure(bg=bg)
        for child in frame.winfo_children():
            try:
                child.configure(bg=bg)
            except:
                pass

    def _switch_tab(self, tab_id):
        self.current_tab = tab_id
        self._build_layout()

    def _toggle_pin(self):
        self.is_pinned = not self.is_pinned
        color = self.COLORS['accent'] if self.is_pinned else self.COLORS['text_tertiary']
        self.pin_btn.configure(
            text="📌" if self.is_pinned else "📍",
            fg=color
        )

    def _clear_all(self):
        self.storage.clear()
        self.image_history.clear()
        self.pinned_items.clear()
        self._build_layout()

    def _build_clipboard(self, parent):
        # Scrollable container
        canvas = tk.Canvas(parent, bg=self.COLORS['surface'], highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=self.COLORS['surface'])
        
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor='nw', width=348)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mouse wheel scrolling (safe - check if canvas exists)
        def safe_scroll_up(e):
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(-1, "units")
            except:
                pass
        
        def safe_scroll_down(e):
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(1, "units")
            except:
                pass
        
        canvas.bind("<Button-4>", safe_scroll_up)
        canvas.bind("<Button-5>", safe_scroll_down)
        scroll_frame.bind("<Button-4>", safe_scroll_up)
        scroll_frame.bind("<Button-5>", safe_scroll_down)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Images first
        for i, img_data in enumerate(self.image_history[:3]):
            self._create_image_card(scroll_frame, i, img_data)
        
        # Text items
        history = self.storage.get_history()
        
        if not history and not self.image_history:
            self._show_empty(scroll_frame)
            return
        
        for idx, item in enumerate(history[:15]):
            self._create_text_card(scroll_frame, idx, item)

    def _show_empty(self, parent):
        empty = tk.Frame(parent, bg=self.COLORS['surface'])
        empty.pack(fill=tk.BOTH, expand=True, pady=50)
        
        tk.Label(
            empty,
            text="📋",
            bg=self.COLORS['surface'],
            font=('Segoe UI Emoji', 36)
        ).pack()
        
        tk.Label(
            empty,
            text="Your clipboard is empty",
            bg=self.COLORS['surface'],
            fg=self.COLORS['text_secondary'],
            font=self.fonts['body']
        ).pack(pady=(12, 4))
        
        tk.Label(
            empty,
            text="Items you copy will appear here",
            bg=self.COLORS['surface'],
            fg=self.COLORS['text_tertiary'],
            font=self.fonts['caption']
        ).pack()

    def _create_image_card(self, parent, idx, img_data):
        card = tk.Frame(parent, bg=self.COLORS['acrylic_tint'], cursor='hand2')
        card.pack(fill=tk.X, pady=3, padx=4)
        
        inner = tk.Frame(card, bg=self.COLORS['acrylic_tint'])
        inner.pack(fill=tk.X, padx=12, pady=10)
        
        # Thumbnail
        try:
            photo = ImageTk.PhotoImage(img_data['thumbnail'])
            img_label = tk.Label(inner, image=photo, bg=self.COLORS['acrylic_tint'])
            img_label.image = photo
            img_label.pack(side=tk.LEFT, padx=(0, 10))
        except:
            pass
        
        # Info
        size = img_data['image'].size
        info = tk.Label(
            inner,
            text=f"Image • {size[0]}×{size[1]}",
            bg=self.COLORS['acrylic_tint'],
            fg=self.COLORS['text_primary'],
            font=self.fonts['body']
        )
        info.pack(side=tk.LEFT)
        
        # Actions
        self._add_card_actions(inner, idx, img_data, is_image=True)
        
        # Hover effects
        self._bind_card_hover(card, inner, lambda: self._paste_image(img_data['image']))

    def _create_text_card(self, parent, idx, item):
        is_pinned = idx in self.pinned_items
        
        card = tk.Frame(parent, bg=self.COLORS['acrylic_tint'], cursor='hand2')
        card.pack(fill=tk.X, pady=3, padx=4)
        
        # Accent border for pinned items
        if is_pinned:
            card.configure(highlightbackground=self.COLORS['accent'], highlightthickness=1)
        
        inner = tk.Frame(card, bg=self.COLORS['acrylic_tint'])
        inner.pack(fill=tk.X, padx=12, pady=10)
        
        # Text preview (2 lines)
        lines = item.split('\n')[:2]
        preview = []
        for line in lines:
            line = line.strip()
            if len(line) > 38:
                line = line[:35] + '...'
            if line:
                preview.append(line)
        text = '\n'.join(preview) if preview else '(empty)'
        
        text_label = tk.Label(
            inner,
            text=text,
            bg=self.COLORS['acrylic_tint'],
            fg=self.COLORS['text_primary'],
            font=self.fonts['body'],
            anchor='w',
            justify=tk.LEFT,
            wraplength=240
        )
        text_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Actions
        self._add_card_actions(inner, idx, item, is_image=False)
        
        # Hover effects
        self._bind_card_hover(card, inner, lambda t=item: self._paste_text(t))

    def _add_card_actions(self, parent, idx, item, is_image=False):
        actions = tk.Frame(parent, bg=self.COLORS['acrylic_tint'])
        actions.pack(side=tk.RIGHT)
        
        if not is_image:
            # Pin button
            pin_text = "📌" if idx in self.pinned_items else "📍"
            pin_color = self.COLORS['accent'] if idx in self.pinned_items else self.COLORS['text_disabled']
            
            pin_btn = tk.Label(
                actions,
                text=pin_text,
                bg=self.COLORS['acrylic_tint'],
                fg=pin_color,
                font=self.fonts['emoji_small'],
                cursor='hand2'
            )
            pin_btn.pack(side=tk.LEFT, padx=2)
            pin_btn.bind("<Button-1>", lambda e, i=idx, b=pin_btn: self._toggle_item_pin(i, b))
        
        # Delete button
        del_btn = tk.Label(
            actions,
            text="🗑",
            bg=self.COLORS['acrylic_tint'],
            fg=self.COLORS['text_disabled'],
            font=self.fonts['emoji_small'],
            cursor='hand2'
        )
        del_btn.pack(side=tk.LEFT, padx=2)
        
        if is_image:
            del_btn.bind("<Button-1>", lambda e, i=idx: self._delete_image(i))
        else:
            del_btn.bind("<Button-1>", lambda e, i=item: self._delete_item(i))
        
        del_btn.bind("<Enter>", lambda e: del_btn.configure(fg=self.COLORS['danger']))
        del_btn.bind("<Leave>", lambda e: del_btn.configure(fg=self.COLORS['text_disabled']))

    def _bind_card_hover(self, card, inner, click_action):
        def on_enter(e):
            card.configure(bg=self.COLORS['card_hover'])
            inner.configure(bg=self.COLORS['card_hover'])
            for w in inner.winfo_children():
                try: w.configure(bg=self.COLORS['card_hover'])
                except: pass
        
        def on_leave(e):
            card.configure(bg=self.COLORS['acrylic_tint'])
            inner.configure(bg=self.COLORS['acrylic_tint'])
            for w in inner.winfo_children():
                try: w.configure(bg=self.COLORS['acrylic_tint'])
                except: pass
        
        for widget in [card, inner] + list(inner.winfo_children()):
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            if not isinstance(widget, tk.Frame) or widget == card:
                widget.bind("<Button-1>", lambda e: click_action())

    def _toggle_item_pin(self, idx, btn):
        if idx in self.pinned_items:
            self.pinned_items.discard(idx)
            btn.configure(text="📍", fg=self.COLORS['text_disabled'])
        else:
            self.pinned_items.add(idx)
            btn.configure(text="📌", fg=self.COLORS['accent'])
        self._build_layout()

    def _delete_item(self, item):
        try:
            self.storage.history.remove(item)
        except:
            pass
        self._build_layout()

    def _delete_image(self, idx):
        try:
            del self.image_history[idx]
        except:
            pass
        self._build_layout()

    def _paste_text(self, text):
        try:
            pyperclip.copy(text)
            if not self.is_pinned:
                self.root.withdraw()
            time.sleep(0.12)
            subprocess.run(['xdotool', 'key', 'ctrl+v'], timeout=2)
            print(f"✓ Pasted")
        except Exception as e:
            print(f"Error: {e}")

    def _paste_image(self, img):
        try:
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
                img.save(f.name, 'PNG')
                subprocess.run(['xclip', '-selection', 'clipboard', '-t', 'image/png', '-i', f.name], timeout=2)
            if not self.is_pinned:
                self.root.withdraw()
            time.sleep(0.12)
            subprocess.run(['xdotool', 'key', 'ctrl+v'], timeout=2)
            print(f"✓ Image pasted")
        except Exception as e:
            print(f"Error: {e}")

    def _paste_emoji(self, emoji):
        try:
            if not self.is_pinned:
                self.root.withdraw()
            time.sleep(0.08)
            subprocess.run(['xdotool', 'type', '--clearmodifiers', emoji], timeout=2)
            print(f"✓ {emoji}")
        except:
            try:
                self.storage.skip_items.add(emoji)
                pyperclip.copy(emoji)
                time.sleep(0.08)
                subprocess.run(['xdotool', 'key', 'ctrl+v'], timeout=2)
            except:
                pass

    def _build_emoji(self, parent):
        # Category selector
        cat_frame = tk.Frame(parent, bg=self.COLORS['surface'])
        cat_frame.pack(fill=tk.X, padx=8, pady=8)
        
        if not hasattr(self, 'emoji_cat'):
            self.emoji_cat = 'Smileys'
        
        for cat in self.EMOJIS.keys():
            first_emoji = self.EMOJIS[cat][0]
            is_active = cat == self.emoji_cat
            
            btn = tk.Label(
                cat_frame,
                text=first_emoji,
                bg=self.COLORS['selected'] if is_active else self.COLORS['surface'],
                font=self.fonts['emoji_small'],
                cursor='hand2',
                padx=6,
                pady=4
            )
            btn.pack(side=tk.LEFT, padx=2)
            btn.bind("<Button-1>", lambda e, c=cat: self._switch_emoji_cat(c, parent))
        
        # Emoji grid
        grid = tk.Frame(parent, bg=self.COLORS['surface'])
        grid.pack(fill=tk.BOTH, expand=True, padx=8)
        
        emojis = self.EMOJIS.get(self.emoji_cat, '')
        cols = 8
        
        for i, emoji in enumerate(emojis):
            btn = tk.Label(
                grid,
                text=emoji,
                bg=self.COLORS['surface'],
                font=self.fonts['emoji'],
                cursor='hand2'
            )
            btn.grid(row=i//cols, column=i%cols, padx=3, pady=3)
            btn.bind("<Button-1>", lambda e, em=emoji: self._paste_emoji(em))
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.COLORS['hover']))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.COLORS['surface']))

    def _switch_emoji_cat(self, cat, parent):
        self.emoji_cat = cat
        for w in parent.winfo_children():
            w.destroy()
        self._build_emoji(parent)

    def _build_kaomoji(self, parent):
        scroll = tk.Frame(parent, bg=self.COLORS['surface'])
        scroll.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        cols = 3
        for i, kao in enumerate(self.KAOMOJI):
            btn = tk.Label(
                scroll,
                text=kao,
                bg=self.COLORS['acrylic_tint'],
                fg=self.COLORS['text_primary'],
                font=self.fonts['body'],
                cursor='hand2',
                padx=6,
                pady=6
            )
            btn.grid(row=i//cols, column=i%cols, padx=2, pady=2, sticky='ew')
            btn.bind("<Button-1>", lambda e, k=kao: self._paste_emoji(k))
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.COLORS['hover']))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.COLORS['acrylic_tint']))

    def _build_symbols(self, parent):
        grid = tk.Frame(parent, bg=self.COLORS['surface'])
        grid.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        cols = 10
        for i, sym in enumerate(self.SYMBOLS):
            btn = tk.Label(
                grid,
                text=sym,
                bg=self.COLORS['surface'],
                fg=self.COLORS['text_primary'],
                font=('Segoe UI', 14),
                cursor='hand2',
                width=2
            )
            btn.grid(row=i//cols, column=i%cols, padx=2, pady=2)
            btn.bind("<Button-1>", lambda e, s=sym: self._paste_emoji(s))
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.COLORS['hover']))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.COLORS['surface']))

    def _build_placeholder(self, parent, tab_name):
        placeholder = tk.Frame(parent, bg=self.COLORS['surface'])
        placeholder.pack(fill=tk.BOTH, expand=True, pady=50)
        
        tk.Label(
            placeholder,
            text=tab_name.upper(),
            bg=self.COLORS['surface'],
            fg=self.COLORS['text_tertiary'],
            font=('Segoe UI', 18, 'bold')
        ).pack()
        
        tk.Label(
            placeholder,
            text="Coming soon",
            bg=self.COLORS['surface'],
            fg=self.COLORS['text_disabled'],
            font=self.fonts['body']
        ).pack(pady=(8, 0))
