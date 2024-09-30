import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

class TrayApp:
    def __init__(self):
        # Create the tray icon
        self.status_icon = Gtk.StatusIcon()
        self.status_icon.set_from_icon_name("dialog-information")
        self.status_icon.connect("activate", self.on_left_click)
        self.status_icon.connect("popup-menu", self.on_right_click)
        self.count = 0
        self.dialog = None
        self.dialog_label = None
        self.hours_button = None
        self.minutes_button = None
        self.seconds_button = None

        GLib.timeout_add(1000, self.increment_counter)

    def increment_counter(self):
        self.count += 1
        self.status_icon.set_tooltip_text(str(self.count))

        if self.dialog:
            self.dialog_label.set_text(str(self.count))

        return True

    def create_dialog(self):
        self.dialog = Gtk.Dialog(
                title = "Timer",
                transient_for = None,
                flags = 0
                )
        box = self.dialog.get_content_area()

        self.dialog_label = Gtk.Label(label = str(self.count))
        box.add(self.dialog_label)

        self.hours_button = Gtk.SpinButton()
        self.minutes_button = Gtk.SpinButton()
        self.seconds_button = Gtk.SpinButton()
        box.add(self.hours_button)
        box.add(self.minutes_button)
        box.add(self.seconds_button)

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
        # Create a menu
        menu = Gtk.Menu()
        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", Gtk.main_quit)
        menu.append(quit_item)
        menu.show_all()
        menu.popup(None, None, None, None, button, time)

app = TrayApp()
Gtk.main()
