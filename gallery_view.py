import pygame

import os

import subprocess

import math



# --- Einstellungen ---

IMAGE_FOLDER = os.path.dirname(os.path.abspath(__file__))

TILE_W, TILE_H = 240, 180  # "Tilegröße" = Thumbnail-Größe

PADDING = 15

WINDOW_W, WINDOW_H = 640, 480



def load_images(folder):

    imgs = []

    for fname in sorted([f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))], reverse=True):

        path = os.path.join(folder, fname)

        try:

            img = pygame.image.load(path).convert()

            img = pygame.transform.scale(img, (TILE_W, TILE_H))

            imgs.append((img, path))

        except Exception as e:

            print(f"Fehler bei {fname}: {e}")

    return imgs



pygame.init()

screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))

pygame.display.set_caption("Tile-Scroll Galerie")



images = load_images(IMAGE_FOLDER)



# Layout

cols = max(1, WINDOW_W // (TILE_W + PADDING))

rows = math.ceil(len(images) / cols)



scroll_x = 0

scroll_y = 0

dragging = False

drag_start_y = 0

scroll_start_y = 0



running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            dragging = True

            drag_start_y = event.pos[1]

            scroll_start_y = scroll_y

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:

            dragging = False

        elif event.type == pygame.MOUSEMOTION and dragging:

            dy = event.pos[1] - drag_start_y


            scroll_y = max(0, min(rows*(TILE_H+PADDING)-WINDOW_H, scroll_start_y - dy))


            # Touch-typisch: Nach unten ziehen -> nach unten scrollen


            scroll_y = max(0, min(max(0, rows*(TILE_H+PADDING)-WINDOW_H), scroll_start_y + dy))



    screen.fill((30, 30, 30))



    # Dein Rasterprinzip:

    # Starte bei dem Versatz innerhalb eines Tiles (modulo)

    start_y = -(scroll_y % (TILE_H + PADDING))

    first_row = scroll_y // (TILE_H + PADDING)



    y_pos = start_y

    row = first_row

    while y_pos < WINDOW_H and row < rows:

        for col in range(cols):

            idx = row * cols + col

            if idx < len(images):

                x_pos = col * (TILE_W + PADDING) + PADDING

                screen.blit(images[idx][0], (x_pos, y_pos))

        y_pos += TILE_H + PADDING

        row += 1



    pygame.display.flip()

