#!/bin/bash

ACTIVE_JSON=$(hyprctl activewindow -j 2>/dev/null)
[ -z "$ACTIVE_JSON" ] && exit 0

ACTIVE_CLASS=$(echo "$ACTIVE_JSON" | jq -r '.class // .initialClass // empty' | tr '[:upper:]' '[:lower:]')
ACTIVE_TITLE=$(echo "$ACTIVE_JSON" | jq -r '.title // empty' | tr '[:upper:]' '[:lower:]')

NOTIF_APP=$(echo "$SWAYNC_APP_NAME" | tr '[:upper:]' '[:lower:]')
NOTIF_ENTRY=$(echo "$SWAYNC_DESKTOP_ENTRY" | tr '[:upper:]' '[:lower:]')

[ -z "$ACTIVE_CLASS" ] && exit 0

MATCH=0

if [ -n "$NOTIF_APP" ]; then
    if [[ "$ACTIVE_CLASS" == *"$NOTIF_APP"* ]] || [[ "$NOTIF_APP" == *"$ACTIVE_CLASS"* ]]; then
        MATCH=1
    fi
fi

if [ -n "$NOTIF_ENTRY" ]; then
    if [[ "$ACTIVE_CLASS" == *"$NOTIF_ENTRY"* ]] || [[ "$NOTIF_ENTRY" == *"$ACTIVE_CLASS"* ]]; then
        MATCH=1
    fi
fi

if [ "$MATCH" -eq 1 ]; then
    # Suppress / dismiss notification immediately because user is focused on the application
    swaync-client --close-latest 2>/dev/null || true
fi
