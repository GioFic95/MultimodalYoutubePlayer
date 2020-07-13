import hashlib
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

        self.username_label = Gtk.Label("Username")
        mainBox.pack_start(self.username_label, True, True, 0)
        self.username_entry = Gtk.Entry()
        self.username_entry.set_placeholder_text("Insert your username")
        mainBox.pack_start(self.username_entry, True, True, 0)

        self.password_label = Gtk.Label("Password")
        mainBox.pack_start(self.password_label, True, True, 0)
        self.password_entry = Gtk.Entry()
        self.password_entry.set_visibility(False)
        self.password_entry.set_placeholder_text("Insert your password")
        mainBox.pack_start(self.password_entry, True, True, 0)

        self.submit_button = Gtk.Button.new_with_label("Submit")
        self.submit_button.connect('clicked', self.submit)
        mainBox.pack_start(self.submit_button, True, True, 0)

    def submit(self, button):
        psw = hashlib.sha256(self.password_entry.get_text().encode()).hexdigest()
        query = f"SELECT * FROM users WHERE username='{self.username_entry.get_text()}' AND psw='{psw}';"
        users = util.execute_query(query).fetchall()

        if len(users) == 1:
            self.window.youtube.show_button(self.window)
            self.hide()
        else:
            self.infoLabel.set_text("Wrong credentials.")

    def show(self, window):
        window.show_all()
        self.username_entry.grab_focus()
    
    def hide(self):
        self.username_label.hide()
        self.username_entry.hide()
        self.password_label.hide()
        self.password_entry.hide()
        self.submit_button.hide()

    def keyPressed(self, widget, event, data=None):
        key = event.keyval

        if key == ENTER:
            self.submit(self.submit_button)
