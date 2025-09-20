import os
from kivy.app import App
from kivy.uix.image import AsyncImage
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

# Konfiguration
IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), "bilder")
THUMB_W, THUMB_H = 240, 180
COLS = 3
SPACING = 10

class GalleryApp(App):
    def build(self):
        # Fensterfarbe setzen (optional)
        Window.clearcolor = (0.12, 0.12, 0.12, 1)

        # Grid für Thumbnails
        layout = GridLayout(cols=COLS,
                            spacing=SPACING,
                            size_hint_y=None,
                            padding=SPACING)
        layout.bind(minimum_height=layout.setter('height'))

        # Bilder laden
        files = sorted([f for f in os.listdir(IMAGE_FOLDER)
                        if f.lower().endswith((".jpg", ".jpeg", ".png"))], reverse=True)

        for fname in files:
            path = os.path.join(IMAGE_FOLDER, fname)
            # AsyncImage lädt direkt Texture & skaliert
            img = AsyncImage(source=path,
                             size_hint=(None, None),
                             size=(THUMB_W, THUMB_H))
            layout.add_widget(img)

        # ScrollView für vertikales Scrollen
        scroll = ScrollView(size_hint=(1, 1), bar_width=8)
        scroll.add_widget(layout)

        return scroll

if __name__ == "__main__":
    GalleryApp().run()