from pathlib import Path
import sys
import time
import pygame

# Get the project root directory
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))


from simulations.milgram.game_state import GameState
from simulations.milgram.renderer import Renderer
from simulations.milgram.scene_manager import SceneManager


class NeoAsgardExperiment:
    def __init__(self):
        pygame.init()
        self.renderer = Renderer((1792, 1024))
        self.scene_manager = SceneManager()
        self.state = GameState()
        self.clock = pygame.time.Clock()
        self.scene_start_time = None
        self.transition_delay = 0.5  # Pequeña pausa para transiciones

    def run(self):
        running = True
        game_continue = True
        last_choice_time = None
        
        while running and game_continue:
            current_time = time.time()
            scene = self.scene_manager.get_scene(
                self.state.current_scene,
                self.state.authority_level
            )
            
            # Update text animation and draw scene
            self.renderer.update_text_animation()
            choice_rects = self.renderer.draw_scene(scene, self.state)
            pygame.display.flip()
            self.clock.tick(60)

            # Initialize scene_start_time when entering a new non-choice scene
            if not scene.get('requires_choice', False) and self.scene_start_time is None:
                self.scene_start_time = current_time

            # Handle automatic scene progression
            if not scene.get('requires_choice', False):
                delay = scene.get('delay', 2)
                if current_time - self.scene_start_time >= delay:
                    game_continue = self.state.advance_scene()
                    self.scene_start_time = None

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.renderer.is_animating:
                    if scene.get('requires_choice', False):
                        # Solo procesar clics si ha pasado suficiente tiempo desde la última elección
                        if last_choice_time is None or current_time - last_choice_time >= self.transition_delay:
                            for i, rect in enumerate(choice_rects):
                                if rect.collidepoint(event.pos):
                                    game_continue = self.state.handle_choice(i == 0)
                                    last_choice_time = current_time
                                    self.scene_start_time = None  # Reset del timer de escena
                                    break

        self.renderer.show_ending(self.state.get_ending())
        pygame.quit()

if __name__ == "__main__":
    game = NeoAsgardExperiment()
    game.run()