#!/usr/bin/env bash
set -e

DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> Restoring dotfiles..."
mkdir -p ~/.config

# Symlink or copy .config directories
for dir in "$DOTFILES_DIR/.config"/*; do
    target="$HOME/.config/$(basename "$dir")"
    if [ -d "$target" ] || [ -f "$target" ]; then
        echo "Backing up existing $target to ${target}.bak"
        mv "$target" "${target}.bak"
    fi
    ln -sfn "$dir" "$target"
    echo "Linked: $dir -> $target"
done

# Link bashrc
if [ -f "$DOTFILES_DIR/.bashrc" ]; then
    ln -sf "$DOTFILES_DIR/.bashrc" "$HOME/.bashrc"
    echo "Linked: .bashrc"
fi

echo "==> Setup complete!"
echo "To reinstall packages, run:"
echo "  sudo pacman -S --needed - < pkglist-native.txt"
echo "  yay -S --needed - < pkglist-aur.txt"
