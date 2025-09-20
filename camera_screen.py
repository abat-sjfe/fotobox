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

def draw_rounded_button(surface, rect, color, border_color, text, radius=20, border_width=4):
    # Transparente Fläche erstellen
    button_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

    # Abgerundetes Rechteck zeichnen
    pygame.draw.rect(button_surf, color, button_surf.get_rect(), border_radius=radius)
    pygame.draw.rect(button_surf, border_color, button_surf.get_rect(), border_width, border_radius=radius)
    
    # Text zentriert hinzufügen
    text_surf = font.render(text, True, border_color)
    text_rect = text_surf.get_rect(center=button_surf.get_rect().center)
    button_surf.blit(text_surf, text_rect)

    # Button auf Hauptfläche zeichnen
    surface.blit(button_surf, rect)

# Farbeinstellungen
button_color = (255, 255, 255, 100)   # halb transparent
border_color = (255, 0, 0)            # rot

button_rect = pygame.Rect(220, 380, 200, 60)  # Position und Größe

clock = pygame.time.Clock()

while True:
    # Kamera-Frame holen
    frame = picam2.capture_array()

    # In Pygame Surface konvertieren
    frame_surface = pygame.surfarray.make_surface(np.rot90(frame))

    # Vorschau zeichnen
    screen.blit(frame_surface, (0, 0))

    # Button zeichnen
    draw_rounded_button(screen, button_rect, button_color, border_color, "Aufnehmen")

    # Bildschirm aktualisieren
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                print("Foto machen!")  # hier Aufnahmefunktion einbauen
    
    clock.tick(30)