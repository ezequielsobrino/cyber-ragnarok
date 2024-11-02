from typing import Tuple
import pygame


class TextManager:
    def __init__(self):
        self.current_text = ""
        self.target_text = ""
        self.text_animation_speed = 50
        self.last_char_time = 0
        self.is_animating = False
        self.font = pygame.font.SysFont('Arial', 20)

    def start_text_animation(self, text: str):
        self.target_text = text
        self.current_text = ""
        self.last_char_time = pygame.time.get_ticks()
        self.is_animating = True

    def update_text_animation(self) -> bool:
        if not self.is_animating:
            return False

        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.last_char_time
        chars_to_add = int(elapsed * self.text_animation_speed / 1000)

        if chars_to_add > 0:
            remaining_text = self.target_text[len(self.current_text):]
            new_chars = remaining_text[:chars_to_add]
            self.current_text += new_chars
            self.last_char_time = current_time

        if self.current_text == self.target_text:
            self.is_animating = False

        return self.is_animating

    def draw_text(self, screen: pygame.Surface, text: str, position: Tuple[int, int], 
                 color=(200, 200, 200), max_width=700, animated=False) -> int:
        if animated and self.target_text != text:
            self.start_text_animation(text)
            text_to_render = self.current_text
        elif animated:
            text_to_render = self.current_text
        else:
            text_to_render = text

        words = text_to_render.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            test_surface = self.font.render(test_line, True, color)
            if test_surface.get_width() > max_width:
                current_line.pop()
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        total_height = len(lines) * 25
        for i, line in enumerate(lines):
            surface = self.font.render(line, True, color)
            screen.blit(surface, (position[0], position[1] + i * 25))
        
        return total_height