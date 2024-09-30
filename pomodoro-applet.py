import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

class TrayApp:
    def __init__(self):
        self.status_icon = Gtk.StatusIcon()
        self.status_icon.set_from_icon_name("dialog-information")
        self.status_icon.connect("activate", self.on_left_click)
        self.status_icon.connect("popup-menu", self.on_right_click)
        self.dialog = None
        self.hours_button = None
        self.minutes_button = None
        self.seconds_button = None
        self.timer_label = None
        self.timer = 0
        self.timer_timeout = None


    def on_start(self, button):
        self.timer = self.hours_button.get_value() * 360 + \
                self.minutes_button.get_value() * 60 + \
                self.seconds_button.get_value()
        self.timer_label.set_text(str(self.timer))

        if self.timer_timeout:
            GLib.source_remove(self.timer_timeout)

        self.timer_timeout = GLib.timeout_add(1000, self.decrement_timer)

    def on_clear(self, button):
        if self.timer:
            self.timer = 0 
            self.timer_label.set_text(str(self.timer))

        if self.timer_timeout:
            GLib.source_remove(self.timer_timeout)
            self.timer_timeout = None

    def decrement_timer(self):
        if self.timer == 0:
            return False

        self.timer -= 1
        self.status_icon.set_tooltip_text(str(self.timer))

        if self.dialog:
            self.timer_label.set_text(str(self.timer))

        return True

    def create_dialog(self):
        self.dialog = Gtk.Dialog(
                title = "Timer",
                transient_for = None,
                flags = 0
                )
        box = self.dialog.get_content_area()
        box.set_border_width(16)

        
        self.hours_button = Gtk.SpinButton()
        self.minutes_button = Gtk.SpinButton()
        self.seconds_button = Gtk.SpinButton()

        spin_buttons = [self.hours_button, self.minutes_button,
                        self.seconds_button]
        spin_button_names = ["Hours", "Minutes", "Seconds"]

        for (button, name) in zip(spin_buttons, spin_button_names):
            button.set_numeric(True)
            adjustment = Gtk.Adjustment(upper=59, step_increment=1)
            button.set_adjustment(adjustment)
            box.add(Gtk.Label(label = name))
            box.add(button)

        self.timer_label = Gtk.Label(label = str(self.timer))
        box.add(self.timer_label)

        start_button = Gtk.Button.new_with_label("Start")
        start_button.connect("clicked", self.on_start)
        box.add(start_button)

        clear_button = Gtk.Button.new_with_label("Clear")
        clear_button.connect("clicked", self.on_clear)
        box.add(clear_button)

        
        self.dialog.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
    
    def on_dialog_close(self, dialog, response):
        self.dialog.destroy()
        self.dialog = None

    def on_left_click(self, icon):
        if not self.dialog:
            self.create_dialog()
            self.dialog.show_all()
            self.dialog.connect("response", self.on_dialog_close)
    
    def on_right_click(self, icon, button, time):
        menu = Gtk.Menu()
        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", Gtk.main_quit)
        menu.append(quit_item)
        menu.show_all()
        menu.popup(None, None, None, None, button, time)

app = TrayApp()
Gtk.main()
