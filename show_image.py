import os
import sys
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.properties import StringProperty

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(SCRIPT_DIR, "bilder")

class SwipeImageViewer(FloatLayout):
    current_image = StringProperty("")

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

        # Optional caption
        self.caption = Label(
            text=os.path.basename(self.image_list[self.index]),
            size_hint=(1, None),
            height=50,
            pos_hint={"center_x": 0.5, "y": 0},
            color=(1, 1, 1, 1)
        )
        self.add_widget(self.caption)

        # For swipe detection
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
        SWIPE_THRESHOLD = Window.width * 0.2  # 20% swipe length
        if dx > SWIPE_THRESHOLD:
            self.show_previous()
        elif dx < -SWIPE_THRESHOLD:
            self.show_next()
        else:
            # treat as tap to close
            App.get_running_app().stop()
        self.touch_start_x = None

    def _on_key_down(self, window, key, scancode, codepoint, modifier):
        if key in (276, 80):  # left arrow / Kivy left
            self.show_previous()
        elif key in (275, 79):  # right arrow / Kivy right
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


class ShowImageApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 1)
        # Determine which image to start with
        if len(sys.argv) > 1:
            start_path = os.path.abspath(sys.argv[1])
        else:
            # open newest if no file given
            all_imgs = self._get_image_list()
            start_path = all_imgs[0] if all_imgs else ""

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