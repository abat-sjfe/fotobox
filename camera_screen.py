import pygame
import sys
from picamera2 import Picamera2
import numpy as np

# Kamera vorbereiten
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)})
picam2.configure(preview_config)
picam2.start()

# Pygame Setup
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Fotobox")

font = pygame.font.SysFont(None, 48)

def draw_rounded_button(surface, rect, color, border_color, text, radius=20, border_width=2):
    button_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(button_surf, color, button_surf.get_rect(), border_radius=radius)
    pygame.draw.rect(button_surf, border_color, button_surf.get_rect(), border_width, border_radius=radius)
    text_surf = font.render(text, True, border_color)
    text_rect = text_surf.get_rect(center=button_surf.get_rect().center)
    button_surf.blit(text_surf, text_rect)
    surface.blit(button_surf, rect)

# Farbeinstellungen
button_color = (255, 255, 255, 25)   # halb transparent
border_color = (0, 0, 0)             # schwarz

# Buttons
button_photo = pygame.Rect(220, 380, 200, 60)   # unten mittig
button_gallery = pygame.Rect(20, 20, 100, 60)    # oben links

clock = pygame.time.Clock()

while True:
    frame = picam2.capture_array()
    frame_surface = pygame.surfarray.make_surface(np.rot90(frame))
    screen.blit(frame_surface, (0, 0))

    # Buttons zeichnen
    draw_rounded_button(screen, button_photo, button_color, border_color, "Aufnehmen")
    draw_rounded_button(screen, button_gallery, button_color, border_color, "Gallerie")

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_photo.collidepoint(event.pos):
                print("Foto machen!")
            elif button_gallery.collidepoint(event.pos):
                print("Gallerie-Button gedrückt!")

    clock.tick(30)