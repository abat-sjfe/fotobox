# show_image.py
import sys
import pygame
import os

def show_image(path):
    # Falls Datei nicht existiert
    if not os.path.exists(path):
        print(f"Datei nicht gefunden: {path}")
        return

    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Fotoanzeige")

    # Bild laden
    img = pygame.image.load(path)
    img = pygame.transform.scale(img, (640, 480))

    running = True
    while running:
        screen.blit(img, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = False

    pygame.quit()


# Damit man das Skript auch separat starten kann:
if __name__ == "__main__":
    if len(sys.argv) > 1:
        show_image(sys.argv[1])
    else:
        print("Benutzung: python3 show_image.py <bilddatei>")