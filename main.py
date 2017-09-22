import subprocess
from os import path
from json import load
from functools import partial
from Xlib import X, XK
from Xlib.display import Display
from Xlib.ext.xtest import fake_input

import pyxhook

class Gkbls():
    display = Display()

    def __init__(self):
        self.hook_manager = pyxhook.HookManager()
        self.hook_manager.KeyDown = self.on_key_down
        self.hook_manager.KeyUp = self.on_key_up
        self.hook_manager.HookKeyboard()
        self.hook_manager.start()

        self.is_another_key_pressed = False
        self.current_expected_combo = set()
        self.current_exit_combo = set()
        
        with open(path.join(path.dirname(__file__), './config.json')) as config_file:
            config_data = load(config_file)
            self.config_actual_combo = set(config_data['actual_combo_to_switch_layout'])
            self.config_expected_combo = set(config_data['expected_combo_to_switch_layout'])
            self.config_exit_combo = set(config_data['exit_combo_to_close_script'])

            dconf_combo = config_data['dconf_combo_to_switch_layout']
            subprocess.Popen(['gsettings', 'set', 'org.gnome.desktop.wm.keybindings', 'switch-input-source-backward', '[]'])
            subprocess.Popen(['gsettings', 'set', 'org.gnome.desktop.wm.keybindings', 'switch-input-source', '["' + dconf_combo + '"]'])

    def on_key_down(self, event):
        key_name = 'XK_' + event.Key
        
        if key_name in self.config_exit_combo:
            self.current_exit_combo.add(key_name)
        
        if key_name in self.config_expected_combo:
            self.current_expected_combo.add(key_name)
        else:
            self.is_another_key_pressed = True

        if len(self.current_exit_combo ^ self.config_exit_combo) == 0:
            self.hook_manager.cancel()

    def on_key_up(self, event):
        key_name = 'XK_' + event.Key
        
        if key_name in self.config_exit_combo and key_name in self.current_exit_combo:
            self.current_exit_combo.remove(key_name)
        
        if key_name in self.config_expected_combo and key_name in self.current_expected_combo:
            should_layout_be_switched = False
            if not self.is_another_key_pressed and len(self.current_expected_combo ^ self.config_expected_combo) == 0:
                should_layout_be_switched = True
            self.current_expected_combo.remove(key_name)
            if should_layout_be_switched:
                self.on_layout_switch()
        
        if len(self.current_expected_combo) == 0:
            self.is_another_key_pressed = False

    def on_layout_switch(self):
        key_sym_combo = map(partial(getattr, XK), self.config_expected_combo)
        for key_sym in key_sym_combo:
            key_code = self.display.keysym_to_keycode(key_sym)
            fake_input(self.display, X.KeyRelease, key_code)

        key_sym_combo = map(partial(getattr, XK), self.config_actual_combo)
        for action in (X.KeyPress, X.KeyRelease):
            for key_sym in key_sym_combo:
                key_code = self.display.keysym_to_keycode(key_sym)
                fake_input(self.display, action, key_code)
            self.display.sync()

        self.is_another_key_pressed = False

def main():
    gkbls = Gkbls()

if __name__ == '__main__':
    main()
