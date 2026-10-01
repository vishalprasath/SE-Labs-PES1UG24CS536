import pygame
from .player import Player
from .platform import Platform
from .hazard import Hazard
from .sounds import Sounds

# Game Engine

WHITE = (255, 255, 255)
BROWN = (150, 100, 60)
RED = (220, 60, 60)
GREEN = (0, 200, 0)

# Gravity / jump strength for each difficulty. Medium is the original
# physics; every setting was checked to still allow reaching the goal.
DIFFICULTIES = {
    "Easy":   {"gravity": 0.45, "jump_strength": -11},
    "Medium": {"gravity": 0.6,  "jump_strength": -12},
    "Hard":   {"gravity": 0.9,  "jump_strength": -15},
}
DIFFICULTY_KEYS = {pygame.K_1: "Easy", pygame.K_2: "Medium", pygame.K_3: "Hard"}

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.start_x, self.start_y = 40, height - 120

        # A simple hand-built level: platforms with gaps between them
        # (falling into a gap means falling off the bottom of the
        # screen), one hazard, and a goal near the right edge.
        ground_y = height - 40
        self.platforms = [
            Platform(0, ground_y, 160),
            Platform(220, ground_y, 140),
            Platform(420, ground_y - 60, 120),
            Platform(600, ground_y, 180),
        ]
        self.hazards = [Hazard(240, ground_y - 14, 100)]
        self.goal_x = 740

        self.font = pygame.font.SysFont("Arial", 30)
        self.big_font = pygame.font.SysFont("Arial", 64, bold=True)
        self.quit_requested = False
        self.sounds = Sounds()
        self.reset("Medium")

    def reset(self, difficulty):
        # Start a fresh game with the chosen difficulty's physics
        settings = DIFFICULTIES[difficulty]
        self.difficulty = difficulty
        self.gravity = settings["gravity"]
        self.player = Player(self.start_x, self.start_y)
        self.player.jump_strength = settings["jump_strength"]
        self.score = 0
        self.game_over = False

    def handle_event(self, event):
        if self.game_over:
            # On the Game Over screen: 1/2/3 replays at that difficulty, Esc exits.
            if event.type == pygame.KEYDOWN:
                if event.key in DIFFICULTY_KEYS:
                    self.reset(DIFFICULTY_KEYS[event.key])
                elif event.key == pygame.K_ESCAPE:
                    self.quit_requested = True
            return
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
            if self.player.on_ground:  # only beep when the jump actually happens
                self.sounds.play("jump")
            self.player.jump()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.player.vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.vx = -self.player.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.vx = self.player.speed

    def update(self):
        if self.game_over:
            return

        self.player.vy += self.gravity
        self.player.x = max(0, self.player.x + self.player.vx)

        # Swept landing check: rather than only testing for overlap
        # after the move (which a fast fall can skip over entirely),
        # land on a platform if the player's feet were at or above its
        # top last frame and are at or below it now. This catches the
        # crossing at any fall speed. If several platforms were crossed
        # in one frame, land on the highest one (the first one hit).
        prev_bottom = self.player.y + self.player.height
        self.player.y += self.player.vy
        new_bottom = self.player.y + self.player.height
        self.player.on_ground = False
        if self.player.vy >= 0:
            landing = None
            for platform in self.platforms:
                overlaps_x = (self.player.x < platform.x + platform.width and
                              self.player.x + self.player.width > platform.x)
                if overlaps_x and prev_bottom <= platform.y <= new_bottom:
                    if landing is None or platform.y < landing.y:
                        landing = platform
            if landing is not None:
                self.player.y = landing.y - self.player.height
                self.player.vy = 0
                self.player.on_ground = True

        for hazard in self.hazards:
            if self.player.rect().colliderect(hazard.rect()):
                self.game_over = True
                self.sounds.play("death")
                return

        if self.player.y > self.height:
            self.game_over = True
            self.sounds.play("death")
            return

        if self.player.x >= self.goal_x:
            self.score += 1
            self.sounds.play("goal")
            self.player.x, self.player.y = self.start_x, self.start_y
            self.player.vy = 0

    def render(self, screen):
        for platform in self.platforms:
            pygame.draw.rect(screen, BROWN, platform.rect())
        for hazard in self.hazards:
            pygame.draw.rect(screen, RED, hazard.rect())

        goal_rect = pygame.Rect(self.goal_x, 0, 6, self.height)
        pygame.draw.rect(screen, GREEN, goal_rect)

        pygame.draw.rect(screen, WHITE, self.player.rect())

        score_text = self.font.render(f"Score: {self.score}   {self.difficulty}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if self.game_over:
            self.render_game_over(screen)

    def render_game_over(self, screen):
        # Dim the frozen game scene behind the message
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        cx, cy = self.width // 2, self.height // 2
        lines = [
            (self.big_font, "GAME OVER", RED, cy - 90),
            (self.font, f"Final score: {self.score}  ({self.difficulty})", WHITE, cy - 20),
            (self.font, "Play again:  1 Easy   2 Medium   3 Hard", WHITE, cy + 35),
            (self.font, "Esc to quit", WHITE, cy + 80),
        ]
        for font, text, color, y in lines:
            surface = font.render(text, True, color)
            screen.blit(surface, surface.get_rect(center=(cx, y)))