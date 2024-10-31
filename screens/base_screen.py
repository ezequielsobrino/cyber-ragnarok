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
        
        # Control de velocidad de animaciones
        self.time = 0
        self.time_speed = 0.05         # Velocidad general de animaciones
        self.particle_speed = 1.0      # Velocidad de las partículas
        self.particle_life = 40        # Duración de las partículas
        self.energy_field_speed = 1    # Velocidad de pulsación
        self.lightning_probability = 0.3  # Probabilidad de rayos
        self.max_particles = 0         # Partículas por frame
        self.lightning_offset = 10     # Desviación de los rayos
        self.energy_field_amplitude = 8  # Amplitud de pulsación
        
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
        self.min_font_size = int(height * 0.025)  # Smaller size for metrics
        self.font_large = int(height * 0.1)
        self.font = pygame.font.Font(None, self.original_font_size)
        self.font_small = pygame.font.Font(None, self.min_font_size)  # New font for metrics
        self.font_big = pygame.font.Font(None, self.font_large)
        self.TEXT_COLOR = (255, 255, 255)
        
        # Metrics display settings
        self.metrics_spacing = 5
        self.metrics_padding = 10

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
            offset = pygame.Vector2(
                random.randint(-self.lightning_offset, self.lightning_offset),
                random.randint(-self.lightning_offset, self.lightning_offset)
            )
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
            if random.random() < self.lightning_probability:
                pygame.draw.lines(self.screen, color, False, lightning_points, 2)

    def _draw_energy_field(self, rect, color, time):
        """Dibuja un campo de energía pulsante"""
        num_circles = 2  # Reducido a 2 círculos para un efecto más limpio
        for i in range(num_circles):
            offset = math.sin(time * self.energy_field_speed + i) * self.energy_field_amplitude
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
        """Dibuja las partículas"""
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / self.particle_life))
            color = list(particle['color'])
            if len(color) == 3:
                color.append(alpha)
            pygame.draw.circle(self.screen, color,
                             [int(particle['pos'][0]), int(particle['pos'][1])],
                             2)

    def _format_metrics(self, metrics):
        """Format metrics for display"""
        if metrics.total_moves == 0:
            return []
            
        avg_time = metrics.total_time / metrics.total_moves
        avg_tokens = metrics.total_tokens / metrics.total_moves
        avg_cost = metrics.total_cost / metrics.total_moves
        accuracy = (metrics.valid_moves/metrics.total_moves*100)
        
        return [
            f"Moves: {metrics.valid_moves}/{metrics.total_moves}",
            f"Accuracy: {accuracy:.1f}%",
            f"Avg Time: {avg_time:.2f}s",
            f"Avg Tokens: {avg_tokens:.1f}",
            f"Cost: ${metrics.total_cost:.2e}",
            f"$/Move: ${avg_cost:.2e}"  
        ]

    def _draw_metrics(self, rect, metrics, color):
        """Draw metrics below the given rectangle"""
        if not metrics:
            return
            
        formatted_metrics = self._format_metrics(metrics)
        if not formatted_metrics:
            return
            
        # Calculate metrics box dimensions
        line_height = self.font_small.get_height()
        total_height = (line_height + self.metrics_spacing) * len(formatted_metrics)
        max_width = max(self.font_small.size(line)[0] for line in formatted_metrics)
        
        # Create metrics box below the character
        metrics_rect = pygame.Rect(
            rect.x,
            rect.bottom + self.metrics_spacing,
            max_width + (self.metrics_padding * 2),
            total_height + (self.metrics_padding * 2)
        )
        
        # Draw background and frame
        pygame.draw.rect(self.screen, self.RAVEN_BLACK, metrics_rect)
        self._draw_epic_frame(metrics_rect, color)
        
        # Draw metrics text
        for i, line in enumerate(formatted_metrics):
            text = self.font_small.render(line, True, color)
            text_rect = text.get_rect(
                left=metrics_rect.left + self.metrics_padding,
                top=metrics_rect.top + self.metrics_padding + (i * (line_height + self.metrics_spacing))
            )
            self.screen.blit(text, text_rect)

    def _draw_model_images(self, model1_img, model2_img, winner=None, final_winner=False, model1_metrics=None, model2_metrics=None):
        if model1_img and model2_img:
            self.time += self.time_speed
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
            
            # Draw metrics if available
            if model1_metrics:
                self._draw_metrics(border_rect_1, model1_metrics, self.NEON_BLUE)
            if model2_metrics:
                self._draw_metrics(border_rect_2, model2_metrics, self.NEON_RED)

    @abstractmethod
    def render(self, **kwargs):
        pass