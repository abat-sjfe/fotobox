import os
import sys
import pygame

# --- Einstellungen ---
IMAGE_FOLDER = os.path.dirname(os.path.abspath(__file__))  # aktueller Ordner
THUMB_WIDTH = 200
PADDING = 10
WINDOW_SIZE = (640, 480)

def load_images_from_folder(folder):
    """Sucht JPG-Bilder im Ordner und erstellt Thumbnails."""
    images = []
    for fname in sorted(os.listdir(folder), reverse=True):
        if fname.lower().endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(folder, fname)
            try:
                img = pygame.image.load(path)
                # Verhältnis beibehalten
                ratio = THUMB_WIDTH / img.get_width()
                new_height = int(img.get_height() * ratio)
                img = pygame.transform.scale(img, (THUMB_WIDTH, new_height))
                images.append((img, path))
            except Exception as e:
                print(f"Fehler beim Laden von {fname}: {e}")
    return images

def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Bilder-Galerie")

    font = pygame.font.SysFont(None, 24)

    images = load_images_from_folder(IMAGE_FOLDER)

    scroll_y = 0  # Startposition
    max_scroll = max(0, sum(img.get_height() + PADDING for img, _ in images) - WINDOW_SIZE[1])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    scroll_y = min(scroll_y + 30, max_scroll)
                elif event.key == pygame.K_UP:
                    scroll_y = max(scroll_y - 30, 0)
            elif event.type == pygame.MOUSEWHEEL:
                scroll_y = max(0, min(max_scroll, scroll_y - event.y * 30))

        screen.fill((50, 50, 50))

        y = -scroll_y
        for thumb, path in images:
            screen.blit(thumb, (PADDING, y))
            # Dateiname zeichnen
            filename = os.path.basename(path)
            text_surface = font.render(filename, True, (255, 255, 255))
            screen.blit(text_surface, (THUMB_WIDTH + 2 * PADDING, y + 10))
            y += thumb.get_height() + PADDING

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()