# viewer_kv.py
import os
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(SCRIPT_DIR, "bilder")

class SwipeImageViewer(FloatLayout):
    def __init__(self, image_list, start_index=0, parent_app=None, **kwargs):
        super().__init__(**kwargs)
        self.image_list = image_list
        self.index = start_index
        self.parent_app = parent_app

        # Image
        self.image_widget = Image(source=self.image_list[self.index],
                                  allow_stretch=True, keep_ratio=True)
        self.add_widget(self.image_widget)

        # Caption
        self.caption = Label(text=os.path.basename(self.image_list[self.index]),
                             size_hint=(1, None), height=40,
                             pos_hint={"center_x": 0.5, "y": 0.9})
        self.add_widget(self.caption)

        # Save & Delete Buttons
        self.save_button = Button(text="Speichern", size_hint=(None, None),
                                  size=(180, 60), pos_hint={"x": 0.15, "y": 0.05})
        self.save_button.bind(on_release=self.keep_photo)
        self.add_widget(self.save_button)

        self.delete_button = Button(text="Löschen", size_hint=(None, None),
                                    size=(180, 60), pos_hint={"right": 0.85, "y": 0.05})
        self.delete_button.bind(on_release=self.delete_photo)
        self.add_widget(self.delete_button)

        # Swipe detection
        Window.bind(on_touch_down=self._on_touch_down)
        Window.bind(on_touch_up=self._on_touch_up)
        self.touch_start_x = None

    def _on_touch_down(self, window, touch):
        self.touch_start_x = touch.x

    def _on_touch_up(self, window, touch):
        dx = touch.x - self.touch_start_x
        SWIPE_THRESHOLD = Window.width * 0.2
        if dx > SWIPE_THRESHOLD:
            self.show_previous()
        elif dx < -SWIPE_THRESHOLD:
            self.show_next()
        self.touch_start_x = None

    def show_next(self):
        if self.index < len(self.image_list) - 1:
            self.index += 1
            self.update_image()

    def show_previous(self):
        if self.index > 0:
            self.index -= 1
            self.update_image()

    def update_image(self):
        self.image_widget.source = self.image_list[self.index]
        self.caption.text = os.path.basename(self.image_list[self.index])

    def keep_photo(self, instance):
        self.parent_app.stop()

    def delete_photo(self, instance):
        current_file = self.image_list[self.index]
        try:
            os.remove(current_file)
        except:
            pass
        del self.image_list[self.index]
        if self.index >= len(self.image_list):
            self.index = len(self.image_list) - 1
        if not self.image_list:
            self.parent_app.stop()
        else:
            self.update_image()

class ShowImageApp(App):
    def __init__(self, start_path=None, **kwargs):
        super().__init__(**kwargs)
        self.start_path = start_path

    def build(self):
        image_list = self._get_image_list()
        start_index = image_list.index(self.start_path) if self.start_path in image_list else 0
        return SwipeImageViewer(image_list, start_index=start_index, parent_app=self)

    def _get_image_list(self):
        files = sorted(
            [os.path.join(IMAGE_FOLDER, f) for f in os.listdir(IMAGE_FOLDER)
             if f.lower().endswith((".jpg", ".jpeg", ".png"))],
            reverse=True
        )
        return files

    def run(self):
        super().run()
        return "gallery"