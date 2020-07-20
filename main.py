#!/usr/bin/python3

import time
import threading
import json
from collections import Counter
import requests
import gi
import vlc
import cv2 as cv

gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, Notify, GLib

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
        self.infoLabel = Gtk.Label(label="Multimodal YouTubePlayer")
        self.infoLabel.set_line_wrap(True)
        mainBox.pack_start(self.infoLabel, True, True, 0)

        # Login
        self.login = login.LoginBox(self, mainBox, self.infoLabel)
        mainBox.pack_start(self.login, True, True, 0)
        self.login.show(self)

        # YouTube
        self.youtube = youtubeplayer.YouTubePlayer(self, mainBox, headerBar, self.infoLabel)
        self.youtube.show(self)

        # Init webcam monitoring
        self.running = True
        self.thread = threading.Thread(target=self.web_capture)
        self.thread.start()

    def keyPressed(self, widget, event, data=None):
        if self.youtube.entry.is_visible():
            self.youtube.keyPressed(widget, event, data)
        elif self.login.login_button.is_visible():
            self.login.keyPressed(widget, event, data)

    def web_capture(self):
        print("start web capture")
        img_counter = 0
        while self.running:
            time.sleep(1.5)
            cam = cv.VideoCapture(0)
            if self.youtube.entry.is_visible():
                ret, frame = cam.read()
                if not ret:
                    print("failed to grab frame")
                    continue
                img_name = f"images/test-img/opencv_frame_{img_counter}.png"
                cv.imwrite(img_name, frame)
                print(f"{img_name} written!")

                url = 'https://api-us.faceplusplus.com/humanbodypp/v1/gesture'
                files = {
                    'api_key': (None, util.get_property("gest_api_key")),
                    'api_secret': (None, util.get_property("gest_api_secret")),
                    'image_file': ('images/test-img/opencv_frame_0.png', open('images/test-img/opencv_frame_0.png', 'rb')),
                    'return_gesture': (None, '1'),
                }
                x = requests.post(url, files=files)
                hands = json.loads(x.text)['hands']
                print("hands:", hands)
                for h in hands:
                    gesture = Counter(h["gesture"]).most_common(1)[0][0]
                    print(gesture)
                    # GLib.idle_add(self.infoLabel.set_text, "TRE")

                img_counter += 1

    def quit(self, widget=None, *data):
        self.running = False
        self.thread.join()
        Gtk.main_quit()


if not util.check_db():
    print("creating DB...")
    util.create_db()

window = MainWindow()
window.set_icon_from_file('images/icons/youtube.svg')
window.connect('key-release-event', window.keyPressed)
window.connect('delete-event', window.quit)
window.login.username_entry.grab_focus()

Gtk.main()
