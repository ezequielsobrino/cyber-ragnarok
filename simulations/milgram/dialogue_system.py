# dialogue_system.py
import pygame
from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class DialogueMessage:
    speaker_name: str
    content: str
    color: tuple
    completed: bool = False
    current_index: int = 0

class DialogueBox:
    def __init__(self, width: int, height: int, font: pygame.font.Font, position: Tuple[int, int] = None):
        # Configuración básica
        self.width = width
        self.height = 200
        self.x = position[0] if position else 0
        self.y = position[1] if position else height - self.height
        self.font = font
        
        # Parámetros de visualización
        self.text_speed = 2
        self.padding = 20
        self.text_color = (255, 255, 255)
        self.portrait_size = 150
        self.bg_alpha = 200
        
        # Estado del diálogo
        self.current_messages: List[DialogueMessage] = []
        self.last_update_time = 0
        self.waiting_for_input = False 
        
    def update(self, current_time: int):
        if not self.current_messages:
            return
            
        current_message = self.current_messages[0]
        if not current_message.completed:
            if current_time - self.last_update_time > 20:
                current_message.current_index += self.text_speed
                if current_message.current_index >= len(current_message.content):
                    current_message.current_index = len(current_message.content)
                    current_message.completed = True
                    self.waiting_for_input = True
                self.last_update_time = current_time
    
    def advance_dialogue(self):
        if not self.current_messages:
            return
            
        if self.current_messages[0].completed:
            self.current_messages.pop(0)
            if self.current_messages:
                self.current_messages[0].current_index = 0
                self.current_messages[0].completed = False
                self.waiting_for_input = False 
    
    def set_messages(self, messages: List[DialogueMessage]):
        self.current_messages = messages
        if self.current_messages:
            self.current_messages[0].current_index = 0
            self.current_messages[0].completed = False
            self.waiting_for_input = False
    
    def draw(self, screen, characters: dict):
        if not self.current_messages:
            return
            
        current_message = self.current_messages[0]
        
        # Fondo semi-transparente
        self._draw_background(screen, current_message.color)
        
        # Dibujar el retrato y nombre del personaje
        if current_character := characters.get(current_message.speaker_name):
            portrait_pos = self._draw_character_portrait(screen, current_character, current_message)
            
            # Dibujar el texto del mensaje
            self._draw_message_text(screen, current_message, portrait_pos)
        
        # Indicador de continuar
        if current_message.completed:
            self._draw_continue_indicator(screen, current_message.color)
    
    def _draw_background(self, screen, border_color):
        dialog_surface = pygame.Surface((self.width, self.height))
        dialog_surface.fill((0, 0, 0))
        dialog_surface.set_alpha(self.bg_alpha)
        screen.blit(dialog_surface, (self.x, self.y))
        pygame.draw.rect(screen, border_color, (self.x, self.y, self.width, self.height), 2)
    
    def _draw_character_portrait(self, screen, character, message) -> Tuple[int, int]:
        portrait = pygame.transform.scale(character.image, (self.portrait_size, self.portrait_size))
        portrait_x = self.x + self.padding
        portrait_y = self.y + (self.height - self.portrait_size) // 2
        
        # Dibujar retrato
        screen.blit(portrait, (portrait_x, portrait_y))
        
        # Dibujar nombre del personaje
        name_surface = self.font.render(message.speaker_name, True, message.color)
        name_bg = pygame.Surface((name_surface.get_width() + 20, name_surface.get_height() + 10))
        name_bg.fill((0, 0, 0))
        name_bg.set_alpha(150)
        
        name_y = portrait_y - name_surface.get_height() - 5
        screen.blit(name_bg, (portrait_x, name_y))
        screen.blit(name_surface, (portrait_x + 10, name_y + 3))
        
        return (portrait_x, portrait_y)
    
    def _draw_message_text(self, screen, message: DialogueMessage, portrait_pos: Tuple[int, int]):
        text_start_x = portrait_pos[0] + self.portrait_size + self.padding
        text_start_y = self.y + self.padding
        max_width = self.width - self.portrait_size - (self.padding * 3)
        
        displayed_text = message.content[:message.current_index]
        self._draw_wrapped_text(
            screen,
            displayed_text,
            (text_start_x, text_start_y),
            max_width
        )
    
    def _draw_continue_indicator(self, screen, color):
        continue_text = self.font.render("Press SPACE to continue", True, color)
        screen.blit(
            continue_text,
            (self.width - continue_text.get_width() - self.padding,
             self.y + self.height - continue_text.get_height() - self.padding)
        )
    
    def _draw_wrapped_text(self, screen, text: str, pos: Tuple[int, int], max_width: int):
        words = text.split(' ')
        lines = []
        current_line = []
        x, y = pos
        
        for word in words:
            current_line.append(word)
            text_width = self.font.size(' '.join(current_line))[0]
            if text_width > max_width:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        
        lines.append(' '.join(current_line))
        
        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, self.text_color)
            screen.blit(text_surface, (x, y + i * self.font.get_linesize()))