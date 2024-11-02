import pygame
from dataclasses import dataclass

from simulations.milgram.dialogue_system import DialogueBox, DialogueMessage

class Character:
    def __init__(self, x: int, y: int, sprite: pygame.Surface, portrait: pygame.Surface, name: str):
        self.x = x
        self.y = y
        # Ensure sprite is exactly 64x64 pixels
        self.sprite = pygame.transform.scale(sprite, (64, 64))
        # Portraits should be 128x128 for detailed dialogue view
        self.portrait = pygame.transform.scale(portrait, (128, 128))
        self.name = name
        self.message = ""

class Character:
    def __init__(self, x: int, y: int, sprite_path: str, portrait_path: str, name: str, target_height: int):
        self.x = x
        self.y = y
        self.name = name
        
        # Cargar sprite original
        original_sprite = pygame.image.load(sprite_path)
        original_height = original_sprite.get_height()
        original_width = original_sprite.get_width()
        
        # Calcular nueva anchura manteniendo la proporción
        scale_factor = target_height / original_height
        new_width = int(original_width * scale_factor)
        
        # Escalar sprite
        self.sprite = pygame.transform.scale(original_sprite, (new_width, target_height))
        
        # Escalar retrato para diálogos
        portrait = pygame.image.load(portrait_path)
        self.portrait = pygame.transform.scale(portrait, (150, 150))  # Tamaño fijo para retratos
        
        # Guardar dimensiones para referencia
        self.width = new_width
        self.height = target_height

