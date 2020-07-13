#!/usr/bin/python3

import gi
import vlc

gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, Notify

from core import youtubeplayer, login, util

Notify.init('Multimodal YouTube Player')
instance = vlc.Instance('--no-xlib')


class MainWindow(Gtk.Window):
    def __init__(self):
        # Metadata
        self.title = "Multimodal YouTubePlayer"
        Gtk.Window.__init__(self)
        self.set_size_request(520, 100)

        # Title bar tweaks
        headerBar = Gtk.HeaderBar()
        headerBar.set_show_close_button(True)
        self.set_titlebar(headerBar)
        self.set_resizable(False)

        # Main Box: All widgets are inside this
        mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        mainBox.set_property('margin', 10)
        mainBox.set_size_request(400, 100)

        # Title
        infoLabel = Gtk.Label(label="Multimodal YouTubePlayer")
        infoLabel.set_line_wrap(True)
        mainBox.pack_start(infoLabel, True, True, 0)

        # Login
        self.login = login.LoginBox(self, mainBox, infoLabel)
        mainBox.pack_start(self.login, True, True, 0)
        self.login.show(self)

        # YouTube
        self.youtube = youtubeplayer.YouTubePlayer(self, mainBox, headerBar, infoLabel)
        self.youtube.show(self)

    def keyPressed(self, widget, event, data=None):
        if self.youtube.entry.is_visible():
            self.youtube.keyPressed(widget, event, data)
        elif self.login.login_button.is_visible():
            self.login.keyPressed(widget, event, data)


if not util.check_db():
    print("creating DB...")
    util.create_db()

window = MainWindow()
window.set_icon_from_file('images/icons/youtube.svg')
window.connect("delete-event", Gtk.main_quit)
window.connect('key-release-event', window.keyPressed)
window.login.username_entry.grab_focus()

Gtk.main()
