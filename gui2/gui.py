import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk

from time import sleep
import threading

import globals
import myfuncs
import helperfuncs


class DICVA:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("/home/horia/dicvcaa/practic/gui2/main_layout.glade")
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("main_window")
        self.window.set_icon_from_file('/home/horia/dicvcaa/practic/gui2/icon-nobg2.png')
        self.window.show_all()

        self.progr_bar = self.builder.get_object("progr1")
        self.progr_value = 0.0

        self.username_entry = self.builder.get_object("username_entry")

        self.radio_conversation = self.builder.get_object("radio_conversation")
        self.radio_system = self.builder.get_object("radio_system")
        self.radio_search = self.builder.get_object("radio_search")
        self.type_buttons = [self.radio_conversation, self.radio_system, self.radio_search]

        self.command_name = self.builder.get_object("command_name")
        self.command_description = self.builder.get_object("command_description")
        self.command_handler = self.builder.get_object("command_handler")

        self.sup_commands = []

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

    def on_edit_clicked(self, widget, label=None):
        new_command_window = self.builder.get_object("new_command_window")
        self.command_name.set_text(f"{label}")

        for elem in globals.supported_commands:
            if elem['name'] == label:
                command_type = elem['type']

                self.command_description.set_text(f"{elem['description']}")
                self.command_handler.set_text(f"{elem['handler']}")

                if command_type == 'conversation':
                    self.on_conversation_toggled(None)
                elif command_type == 'search':
                    self.on_search_toggled(None)
                elif command_type == 'system':
                    self.on_system_toggled(None)

        globals.supported_commands = [elem for elem in globals.supported_commands if elem['name'] != label]
        helperfuncs.store_commands(globals.supported_commands)
        globals.supported_commands = helperfuncs.update_supported_commands()

        new_command_window.show_all()

    def on_delete_clicked(self, widget, label=None):
        globals.supported_commands = [elem for elem in globals.supported_commands if elem['name'] != label]
        helperfuncs.store_commands(globals.supported_commands)
        globals.supported_commands = helperfuncs.update_supported_commands()

        self.on_commands_closed(None, None)
        self.on_commands_clicked(None)

    def populate_grid(self, grid, command_type):
        commands = [command['name'] for command in globals.supported_commands if command['type'] == command_type]
        commands.sort()
        print(commands)

        for command in enumerate(commands):
            if command[1] == 'hello' or command[1] == 'stop':
                label = Gtk.Label.new(command[1])
                label.set_margin_top(10)
                label.set_margin_bottom(10)
                label.set_margin_end(10)
                label.set_margin_start(10)

                grid.attach(label, 0, command[0] + 1, 1, 1)
            else:
                griddy = Gtk.Grid.new()
                grid.attach(griddy, 0, command[0] + 1, 1, 1)

                buttons_grid = Gtk.Grid.new()
                buttons_grid.set_column_spacing(5)
                griddy.attach(buttons_grid, 0, 0, 1, 1)

                edit_button = Gtk.Button.new_from_icon_name("gtk-edit", 1)
                edit_button.set_tooltip_text("Edit")
                edit_button.set_margin_top(10)
                edit_button.set_margin_bottom(10)
                edit_button.connect("clicked", self.on_edit_clicked, command[1])

                delete_button = Gtk.Button.new_from_icon_name("gtk-delete", 1)
                delete_button.set_tooltip_text("Delete")
                delete_button.set_margin_top(10)
                delete_button.set_margin_bottom(10)
                delete_button.connect("clicked", self.on_delete_clicked, command[1])

                buttons_grid.attach(edit_button, 0, 0, 1, 1)
                buttons_grid.attach(delete_button, 1, 0, 1, 1)

                label = Gtk.Label.new(command[1])
                label.set_margin_top(10)
                label.set_margin_bottom(10)
                label.set_margin_end(10)
                label.set_margin_start(50)
                griddy.attach(label, 1, 0, 1, 1)

            for s_command in globals.supported_commands:
                if s_command['name'] == command[1]:
                    description_text = s_command['description']
                    break

            description = Gtk.Label.new(description_text)
            description.set_halign(Gtk.Align.START)
            description.set_margin_top(10)
            description.set_margin_bottom(10)
            description.set_margin_end(10)
            description.set_margin_start(10)

            grid.attach(description, 1, command[0] + 1, 1, 1)

            if command[1] == 'hello' or command[1] == 'stop':
                if (label, description) not in self.sup_commands:
                    self.sup_commands.append((label, description))
            else:
                if (griddy, description) not in self.sup_commands:
                    self.sup_commands.append((griddy, description))

    def display_commands(self):
        conversation_grid = self.builder.get_object("conversation_grid")
        system_grid = self.builder.get_object("system_grid")
        search_grid = self.builder.get_object("search_grid")

        self.populate_grid(conversation_grid, 'conversation')
        self.populate_grid(system_grid, 'system')
        self.populate_grid(search_grid, 'search')

    def on_commands_clicked(self, widget):
        commands_window = self.builder.get_object("commands_window")

        globals.supported_commands = helperfuncs.update_supported_commands()

        frame1 = self.builder.get_object("frame1")
        frame2 = self.builder.get_object("frame2")
        frame3 = self.builder.get_object("frame3")
        color = Gdk.RGBA(52/255, 55/255, 56/255)
        frame1.override_background_color(0, color)
        frame2.override_background_color(0, color)
        frame3.override_background_color(0, color)

        self.display_commands()

        commands_window.show_all()

    def on_commands_closed(self, widget, event):
        for command in self.sup_commands:
            command[0].destroy()
            command[1].destroy()

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

    def on_new_command_button_clicked(self, widget):
        new_command_window = self.builder.get_object("new_command_window")

        new_command_window.show_all()

    def on_new_command_window_closed(self, widget, event):
        return self.builder.get_object("new_command_window").hide_on_delete()

    def on_conversation_toggled(self, widget):
        state = self.radio_conversation.get_active()

        if state:
            self.radio_system.set_active(False)
            self.radio_search.set_active(False)
        else:
            if not self.radio_system.get_active() and not self.radio_search.get_active():
                self.radio_conversation.set_active(True)

    def on_system_toggled(self, widget):
        state = self.radio_system.get_active()

        if state:
            self.radio_conversation.set_active(False)
            self.radio_search.set_active(False)
        else:
            if not self.radio_conversation.get_active() and not self.radio_search.get_active():
                self.radio_system.set_active(True)

    def on_search_toggled(self, widget):
        state = self.radio_search.get_active()

        if state:
            self.radio_conversation.set_active(False)
            self.radio_system.set_active(False)
        else:
            if not self.radio_conversation.get_active() and not self.radio_system.get_active():
                self.radio_search.set_active(True)

    def on_save_command_clicked(self, widget):
        for elem in self.type_buttons:
            if elem.get_active():
                type_of_command = elem.get_label().lower()

        globals.supported_commands.append(
            {
                'name': self.command_name.get_text().lower(),
                'description': self.command_description.get_text(),
                'type': type_of_command,
                'handler': f"{self.command_handler.get_text()}"
            }
        )

        helperfuncs.store_commands(globals.supported_commands)

        self.on_new_command_window_closed(None, None)
        self.on_commands_closed(None, None)
        self.on_commands_clicked(None)


globals.supported_commands = helperfuncs.update_supported_commands()
DICVA()
Gtk.main()
