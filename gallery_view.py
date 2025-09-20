import os
import pygame

# === EINSTELLUNGEN ===
IMAGE_FOLDER = os.path.dirname(os.path.abspath(__file__))  # Ordner mit den Fotos
THUMB_WIDTH = 200
PADDING = 10
WINDOW_SIZE = (640, 480)

def load_images_from_folder(folder):
    """Alle JPG/PNG finden und Thumbnails erzeugen."""
    images = []
    files = [f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    for fname in sorted(files, reverse=True):  # neueste zuerst
        path = os.path.join(folder, fname)
        try:
            img = pygame.image.load(path).convert()
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

    scroll_y = 0
    max_scroll = max(0, sum(img.get_height() + PADDING for img, _ in images) - WINDOW_SIZE[1])

    dragging = False
    drag_start_y = 0
    scroll_start_y = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEWHEEL:
                scroll_y -= event.y * 30
                scroll_y = max(0, min(max_scroll, scroll_y))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Linksklick
                    dragging = True
                    drag_start_y = event.pos[1]
                    scroll_start_y = scroll_y

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False

            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    dy = event.pos[1] - drag_start_y
                    scroll_y = scroll_start_y - dy  # natürliches Scrollen
                    scroll_y = max(0, min(max_scroll, scroll_y))

        # Hintergrund
        screen.fill((50, 50, 50))

        # Bilder rendern
        y = -scroll_y
        for thumb, path in images:
            screen.blit(thumb, (PADDING, y))
            filename = os.path.basename(path)
            text_surface = font.render(filename, True, (255, 255, 255))
            screen.blit(text_surface, (THUMB_WIDTH + 2 * PADDING, y + 10))
            y += thumb.get_height() + PADDING

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()