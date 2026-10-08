#!/usr/bin/env python3
import sys
import subprocess
import threading
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
    except Exception:
        return ""

class WifiWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Wi-Fi Networks")
        self.set_wmclass("wifi-menu", "wifi-menu")
        self.set_default_size(360, 440)
        self.set_resizable(False)
        self.set_decorated(True)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_keep_above(True)

        self.connecting_ssid = None

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        main_box.set_margin_start(12)
        main_box.set_margin_end(12)
        main_box.set_margin_top(10)
        main_box.set_margin_bottom(10)

        # Header controls
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        title = Gtk.Label(label="<b>󰤨  Wi-Fi Networks</b>")
        title.set_use_markup(True)
        title.set_xalign(0)
        
        self.rescan_btn = Gtk.Button(label="󰑐 Scan")
        self.rescan_btn.connect("clicked", self.on_rescan)
        
        header.pack_start(title, True, True, 0)
        header.pack_end(self.rescan_btn, False, False, 0)
        main_box.pack_start(header, False, False, 0)

        # Status label / spinner
        self.status_label = Gtk.Label(label="Scanning networks...")
        self.status_label.set_xalign(0)
        main_box.pack_start(self.status_label, False, False, 0)

        # Scrolled list
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_min_content_height(320)

        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        scrolled.add(self.listbox)
        main_box.pack_start(scrolled, True, True, 0)

        # Bottom Editor Button
        editor_btn = Gtk.Button(label="󰢻 Advanced Settings")
        editor_btn.connect("clicked", lambda b: subprocess.Popen(["nm-connection-editor"]))
        main_box.pack_start(editor_btn, False, False, 0)

        self.add(main_box)
        self.connect("key-press-event", self.on_key)
        self.connect("destroy", Gtk.main_quit)

        self.refresh_networks()

    def on_key(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            self.destroy()

    def on_rescan(self, btn):
        self.status_label.set_text("Scanning nearby Wi-Fi...")
        self.rescan_btn.set_sensitive(False)
        threading.Thread(target=self._rescan_thread, daemon=True).start()

    def _rescan_thread(self):
        run_cmd(["nmcli", "dev", "wifi", "rescan"])
        GLib.idle_add(self.refresh_networks)

    def refresh_networks(self):
        self.status_label.set_text("Loading...")
        threading.Thread(target=self._load_networks_thread, daemon=True).start()

    def _load_networks_thread(self):
        out = run_cmd(["nmcli", "-t", "-f", "IN-USE,SSID,SIGNAL,SECURITY", "dev", "wifi", "list"])
        networks = []
        seen = set()
        for line in out.strip().split("\n"):
            if not line:
                continue
            parts = line.split(":")
            if len(parts) >= 4:
                in_use = parts[0].strip() == "*"
                ssid = parts[1].strip()
                signal = parts[2].strip()
                security = ":".join(parts[3:]).strip()
                if ssid and ssid not in seen:
                    seen.add(ssid)
                    networks.append({
                        "in_use": in_use,
                        "ssid": ssid,
                        "signal": int(signal) if signal.isdigit() else 0,
                        "security": security
                    })
        GLib.idle_add(self._populate_list, networks)

    def _populate_list(self, networks):
        for child in self.listbox.get_children():
            self.listbox.remove(child)

        self.rescan_btn.set_sensitive(True)
        if not networks:
            self.status_label.set_text("No Wi-Fi networks found.")
            return

        self.status_label.set_text(f"Found {len(networks)} networks")

        # Sort: connected first, then signal descending
        networks.sort(key=lambda n: (not n["in_use"], -n["signal"]))

        for net in networks:
            row = Gtk.ListBoxRow()
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            box.set_margin_start(8)
            box.set_margin_end(8)
            box.set_margin_top(6)
            box.set_margin_bottom(6)

            # Signal icon
            sig = net["signal"]
            if sig > 75:
                sig_icon = "󰤨"
            elif sig > 50:
                sig_icon = "󰤥"
            elif sig > 25:
                sig_icon = "󰤢"
            else:
                sig_icon = "󰤟"

            sec_icon = " " if net["security"] and net["security"] != "--" else ""
            
            label_text = f"{sig_icon} <b>{net['ssid']}</b>{sec_icon} <small>({sig}%)</small>"
            if net["in_use"]:
                label_text = f"<span color='#a6e3a1'>󰄬</span> " + label_text

            lbl = Gtk.Label()
            lbl.set_markup(label_text)
            lbl.set_xalign(0)
            box.pack_start(lbl, True, True, 0)

            if net["in_use"]:
                dis_btn = Gtk.Button(label="Disconnect")
                dis_btn.connect("clicked", lambda b, s=net['ssid']: self.disconnect_network(s))
                box.pack_end(dis_btn, False, False, 0)
            else:
                con_btn = Gtk.Button(label="Connect")
                con_btn.connect("clicked", lambda b, n=net: self.prompt_connect(n))
                box.pack_end(con_btn, False, False, 0)

            row.add(box)
            self.listbox.add(row)

        self.listbox.show_all()

    def disconnect_network(self, ssid):
        self.status_label.set_text(f"Disconnecting from {ssid}...")
        threading.Thread(target=lambda: (run_cmd(["nmcli", "con", "down", "id", ssid]), GLib.idle_add(self.refresh_networks)), daemon=True).start()

    def prompt_connect(self, net):
        ssid = net["ssid"]
        has_security = net["security"] and net["security"] != "--"
        
        # Try connecting directly (if already saved)
        self.status_label.set_text(f"Connecting to {ssid}...")
        threading.Thread(target=self._try_connect_thread, args=(net,), daemon=True).start()

    def _try_connect_thread(self, net):
        ssid = net["ssid"]
        res = subprocess.run(["nmcli", "dev", "wifi", "connect", ssid], capture_output=True, text=True)
        if res.returncode == 0:
            GLib.idle_add(lambda: (self.status_label.set_text(f"Connected to {ssid}!"), self.refresh_networks()))
        else:
            # Need password dialog
            GLib.idle_add(lambda: self._show_password_dialog(ssid))

    def _show_password_dialog(self, ssid):
        dialog = Gtk.Dialog(title=f"Connect to {ssid}", transient_for=self, flags=0)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)
        
        content = dialog.get_content_area()
        content.set_spacing(10)
        content.set_margin_start(16)
        content.set_margin_end(16)
        content.set_margin_top(12)
        content.set_margin_bottom(12)

        lbl = Gtk.Label(label=f"Enter password for <b>{ssid}</b>:")
        lbl.set_use_markup(True)
        lbl.set_xalign(0)
        content.pack_start(lbl, False, False, 0)

        entry = Gtk.Entry()
        entry.set_visibility(False)
        entry.set_activates_default(True)
        content.pack_start(entry, False, False, 0)

        dialog.set_default_response(Gtk.ResponseType.OK)
        dialog.show_all()

        response = dialog.run()
        password = entry.get_text().strip()
        dialog.destroy()

        if response == Gtk.ResponseType.OK and password:
            self.status_label.set_text(f"Connecting to {ssid}...")
            threading.Thread(target=self._connect_with_password, args=(ssid, password), daemon=True).start()
        else:
            self.status_label.set_text("Connection cancelled")

    def _connect_with_password(self, ssid, password):
        res = subprocess.run(["nmcli", "dev", "wifi", "connect", ssid, "password", password], capture_output=True, text=True)
        if res.returncode == 0:
            GLib.idle_add(lambda: (self.status_label.set_text(f"Successfully connected to {ssid}!"), self.refresh_networks()))
        else:
            err = res.stderr.strip() or res.stdout.strip()
            GLib.idle_add(lambda: self.status_label.set_text(f"Failed: {err[:40]}"))

if __name__ == "__main__":
    win = WifiWindow()
    win.show_all()
    Gtk.main()
