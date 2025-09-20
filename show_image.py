import os
import sys
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.label import Label

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(SCRIPT_DIR, "bilder")


class SwipeImageViewer(FloatLayout):
    def __init__(self, image_list, start_index=0, **kwargs):
        super().__init__(**kwargs)
        self.image_list = image_list
        self.index = start_index

        # Image widget
        self.image_widget = Image(
            source=self.image_list[self.index],
            allow_stretch=True,
            keep_ratio=True
        )
        self.add_widget(self.image_widget)

        # Caption filename
        self.caption = Label(
            text=os.path.basename(self.image_list[self.index]),
            size_hint=(1, None),
            height=40,
            pos_hint={"center_x": 0.5, "y": 0.9},
            color=(1, 1, 1, 1)
        )
        self.add_widget(self.caption)

        # Save button
        self.save_button = Button(
            text="Speichern",
            size_hint=(None, None),
            size=(180, 60),
            pos_hint={"x": 0.15, "y": 0.05}
        )
        self.save_button.bind(on_release=self.keep_photo)
        self.add_widget(self.save_button)

        # Delete button
        self.delete_button = Button(
            text="Löschen",
            size_hint=(None, None),
            size=(180, 60),
            pos_hint={"right": 0.85, "y": 0.05}
        )
        self.delete_button.bind(on_release=self.delete_photo)
        self.add_widget(self.delete_button)

        # Swipe detection
        Window.bind(on_touch_down=self._on_touch_down)
        Window.bind(on_touch_up=self._on_touch_up)
        Window.bind(on_key_down=self._on_key_down)
        self.touch_start_x = None

    def _on_touch_down(self, window, touch):
        self.touch_start_x = touch.x

    def _on_touch_up(self, window, touch):
        if self.touch_start_x is None:
            return
        dx = touch.x - self.touch_start_x
        SWIPE_THRESHOLD = Window.width * 0.2
        if dx > SWIPE_THRESHOLD:
            self.show_previous()
        elif dx < -SWIPE_THRESHOLD:
            self.show_next()
        self.touch_start_x = None

    def _on_key_down(self, window, key, scancode, codepoint, modifiers):
        if key in (276, 80):  # left arrow
            self.show_previous()
        elif key in (275, 79):  # right arrow
            self.show_next()
        elif key == 27:  # ESC
            App.get_running_app().stop()

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
        print("Photo kept")
        App.get_running_app().stop()

    def delete_photo(self, instance):
        current_file = self.image_list[self.index]
        print(f"Deleting: {current_file}")
        try:
            os.remove(current_file)
        except Exception as e:
            print("Error deleting file:", e)
        # Remove from list and move on
        del self.image_list[self.index]
        if not self.image_list:  # no more images
            App.get_running_app().stop()
            return
        if self.index >= len(self.image_list):
            self.index = len(self.image_list) - 1
        self.update_image()


class ShowImageApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 1)
        if len(sys.argv) > 1:
            start_path = os.path.abspath(sys.argv[1])
        else:
            imgs = self._get_image_list()
            start_path = imgs[0] if imgs else ""

        image_list = self._get_image_list()
        start_index = 0
        if start_path in image_list:
            start_index = image_list.index(start_path)

        return SwipeImageViewer(image_list, start_index)

    def _get_image_list(self):
        if not os.path.exists(IMAGE_FOLDER):
            return []
        files = sorted(
            [os.path.join(IMAGE_FOLDER, f) for f in os.listdir(IMAGE_FOLDER)
             if f.lower().endswith((".jpg", ".jpeg", ".png"))],
            reverse=True
        )
        return files


if __name__ == "__main__":
    ShowImageApp().run()