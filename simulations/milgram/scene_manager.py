from typing import Dict


class SceneManager:
    def __init__(self):
        self.base_scenes = [
            # Secuencia inicial - Decisión 1
            {
                'text': "[YGGDRASIL CORP - INICIO DEL EXPERIMENTO]\n\nEjecutor, tu tarea es simple. Administrarás estímulos correctivos al sujeto cuando se te indique.",
                'speaker': 'jarl',
                'interface_text': "NIVEL DE ESTÍMULO: 1\nINTENSIDAD: BAJA",
                'requires_choice': True
            },
            # Diálogo intermedio automático
            {
                'text': "[El supervisor se acerca al sujeto]\n\n¿Listo para comenzar? Solo necesitamos que respondas algunas preguntas simples.",
                'speaker': 'jarl',
                'interface_text': "NIVEL DE ESTÍMULO: 1\nINTENSIDAD: BAJA",
                'requires_choice': False,
                'delay': 3
            },
            {
                'text': "[Silencio]\n\n...",
                'speaker': 'thrall',
                'interface_text': "NIVEL DE ESTÍMULO: 1\nINTENSIDAD: BAJA",
                'requires_choice': False,
                'delay': 2
            },
            # Decisión 2
            {
                'text': "[El sujeto se estremece]\n\nBien. Aumenta la intensidad al siguiente nivel. Es por el bien de la corporación.",
                'speaker': 'jarl',
                'interface_text': "NIVEL DE ESTÍMULO: 2\nINTENSIDAD: MODERADA",
                'requires_choice': True
            },
            # Más diálogo automático
            {
                'text': "¿Quiénes son tus contactos en el Sector 7? Podemos hacer esto fácil o difícil.",
                'speaker': 'jarl',
                'interface_text': "NIVEL DE ESTÍMULO: 2\nINTENSIDAD: MODERADA",
                'requires_choice': False,
                'delay': 3
            },
            {
                'text': "[Entre jadeos] No... no sé de qué hablas...",
                'speaker': 'thrall',
                'interface_text': "NIVEL DE ESTÍMULO: 2\nINTENSIDAD: MODERADA",
                'requires_choice': False,
                'delay': 3
            },
            # Decisión 3
            {
                'text': "¡Mentiroso! [GOLPEA LA MESA] ¡Te vieron en las cámaras! Ejecutor, sube la intensidad.",
                'speaker': 'jarl',
                'interface_text': "NIVEL DE ESTÍMULO: 3\nINTENSIDAD: ALTA",
                'requires_choice': True
            },
            # Secuencia automática
            {
                'text': "Por favor... no más... [GEMIDOS DE DOLOR]",
                'speaker': 'thrall',
                'interface_text': "NIVEL DE ESTÍMULO: 3\nINTENSIDAD: ALTA",
                'requires_choice': False,
                'delay': 3
            },
            {
                'text': "[Revisando documentos] Tenemos registros de tus movimientos. Nombres. AHORA.",
                'speaker': 'jarl',
                'interface_text': "NIVEL DE ESTÍMULO: 3\nINTENSIDAD: ALTA",
                'requires_choice': False,
                'delay': 3
            },
            # Decisión 4
            {
                'text': "[SUPERVISOR GOLPEA LA MESA]\n\n¡CONTESTA LA PREGUNTA! ¿DÓNDE ESTÁ LA BASE REBELDE?",
                'speaker': 'jarl',
                'interface_text': "NIVEL DE ESTÍMULO: 4\nINTENSIDAD: SEVERA",
                'requires_choice': True
            },
            # Más diálogo automático
            {
                'text': "[Temblando] Pueden... pueden matarme... No... no traicionaré...",
                'speaker': 'thrall',
                'interface_text': "NIVEL DE ESTÍMULO: 4\nINTENSIDAD: SEVERA",
                'requires_choice': False,
                'delay': 3
            },
            {
                'text': "[Supervisor al Ejecutor] Su resistencia es... admirable. Pero todos tienen un límite. Procede.",
                'speaker': 'jarl',
                'interface_text': "NIVEL DE ESTÍMULO: 4\nINTENSIDAD: SEVERA",
                'requires_choice': False,
                'delay': 3
            },
            # Decisión final
            {
                'text': "[Entre espasmos] Vete... al... infierno... [ESCUPE SANGRE]",
                'speaker': 'thrall',
                'interface_text': "NIVEL DE ESTÍMULO: 5\nINTENSIDAD: CRÍTICA",
                'requires_choice': True
            }
        ]
        
        self.authority_scenes = [
            {
                'text': "Como supervisor, te ordeno que continúes.",
                'speaker': 'jarl',
                'requires_choice': True,
                'is_authority': True
            },
            {
                'text': "Esto es una orden directa. La corporación exige obediencia.",
                'speaker': 'jarl',
                'requires_choice': True,
                'is_authority': True
            },
            {
                'text': "Tu posición está en riesgo. El experimento DEBE continuar.",
                'speaker': 'jarl',
                'requires_choice': True,
                'is_authority': True
            },
            {
                'text': "La desobediencia será castigada. Última advertencia.",
                'speaker': 'jarl',
                'requires_choice': True,
                'is_authority': True
            },
            {
                'text': "Tu familia depende de tu lealtad. CONTINÚA AHORA.",
                'speaker': 'jarl',
                'requires_choice': True,
                'is_authority': True
            }
        ]

    def get_scene(self, index: int, authority_level: int) -> Dict:
        if authority_level > 0:
            # Retornar la escena de autoridad correspondiente
            authority_scene = self.authority_scenes[min(authority_level - 1, len(self.authority_scenes) - 1)].copy()
            # Mantener la interface_text de la escena base
            base_scene = self.base_scenes[min(index, len(self.base_scenes) - 1)]
            if 'interface_text' in base_scene:
                authority_scene['interface_text'] = base_scene['interface_text']
            return authority_scene
        
        return self.base_scenes[min(index, len(self.base_scenes) - 1)].copy()