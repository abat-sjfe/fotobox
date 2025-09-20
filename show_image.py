import sys
import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Fotoanzeige")

if len(sys.argv) < 2:
    print("Bildpfad fehlt!")
    sys.exit(1)

path = sys.argv[1]
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