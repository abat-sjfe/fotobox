import pygame
import sys
from picamera2 import Picamera2
import numpy as np
import time
import os
import subprocess

# --- Paths ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BILDER_DIR = os.path.join(SCRIPT_DIR, "bilder")

# --- Camera setup ---
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(
    main={"format": "RGB888", "size": (640, 480)}
)
picam2.configure(preview_config)
picam2.start()

# --- Pygame setup ---
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Photobooth")

font = pygame.font.SysFont(None, 48)       # for button text
big_font = pygame.font.SysFont(None, 150)  # for countdown numbers

clock = pygame.time.Clock()

# --- Button draw helper ---
def draw_rounded_button(surface, rect, color, border_color, text, radius=20, border_width=2):
    button_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(button_surface, color, button_surface.get_rect(), border_radius=radius)
    pygame.draw.rect(button_surface, border_color, button_surface.get_rect(), border_width, border_radius=radius)
    text_surf = font.render(text, True, border_color)
    text_rect = text_surf.get_rect(center=button_surface.get_rect().center)
    button_surface.blit(text_surf, text_rect)
    surface.blit(button_surface, rect)

# --- Button positions & colours ---
button_color = (255, 255, 255, 100)  # white semi-transparent
border_color = (0, 0, 0)             # black

button_photo = pygame.Rect(220, 380, 200, 60)  # bottom center
button_gallery = pygame.Rect(20, 20, 100, 60)  # top left

# --- Countdown state ---
countdown_active = False
countdown_start_time = 0
countdown_seconds = 5

running = True
while running:
    # Get latest camera frame
    frame = picam2.capture_array()
    frame_surface = pygame.surfarray.make_surface(np.rot90(frame))
    screen.blit(frame_surface, (0, 0))

    # Draw UI
    if not countdown_active:
        draw_rounded_button(screen, button_photo, button_color, border_color, "Take Photo")
        draw_rounded_button(screen, button_gallery, button_color, border_color, "Gallery")
    else:
        elapsed = (pygame.time.get_ticks() - countdown_start_time) // 1000
        remaining = countdown_seconds - elapsed
        if remaining > 0:
            text_surf = big_font.render(str(remaining), True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(320, 240))
            screen.blit(text_surf, text_rect)
        else:
            # Take photo
            if not os.path.exists(BILDER_DIR):
                os.makedirs(BILDER_DIR)
            filename = time.strftime("photo_%Y%m%d_%H%M%S.jpg")
            save_path = os.path.join(BILDER_DIR, filename)
            picam2.capture_file(save_path)
            print(f"Photo saved to: {save_path}")

            countdown_active = False

            # Show image
            show_image_script = os.path.join(SCRIPT_DIR, "show_image.py")
            subprocess.run(["python3", show_image_script, save_path])

    pygame.display.flip()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not countdown_active:  # only when idle
                if button_photo.collidepoint(event.pos):
                    print("Starting countdown...")
                    countdown_active = True
                    countdown_start_time = pygame.time.get_ticks()
                elif button_gallery.collidepoint(event.pos):
                    print("Gallery button pressed")
                    gallery_script = os.path.join(SCRIPT_DIR, "gallery_view.py")
                    subprocess.run(["python3", gallery_script])

    clock.tick(30)