#!/usr/bin/env python3
import sys
import subprocess
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

def get_brightness():
    try:
        out = subprocess.check_output(['brightnessctl', 'g'], text=True).strip()
        max_b = subprocess.check_output(['brightnessctl', 'm'], text=True).strip()
        return int(out), int(max_b)
    except Exception:
        return 50, 100

def set_brightness(val):
    subprocess.run(['brightnessctl', 'set', f'{int(val)}%'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

class BrightnessWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Brightness")
        self.set_wmclass("brightness-dialog", "brightness-dialog")
        self.set_default_size(300, 70)
        self.set_resizable(False)
        self.set_decorated(False)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_keep_above(True)

        current, max_b = get_brightness()
        curr_pct = int((current / max_b) * 100) if max_b > 0 else 50

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box.set_margin_start(16)
        box.set_margin_end(16)
        box.set_margin_top(12)
        box.set_margin_bottom(12)

        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.label_title = Gtk.Label(label="󰃠  Brightness")
        self.label_title.set_xalign(0)
        self.label_pct = Gtk.Label(label=f"{curr_pct}%")
        self.label_pct.set_xalign(1)
        
        header.pack_start(self.label_title, True, True, 0)
        header.pack_end(self.label_pct, False, False, 0)
        box.pack_start(header, False, False, 0)

        # Scale slider
        self.scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 1, 100, 1)
        self.scale.set_value(curr_pct)
        self.scale.set_draw_value(False)
        self.scale.connect("value-changed", self.on_change)
        box.pack_start(self.scale, True, True, 0)

        self.add(box)
        self.connect("key-press-event", self.on_key)
        self.connect("focus-out-event", lambda w, e: self.destroy())

    def on_change(self, widget):
        val = int(widget.get_value())
        self.label_pct.set_text(f"{val}%")
        set_brightness(val)

    def on_key(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            self.destroy()

win = BrightnessWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
