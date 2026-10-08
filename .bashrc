#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'
PS1='[\u@\h \W]\$ '

# ── EndeavourOS Setup Script Additions ──

# ── History ──
HISTSIZE=50000
HISTFILESIZE=100000
HISTCONTROL=ignoreboth:erasedups
shopt -s histappend

# ── Navigation ──
shopt -s autocd         # cd into directories by typing the name
shopt -s cdspell        # Correct minor typos in cd
shopt -s dirspell       # Correct minor typos in directory names

# ── Modern CLI aliases ──
alias ls='eza --icons --group-directories-first'
alias ll='eza -la --icons --group-directories-first --git'
alias lt='eza -T --icons --level=2'
alias cat='bat --paging=never'
alias grep='rg'
alias find='fd'
alias cd='z'

# ── Git shortcuts ──
alias gs='git status -sb'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline --graph --decorate -20'
alias gd='git diff'
alias lg='lazygit'

# ── System shortcuts ──
alias update='sudo pacman -Syu && yay -Sua'
alias cleanup='sudo pacman -Rns $(pacman -Qdtq) 2>/dev/null; yay -Sc --noconfirm'
alias myip='curl -s ifconfig.me && echo'
alias ports='sudo ss -tulnp'
alias ..='cd ..'
alias ...='cd ../..'

# ── Docker shortcuts ──
alias dps='docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"'
alias dpa='docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"'
alias dlog='docker logs -f'

# ── kubectl shortcuts ──
alias k='kubectl'
alias kgp='kubectl get pods'
alias kgs='kubectl get svc'

# ── Starship prompt ──
eval "$(starship init bash)"

# ── Zoxide (smart cd) ──
eval "$(zoxide init bash)"

# ── fzf keybindings & completion ──
eval "$(fzf --bash)"

# ── Environment ──
export EDITOR=nvim
export VISUAL=nvim
export BROWSER=google-chrome-stable
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$HOME/go/bin:$PATH"

