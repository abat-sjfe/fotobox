import os
import pygame
import subprocess
import math

# === EINSTELLUNGEN ===
IMAGE_FOLDER = os.path.dirname(os.path.abspath(__file__))  # Foto-Ordner
THUMB_SIZE = (200, 150)    # Größe der Thumbnails (Breite, Höhe)
PADDING = 10               # Abstand zwischen Bildern
WINDOW_SIZE = (640, 480)   # Fenstergröße

def load_images_from_folder(folder):
    images = []
    files = [f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    for fname in sorted(files, reverse=True):  # neueste zuerst
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
    pygame.display.set_caption("Fotobox Galerie")

    images = load_images_from_folder(IMAGE_FOLDER)
    scroll_y = 0
    dragging = False
    drag_start_y = 0
    scroll_start_y = 0

    # Berechne Layout
    cols = max(1, WINDOW_SIZE[0] // (THUMB_SIZE[0] + PADDING))
    rows_needed = math.ceil(len(images) / cols)
    max_scroll = max(0, rows_needed * (THUMB_SIZE[1] + PADDING) - WINDOW_SIZE[1])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEWHEEL:
                scroll_y -= event.y * 30
                scroll_y = max(0, min(max_scroll, scroll_y))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging = True
                    drag_start_y = event.pos[1]
                    scroll_start_y = scroll_y

                    # --- Bildklick prüfen ---
                    mx, my = event.pos
                    my += scroll_y
                    col = mx // (THUMB_SIZE[0] + PADDING)
                    row = my // (THUMB_SIZE[1] + PADDING)
                    index = row * cols + col
                    if 0 <= index < len(images):
                        # Pfad des angeklickten Bildes
                        _, path = images[index]
                        # show_image.py aufrufen
                        try:
                            subprocess.run(["python3", os.path.join(IMAGE_FOLDER, "show_image.py"), path])
                        except FileNotFoundError:
                            print("show_image.py nicht gefunden! Lege es ins gleiche Verzeichnis.")

                elif event.button == 4:  # Mausrad hoch (Fallback)
                    scroll_y = max(0, scroll_y - 30)
                elif event.button == 5:  # Mausrad runter (Fallback)
                    scroll_y = min(max_scroll, scroll_y + 30)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False

            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    dy = event.pos[1] - drag_start_y
                    scroll_y = scroll_start_y - dy
                    scroll_y = max(0, min(max_scroll, scroll_y))

        # --- Zeichnen ---
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