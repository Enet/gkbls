# gkbls
Gnome Keyboard Layout Switcher

As you know Ubuntu 17.10 migrated to Gnome desktop environment. It means that all the users which usually switch keyboard layout with Control+Shift combo will be disappointed, because this bug https://bugs.launchpad.net/ubuntu/+source/gnome-settings-daemon/+bug/1245473 is still not fixed. You can't use that combo to switch layout at the moment!!!

I would use another linux distro rather than start switching layout through Super+Space combo as Gnome developers want to force me. That's why I've written this script. It does only three things:
1. Change key bindings for switching layout to Control+Shift+0.
2. Wait while Control+Shift will be pressed.
3. Simulate keystroke of Control+Shift+0.

Also script will be closed by Control+Shift+Escape. In such way you are able **to change keyboard layout using Control+Shift or Alt+Shift!!!** And it works after keyup-event instead default behaviour!

## How to use
To use the script you need:
```sh
# install dependencies
sudo apt-get -y install python python-xlib
# download the script
git clone git@github.com:Enet/gkbls.git
# start the script
cd gkbls && python main.py
```

If you want to use Alt+Shift rather that Control+Shift, it is required to modify **config.json**: replace *XK_Control_L* to *XK_Alt_L* **only** for key **expected_combo_to_switch_layout**. Be careful during configuration, because it's very sensitive to the assigned keys (some combinations don't work for some reasons).

Also be free to use empty array for **exit_combo_to_close_script** if you're going to add **gkbls** to autostart.