import math
import random

import pygame

from src.background import Background
from src.constants import (
    BASE_SPAWN_GAP,
    BASE_SPEED,
    DEAD,
    FPS,
    HEIGHT,
    MIN_SPAWN_GAP,
    PLAYING,
    SCORE_RATE,
    SPAWN_GAP_DECAY,
    SPEED_CAP,
    SPEED_RAMP,
    START,
    WIDTH,
)
from src.obstacles import obstacle_factory
from src.player import Player
from src.ui import UI
from src.utils import check_collision, draw_particles, spawn_burst, update_particles


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.state = START
        self.score = 0
        self.speed = BASE_SPEED
        self.frame = 0
        self.ground_offset = 0
        self.spawn_timer = 0

        self.background = Background()
        self.player = Player()
        self.ui = UI()
        self.obstacles = []
        self.particles = []

        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    if self.state == PLAYING:
                        self.player.jump(self.particles)
                    else:
                        self.start_game()
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if self.state == PLAYING:
                        self.player.slide()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state != PLAYING:
                    self.start_game()
                else:
                    if event.pos[1] < HEIGHT * 0.55:
                        self.player.jump(self.particles)
                    else:
                        self.player.slide()

        return self.running

    def start_game(self):
        self.state = PLAYING
        self.score = 0
        self.speed = BASE_SPEED
        self.frame = 0
        self.ground_offset = 0
        self.spawn_timer = 0
        self.obstacles = []
        self.particles = []
        self.player = Player()

    def kill_player(self):
        self.state = DEAD
        self.particles.extend(
            spawn_burst(
                self.player.cx, self.player.cy, 28,
                [(255, 60, 60), (255, 140, 30), (255, 255, 255), (255, 200, 50), (255, 182, 182)],
            )
        )
        new_record = self.ui.check_high_score(self.score)

    def update(self):
        if self.state != PLAYING:
            return

        self.frame += 1
        self.score += self.speed * SCORE_RATE

        # speed ramp
        self.speed = min(BASE_SPEED + math.floor(self.score / SPEED_RAMP) * 0.5, SPEED_CAP)

        self.ground_offset += self.speed

        # spawn obstacles
        self.spawn_timer += 1
        spawn_gap = max(MIN_SPAWN_GAP, BASE_SPAWN_GAP - math.floor(self.score / SPAWN_GAP_DECAY) * 5)
        if self.spawn_timer >= spawn_gap + random.random() * 28:
            self.obstacles.append(obstacle_factory(self.score))
            self.spawn_timer = 0

        # update obstacles
        for o in self.obstacles:
            o.update(self.speed)
        self.obstacles = [o for o in self.obstacles if not o.is_offscreen()]

        # update player
        self.player.update(self.speed, BASE_SPEED)

        # collision
        for o in self.obstacles:
            if check_collision(self.player, o):
                self.kill_player()
                return

        # particles
        self.particles = update_particles(self.particles)

    def draw(self):
        self.screen.fill((135, 206, 235))

        self.background.draw(self.screen, self.ground_offset)

        # obstacles
        for o in self.obstacles:
            o.draw(self.screen)

        # player
        if self.state != DEAD:
            self.player.draw(self.screen)

        # particles
        draw_particles(self.screen, self.particles)

        # UI overlays
        if self.state == PLAYING:
            self.ui.draw_hud(self.screen, self.score, self.speed, self.player)
        elif self.state == START:
            self.ui.draw_start_screen(self.screen, self.frame)
        elif self.state == DEAD:
            new_record = self.ui.high_score == int(self.score) and int(self.score) > 0
            self.ui.draw_game_over_screen(self.screen, self.frame, self.score, new_record)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.running = self.handle_events()
            if not self.running:
                break
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def cleanup(self):
        self.ui.save_high_score()
