import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk

from time import sleep
import threading

import globals
import myfuncs


class DICVA:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("/home/horia/dicvcaa/practic/gui/main_layout.glade")
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("main_window")
        self.window.set_icon_from_file('/home/horia/dicvcaa/practic/gui/icon-nobg2.png')
        self.window.show_all()

        self.progr_bar = self.builder.get_object("progr1")
        self.progr_value = 0.0

        self.username_entry = self.builder.get_object("username_entry")

    def on_main_window_destroy(self, *args):
        Gtk.main_quit()

    def on_calibrate(self, widget):
        calibrate_window = self.builder.get_object("calibrate_window")
        calibrate_window.show_all()

        self.progr_bar.set_fraction(0.0)

    def update_progressbar(self):
        measurement = threading.Thread(target=myfuncs.measure_noise)
        measurement.daemon = True
        measurement.start()

        for i in range(5):
            sleep(1)
            self.progr_bar.set_fraction(self.progr_value + 0.2)
            self.progr_value += 0.2

        sleep(0.5)

        self.on_calibrate_closed(None, None)

    def on_start_calibration(self, widget):
        self.progr_value = 0.0
        self.progr_bar.set_fraction(self.progr_value)

        thread = threading.Thread(target=self.update_progressbar)
        thread.daemon = True
        thread.start()

    def on_calibrate_closed(self, widget, event):
        return self.builder.get_object("calibrate_window").hide_on_delete()

    def on_start_clicked(self, widget):
        if globals.noise_max == 0 or globals.noise_max > 0.2:
            print("You need to calibrate!")
            self.on_calibrate(None)
        else:
            record_window = self.builder.get_object("record_window")
            record_window.show_all()

    def on_record_closed(self, widget, event):
        return self.builder.get_object("record_window").hide_on_delete()

    def on_start_record(self, widget):
        recording_thread = threading.Thread(target=myfuncs.continuous_rec)
        recording_thread.daemon = True
        recording_thread.start()

    def on_commands_clicked(self, widget):
        commands_window = self.builder.get_object("commands_window")

        frame1 = self.builder.get_object("frame1")
        frame2 = self.builder.get_object("frame2")
        frame3 = self.builder.get_object("frame3")
        color = Gdk.RGBA(52/255, 55/255, 56/255)
        frame1.override_background_color(0, color)
        frame2.override_background_color(0, color)
        frame3.override_background_color(0, color)

        commands_window.show_all()

    def on_commands_closed(self, widget, event):
        return self.builder.get_object("commands_window").hide_on_delete()

    def on_settings_clicked(self, widget):
        settings_window = self.builder.get_object("settings_window")
        settings_window.show_all()

        self.username_entry.set_text(globals.username)

    def on_settings_closed(self, widget, event):
        return self.builder.get_object("settings_window").hide_on_delete()

    def on_save_settings_clicked(self, widget):
        new_username = self.username_entry.get_text()

        globals.username = new_username
        self.on_settings_closed(None, None)

DICVA()
Gtk.main()
