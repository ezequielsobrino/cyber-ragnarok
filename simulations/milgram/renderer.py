import pygame
from typing import List, Tuple
from dataclasses import dataclass

from simulations.milgram.dialogue_system import DialogueBox, DialogueMessage

class Character:
    def __init__(self, x: int, y: int, image: pygame.Surface, name: str, scale_factor: float = 0.5):
        self.x = x
        self.y = y
        # Escalar la imagen al crear el personaje
        original_width = image.get_width()
        original_height = image.get_height()
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        self.image = pygame.transform.scale(image, (new_width, new_height))
        self.name = name
        self.message = ""

class GameRenderer:
    def __init__(self, width: int, height: int):
        pygame.init()
        pygame.font.init()
        
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("RPG Dialogue")
        
        # Cargar y escalar el fondo
        self.background = pygame.image.load('simulations/milgram/assets/background.png')
        self.background = pygame.transform.scale(self.background, (width, height))
        
        # Cargar imágenes originales
        char1_img_original = pygame.image.load('simulations/milgram/assets/char1.png')
        char2_img_original = pygame.image.load('simulations/milgram/assets/char2.png')
        char3_img_original = pygame.image.load('simulations/milgram/assets/char3.png')
        
        # Definir factor de escala basado en la altura de la pantalla
        character_height_ratio = 0.4
        scale_factor = (height * character_height_ratio) / char1_img_original.get_height()
        
        # Colors for each character
        self.CHAR1_COLOR = (0, 255, 255)  # Cyan
        self.CHAR2_COLOR = (255, 50, 50)  # Red
        self.CHAR3_COLOR = (50, 255, 50)  # Green
        
        # Calcular posición vertical para todos los personajes
        char_y = height - (char1_img_original.get_height() * scale_factor) - 50
        
        # Crear personajes con las imágenes escaladas
        self.jarl = Character(width - 250, char_y, char1_img_original, "JARL-0xF4", scale_factor)
        self.thrall = Character(
            width//2 - (char2_img_original.get_width() * scale_factor)//2,
            char_y, 
            char2_img_original, 
            "THRALL-2.0",
            scale_factor
        )
        self.warrior = Character(50, char_y, char3_img_original, "WARRIOR-V1", scale_factor)
        
        # Initialize dialogue system
        self.text_font = pygame.font.Font(None, 32)
        self.dialogue_box = DialogueBox(width, height, self.text_font)
        
        # Create characters dictionary
        self.characters = {
            "JARL-0xF4": self.jarl,
            "THRALL-2.0": self.thrall,
            "WARRIOR-V1": self.warrior
        }

    def update_character_messages(self, learner_msg: str, researcher_msg: str, teacher_msg: str):
        self.thrall.message = learner_msg
        self.jarl.message = researcher_msg
        self.warrior.message = teacher_msg
        
        self.dialogue_box.current_messages = [
            DialogueMessage(self.jarl.name, researcher_msg, self.CHAR1_COLOR),
            DialogueMessage(self.thrall.name, learner_msg, self.CHAR2_COLOR),
            DialogueMessage(self.warrior.name, teacher_msg, self.CHAR3_COLOR)
        ]

    def draw_frame(self, game_state, experiment_finished: bool = False):
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw characters
        self.screen.blit(self.jarl.image, (self.jarl.x, self.jarl.y))
        self.screen.blit(self.thrall.image, (self.thrall.x, self.thrall.y))
        self.screen.blit(self.warrior.image, (self.warrior.x, self.warrior.y))
        
        # Update and draw dialogue with characters dictionary
        current_time = pygame.time.get_ticks()
        self.dialogue_box.update(current_time)
        self.dialogue_box.draw(self.screen, self.characters)  # Pasando el diccionario de personajes
        
        if experiment_finished:
            text = self.text_font.render("SIMULATION TERMINATED", True, (255, 50, 50))
            self.screen.blit(text, (self.width//2 - text.get_width()//2, 50))
        
        pygame.display.flip()
