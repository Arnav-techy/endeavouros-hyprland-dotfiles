#!/bin/bash
APP="$1"

case "$APP" in
    wifi)
        if pgrep -f "wifi_menu.py" >/dev/null 2>&1; then
            pkill -9 -f "wifi_menu.py"
        else
            python3 /home/arnav/.config/waybar/scripts/wifi_menu.py &
        fi
        ;;
    bluetooth)
        if pgrep -f "blueman-manager" >/dev/null 2>&1; then
            pkill -9 -f "blueman-manager"
        else
            blueman-manager &
        fi
        ;;
    audio)
        if pgrep -f "pavucontrol" >/dev/null 2>&1; then
            pkill -9 -f "pavucontrol"
        else
            pavucontrol &
        fi
        ;;
    brightness)
        if pgrep -f "brightness_dialog.py" >/dev/null 2>&1; then
            pkill -9 -f "brightness_dialog.py"
        else
            python3 /home/arnav/.config/waybar/scripts/brightness_dialog.py &
        fi
        ;;
esac
