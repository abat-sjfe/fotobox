import pygame
import sys
from picamera2 import Picamera2
import numpy as np
import time
import os
import subprocess

# Ordner, in dem dieses Script liegt (damit Pfade immer stimmen)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Kamera vorbereiten
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(
    main={"format": "RGB888", "size": (640, 480)}
)
picam2.configure(preview_config)
picam2.start()

# Pygame Setup
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Fotobox")

font = pygame.font.SysFont(None, 48)
big_font = pygame.font.SysFont(None, 150)  # für Countdown-Zahlen

def draw_rounded_button(surface, rect, color, border_color, text, radius=20, border_width=2):
    """Zeichnet einen abgerundeten Button mit Text auf die Oberfläche."""
    button_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(button_surf, color, button_surf.get_rect(), border_radius=radius)
    pygame.draw.rect(button_surf, border_color, button_surf.get_rect(), border_width, border_radius=radius)
    text_surf = font.render(text, True, border_color)
    text_rect = text_surf.get_rect(center=button_surf.get_rect().center)
    button_surf.blit(text_surf, text_rect)
    surface.blit(button_surf, rect)

# Farben
button_color = (255, 255, 255, 50)  # halb transparent
border_color = (0, 0, 0)            # schwarz

# Buttons
button_photo = pygame.Rect(220, 380, 200, 60)  # unten
button_gallery = pygame.Rect(20, 20, 100, 60)  # oben links

clock = pygame.time.Clock()

# Countdown-Status
countdown_active = False
countdown_start_time = 0
countdown_seconds = 5

while True:
    frame = picam2.capture_array()
    frame_surface = pygame.surfarray.make_surface(np.rot90(frame))
    screen.blit(frame_surface, (0, 0))

    # Buttons nur zeichnen, wenn kein Countdown läuft
    if not countdown_active:
        draw_rounded_button(screen, button_photo, button_color, border_color, "Aufnehmen")
        draw_rounded_button(screen, button_gallery, button_color, border_color, "Fotos")
    else:
        # Aktuelle Countdown-Zahl berechnen
        elapsed = (pygame.time.get_ticks() - countdown_start_time) // 1000
        remaining = countdown_seconds - elapsed

        if remaining > 0:
            # große Zahl in die Mitte schreiben
            text_surf = big_font.render(str(remaining), True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(320, 240))
            screen.blit(text_surf, text_rect)
        else:
            # Foto aufnehmen

            # Unterordner 'bilder' verwenden
            bilder_dir = os.path.join(SCRIPT_DIR, "bilder")
            if not os.path.exists(bilder_dir):
                os.makedirs(bilder_dir)
            filename = time.strftime("foto_%Y%m%d_%H%M%S.jpg")
            save_path = os.path.join(bilder_dir, filename)
            picam2.capture_file(save_path)
            print(f"Foto gespeichert unter: {save_path}")

            # Zurück in den Vorschau-Modus
            countdown_active = False
            
            # Absoluter Pfad zur show_image.py
            show_image_script = os.path.join(SCRIPT_DIR, "show_image.py")

            # show_image.py starten und Foto anzeigen
            subprocess.run(["python3", show_image_script, save_path])



    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not countdown_active:  # nur wenn kein Countdown läuft
                if button_photo.collidepoint(event.pos):
                    print("Countdown startet...")
                    countdown_active = True
                    countdown_start_time = pygame.time.get_ticks()
                elif button_gallery.collidepoint(event.pos):
                    print("Galerie-Button gedrückt!")
                    gallery_script = os.path.join(SCRIPT_DIR, "gallery_view.py")
                    subprocess.run(["python3", gallery_script])

    clock.tick(30)