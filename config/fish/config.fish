#  ___ _    _
# | __(_)__| |_
# | _|| (_-< ' \
# |_| |_/__/_||_|
#
# Author: Christopher Dowell <cbdowell@gmail.com>
# License: MIT
# Locale

set -gx LC_ALL               en_US.UTF-8
set -gx LANG                 en_US.UTF-8

set -gx QT_QPA_PLATFORMTHEME "qt5ct"
set -gx GPG_TTY              (tty)

set -gx EDITOR        /usr/bin/nano
set -gx GTK2_RC_FILES "$HOME/.gtkrc-2.0"
set -gx BROWSER       /usr/bin/firefox

# ghq
set -gx GHQ_ROOT ~/.ghq

# exa
if type -q exa
    echo "✓ Exa"
    abbr ls  'exa'
    abbr la  'exa -lah'
    abbr l   'exa'
    abbr ll  'exa -l'
    abbr lt  'exa --sort=created -l --reverse'
    abbr lta 'exa --sort=created -l --reverse -a'
    abbr lT  'exa -T'
end

# pywal
type -q wal
    and test -f ~/.cache/wal/colors.fish
    and source ~/.cache/wal/colors.fish

# fisher
if not functions -q fisher
    set -q XDG_CONFIG_HOME; or set XDG_CONFIG_HOME ~/.config
    curl https://git.io/fisher --create-dirs -sLo $XDG_CONFIG_HOME/fish/functions/fisher.fish
    fish -c fisher
end

# starship
starship init fish | source
