# EndeavourOS + Hyprland Dotfiles

Personal EndeavourOS configuration with Hyprland, Waybar, Kitty, SwayNC, and Tofi.

## Structure
- `.config/` - Hyprland, Waybar, Kitty, SwayNC, Waypaper, Tofi, Wlogout configurations
- `.bashrc` - Shell configuration
- `pkglist-native.txt` - Installed official Pacman packages
- `pkglist-aur.txt` - Installed AUR packages

## Installation on Fresh System
```bash
git clone <your-repo-url> ~/Projects/endeavouros-dotfiles
cd ~/Projects/endeavouros-dotfiles
./install.sh
```

## Package Restore
```bash
sudo pacman -S --needed - < pkglist-native.txt
yay -S --needed - < pkglist-aur.txt
```
