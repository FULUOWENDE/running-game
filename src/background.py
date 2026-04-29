import os

import pygame

from src.constants import (
    GROUND_DARK,
    GROUND_H,
    GROUND_LIGHT,
    GROUND_Y,
    HEIGHT,
    OUTLINE,
    WIDTH,
)


class Background:
    def __init__(self):
        bg_path = os.path.join(os.path.dirname(__file__), "resources", "江西师大背景图.jpg")
        self._bg_image = pygame.image.load(bg_path).convert()
        self._bg_image = pygame.transform.scale(self._bg_image, (WIDTH, HEIGHT))
        self._ground_surf = self._build_ground()

    def _build_ground(self):
        surf = pygame.Surface((WIDTH, GROUND_H))
        for y in range(GROUND_H):
            t = y / GROUND_H
            r = int(GROUND_LIGHT[0] + (GROUND_DARK[0] - GROUND_LIGHT[0]) * t)
            g = int(GROUND_LIGHT[1] + (GROUND_DARK[1] - GROUND_LIGHT[1]) * t)
            b = int(GROUND_LIGHT[2] + (GROUND_DARK[2] - GROUND_LIGHT[2]) * t)
            pygame.draw.line(surf, (r, g, b), (0, y), (WIDTH, y))
        return surf

    def draw(self, surface, ground_offset):
        surface.blit(self._bg_image, (0, 0))
        surface.blit(self._ground_surf, (0, GROUND_Y))
        pygame.draw.line(surface, OUTLINE, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)
        # scrolling road dashes
        dash_w = 40
        gap_w = 20
        dash_y = GROUND_Y + 30
        total_w = dash_w + gap_w
        start_x = -(ground_offset % total_w)
        x = start_x
        while x < WIDTH + total_w:
            if x + dash_w > 0 and x < WIDTH:
                dash_rect = pygame.Rect(max(x, 0), dash_y, min(x + dash_w, WIDTH) - max(x, 0), 4)
                pygame.draw.rect(surface, (220, 220, 200), dash_rect)
            x += total_w
