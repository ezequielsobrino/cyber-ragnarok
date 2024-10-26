

import pygame
from abc import ABC, abstractmethod
import math
import random

class BaseScreen(ABC):
    def __init__(self, width: int, height: int, fps: int, assets_manager):
        self.width = width
        self.height = height
        self.fps = fps
        self.assets_manager = assets_manager
        self.screen = pygame.Surface((width, height))
        self.time = 0
        self.particles = []  # Para efectos de partículas
        
        # Cyberpunk Viking color palette - Colores más intensos
        self.RAVEN_BLACK = (10, 10, 20)         # Negro más profundo
        self.NEON_BLUE = (0, 255, 255)          # Azul eléctrico
        self.PLASMA_BLUE = (150, 230, 255)      # Azul plasma
        self.NEON_RED = (255, 20, 100)          # Rojo neón
        self.NORDIC_GOLD = (255, 215, 0)        # Oro vikingo
        self.FROST_BLUE = (200, 255, 255)       # Hielo brillante
        self.BLOOD_NEON = (255, 0, 50)          # Sangre neón
        self.RUNE_GREEN = (50, 255, 150)        # Verde rúnico
        self.THUNDER_PURPLE = (200, 50, 255)    # Púrpura eléctrico
        self.ENERGY_ORANGE = (255, 150, 0)      # Naranja energético
        
        # Efectos especiales
        self.LIGHTNING_COLORS = [self.NORDIC_GOLD, self.THUNDER_PURPLE, self.NEON_BLUE]
        
        # Fonts
        self.original_font_size = int(height * 0.06)
        self.min_font_size = int(height * 0.03)
        self.font_large = int(height * 0.1)
        self.font = pygame.font.Font(None, self.original_font_size)
        self.font_big = pygame.font.Font(None, self.font_large)
        self.TEXT_COLOR = (255, 255, 255)

    def _create_lightning(self, start_pos, end_pos, branches=3):
        """Crea un efecto de rayo entre dos puntos"""
        points = [start_pos]
        current = pygame.Vector2(start_pos)
        target = pygame.Vector2(end_pos)
        distance = current.distance_to(target)
        
        segments = int(distance / 20)
        for _ in range(segments):
            direction = (target - current).normalize()
            current += direction * (distance / segments)
            offset = pygame.Vector2(random.randint(-10, 10), random.randint(-10, 10))
            points.append((current + offset))
        
        points.append(end_pos)
        return points

    def _draw_lightning_effect(self, rect, color):
        """Dibuja efectos de rayos alrededor del marco"""
        corners = [rect.topleft, rect.topright, rect.bottomleft, rect.bottomright]
        for i in range(len(corners)):
            start = corners[i]
            end = corners[(i + 1) % len(corners)]
            lightning_points = self._create_lightning(start, end)
            if random.random() < 0.3:  # 30% de probabilidad de dibujar cada rayo
                pygame.draw.lines(self.screen, color, False, lightning_points, 2)

    def _draw_energy_field(self, rect, color, time):
        """Dibuja un campo de energía pulsante"""
        num_circles = 2  # Reducido a 2 círculos para un efecto más limpio
        max_offset = 8
        for i in range(num_circles):
            offset = math.sin(time * 2 + i) * max_offset
            expanded_rect = rect.inflate(offset * 2, offset * 2)
            pygame.draw.rect(self.screen, color, expanded_rect, 2)

    def _draw_epic_frame(self, rect, color, is_winner=False):
        """Dibuja un marco épico con efectos"""
        # Marco base con bordes gruesos
        pygame.draw.rect(self.screen, color, rect, 4)
        
        # Esquinas decorativas
        corner_size = 30
        thickness = 3
        for corner in [(rect.topleft, (1, 1)), (rect.topright, (-1, 1)),
                      (rect.bottomleft, (1, -1)), (rect.bottomright, (-1, -1))]:
            pos, direction = corner
            x, y = pos
            dx, dy = direction
            
            # Líneas principales
            pygame.draw.line(self.screen, color,
                           (x, y),
                           (x + (corner_size * dx), y), thickness)
            pygame.draw.line(self.screen, color,
                           (x, y),
                           (x, y + (corner_size * dy)), thickness)
            
            # Detalles adicionales
            pygame.draw.line(self.screen, color,
                           (x + (corner_size//2 * dx), y),
                           (x + (corner_size//2 * dx), y + (corner_size//2 * dy)), thickness-1)
            
            if is_winner:
                # Añadir detalles extra para el ganador
                pygame.draw.circle(self.screen, self.NORDIC_GOLD,
                                (x + (corner_size//2 * dx), y + (corner_size//2 * dy)),
                                5)

    def _update_particles(self):
        """Actualiza el sistema de partículas"""
        new_particles = []
        for particle in self.particles:
            particle['life'] -= 1
            if particle['life'] > 0:
                particle['pos'][0] += particle['vel'][0]
                particle['pos'][1] += particle['vel'][1]
                new_particles.append(particle)
        self.particles = new_particles

    def _add_victory_particles(self, rect):
        """Añade partículas de victoria"""
        for _ in range(3):  # Reducido a 3 partículas por frame para un efecto más limpio
            particle = {
                'pos': [rect.centerx + random.randint(-50, 50),
                       rect.centery + random.randint(-50, 50)],
                'vel': [random.uniform(-2, 2), random.uniform(-2, 2)],
                'life': random.randint(20, 40),
                'color': random.choice([self.NORDIC_GOLD, self.NEON_BLUE, self.THUNDER_PURPLE])
            }
            self.particles.append(particle)

    def _draw_particles(self):
        """Dibuja las partículas"""
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / 40))
            color = list(particle['color'])
            if len(color) == 3:
                color.append(alpha)
            pygame.draw.circle(self.screen, color,
                             [int(particle['pos'][0]), int(particle['pos'][1])],
                             2)

    def _draw_model_images(self, model1_img, model2_img, winner=None, final_winner=False):
        if model1_img and model2_img:
            self.time += 0.1
            img_y = (self.height - model1_img.get_height()) // 2
            margin = 20
            border_thickness = 4

            # Actualizar sistema de partículas
            self._update_particles()

            # Modelo 1
            border_rect_1 = pygame.Rect(
                margin - border_thickness,
                img_y - border_thickness,
                model1_img.get_width() + (border_thickness * 2),
                model1_img.get_height() + (border_thickness * 2)
            )
            
            # Efectos base para modelo 1
            self._draw_epic_frame(border_rect_1, self.NEON_BLUE, winner == 'X')

            if winner == 'X':
                winner_rect_1 = border_rect_1.inflate(20, 20)
                self._draw_energy_field(winner_rect_1, self.NORDIC_GOLD, self.time)
                self._draw_lightning_effect(winner_rect_1, random.choice(self.LIGHTNING_COLORS))
                
                if final_winner:
                    final_rect_1 = winner_rect_1.inflate(40, 40)
                    self._draw_lightning_effect(final_rect_1, self.BLOOD_NEON)
                    self._add_victory_particles(final_rect_1)

            # Modelo 2
            border_rect_2 = pygame.Rect(
                self.width - model2_img.get_width() - margin - border_thickness,
                img_y - border_thickness,
                model2_img.get_width() + (border_thickness * 2),
                model2_img.get_height() + (border_thickness * 2)
            )
            
            # Efectos base para modelo 2
            self._draw_epic_frame(border_rect_2, self.NEON_RED, winner == 'O')

            if winner == 'O':
                winner_rect_2 = border_rect_2.inflate(20, 20)
                self._draw_energy_field(winner_rect_2, self.NORDIC_GOLD, self.time)
                self._draw_lightning_effect(winner_rect_2, random.choice(self.LIGHTNING_COLORS))
                
                if final_winner:
                    final_rect_2 = winner_rect_2.inflate(40, 40)
                    self._draw_lightning_effect(final_rect_2, self.BLOOD_NEON)
                    self._add_victory_particles(final_rect_2)

            # Dibujar partículas
            self._draw_particles()

            # Dibujar imágenes de modelos sobre los efectos
            self.screen.blit(model1_img, (margin, img_y))
            self.screen.blit(model2_img, (self.width - model2_img.get_width() - margin, img_y))

    @abstractmethod
    def render(self, **kwargs):
        pass