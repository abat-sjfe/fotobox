import os
import subprocess
from kivy.app import App
from kivy.uix.image import AsyncImage
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import ButtonBehavior
from kivy.core.window import Window

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(SCRIPT_DIR, "bilder")
THUMB_W, THUMB_H = 240, 180
COLS = 3
SPACING = 10

# Clickable Image widget
class ClickableImage(ButtonBehavior, AsyncImage):
    def __init__(self, image_path, **kwargs):
        super().__init__(**kwargs)
        self.image_path = image_path

    def on_press(self):
        # Open the selected image in show_image_galery.py
        subprocess.Popen(
            ["python3", os.path.join(SCRIPT_DIR, "show_image.py"), self.image_path]
        )

class GalleryApp(App):
    def build(self):
        Window.clearcolor = (0.12, 0.12, 0.12, 1)

        # Outer ScrollView
        scroll = ScrollView(size_hint=(1, 1), bar_width=8)

        # GridLayout for thumbnails
        layout = GridLayout(
            cols=COLS,
            spacing=SPACING,
            padding=SPACING,
            size_hint_y=None
        )
        layout.bind(minimum_height=layout.setter('height'))

        # Load images from folder
        if not os.path.exists(IMAGE_FOLDER):
            os.makedirs(IMAGE_FOLDER)

        files = sorted(
            [f for f in os.listdir(IMAGE_FOLDER)
             if f.lower().endswith((".jpg", ".jpeg", ".png"))],
            reverse=True
        )

        for fname in files:
            path = os.path.join(IMAGE_FOLDER, fname)
            thumb = ClickableImage(
                image_path=path,
                source=path,
                size_hint=(None, None),
                size=(THUMB_W, THUMB_H)
            )
            layout.add_widget(thumb)

        scroll.add_widget(layout)
        return scroll

if __name__ == "__main__":
    GalleryApp().run()