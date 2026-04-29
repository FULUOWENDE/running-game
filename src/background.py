import math
import random

import pygame

from src.constants import (
    BUILDING_PALETTE,
    CLOUD,
    GROUND_DARK,
    GROUND_H,
    GROUND_LIGHT,
    GROUND_Y,
    HEIGHT,
    OUTLINE,
    ROAD_LINE,
    SKY_BOTTOM,
    SKY_TOP,
    WIDTH,
)


class Background:
    def __init__(self):
        self._sky_surf = self._build_sky()
        self.clouds = self._build_clouds()
        self.buildings = self._build_buildings()
        self.trees = self._build_trees()
        self._ground_surf = self._build_ground()

    # ── Sky ───────────────────────────────────────────────────────
    def _build_sky(self):
        surf = pygame.Surface((WIDTH, GROUND_Y))
        for y in range(GROUND_Y):
            t = y / GROUND_Y
            r = int(SKY_TOP[0] + (SKY_BOTTOM[0] - SKY_TOP[0]) * t)
            g = int(SKY_TOP[1] + (SKY_BOTTOM[1] - SKY_TOP[1]) * t)
            b = int(SKY_TOP[2] + (SKY_BOTTOM[2] - SKY_TOP[2]) * t)
            pygame.draw.line(surf, (r, g, b), (0, y), (WIDTH, y))
        return surf

    # ── Clouds ────────────────────────────────────────────────────
    def _build_clouds(self):
        clouds = []
        for i in range(6):
            cw = 60 + random.random() * 100
            ch = 22 + random.random() * 18
            clouds.append({
                "x": (i / 6) * WIDTH + random.random() * 80,
                "y": 40 + random.random() * 90,
                "rw": cw,
                "rh": ch,
                "spd": 0.4 + random.random() * 0.5,
            })
        return clouds

    def update_clouds(self, speed_factor):
        for cl in self.clouds:
            cl["x"] -= cl["spd"] * speed_factor * 0.35
            if cl["x"] + cl["rw"] < 0:
                cl["x"] = WIDTH + cl["rw"]
                cl["y"] = 40 + random.random() * 90

    def draw_clouds(self, surface):
        for cl in self.clouds:
            cx, cy = cl["x"], cl["y"]
            rw, rh = cl["rw"] / 2, cl["rh"] / 2
            alpha_surf = pygame.Surface((WIDTH, GROUND_Y), pygame.SRCALPHA)
            cloud_color = (*CLOUD, 33)
            pygame.draw.ellipse(alpha_surf, cloud_color, (cx, cy, rw, rh * 2))
            pygame.draw.ellipse(alpha_surf, cloud_color, (cx - rw * 0.28, cy + 4, rw * 0.64, rh * 1.6))
            pygame.draw.ellipse(alpha_surf, cloud_color, (cx + rw * 0.28, cy + 4, rw * 0.54, rh * 1.52))
            surface.blit(alpha_surf, (0, 0))

    # ── Buildings ─────────────────────────────────────────────────
    def _build_buildings(self):
        defs = [
            (30, 38, 100), (78, 28, 125), (115, 48, 80), (172, 32, 140),
            (214, 24, 100), (248, 44, 90), (302, 36, 110), (348, 52, 75),
            (410, 28, 130), (448, 42, 85), (500, 30, 115), (540, 50, 70),
            (600, 36, 105), (646, 28, 125), (684, 48, 80), (742, 30, 120),
            (782, 44, 90), (836, 26, 100),
        ]
        buildings = []
        for bx, bw, bh in defs:
            color = random.choice(BUILDING_PALETTE)
            windows = []
            for wy in range(int(GROUND_Y - bh + 10), int(GROUND_Y - 15), 16):
                for wx in range(bx + 5, bx + bw - 6, 12):
                    windows.append({"x": wx, "y": wy, "lit": random.random() > 0.38})
            buildings.append({"x": bx, "w": bw, "h": bh, "color": color, "windows": windows})
        return buildings

    def draw_buildings(self, surface, offset):
        for b in self.buildings:
            bx = b["x"] - offset
            if bx + b["w"] < -50:
                bx += WIDTH + 200
            rect = pygame.Rect(bx, GROUND_Y - b["h"], b["w"], b["h"])
            pygame.draw.rect(surface, b["color"], rect)
            pygame.draw.rect(surface, OUTLINE, rect, width=1)
            for wn in b["windows"]:
                if wn["lit"]:
                    wx = wn["x"] - offset
                    while wx < -10:
                        wx += WIDTH + 200
                    while wx > WIDTH + 10:
                        wx -= WIDTH + 200
                    pygame.draw.rect(surface, (255, 240, 150), (wx, wn["y"], 5, 8))

    # ── Trees ─────────────────────────────────────────────────────
    def _build_trees(self):
        trees = []
        for _ in range(8):
            trees.append({
                "x": random.random() * WIDTH,
                "height": 40 + random.random() * 40,
                "width": 18 + random.random() * 16,
            })
        return trees

    def draw_trees(self, surface, offset):
        for t in self.trees:
            tx = t["x"] - offset
            while tx < -50:
                tx += WIDTH + 100
            while tx > WIDTH + 50:
                tx -= WIDTH + 100
            base_y = GROUND_Y
            # trunk
            trunk_w = 6
            pygame.draw.rect(surface, (120, 80, 50), (tx - trunk_w / 2, base_y - t["height"] * 0.5, trunk_w, t["height"] * 0.5))
            # foliage (3 overlapping circles)
            fw = t["width"]
            fh = t["height"] * 0.6
            pygame.draw.circle(surface, (60, 150, 70), (tx, int(base_y - t["height"] * 0.55)), int(fw * 0.7))
            pygame.draw.circle(surface, (80, 170, 90), (tx - fw * 0.35, int(base_y - t["height"] * 0.35)), int(fw * 0.55))
            pygame.draw.circle(surface, (100, 190, 110), (tx + fw * 0.35, int(base_y - t["height"] * 0.38)), int(fw * 0.5))

    # ── Ground ────────────────────────────────────────────────────
    def _build_ground(self):
        surf = pygame.Surface((WIDTH, GROUND_H))
        for y in range(GROUND_H):
            t = y / GROUND_H
            r = int(GROUND_LIGHT[0] + (GROUND_DARK[0] - GROUND_LIGHT[0]) * t)
            g = int(GROUND_LIGHT[1] + (GROUND_DARK[1] - GROUND_LIGHT[1]) * t)
            b = int(GROUND_LIGHT[2] + (GROUND_DARK[2] - GROUND_LIGHT[2]) * t)
            pygame.draw.line(surf, (r, g, b), (0, y), (WIDTH, y))
        return surf

    def draw_ground(self, surface, offset):
        surface.blit(self._ground_surf, (0, GROUND_Y))
        # Horizon line
        pygame.draw.line(surface, OUTLINE, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)
        # Scrolling road dashes
        dash_w = 40
        gap_w = 20
        dash_y = GROUND_Y + 30
        total_w = dash_w + gap_w
        start_x = -(offset % total_w)
        x = start_x
        while x < WIDTH + total_w:
            if x + dash_w > 0 and x < WIDTH:
                dash_rect = pygame.Rect(max(x, 0), dash_y, min(x + dash_w, WIDTH) - max(x, 0), 4)
                pygame.draw.rect(surface, (220, 220, 200), dash_rect)
            x += total_w

    # ── Public draw ───────────────────────────────────────────────
    def draw(self, surface, ground_offset, speed, state_playing):
        surface.blit(self._sky_surf, (0, 0))
        speed_factor = speed / 5.5 if state_playing else 0
        self.draw_clouds(surface)
        if state_playing:
            self.update_clouds(speed_factor)
        bld_offset = (ground_offset * 0.5) % (WIDTH + 200)
        self.draw_buildings(surface, bld_offset)
        tree_offset = (ground_offset * 0.7) % (WIDTH + 100)
        self.draw_trees(surface, tree_offset)
        self.draw_ground(surface, ground_offset)
