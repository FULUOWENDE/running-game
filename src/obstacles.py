import random

import pygame

from src.constants import (
    BIKE_GREEN,
    BIKE_RIDER,
    BIKE_TIRE,
    BUMP_BLACK,
    BUMP_YELLOW,
    CART_RED,
    CART_SILVER,
    CONE_ORANGE,
    CONE_WHITE,
    GROUND_Y,
    MIN_SPAWN_GAP,
    OUTLINE,
    SIGN_BOARD,
    SIGN_POLE,
    TAPE_YELLOW,
    TRASH_CAN,
    TRASH_LID,
    WIDTH,
)
from src.utils import (
    draw_circle_outlined,
    draw_ellipse_outlined,
    draw_polygon_outlined,
    draw_rounded_rect,
)


class Obstacle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.scored = False

    def update(self, speed):
        self.x -= speed

    def is_offscreen(self):
        return self.x + self.w < -50

    def draw(self, surface):
        raise NotImplementedError


# ── TrashCan (垃圾桶) ──────────────────────────────────────────────
class TrashCan(Obstacle):
    def __init__(self, x=0):
        super().__init__(x, GROUND_Y - 36, 32, 36)

    def draw(self, surface):
        # body
        body_rect = pygame.Rect(self.x, self.y + 6, self.w, self.h - 6)
        draw_rounded_rect(surface, body_rect, TRASH_CAN, 4)
        # lid
        lid_rect = pygame.Rect(self.x - 2, self.y, self.w + 4, 12)
        draw_rounded_rect(surface, lid_rect, TRASH_LID, 3)
        # handle dots
        pygame.draw.circle(surface, OUTLINE, (self.x + self.w // 2, self.y + 5), 3)
        # recycle symbol (small dots)
        for dx, dy in [(-4, 20), (4, 20), (0, 28)]:
            pygame.draw.circle(surface, (180, 210, 200), (int(self.x + self.w / 2 + dx), int(self.y + dy)), 2)


# ── SignPost (校园指示牌) ──────────────────────────────────────────
class SignPost(Obstacle):
    def __init__(self, x=0):
        super().__init__(x, GROUND_Y - 68, 28, 68)

    def draw(self, surface):
        # pole
        pole_w = 6
        pole_x = self.x + (self.w - pole_w) / 2
        pole_rect = pygame.Rect(pole_x, self.y + 22, pole_w, self.h - 22)
        draw_rounded_rect(surface, pole_rect, SIGN_POLE, 2)
        # signboard
        board_rect = pygame.Rect(self.x, self.y, self.w, 24)
        draw_rounded_rect(surface, board_rect, SIGN_BOARD, 3)
        # text squiggles (white lines)
        for i in range(3):
            ly = self.y + 8 + i * 6
            pygame.draw.line(surface, (255, 255, 255), (self.x + 4, ly), (self.x + self.w - 4, ly + (i % 2) * 2), 2)


# ── TapeBarrier (警戒线/路障) ──────────────────────────────────────
class TapeBarrier(Obstacle):
    def __init__(self, x=0):
        super().__init__(x, GROUND_Y - 36, 76, 36)

    def draw(self, surface):
        # left cone (trapezoid)
        self._draw_cone(surface, self.x + 4, self.y + 6)
        # right cone
        self._draw_cone(surface, self.x + 44, self.y + 6)
        # caution tape between cones
        tape_y = self.y + 8
        pygame.draw.line(surface, OUTLINE, (self.x + 16, tape_y), (self.x + 56, tape_y), 5)
        pygame.draw.line(surface, TAPE_YELLOW, (self.x + 16, tape_y), (self.x + 56, tape_y), 3)

    def _draw_cone(self, surface, cx, top_y):
        cone_w = 16
        cone_h = 24
        points = [
            (cx - cone_w // 2, top_y + cone_h),
            (cx + cone_w // 2, top_y + cone_h),
            (cx + 3, top_y),
            (cx - 3, top_y),
        ]
        draw_polygon_outlined(surface, CONE_ORANGE, points)
        # white stripes
        for i, strip_y in enumerate([top_y + 15, top_y + 20]):
            sw = 10 - i * 2
            sx = cone_w - sw - 2
            points_s = [
                (cx - sx // 2, strip_y),
                (cx + sx // 2, strip_y),
                (cx + sx // 2 - 1, strip_y + 3),
                (cx - sx // 2 + 1, strip_y + 3),
            ]
            pygame.draw.polygon(surface, CONE_WHITE, points_s)


# ── CartHandle (食堂餐车把手) ──────────────────────────────────────
class CartHandle(Obstacle):
    def __init__(self, x=0):
        super().__init__(x, GROUND_Y - 56, 52, 22)

    def draw(self, surface):
        # cart body (visual only, below collision area, no outline — decorative)
        cart_body = pygame.Rect(self.x + 4, GROUND_Y - 22, self.w - 8, 22)
        draw_rounded_rect(surface, cart_body, CART_RED, 5)
        # wheels
        for wx in [self.x + 10, self.x + self.w - 14]:
            draw_circle_outlined(surface, (int(wx), GROUND_Y - 4), 6, (60, 60, 60), outline=1)
        # handlebar (collision area)
        bar_rect = pygame.Rect(self.x, self.y + 2, self.w, 12)
        draw_rounded_rect(surface, bar_rect, CART_SILVER, 4)
        # cart text
        text_surf = pygame.Surface((self.w - 8, 12), pygame.SRCALPHA)
        text_surf.fill((0, 0, 0, 0))
        pygame.draw.rect(text_surf, (255, 255, 255, 120), (2, 2, self.w - 12, 8))
        surface.blit(text_surf, (self.x + 4, GROUND_Y - 16))


# ── SpeedBump (减速带) ────────────────────────────────────────────
class SpeedBump(Obstacle):
    def __init__(self, x=0):
        super().__init__(x, GROUND_Y - 14, 64, 14)

    def draw(self, surface):
        bump_rect = pygame.Rect(self.x, self.y, self.w, self.h)
        draw_rounded_rect(surface, bump_rect, BUMP_YELLOW, 4)
        # diagonal black stripes
        for i in range(5):
            sx = self.x + i * 13 - 5
            points = [
                (sx, self.y + 2),
                (sx + 6, self.y + 2),
                (sx + 6, self.y + self.h - 2),
                (sx, self.y + self.h - 2),
            ]
            pygame.draw.polygon(surface, BUMP_BLACK, points)


# ── ElectricBike (电动车) ─────────────────────────────────────────
class ElectricBike(Obstacle):
    def __init__(self, x=0):
        super().__init__(x, GROUND_Y - 58, 44, 28)

    def draw(self, surface):
        x, y = self.x, self.y
        # wheels
        draw_circle_outlined(surface, (int(x + 8), int(GROUND_Y - 6)), 8, BIKE_TIRE, outline=1)
        draw_circle_outlined(surface, (int(x + self.w - 8), int(GROUND_Y - 6)), 8, BIKE_TIRE, outline=1)
        # wheel hubs
        pygame.draw.circle(surface, (180, 180, 180), (int(x + 8), int(GROUND_Y - 6)), 3)
        pygame.draw.circle(surface, (180, 180, 180), (int(x + self.w - 8), int(GROUND_Y - 6)), 3)
        # body
        body_rect = pygame.Rect(x + 4, y + 8, self.w - 8, 10)
        draw_rounded_rect(surface, body_rect, BIKE_GREEN, 4)
        # seat
        seat_rect = pygame.Rect(x + self.w - 20, y + 4, 12, 6)
        draw_rounded_rect(surface, seat_rect, (30, 30, 30), 2)
        # rider head (helmet)
        rider_cx = int(x + self.w - 14)
        rider_cy = int(y + 2)
        draw_circle_outlined(surface, (rider_cx, rider_cy), 6, BIKE_RIDER)
        # handlebars
        hb_x = int(x + 8)
        pygame.draw.line(surface, OUTLINE, (hb_x, y + 12), (hb_x, y + 2), 4)
        pygame.draw.line(surface, CART_SILVER, (hb_x, y + 12), (hb_x, y + 2), 2)


# ── Obstacle Type Registry & Factory ──────────────────────────────
OBSTACLE_TYPES = [TrashCan, SignPost, TapeBarrier, CartHandle, SpeedBump, ElectricBike]


def obstacle_factory(score):
    if score < 300:
        pool = [0, 0, 0, 1, 2]
    elif score < 800:
        pool = [0, 1, 2, 3, 4, 5]
    else:
        pool = [0, 1, 1, 2, 3, 4, 5, 5]
    idx = random.choice(pool)
    return OBSTACLE_TYPES[idx](WIDTH + 40)
