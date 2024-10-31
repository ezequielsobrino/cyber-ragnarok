import math
import pygame
import random

class ModelDisplay:
    def __init__(self, screen_width, screen_height, assets_manager):
        # Initialize with screen dimensions and assets
        self.width = screen_width
        self.height = screen_height
        self.assets_manager = assets_manager
        
        # Colors from BaseScreen
        self.RAVEN_BLACK = (10, 10, 20)
        self.NEON_BLUE = (0, 255, 255)
        self.PLASMA_BLUE = (150, 230, 255)
        self.NEON_RED = (255, 20, 100)
        self.NORDIC_GOLD = (255, 215, 0)
        self.FROST_BLUE = (200, 255, 255)
        self.BLOOD_NEON = (255, 0, 50)
        self.THUNDER_PURPLE = (200, 50, 255)
        
        # Effect settings
        self.time = 0
        self.time_speed = 0.05
        self.particle_speed = 1.0
        self.particle_life = 40
        self.energy_field_speed = 1
        self.lightning_probability = 0.3
        self.max_particles = 0
        self.lightning_offset = 10
        self.energy_field_amplitude = 8
        self.particles = []
        
        # Font settings
        self.min_font_size = int(self.height * 0.025)
        self.font_small = pygame.font.Font(None, self.min_font_size)
        self.font_model_name = pygame.font.Font(None, int(self.height * 0.04))  # Larger font for model names
        self.metrics_spacing = 5
        self.metrics_padding = 10
        
        self.LIGHTNING_COLORS = [self.NORDIC_GOLD, self.THUNDER_PURPLE, self.NEON_BLUE]

    def _draw_model_name(self, screen, name, rect, color):
        """Draw model name centered above the model image"""
        name_surface = self.font_model_name.render(name, True, color)
        name_rect = name_surface.get_rect(
            centerx=rect.centerx,
            bottom=rect.top - 10  # 10 pixels gap between name and image
        )
        
        # Optional: Add a subtle glow effect
        glow_surf = self.font_model_name.render(name, True, (color[0]//4, color[1]//4, color[2]//4))
        glow_rect = glow_surf.get_rect(center=name_rect.center)
        
        for offset in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
            screen.blit(glow_surf, (glow_rect.x + offset[0], glow_rect.y + offset[1]))
            
        screen.blit(name_surface, name_rect)
        
        return name_rect

    
    def _create_lightning(self, start_pos, end_pos, branches=3):
        """Create lightning effect between two points"""
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

    def _draw_lightning_effect(self, screen, rect, color):
        """Draw lightning effects around frame"""
        corners = [rect.topleft, rect.topright, rect.bottomleft, rect.bottomright]
        for i in range(len(corners)):
            start = corners[i]
            end = corners[(i + 1) % len(corners)]
            lightning_points = self._create_lightning(start, end)
            if random.random() < self.lightning_probability:
                pygame.draw.lines(screen, color, False, lightning_points, 2)

    def _draw_energy_field(self, screen, rect, color, time):
        """Draw pulsating energy field"""
        num_circles = 2
        for i in range(num_circles):
            offset = math.sin(time * self.energy_field_speed + i) * self.energy_field_amplitude
            expanded_rect = rect.inflate(offset * 2, offset * 2)
            pygame.draw.rect(screen, color, expanded_rect, 2)

    def _draw_epic_frame(self, screen, rect, color, is_winner=False):
        """Draw epic frame with effects"""
        pygame.draw.rect(screen, color, rect, 4)
        
        corner_size = 30
        thickness = 3
        for corner in [(rect.topleft, (1, 1)), (rect.topright, (-1, 1)),
                      (rect.bottomleft, (1, -1)), (rect.bottomright, (-1, -1))]:
            pos, direction = corner
            x, y = pos
            dx, dy = direction
            
            pygame.draw.line(screen, color,
                           (x, y),
                           (x + (corner_size * dx), y), thickness)
            pygame.draw.line(screen, color,
                           (x, y),
                           (x, y + (corner_size * dy)), thickness)
            
            pygame.draw.line(screen, color,
                           (x + (corner_size//2 * dx), y),
                           (x + (corner_size//2 * dx), y + (corner_size//2 * dy)), thickness-1)
            
            if is_winner:
                pygame.draw.circle(screen, self.NORDIC_GOLD,
                                (x + (corner_size//2 * dx), y + (corner_size//2 * dy)),
                                5)

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

    def _draw_metrics(self, screen, rect, metrics, color):
        """Draw metrics with cyberpunk style"""
        if not metrics:
            return
                
        formatted_metrics = self._format_metrics(metrics)
        if not formatted_metrics:
            return
                
        line_height = self.font_small.get_height()
        total_height = (line_height + self.metrics_spacing) * len(formatted_metrics)
        max_width = max(self.font_small.size(line)[0] for line in formatted_metrics)
        
        box_width = max(max_width + (self.metrics_padding * 3), rect.width * 0.8)
        
        metrics_rect = pygame.Rect(
            rect.centerx - (box_width / 2),
            rect.bottom + self.metrics_spacing * 2,
            box_width,
            total_height + (self.metrics_padding * 2)
        )
        
        pygame.draw.rect(screen, self.RAVEN_BLACK, metrics_rect)
        pygame.draw.rect(screen, color, metrics_rect, 2)
        
        corner_size = 8
        for corner in [(metrics_rect.topleft, (1, 1)), (metrics_rect.topright, (-1, 1)),
                    (metrics_rect.bottomleft, (1, -1)), (metrics_rect.bottomright, (-1, -1))]:
            pos, direction = corner
            pygame.draw.line(screen, color,
                            (pos[0], pos[1] + (corner_size * direction[1])),
                            pos, 2)
            pygame.draw.line(screen, color,
                            (pos[0] + (corner_size * direction[0]), pos[1]),
                            pos, 2)
        
        for i, line in enumerate(formatted_metrics):
            if ': ' in line:
                label, value = line.split(': ')
                
                label_surface = self.font_small.render(f"{label}: ", True, (180, 180, 180))
                label_rect = label_surface.get_rect(
                    left=metrics_rect.left + self.metrics_padding,
                    top=metrics_rect.top + self.metrics_padding + 
                        (i * (line_height + self.metrics_spacing))
                )
                
                value_surface = self.font_small.render(value, True, color)
                value_rect = value_surface.get_rect(
                    left=label_rect.right,
                    top=label_rect.top
                )
                
                screen.blit(label_surface, label_rect)
                screen.blit(value_surface, value_rect)
            else:
                text = self.font_small.render(line, True, color)
                text_rect = text.get_rect(
                    left=metrics_rect.left + self.metrics_padding,
                    top=metrics_rect.top + self.metrics_padding + 
                        (i * (line_height + self.metrics_spacing))
                )
                screen.blit(text, text_rect)

    def render(self, screen, model1_name, model2_name, winner=None, final_winner=False, 
               model1_metrics=None, model2_metrics=None):
        """Main render method for model display"""
        self.time += self.time_speed
        
        # Load model images
        model1_img = self.assets_manager.load_model_image(model1_name)
        model2_img = self.assets_manager.load_model_image(model2_name)
        
        if model1_img and model2_img:
            img_y = (self.height - model1_img.get_height()) // 2
            margin = 20
            border_thickness = 4

            # Model 1
            border_rect_1 = pygame.Rect(
                margin - border_thickness,
                img_y - border_thickness,
                model1_img.get_width() + (border_thickness * 2),
                model1_img.get_height() + (border_thickness * 2)
            )
            
            # Draw model 1 name
            self._draw_model_name(screen, model1_name, border_rect_1, self.NEON_BLUE)
            
            self._draw_epic_frame(screen, border_rect_1, self.NEON_BLUE, winner == 'X')

            if winner == 'X':
                winner_rect_1 = border_rect_1.inflate(20, 20)
                self._draw_energy_field(screen, winner_rect_1, self.NORDIC_GOLD, self.time)
                self._draw_lightning_effect(screen, winner_rect_1, random.choice(self.LIGHTNING_COLORS))
                
                if final_winner:
                    final_rect_1 = winner_rect_1.inflate(40, 40)
                    self._draw_lightning_effect(screen, final_rect_1, self.BLOOD_NEON)

            # Model 2
            border_rect_2 = pygame.Rect(
                self.width - model2_img.get_width() - margin - border_thickness,
                img_y - border_thickness,
                model2_img.get_width() + (border_thickness * 2),
                model2_img.get_height() + (border_thickness * 2)
            )
            
            # Draw model 2 name
            self._draw_model_name(screen, model2_name, border_rect_2, self.NEON_RED)
            
            self._draw_epic_frame(screen, border_rect_2, self.NEON_RED, winner == 'O')

            if winner == 'O':
                winner_rect_2 = border_rect_2.inflate(20, 20)
                self._draw_energy_field(screen, winner_rect_2, self.NORDIC_GOLD, self.time)
                self._draw_lightning_effect(screen, winner_rect_2, random.choice(self.LIGHTNING_COLORS))
                
                if final_winner:
                    final_rect_2 = winner_rect_2.inflate(40, 40)
                    self._draw_lightning_effect(screen, final_rect_2, self.BLOOD_NEON)

            # Draw model images
            screen.blit(model1_img, (margin, img_y))
            screen.blit(model2_img, (self.width - model2_img.get_width() - margin, img_y))
            
            # Draw metrics if available
            if model1_metrics:
                self._draw_metrics(screen, border_rect_1, model1_metrics, self.NEON_BLUE)
            if model2_metrics:
                self._draw_metrics(screen, border_rect_2, model2_metrics, self.NEON_RED)

            return border_rect_1, border_rect_2
