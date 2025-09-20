import sys
import pygame
import os

if len(sys.argv) < 2:
    print("Bildpfad fehlt!")
    sys.exit(1)

path = sys.argv[1]

if not os.path.exists(path):
    print(f"Datei nicht gefunden: {path}")
    sys.exit(1)

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Fotoanzeige")

image = pygame.image.load(path)
image = pygame.transform.scale(image, (640, 480))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            running = False

    screen.blit(image, (0, 0))
    pygame.display.flip()

pygame.quit()