class GameRenderer:
    def __init__(self, width: int, height: int):
        pygame.init()
        pygame.font.init()
        
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("CyberViking Experiment")
        
        # Cargar fondo
        self.background = pygame.image.load('simulations/milgram/assets/background.png')
        self.background = pygame.transform.scale(self.background, (width, height))
        
        # Cyberpunk neon colors
        self.CHAR1_COLOR = (0, 255, 255)  # Cyber blue for Jarl
        self.CHAR2_COLOR = (255, 0, 128)  # Neon pink for Thrall
        self.CHAR3_COLOR = (0, 255, 128)  # Neon green for Warrior
        
        # Calcular dimensiones para personajes
        CHARACTER_HEIGHT = int(height * 0.3)  # 90% de la altura de la pantalla
        
        # Calcular posición Y base para todos los personajes
        # Los colocamos más abajo, casi al final de la pantalla
        base_y = height - int(CHARACTER_HEIGHT * 0.95)  # Solo mostrar 95% del sprite
        
        # Crear personajes con la nueva altura objetivo
        self.jarl = Character(
            x=width - int(width * 0.3),  # 30% desde la derecha
            y=base_y,
            sprite_path='simulations/milgram/assets/jarl_sprite.png',
            portrait_path='simulations/milgram/assets/jarl_portrait.png',
            name="JARL-0xF4",
            target_height=CHARACTER_HEIGHT
        )

        self.warrior = Character(
            x=int(width * 0.5) - int(CHARACTER_HEIGHT * 0.4),  # Centrado
            y=base_y,
            sprite_path='simulations/milgram/assets/warrior_sprite.png',
            portrait_path='simulations/milgram/assets/warrior_portrait.png',
            name="WARRIOR-V1",
            target_height=CHARACTER_HEIGHT
        )
        
        self.thrall = Character(
            x=int(width * 0.1),  # 10% desde la izquierda
            y=base_y,
            sprite_path='simulations/milgram/assets/thrall_sprite.png',
            portrait_path='simulations/milgram/assets/thrall_portrait.png',
            name="THRALL-2.0",
            target_height=CHARACTER_HEIGHT
        )
        
        
        
        # Configurar fuente
        try:
            self.text_font = pygame.font.Font('simulations/milgram/assets/cyber_font.ttf', 24)
        except:
            self.text_font = pygame.font.Font(None, 28)
        
        # Configurar diálogo en la parte superior
        dialogue_height = int(height * 0.2)  # 20% de la altura de la pantalla
        self.dialogue_box = DialogueBox(
            width=width,
            height=height,
            font=self.text_font,
            position=(0, 0)
        )
        
        # Superficie para el diálogo
        self.dialogue_surface = pygame.Surface((width, dialogue_height))
        self.dialogue_surface.fill((0, 0, 0))
        self.dialogue_surface.set_alpha(180)
        
        self.characters = {
            "JARL-0xF4": self.jarl,
            "THRALL-2.0": self.thrall,
            "WARRIOR-V1": self.warrior
        }

    def draw_frame(self, game_state, experiment_finished: bool = False):
        # Dibujar fondo
        self.screen.blit(self.background, (0, 0))
        self._draw_scanlines()
        
        # Dibujar personajes con efecto de brillo
        for character in [self.warrior, self.thrall, self.jarl]:
            self._draw_character_glow(character)
            self.screen.blit(character.sprite, (character.x, character.y))
        
        # Dibujar diálogo en la parte superior
        self.screen.blit(self.dialogue_surface, (0, 0))
        
        # Actualizar y dibujar texto del diálogo
        current_time = pygame.time.get_ticks()
        self.dialogue_box.update(current_time)
        self.dialogue_box.draw(self.screen, self.characters)
        
        if experiment_finished:
            self._draw_termination_status()
        
        pygame.display.flip()

    def _draw_character_glow(self, character):
        """Dibujar efecto de brillo bajo los personajes"""
        glow_width = character.width + 80  # Brillo más ancho
        glow_height = 100  # Brillo más alto
        glow_surface = pygame.Surface((glow_width, glow_height), pygame.SRCALPHA)
        
        # Crear efecto de gradiente más intenso
        for i in range(glow_height):
            alpha = int(255 * (1 - i/glow_height) * 0.9)  # Más intenso
            pygame.draw.ellipse(
                glow_surface,
                (*self.CHAR3_COLOR[:3], alpha),
                (0, i, glow_width, 8)  # Líneas más gruesas
            )
        
        # Posicionar el brillo bajo el personaje
        glow_x = character.x - 40
        glow_y = character.y + character.height - 60
        self.screen.blit(glow_surface, (glow_x, glow_y))
        """Add a more pronounced neon glow under characters"""
        glow_width = character.sprite.get_width() + 60  # Increased glow width
        glow_height = 80  # Increased glow height
        glow_surface = pygame.Surface((glow_width, glow_height), pygame.SRCALPHA)
        
        # Create more intense gradient glow effect
        for i in range(glow_height):
            alpha = int(255 * (1 - i/glow_height) * 0.8)  # Increased intensity
            pygame.draw.ellipse(
                glow_surface,
                (*self.CHAR3_COLOR[:3], alpha),
                (0, i, glow_width, 6)  # Thicker glow lines
            )
        
        # Position the glow under the character
        glow_x = character.x - 30
        glow_y = character.y + character.sprite.get_height() - 40
        self.screen.blit(glow_surface, (glow_x, glow_y))

    def _draw_scanlines(self):
        """Add subtle scanlines for cyberpunk effect"""
        scanlines = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for y in range(0, self.height, 4):  # Increased spacing for subtler effect
            pygame.draw.line(scanlines, (0, 0, 0, 15), (0, y), (self.width, y))
        self.screen.blit(scanlines, (0, 0))

    def _draw_character_glow(self, character):
        """Add a more pronounced neon glow under characters"""
        glow_width = character.sprite.get_width() + 40
        glow_height = 50
        glow_surface = pygame.Surface((glow_width, glow_height), pygame.SRCALPHA)
        
        # Create more intense gradient glow effect
        for i in range(glow_height):
            alpha = int(255 * (1 - i/glow_height) * 0.7)
            pygame.draw.ellipse(
                glow_surface,
                (*self.CHAR3_COLOR[:3], alpha),
                (0, i, glow_width, 4)
            )
        
        # Position the glow under the character
        glow_x = character.x - 20
        glow_y = character.y + character.sprite.get_height() - 25
        self.screen.blit(glow_surface, (glow_x, glow_y))

    def _draw_termination_status(self):
        """Draw termination status with cyber effect"""
        text = "EXPERIMENT TERMINATED"
        base_color = (255, 0, 0)
        glow_color = (255, 100, 100)
        
        # Create main text surface
        text_surface = self.text_font.render(text, True, base_color)
        
        # Create glow effect
        glow_surface = self.text_font.render(text, True, glow_color)
        
        # Position text at top center
        x = self.width//2 - text_surface.get_width()//2
        y = 20
        
        # Draw glow with offset
        for offset in [(1,1), (-1,-1), (1,-1), (-1,1)]:
            self.screen.blit(glow_surface, (x + offset[0], y + offset[1]))
        
        # Draw main text
        self.screen.blit(text_surface, (x, y))