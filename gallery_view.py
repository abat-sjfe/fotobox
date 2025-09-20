import os
import pygame
import subprocess
import math
import time

# === EINSTELLUNGEN ===
IMAGE_FOLDER = os.path.dirname(os.path.abspath(__file__))  # Foto-Ordner
THUMB_SIZE = (240, 180)   # Touch-freundliche Größe
PADDING = 15
WINDOW_SIZE = (640, 480)

# Tap/Scroll-Erkennung
TAP_MAX_DISTANCE = 15      # Pixel
TAP_MAX_TIME = 0.25        # Sekunden

def load_images_from_folder(folder):
    images = []
    files = sorted([f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))], reverse=True)
    for fname in files:
        path = os.path.join(folder, fname)
        try:
            img = pygame.image.load(path).convert()
            img = pygame.transform.scale(img, THUMB_SIZE)
            images.append((img, path))
        except Exception as e:
            print(f"Fehler beim Laden von {fname}: {e}")
    return images

def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Fotobox Galerie (Touch Ready)")

    images = load_images_from_folder(IMAGE_FOLDER)

    scroll_y = 0
    dragging = False
    drag_start_y = 0
    scroll_start_y = 0

    tap_start_time = 0
    tap_start_pos = (0, 0)

    # Raster-Berechnung
    cols = max(1, WINDOW_SIZE[0] // (THUMB_SIZE[0] + PADDING))
    rows_needed = math.ceil(len(images) / cols)
    max_scroll = max(0, rows_needed * (THUMB_SIZE[1] + PADDING) - WINDOW_SIZE[1])

    running = True
    while running:
        for event in pygame.event.get():
            # -------------------------------
            # Maus-Events (auch Finger als Maus)
            # -------------------------------
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Linksklick oder Touch
                    dragging = True
                    drag_start_y = event.pos[1]
                    scroll_start_y = scroll_y
                    tap_start_time = time.time()
                    tap_start_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
                    # Prüfen ob TAP
                    tap_duration = time.time() - tap_start_time
                    dist_x = abs(event.pos[0] - tap_start_pos[0])
                    dist_y = abs(event.pos[1] - tap_start_pos[1])
                    if tap_duration <= TAP_MAX_TIME and dist_x < TAP_MAX_DISTANCE and dist_y < TAP_MAX_DISTANCE:
                        mx, my = event.pos
                        my += scroll_y
                        col = mx // (THUMB_SIZE[0] + PADDING)
                        row = my // (THUMB_SIZE[1] + PADDING)
                        index = row * cols + col
                        if 0 <= index < len(images):
                            _, path = images[index]
                            subprocess.run(["python3", os.path.join(IMAGE_FOLDER, "show_image.py"), path])

            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    dy = event.pos[1] - drag_start_y
                    scroll_y = scroll_start_y - dy
                    scroll_y = max(0, min(max_scroll, scroll_y))

            # -------------------------------
            # Touchscreen-Events (FINGER...)
            # -------------------------------
            elif event.type == pygame.FINGERDOWN:
                dragging = True
                # Y in Pixel umrechnen
                drag_start_y = int(event.y * WINDOW_SIZE[1])
                scroll_start_y = scroll_y
                tap_start_time = time.time()
                tap_start_pos = (int(event.x * WINDOW_SIZE[0]), int(event.y * WINDOW_SIZE[1]))

            elif event.type == pygame.FINGERUP:
                dragging = False
                tap_duration = time.time() - tap_start_time
                end_pos = (int(event.x * WINDOW_SIZE[0]), int(event.y * WINDOW_SIZE[1]))
                dist_x = abs(end_pos[0] - tap_start_pos[0])
                dist_y = abs(end_pos[1] - tap_start_pos[1])
                if tap_duration <= TAP_MAX_TIME and dist_x < TAP_MAX_DISTANCE and dist_y < TAP_MAX_DISTANCE:
                    mx, my = end_pos
                    my += scroll_y
                    col = mx // (THUMB_SIZE[0] + PADDING)
                    row = my // (THUMB_SIZE[1] + PADDING)
                    index = row * cols + col
                    if 0 <= index < len(images):
                        _, path = images[index]
                        subprocess.run(["python3", os.path.join(IMAGE_FOLDER, "show_image.py"), path])

            elif event.type == pygame.FINGERMOTION:
                if dragging:
                    dy = int(event.y * WINDOW_SIZE[1]) - drag_start_y
                    scroll_y = scroll_start_y - dy
                    scroll_y = max(0, min(max_scroll, scroll_y))

        # -------------------------------
        # Zeichnen
        # -------------------------------
        screen.fill((30, 30, 30))
        y_offset = -scroll_y

        for i, (thumb, _) in enumerate(images):
            row = i // cols
            col = i % cols
            x = col * (THUMB_SIZE[0] + PADDING) + PADDING
            y = row * (THUMB_SIZE[1] + PADDING) + PADDING + y_offset

            if y + THUMB_SIZE[1] > 0 and y < WINDOW_SIZE[1]:
                screen.blit(thumb, (x, y))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()