from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageChops
import math
import random
import os

def create_epic_vs_screen(image1_path, image2_path, player1_name, player2_name, output_path="epic_vs_screen.png"):
    """
    Crea una pantalla de versus épica con efectos visuales al estilo de juegos de pelea.
    Con manejo adaptativo de texto y alineación personalizada para cada jugador.
    """
    
    # [... Las funciones create_gradient_background y add_energy_effect se mantienen igual ...]
    def create_gradient_background():
        background = Image.new('RGB', (1280, 720), color='black')
        draw = ImageDraw.Draw(background)
        for _ in range(50):
            x = random.randint(0, 1280)
            y = random.randint(0, 720)
            size = random.randint(1, 3)
            brightness = random.randint(30, 100)
            draw.ellipse([x, y, x+size, y+size], fill=(brightness, brightness, brightness))
        return background
    
    def add_energy_effect(img, color):
        effect = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(effect)
        for _ in range(20):
            x1 = random.randint(0, img.width)
            y1 = random.randint(0, img.height)
            x2 = x1 + random.randint(-100, 100)
            y2 = y1 + random.randint(-100, 100)
            draw.line([x1, y1, x2, y2], fill=color, width=2)
        return ImageChops.screen(img.convert('RGBA'), effect)
    
    # Crear el fondo y cargar imágenes
    background = create_gradient_background()
    char1 = Image.open(image1_path).convert('RGBA')
    char2 = Image.open(image2_path).convert('RGBA')
    
    # Función de redimensionamiento
    def resize_image(img, target_width):
        aspect_ratio = img.width / img.height
        target_height = int(target_width / aspect_ratio)
        
        if target_height > 600:
            target_height = 600
            target_width = int(target_height * aspect_ratio)
            
        return img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    # Redimensionar y aplicar efectos
    char1 = resize_image(char1, 500)
    char2 = resize_image(char2, 500)
    char1 = add_energy_effect(char1, (0, 150, 255, 150))
    char2 = add_energy_effect(char2, (255, 100, 0, 150))
    
    # Función para crear sombra
    def create_shadow(img):
        shadow = img.copy().convert('RGBA')
        shadow = shadow.filter(ImageFilter.GaussianBlur(10))
        enhancer = ImageEnhance.Brightness(shadow)
        shadow = enhancer.enhance(0.3)
        return shadow

    # Aplicar sombras
    shadow1 = create_shadow(char1)
    shadow2 = create_shadow(char2)
    
    # Calcular posiciones
    center_y = 720 // 2
    pos1_x = 100
    pos1_y = center_y - char1.height // 2 - 50  # P1 más arriba
    
    pos2_x = 1280 - char2.width - 100
    pos2_y = center_y - char2.height // 2 + 50  # P2 más abajo
    
    # Pegar sombras y personajes
    background.paste(shadow1, (pos1_x+20, pos1_y+20), shadow1)
    background.paste(shadow2, (pos2_x+20, pos2_y+20), shadow2)
    background.paste(char1, (pos1_x, pos1_y), char1)
    background.paste(char2, (pos2_x, pos2_y), char2)
    
    # Función mejorada para texto con alineación
    def draw_epic_text(draw, text, position, main_color=(255, 255, 255), 
                      glow_color=(255, 0, 0), initial_size=70, align='left'):
        try:
            font = ImageFont.truetype("impact.ttf", initial_size)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", initial_size)
            except:
                font = ImageFont.load_default()
                initial_size = 30
        
        # Obtener dimensiones del texto
        text_width = font.getlength(text)
        max_width = 400
        
        # Ajustar tamaño si es necesario
        if text_width > max_width:
            new_size = int(initial_size * (max_width / text_width))
            try:
                font = ImageFont.truetype("impact.ttf", new_size)
            except:
                try:
                    font = ImageFont.truetype("arial.ttf", new_size)
                except:
                    font = ImageFont.load_default()
            text_width = font.getlength(text)
        
        x, y = position
        # Ajustar posición x según alineación
        if align == 'right':
            x = x - text_width
        elif align == 'center':
            x = x - text_width // 2
        
        # Añadir resplandor
        for offset in range(3, 8, 2):
            draw.text((x-offset, y), text, font=font, fill=glow_color)
            draw.text((x+offset, y), text, font=font, fill=glow_color)
            draw.text((x, y-offset), text, font=font, fill=glow_color)
            draw.text((x, y+offset), text, font=font, fill=glow_color)
        
        # Texto principal con borde
        outline_color = (0, 0, 0)
        for adj in range(-2, 3):
            for adj2 in range(-2, 3):
                draw.text((x+adj, y+adj2), text, font=font, fill=outline_color)
        
        # Texto principal
        draw.text((x, y), text, font=font, fill=main_color)
        
        return text_width
    
    draw = ImageDraw.Draw(background)
    
    # Dibujar nombres con alineaciones específicas
    # P1: alineado a la izquierda, P2: alineado a la derecha
    p1_y = pos1_y - 80
    p2_y = pos2_y + char2.height + 20
    
    # Nombre P1 alineado a la izquierda
    draw_epic_text(draw, player1_name, (pos1_x, p1_y), 
                  (200, 220, 255), (0, 100, 255), align='left')
    
    # Nombre P2 alineado a la derecha
    draw_epic_text(draw, player2_name, (1180, p2_y),  # 1180 = 1280 - 100 (margen)
                  (255, 220, 200), (255, 100, 0), align='right')
    
    # VS centrado
    draw_epic_text(draw, "VS", (640, center_y - 60), 
                  (255, 255, 255), (255, 0, 0), 120, align='center')
    
    # Añadir líneas de energía en el centro
    center_x = 640
    for _ in range(10):
        offset = random.randint(-100, 100)
        start_y = random.randint(0, 720)
        end_y = random.randint(0, 720)
        draw.line([(center_x + offset, start_y), 
                  (center_x + offset + random.randint(-50, 50), end_y)],
                 fill=(255, 255, 255, 128), width=2)
    
    # Guardar la imagen
    background.save(output_path, quality=95)
    print(f"Imagen épica guardada como {output_path}")

# Ejemplo de uso
if __name__ == "__main__":
    create_epic_vs_screen(
        "assets/o1_mini.png",
        "assets/o1_preview.png",
        "o1-mini",
        "o1-preview",
        "assets/vs/o1_mini-v-o1_preview.png"
    )