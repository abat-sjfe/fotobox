# gallery_kv.py
import os
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage
from kivy.uix.button import ButtonBehavior
from kivy.core.window import Window

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(SCRIPT_DIR, "bilder")
THUMB_W, THUMB_H = 240, 180
COLS = 3
SPACING = 10

class ClickableImage(ButtonBehavior, AsyncImage):
    def __init__(self, image_path, parent_app, **kwargs):
        super().__init__(**kwargs)
        self.image_path = image_path
        self.parent_app = parent_app

    def on_press(self):
        self.parent_app.selected_image = self.image_path
        self.parent_app.stop()

class GalleryApp(App):
    def build(self):
        Window.clearcolor = (0.12, 0.12, 0.12, 1)
        scroll = ScrollView(size_hint=(1, 1), bar_width=8)
        layout = GridLayout(cols=COLS, spacing=SPACING, padding=SPACING, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        if not os.path.exists(IMAGE_FOLDER):
            os.makedirs(IMAGE_FOLDER)

        files = sorted(
            [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith((".jpg", ".jpeg", ".png"))],
            reverse=True
        )
        for fname in files:
            path = os.path.join(IMAGE_FOLDER, fname)
            thumb = ClickableImage(image_path=path, parent_app=self,
                                   source=path,
                                   size_hint=(None, None),
                                   size=(THUMB_W, THUMB_H))
            layout.add_widget(thumb)

        scroll.add_widget(layout)
        return scroll

    def run(self):
        self.selected_image = None
        super().run()
        if self.selected_image:
            return ("viewer", self.selected_image)
        else:
            return ("camera", None)