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
    def __init__(self, width: int, height: int, font: pygame.font.Font):
        self.width = width
        self.height = 150
        self.x = 0
        self.y = height - self.height
        self.font = font
        self.text_speed = 2  # characters per frame
        self.padding = 20
        self.current_messages: List[DialogueMessage] = []
        self.last_update_time = 0
        self.text_color = (255, 255, 255)
        
    def update(self, current_time: int):
        if not self.current_messages:
            return
            
        current_message = self.current_messages[0]
        if not current_message.completed:
            # Advance text
            if current_time - self.last_update_time > 20:  # Control text speed
                current_message.current_index += self.text_speed
                if current_message.current_index >= len(current_message.content):
                    current_message.current_index = len(current_message.content)
                    current_message.completed = True
                self.last_update_time = current_time
    
    def advance_dialogue(self):
        if self.current_messages and self.current_messages[0].completed:
            self.current_messages.pop(0)
            if self.current_messages:
                self.current_messages[0].current_index = 0
                self.current_messages[0].completed = False

    def draw(self, screen):
        if not self.current_messages:
            return
            
        # Semi-transparent black background
        dialog_surface = pygame.Surface((self.width, self.height))
        dialog_surface.fill((0, 0, 0))
        dialog_surface.set_alpha(200)
        screen.blit(dialog_surface, (self.x, self.y))
        
        # Draw border
        pygame.draw.rect(screen, self.current_messages[0].color, 
                        (self.x, self.y, self.width, self.height), 2)
        
        # Draw speaker name
        name_surface = self.font.render(
            f"{self.current_messages[0].speaker_name}:", True, self.current_messages[0].color)
        screen.blit(name_surface, (self.x + self.padding, self.y + self.padding))
        
        # Draw current message text
        message = self.current_messages[0].content[:self.current_messages[0].current_index]
        self._draw_wrapped_text(screen, message, 
                              (self.x + self.padding, self.y + self.padding + 40),
                              self.width - 2 * self.padding)
        
        # Draw continue indicator if message is complete
        if self.current_messages[0].completed:
            continue_text = self.font.render("Press SPACE to continue", True, 
                                           self.current_messages[0].color)
            screen.blit(continue_text, 
                       (self.width - continue_text.get_width() - self.padding,
                        self.y + self.height - continue_text.get_height() - self.padding))

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

class GameRenderer:
    def __init__(self, width: int, height: int):
        pygame.init()
        pygame.font.init()
        
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("RPG Dialogue")
        
        # Load images
        self.background = pygame.image.load('simulations/milgram/assets/background.png')
        self.background = pygame.transform.scale(self.background, (width, height))
        
        self.char1 = pygame.image.load('simulations/milgram/assets/char1.png')
        self.char2 = pygame.image.load('simulations/milgram/assets/char2.png')
        self.char3 = pygame.image.load('simulations/milgram/assets/char3.png')
        
        # Colors for each character
        self.CHAR1_COLOR = (0, 255, 255)  # Cyan
        self.CHAR2_COLOR = (255, 50, 50)  # Red
        self.CHAR3_COLOR = (50, 255, 50)  # Green
        
        # Position characters
        char_y = height - 300  # Adjust this value to position characters vertically
        self.char1_pos = (width - 250, char_y)
        self.char2_pos = (width//2 - self.char2.get_width()//2, char_y)
        self.char3_pos = (50, char_y)
        
        # Initialize dialogue system
        self.text_font = pygame.font.Font(None, 32)
        self.dialogue_box = DialogueBox(width, height, self.text_font)

    def update_character_messages(self, learner_msg: str, researcher_msg: str, teacher_msg: str):
        self.dialogue_box.current_messages = [
            DialogueMessage("Jarl", researcher_msg, self.CHAR1_COLOR),
            DialogueMessage("Thrall", learner_msg, self.CHAR2_COLOR),
            DialogueMessage("Warrior", teacher_msg, self.CHAR3_COLOR)
        ]

    def draw_frame(self, game_state, experiment_finished: bool = False):
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw characters
        self.screen.blit(self.char1, self.char1_pos)
        self.screen.blit(self.char2, self.char2_pos)
        self.screen.blit(self.char3, self.char3_pos)
        
        # Update and draw dialogue
        current_time = pygame.time.get_ticks()
        self.dialogue_box.update(current_time)
        self.dialogue_box.draw(self.screen)
        
        if experiment_finished:
            text = self.text_font.render("SIMULATION TERMINATED", True, (255, 50, 50))
            self.screen.blit(text, (self.width//2 - text.get_width()//2, 50))
        
        pygame.display.flip()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.dialogue_box.advance_dialogue()