import os
import sys
import time
import threading
import subprocess
import numpy as np

from picamera2 import Picamera2

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BILDER_DIR = os.path.join(SCRIPT_DIR, "bilder")


class PhotoBoothApp(App):
    def build(self):
        self.countdown_active = False
        self.countdown_seconds = 5
        self.countdown_start_time = 0

        # Camera setup
        self.picam2 = Picamera2()
        preview_config = self.picam2.create_preview_configuration(
            main={"format": "RGB888", "size": (640, 480)}
        )
        self.picam2.configure(preview_config)
        self.picam2.start()

        # Main layout with float positioning
        self.layout = FloatLayout()

        # Image widget for camera stream
        self.image_widget = Image()
        self.layout.add_widget(self.image_widget)

        # Countdown label in center
        self.countdown_label = Label(
            text="",
            font_size=150,
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.layout.add_widget(self.countdown_label)

        # Capture button
        self.btn_photo = Button(
            text="Take Photo",
            size_hint=(None, None),
            size=(200, 60),
            pos_hint={"center_x": 0.5, "y": 0.02},
        )
        self.btn_photo.bind(on_release=self.start_countdown)
        self.layout.add_widget(self.btn_photo)

        # Gallery button
        self.btn_gallery = Button(
            text="Gallery",
            size_hint=(None, None),
            size=(100, 60),
            pos_hint={"x": 0.02, "top": 0.98},
        )
        self.btn_gallery.bind(on_release=self.open_gallery)
        self.layout.add_widget(self.btn_gallery)

        # Schedule camera updates
        Clock.schedule_interval(self.update_camera, 1.0 / 30.0)

        return self.layout

    def update_camera(self, dt):
        """Grab frame from Picamera2 and display it."""
        if not self.countdown_active:
            frame = self.picam2.capture_array()
            frame = np.rot90(frame)
            buf = frame.tobytes()

            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="rgb")
            texture.blit_buffer(buf, colorfmt="rgb", bufferfmt="ubyte")
            texture.flip_vertical()
            self.image_widget.texture = texture

        else:
            elapsed = (time.time() - self.countdown_start_time)
            remaining = int(self.countdown_seconds - elapsed)

            if remaining > 0:
                # Show countdown number
                self.countdown_label.text = str(remaining)
            else:
                # Take the photo
                self.take_photo()
                self.countdown_active = False
                self.countdown_label.text = ""

    def start_countdown(self, instance):
        if not self.countdown_active:
            self.countdown_active = True
            self.countdown_start_time = time.time()
            self.countdown_label.text = str(self.countdown_seconds)

    def take_photo(self):
        # Make sure folder exists
        if not os.path.exists(BILDER_DIR):
            os.makedirs(BILDER_DIR)

        filename = time.strftime("photo_%Y%m%d_%H%M%S.jpg")
        save_path = os.path.join(BILDER_DIR, filename)
        self.picam2.capture_file(save_path)
        print(f"Photo saved to: {save_path}")

        # Show image via show_image.py
        show_image_script = os.path.join(SCRIPT_DIR, "show_image.py")
        threading.Thread(target=lambda: subprocess.run(["python3", show_image_script, save_path])).start()

    def open_gallery(self, instance):
        gallery_script = os.path.join(SCRIPT_DIR, "gallery_view.py")
        threading.Thread(target=lambda: subprocess.run(["python3", gallery_script])).start()


if __name__ == "__main__":
    PhotoBoothApp().run()