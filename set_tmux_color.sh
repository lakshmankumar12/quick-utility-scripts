hostname=$(hostname)

if [ "x$hostname" = "xlakshmandevhetzner" ] ; then
    color=45
elif [ "x$hostname" = "xlakshman-VirtualBox" ] ; then
    color=133
else
    color=94
fi

tmux set-option -g status-bg colour${color}
