#!/usr/bin/python3

import gi
import vlc

gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, Notify

Notify.init('Multimodal YouTube Player')
instance = vlc.Instance('--no-xlib')

import youtubeplayer


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

        # Label
        infoLabel = Gtk.Label(label="Multimodal YouTubePlayer")
        infoLabel.set_line_wrap(True)
        mainBox.pack_start(infoLabel, True, True, 0)

        # YouTube
        self.youtube = youtubeplayer.YouTubePlayer(self, mainBox, headerBar, infoLabel)
        self.youtube.show(self)

    def keyPressed(self, widget, event, data=None):
        self.youtube.keyPressed(widget, event, data)


window = MainWindow()
window.set_icon_from_file('images/icons/youtube.svg')
window.connect("delete-event", Gtk.main_quit)
window.connect('key-release-event', window.keyPressed)

Gtk.main()
