import hashlib
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from psycopg2.errors import UniqueViolation
from core import util

ENTER = 65293


class LoginBox(Gtk.Box):
    def __init__(self, window, mainBox, infoLabel):
        Gtk.Box.__init__(self)
        self.mainBox = mainBox
        self.infoLabel = infoLabel
        self.window = window

        # Login
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

        self.login_button = Gtk.Button.new_with_label("Login")
        self.login_button.connect('clicked', self.login)
        mainBox.pack_start(self.login_button, True, True, 0)

        # Separator
        self.space = Gtk.Label("\n")
        mainBox.pack_start(self.space, True, True, 0)
        self.separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        mainBox.pack_start(self.separator, True, True, 0)
        
        # Registration
        self.new_username_label = Gtk.Label("\nNew Username")
        mainBox.pack_start(self.new_username_label, True, True, 0)
        self.new_username_entry = Gtk.Entry()
        self.new_username_entry.set_placeholder_text("Insert your desired username")
        mainBox.pack_start(self.new_username_entry, True, True, 0)

        self.new_password_label = Gtk.Label("New Password")
        mainBox.pack_start(self.new_password_label, True, True, 0)
        self.new_password_entry = Gtk.Entry()
        self.new_password_entry.set_visibility(False)
        self.new_password_entry.set_placeholder_text("Insert your desired password")
        mainBox.pack_start(self.new_password_entry, True, True, 0)

        self.deaf = Gtk.CheckButton("Deaf user   ")
        mainBox.pack_start(self.deaf, True, True, 0)

        self.register_button = Gtk.Button.new_with_label("Register")
        self.register_button.connect('clicked', self.register)
        mainBox.pack_start(self.register_button, True, True, 0)

    def login(self, button):
        user = self.username_entry.get_text()
        psw = hashlib.sha256(self.password_entry.get_text().encode()).hexdigest()
        query = f"SELECT * FROM users WHERE username='{user}' AND psw='{psw}';"
        users = util.execute_query(query).fetchall()

        if len(users) == 1:
            self.infoLabel.set_text(f"Hello {user}.")
            self.window.youtube.show_button(self.window)
            self.hide()
        else:
            self.infoLabel.set_text("Wrong credentials.")

    def register(self, button):
        user = self.new_username_entry.get_text()
        psw = hashlib.sha256(self.new_password_entry.get_text().encode()).hexdigest()

        query = f"INSERT INTO users(username, psw, deaf) VALUES ('{user}', '{psw}', {self.deaf.get_active()});"
        try:
            util.execute_query(query)
            self.infoLabel.set_text(f"Welcome {user}.")
            self.window.youtube.show_button(self.window)
            self.hide()
        except UniqueViolation:
            self.new_username_entry.set_text("")
            self.new_password_entry.set_text("")
            self.infoLabel.set_text("The selected Username already exists.")

    def show(self, window):
        window.show_all()
        self.username_entry.grab_focus()
    
    def hide(self):
        self.username_label.hide()
        self.username_entry.hide()
        self.password_label.hide()
        self.password_entry.hide()
        self.login_button.hide()
        self.space.hide()
        self.separator.hide()
        self.new_username_label.hide()
        self.new_username_entry.hide()
        self.new_password_label.hide()
        self.new_password_entry.hide()
        self.deaf.hide()
        self.register_button.hide()

    def keyPressed(self, widget, event, data=None):
        key = event.keyval

        if key == ENTER:
            self.login(self.login_button)
