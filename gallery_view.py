import pygame
import os
import subprocess
import math

pygame.init()

# --- Einstellungen ---
IMAGE_FOLDER = os.path.dirname(os.path.abspath(__file__))   # Ordner mit Bildern
THUMB_SIZE = (200, 150)
PADDING = 10
WINDOW_SIZE = (640, 480)

# --- Hilfsfunktion zum Laden der Bilder ---
def load_images(folder):
    images = []
    files = sorted([f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))], reverse=True)
    for fname in files:
        path = os.path.join(folder, fname)
        try:
            img = pygame.image.load(path).convert()
            img = pygame.transform.scale(img, THUMB_SIZE)
            images.append((img, path))
        except Exception as e:
            print(f"Fehler bei {fname}: {e}")
    return images

# --- Bilder laden ---
images = load_images(IMAGE_FOLDER)

# --- Layout berechnen ---
cols = max(1, WINDOW_SIZE[0] // (THUMB_SIZE[0] + PADDING))
rows = math.ceil(len(images) / cols)
surface_height = rows * (THUMB_SIZE[1] + PADDING) + PADDING

# --- Offscreen-Oberfläche erstellen ---
intermediate = pygame.Surface((WINDOW_SIZE[0], surface_height))
intermediate.fill((30,30,30))

# --- Thumbnails auf offscreen Oberfläche zeichnen ---
for idx, (thumb, path) in enumerate(images):
    row = idx // cols
    col = idx % cols
    x = col * (THUMB_SIZE[0] + PADDING) + PADDING
    y = row * (THUMB_SIZE[1] + PADDING) + PADDING
    intermediate.blit(thumb, (x, y))

# --- Pygame-Hauptfenster ---
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Galerie mit Scroll-Surface")

# --- Scrollvariablen ---
scroll_y = 0
max_scroll = min(0, WINDOW_SIZE[1] - surface_height)  # negativ

clock = pygame.time.Clock()
dragging = False
drag_start_y = 0
scroll_start_y = 0

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 4:  # Mausrad hoch
                scroll_y = min(scroll_y + 30, 0)
            elif e.button == 5:  # Mausrad runter
                scroll_y = max(scroll_y - 30, max_scroll)
            elif e.button == 1:  # Linksklick / Touch-Drag Start
                dragging = True
                drag_start_y = e.pos[1]
                scroll_start_y = scroll_y

        elif e.type == pygame.MOUSEBUTTONUP:
            if e.button == 1:
                dragging = False
                # Klick auf Bild prüfen
                mx, my = e.pos
                # Koordinaten innerhalb der großen Oberfläche
                my_off = my - scroll_y
                col = mx // (THUMB_SIZE[0] + PADDING)
                row = my_off // (THUMB_SIZE[1] + PADDING)
                idx = row * cols + col
                if 0 <= idx < len(images):
                    _, path = images[idx]
                    subprocess.run(["python3", os.path.join(IMAGE_FOLDER, "show_image.py"), path])

        elif e.type == pygame.MOUSEMOTION and dragging:
            dy = e.pos[1] - drag_start_y
            scroll_y = max(max_scroll, min(0, scroll_start_y + dy))

    # --- Zeichnen: nur verschoben reinblitten ---
    screen.fill((0,0,0))
    screen.blit(intermediate, (0, scroll_y))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()