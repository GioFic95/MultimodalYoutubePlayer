import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from core import util

ENTER = 65293


class LoginBox(Gtk.Box):
    def __init__(self, window, mainBox, infoLabel):
        Gtk.Box.__init__(self)
        self.mainBox = mainBox
        self.infoLabel = infoLabel
        self.window = window

        username_label = Gtk.Label("Username")
        mainBox.pack_start(username_label, True, True, 0)
        self.username_entry = Gtk.Entry()
        self.username_entry.set_placeholder_text("Insert your username")
        mainBox.pack_start(self.username_entry, True, True, 0)


        password_label = Gtk.Label("Password")
        mainBox.pack_start(password_label, True, True, 0)
        self.password_entry = Gtk.Entry()
        self.password_entry.set_visibility(False)
        self.password_entry.set_placeholder_text("Insert your password")
        mainBox.pack_start(self.password_entry, True, True, 0)

        self.submit_button = Gtk.Button.new_with_label("Submit")
        self.submit_button.connect('clicked', self.submit)
        self.submit_button.set_receives_default(True)
        mainBox.pack_start(self.submit_button, True, True, 0)
        window.set_receives_default(self.submit_button)

    def submit(self, button):
        query = f"SELECT * FROM users WHERE username='{self.username_entry.get_text()}' AND psw='{self.password_entry.get_text()}';"
        users = util.execute_query(query).fetchall()

        if len(users) == 1:

            self.window.youtube.show_button(self.window)
        else:
            self.infoLabel.set_text("Wrong credentials.")

    def show(self, window):
        window.show_all()
        self.username_entry.grab_focus()

    def keyPressed(self, widget, event, data=None):
        key = event.keyval

        if key == ENTER:
            self.submit(self.submit_button)
