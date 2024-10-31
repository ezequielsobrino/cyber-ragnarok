import pygame
from abc import ABC, abstractmethod
import math
import random
from screens.model_display import ModelDisplay

class BaseScreen(ABC):
    def __init__(self, width: int, height: int, fps: int, assets_manager):
        # Basic screen setup
        self.width = width
        self.height = height
        self.fps = fps
        self.assets_manager = assets_manager
        self.screen = pygame.Surface((width, height))
        self.model_display = ModelDisplay(width, height, assets_manager)
        
        # Animation control settings
        self.time = 0
        self.time_speed = 0.05        # General animation speed
        self.particle_speed = 1.0     # Particle movement speed
        self.particle_life = 40       # Particle duration
        self.energy_field_speed = 1   # Pulsation speed
        self.lightning_probability = 0.3
        self.max_particles = 0        # Particles per frame
        self.lightning_offset = 10    # Lightning deviation
        self.energy_field_amplitude = 8  # Pulsation amplitude
        
        # Particle system
        self.particles = []
        
        # Cyberpunk Viking color palette
        self.RAVEN_BLACK = (10, 10, 20)         # Deep black
        self.NEON_BLUE = (0, 255, 255)          # Electric blue
        self.PLASMA_BLUE = (150, 230, 255)      # Plasma blue
        self.NEON_RED = (255, 20, 100)          # Neon red
        self.NORDIC_GOLD = (255, 215, 0)        # Viking gold
        self.FROST_BLUE = (200, 255, 255)       # Ice blue
        self.BLOOD_NEON = (255, 0, 50)          # Blood neon
        self.RUNE_GREEN = (50, 255, 150)        # Runic green
        self.THUNDER_PURPLE = (200, 50, 255)    # Electric purple
        self.ENERGY_ORANGE = (255, 150, 0)      # Energy orange
        
        # Special effects colors
        self.LIGHTNING_COLORS = [self.NORDIC_GOLD, self.THUNDER_PURPLE, self.NEON_BLUE]
        
        # Font configuration
        self.original_font_size = int(height * 0.06)
        self.min_font_size = int(height * 0.025)
        self.font_large = int(height * 0.1)
        self.font = pygame.font.Font(None, self.original_font_size)
        self.font_small = pygame.font.Font(None, self.min_font_size)
        self.font_big = pygame.font.Font(None, self.font_large)
        self.TEXT_COLOR = (255, 255, 255)

    def _create_lightning(self, start_pos, end_pos, branches=3):
        """Creates a lightning effect between two points"""
        points = [start_pos]
        current = pygame.Vector2(start_pos)
        target = pygame.Vector2(end_pos)
        distance = current.distance_to(target)
        
        segments = int(distance / 20)
        for _ in range(segments):
            direction = (target - current).normalize()
            current += direction * (distance / segments)
            offset = pygame.Vector2(
                random.randint(-self.lightning_offset, self.lightning_offset),
                random.randint(-self.lightning_offset, self.lightning_offset)
            )
            points.append((current + offset))
        
        points.append(end_pos)
        return points

    def _draw_lightning_effect(self, rect, color):
        """Draws lightning effects around the frame"""
        corners = [rect.topleft, rect.topright, rect.bottomleft, rect.bottomright]
        for i in range(len(corners)):
            start = corners[i]
            end = corners[(i + 1) % len(corners)]
            lightning_points = self._create_lightning(start, end)
            if random.random() < self.lightning_probability:
                pygame.draw.lines(self.screen, color, False, lightning_points, 2)

    def _draw_energy_field(self, rect, color, time):
        """Draws a pulsating energy field effect"""
        num_circles = 2  # Reduced to 2 circles for cleaner effect
        for i in range(num_circles):
            offset = math.sin(time * self.energy_field_speed + i) * self.energy_field_amplitude
            expanded_rect = rect.inflate(offset * 2, offset * 2)
            pygame.draw.rect(self.screen, color, expanded_rect, 2)

    def _draw_epic_frame(self, rect, color, is_winner=False):
        """Draws an epic frame with decorative effects"""
        # Base frame with thick borders
        pygame.draw.rect(self.screen, color, rect, 4)
        
        # Decorative corners
        corner_size = 30
        thickness = 3
        for corner in [(rect.topleft, (1, 1)), (rect.topright, (-1, 1)),
                      (rect.bottomleft, (1, -1)), (rect.bottomright, (-1, -1))]:
            pos, direction = corner
            x, y = pos
            dx, dy = direction
            
            pygame.draw.line(self.screen, color,
                           (x, y),
                           (x + (corner_size * dx), y), thickness)
            pygame.draw.line(self.screen, color,
                           (x, y),
                           (x, y + (corner_size * dy)), thickness)
            
            pygame.draw.line(self.screen, color,
                           (x + (corner_size//2 * dx), y),
                           (x + (corner_size//2 * dx), y + (corner_size//2 * dy)), thickness-1)
            
            if is_winner:
                pygame.draw.circle(self.screen, self.NORDIC_GOLD,
                                (x + (corner_size//2 * dx), y + (corner_size//2 * dy)),
                                5)

    def _update_particles(self):
        """Updates the particle system"""
        new_particles = []
        for particle in self.particles:
            particle['life'] -= 1
            if particle['life'] > 0:
                particle['pos'][0] += particle['vel'][0]
                particle['pos'][1] += particle['vel'][1]
                new_particles.append(particle)
        self.particles = new_particles

    def _add_victory_particles(self, rect):
        """Adds victory celebration particles"""
        for _ in range(self.max_particles):
            particle = {
                'pos': [rect.centerx + random.randint(-50, 50),
                       rect.centery + random.randint(-50, 50)],
                'vel': [random.uniform(-self.particle_speed, self.particle_speed),
                       random.uniform(-self.particle_speed, self.particle_speed)],
                'life': random.randint(self.particle_life//2, self.particle_life),
                'color': random.choice([self.NORDIC_GOLD, self.NEON_BLUE, self.THUNDER_PURPLE])
            }
            self.particles.append(particle)

    def _draw_particles(self):
        """Renders active particles"""
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / self.particle_life))
            color = list(particle['color'])
            if len(color) == 3:
                color.append(alpha)
            pygame.draw.circle(self.screen, color,
                             [int(particle['pos'][0]), int(particle['pos'][1])],
                             2)

    @abstractmethod
    def render(self, **kwargs):
        """Abstract method to be implemented by derived screen classes"""
        pass