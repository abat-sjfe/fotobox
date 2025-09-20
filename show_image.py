import sys
import os
import pygame
import numpy as np

def draw_rounded_button(surface, rect, color, border_color, text, font, radius=20, border_width=2):
    button_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(button_surf, color, button_surf.get_rect(), border_radius=radius)
    pygame.draw.rect(button_surf, border_color, button_surf.get_rect(), border_width, border_radius=radius)
    text_surf = font.render(text, True, border_color)
    text_rect = text_surf.get_rect(center=button_surf.get_rect().center)
    button_surf.blit(text_surf, text_rect)
    surface.blit(button_surf, rect)

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

font = pygame.font.SysFont(None, 48)

# Bild laden
image = pygame.image.load(path)

# === Gleiche Drehung wie im Live-Bild ===
img_array = pygame.surfarray.array3d(image)
img_array = np.rot90(img_array)
image = pygame.surfarray.make_surface(img_array)

# Auf Größe skalieren
image = pygame.transform.scale(image, (640, 480))

# Farben
btn_color = (255, 255, 255, 150)
border_color = (0, 0, 0)

# Buttons
save_button = pygame.Rect(100, 400, 180, 60)
delete_button = pygame.Rect(360, 400, 180, 60)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if save_button.collidepoint(event.pos):
                print("Foto gespeichert und behalten.")
                running = False
            elif delete_button.collidepoint(event.pos):
                print("Foto wird gelöscht!")
                try:
                    os.remove(path)
                    print("Datei erfolgreich gelöscht.")
                except Exception as e:
                    print("Fehler beim Löschen:", e)
                running = False

    screen.blit(image, (0, 0))
    draw_rounded_button(screen, save_button, btn_color, border_color, "Speichern", font)
    draw_rounded_button(screen, delete_button, btn_color, border_color, "Löschen", font)

    pygame.display.flip()

pygame.quit()