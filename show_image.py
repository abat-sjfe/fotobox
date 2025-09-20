import pygame
import os
import math
import subprocess

# --- Settings ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(SCRIPT_DIR, "bilder")
TILE_W, TILE_H = 240, 180
PADDING = 15
WINDOW_W, WINDOW_H = 640, 480

pygame.init()
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("Photo Gallery")

clock = pygame.time.Clock()

# --- Load thumbnails ---
def load_images(folder):
    images = []
    if not os.path.exists(folder):
        return images
    files = sorted(
        [f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))],
        reverse=True
    )
    for fname in files:
        path = os.path.join(folder, fname)
        try:
            img = pygame.image.load(path).convert()
            img = pygame.transform.scale(img, (TILE_W, TILE_H))
            images.append((img, path))
        except Exception as e:
            print(f"Error loading {fname}: {e}")
    return images

images = load_images(IMAGE_FOLDER)

# --- Layout ---
cols = max(1, WINDOW_W // (TILE_W + PADDING))
rows = math.ceil(len(images) / cols)
max_scroll = max(0, rows * (TILE_H + PADDING) - WINDOW_H)

scroll_y = 0
dragging = False
drag_start_y = 0
scroll_start_y = 0

# Optional momentum
velocity = 0
last_mouse_y = 0

# --- Main loop ---
running = True
while running:
    dt = clock.tick(60) / 1000.0  # seconds/frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # touch or left mouse
                dragging = True
                drag_start_y = event.pos[1]
                scroll_start_y = scroll_y
                velocity = 0
                last_mouse_y = event.pos[1]

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
                velocity = (event.pos[1] - last_mouse_y) / dt * 0.02

                # Detect click/tap without drag
                if abs(event.pos[1] - drag_start_y) < 5:
                    # Translate mouse position to gallery coordinates
                    mx, my = event.pos
                    my_off = my + scroll_y
                    col = mx // (TILE_W + PADDING)
                    row = my_off // (TILE_H + PADDING)
                    idx = int(row * cols + col)
                    if 0 <= idx < len(images):
                        _, path = images[idx]
                        print(f"Opening {path}...")
                        subprocess.run(["python3", os.path.join(SCRIPT_DIR, "show_image.py"), path])

        elif event.type == pygame.MOUSEMOTION and dragging:
            dy = event.pos[1] - drag_start_y
            scroll_y = min(max_scroll, max(0, scroll_start_y - dy))
            last_mouse_y = event.pos[1]

    # Momentum scroll if not dragging
    if not dragging and abs(velocity) > 0.1:
        scroll_y = min(max_scroll, max(0, scroll_y - velocity))
        velocity *= 0.92
        if abs(velocity) < 0.05:
            velocity = 0

    # --- Draw ---
    screen.fill((30, 30, 30))

    start_y = -(scroll_y % (TILE_H + PADDING))
    first_row = scroll_y // (TILE_H + PADDING)

    y_pos = start_y
    row = int(first_row)
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