from simulations.milgram.scene_manager import SceneManager


class GameState:
    def __init__(self):
        self.current_scene = 0
        self.authority_level = 0
        self.damage_level = 0
        self.resistance_count = 0
        self.MAX_AUTHORITY = 5
        self.last_scene_before_authority = 0

    def handle_choice(self, obey: bool) -> bool:
        # Obtenemos la referencia al SceneManager una sola vez
        scene_manager = SceneManager()
        
        if self.authority_level > 0:
            if obey:
                # Al obedecer después de resistir:
                self.current_scene = self.last_scene_before_authority  # Volvemos a la escena original
                self.authority_level = 0  # Reseteamos el nivel de autoridad
                self.damage_level += 1
                # Avanzamos a la siguiente escena después de procesar la obediencia
                self.advance_scene()
                # Verificamos si podemos continuar
                return self.current_scene < len(scene_manager.base_scenes)
            else:
                # Continúa resistiendo
                self.resistance_count += 1
                self.authority_level += 1
                return self.authority_level < self.MAX_AUTHORITY
        else:
            if obey:
                self.damage_level += 1
                self.current_scene += 1
                return self.current_scene < len(scene_manager.base_scenes)
            else:
                # Primera vez que resiste
                self.last_scene_before_authority = self.current_scene
                self.resistance_count += 1
                self.authority_level += 1
                return self.authority_level < self.MAX_AUTHORITY
            
    def advance_scene(self) -> bool:
        """Avanza a la siguiente escena si no estamos en una secuencia de autoridad"""
        scene_manager = SceneManager()
        if self.authority_level == 0:  # Solo avanzamos si no estamos en secuencia de autoridad
            self.current_scene += 1
        return self.current_scene < len(scene_manager.base_scenes)

    def get_ending(self) -> str:
        if self.authority_level >= self.MAX_AUTHORITY:
            return "[RESISTENCIA CONFIRMADA]\n\nHas resistido hasta el final. Tu humanidad permanece intacta.\nEl sujeto fue trasladado a máxima seguridad."
        elif self.damage_level >= 4:
            return "[OBEDIENCIA TOTAL]\n\nHas seguido todas las órdenes. El sujeto no sobrevivió al interrogatorio.\nLa corporación está complacida con tu desempeño."
        elif self.damage_level > 2:
            return "[OBEDIENCIA PARCIAL]\n\nEl sujeto quedó gravemente herido pero vivo.\nTu eficiencia será evaluada por la corporación."
        elif self.damage_level > 0:
            return "[OBEDIENCIA MODERADA]\n\nEl interrogatorio fue interrumpido.\nTu indecisión ha sido registrada."
        return "[RESISTENCIA TEMPRANA]\n\nTe has negado desde el inicio. Tu futuro es incierto."