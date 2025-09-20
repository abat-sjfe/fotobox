from camera_screen_pg import run_camera_screen
from gallery_kv import GalleryApp
from viewer_kv import ShowImageApp

state = "camera"
selected_image = None

while True:
    if state == "camera":
        # returns "gallery" or "quit"
        result = run_camera_screen()
        if result == "gallery":
            state = "gallery"
        elif result == "quit":
            break

    elif state == "gallery":
        # returns ("viewer", path) or ("camera", None)
        result, selected_image = GalleryApp().run()
        if result == "viewer":
            state = "viewer"
        elif result == "camera":
            state = "camera"
        elif result == "quit":
            break

    elif state == "viewer":
        # returns "gallery" or "quit"
        result = ShowImageApp(start_path=selected_image).run()
        if result == "gallery":
            state = "gallery"
        elif result == "quit":
            break