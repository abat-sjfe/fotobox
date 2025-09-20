import pygame
import os
import math

# --- Einstellungen ---
IMAGE_FOLDER = os.path.dirname(os.path.abspath(__file__))
TILE_W, TILE_H = 240, 180  # Thumbnail-Größe
PADDING = 15
WINDOW_W, WINDOW_H = 640, 480

def load_images(folder):
    imgs = []
    for fname in sorted(
        [f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))],
        reverse=True
    ):
        path = os.path.join(folder, fname)
        try:
            img = pygame.image.load(path).convert()
            img = pygame.transform.scale(img, (TILE_W, TILE_H))
            imgs.append((img, path))
        except Exception as e:
            print(f"Fehler bei {fname}: {e}")
    return imgs

pygame.init()
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("Tile-Scroll Galerie")

images = load_images(IMAGE_FOLDER)

# Layout
cols = max(1, WINDOW_W // (TILE_W + PADDING))
rows = math.ceil(len(images) / cols)
max_scroll = max(0, rows * (TILE_H + PADDING) - WINDOW_H)

# Scroll-Variablen
scroll_y = 0
dragging = False
drag_start_y = 0
scroll_start_y = 0

# Momentum-Variablen
velocity = 0
last_mouse_y = 0

clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000.0  # Sekunden pro Frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Maus (und Touch emuliert als Maus!)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Linke Taste oder 1-Finger-Touch
                dragging = True
                drag_start_y = event.pos[1]
                scroll_start_y = scroll_y
                velocity = 0  # Momentum wird zurückgesetzt
                last_mouse_y = event.pos[1]

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
                # Geschwindigkeit beim Loslassen merken
                velocity = -(event.pos[1] - last_mouse_y) / dt * 0.02  # Faktor justierbar

        elif event.type == pygame.MOUSEMOTION and dragging:
            dy = event.pos[1] - drag_start_y
            scroll_y = max(0, min(max_scroll, scroll_start_y - dy))
            last_mouse_y = event.pos[1]

    # Momentum-Scroll wenn nicht am Ziehen
    if not dragging and abs(velocity) > 0.1:
        scroll_y = max(0, min(max_scroll, scroll_y + velocity))
        velocity *= 0.92  # Abbremsung pro Frame
        # Stoppen, wenn fast keine Bewegung mehr
        if abs(velocity) < 0.05:
            velocity = 0

    # --- Zeichnen ---
    screen.fill((30, 30, 30))

    # Sichtbare Zeilen berechnen
    start_y = -(scroll_y % (TILE_H + PADDING))
    first_row = scroll_y // (TILE_H + PADDING)

    y_pos = start_y
    row = first_row
    while y_pos < WINDOW_H and row < rows:
        for col in range(cols):
            idx = row * cols + col
            if idx < len(images):
                x_pos = col * (TILE_W + PADDING) + PADDING
                screen.blit(images[idx][0], (x_pos, y_pos))
        y_pos += TILE_H + PADDING
        row += 1

    pygame.display.flip()

pygame.quit()