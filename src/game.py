import pygame
import random
import math
from . import config
from .triangle import Triangle

class Game:
    """
    Clase principal que gestiona el estado y la lógica del juego.
    """
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Pytagoras")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, config.FONT_SIZE)
        self.alert_font = pygame.font.Font(None, config.FONT_SIZE + 8)
        
        self.running = True
        self.game_over = False
        
        self.triangles = []
        self.active_input = True
        self.input_text = ""
        self.current_hypotenuse = 0
        self.message = ""
        self.input_rect = pygame.Rect(0, config.UI_Y_POSITION, config.INPUT_BOX_WIDTH, config.INPUT_BOX_HEIGHT)

    def draw_alert(self, text):
        """
        Dibuja un mensaje de alerta en el centro de la pantalla, lo muestra
        y espera un momento.
        """
        alert_surface = self.alert_font.render(text, True, config.ALERT_COLOR)
        
        alert_rect = alert_surface.get_rect(
            center=(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2)
        )
        
        self.screen.blit(alert_surface, alert_rect)
        
        pygame.display.flip()
        
        pygame.time.wait(1500)


    def start_new_round(self):
        """Inicia una nueva ronda generando una hipotenusa."""
        self.current_hypotenuse = random.randint(config.MIN_HYPOTENUSE, config.MAX_HYPOTENUSE)
        self.message = f"Hipotenusa: {self.current_hypotenuse}. Cateto: "
        self.input_text = ""
        self.active_input = True

    def process_input(self):
        """Procesa el cateto ingresado por el jugador."""
        self.active_input = False
        try:
            cathetus_a = float(self.input_text)
            
            if cathetus_a >= self.current_hypotenuse or cathetus_a <= 0:
                self.draw_alert("¡Medidas imposibles!")
                self.start_new_round()
                return

            cathetus_b = math.sqrt(self.current_hypotenuse**2 - cathetus_a**2)
            self.try_to_place_triangle(cathetus_a, cathetus_b)

        except (ValueError, TypeError):
            # CAMBIO: Llama a la función de alerta si la entrada no es un número
            self.draw_alert("¡Entrada inválida! Ingresa solo números.")
            self.start_new_round()

    def try_to_place_triangle(self, cat_a, cat_b):
        """Intenta encontrar una posición aleatoria para el nuevo triángulo sin colisiones."""
        for _ in range(config.MAX_PLACEMENT_ATTEMPTS):
            pos_x = random.randint(0, config.SCREEN_WIDTH - int(cat_a))
            pos_y = random.randint(config.UI_Y_POSITION + config.INPUT_BOX_HEIGHT + 20, config.SCREEN_HEIGHT - int(cat_b))
            
            random_color = (random.randint(50, 220), random.randint(50, 220), random.randint(50, 220))
            new_triangle = Triangle(cat_a, cat_b, (pos_x, pos_y), random_color)
            
            is_colliding = False
            for t in self.triangles:
                if new_triangle.rect.colliderect(t.rect):
                    is_colliding = True
                    break
            
            if not is_colliding:
                self.triangles.append(new_triangle)
                self.start_new_round()
                return

        self.game_over = True
        self.message = "¡Fin del juego! No hay más espacio."

    def handle_events(self):
        """Gestiona las entradas del usuario (teclado, cerrar ventana)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.active_input and not self.game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.input_text:
                            self.process_input()
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        if event.unicode.isdigit() or (event.unicode == '.' and '.' not in self.input_text):
                            self.input_text += event.unicode

    def draw(self):
        """Dibuja todos los elementos en la pantalla."""
        self.screen.fill(config.BACKGROUND_COLOR)
        
        if config.GRID_COLOR:
            for x in range(0, config.SCREEN_WIDTH, 50):
                pygame.draw.line(self.screen, config.GRID_COLOR, (x, 0), (x, config.SCREEN_HEIGHT))
            for y in range(0, config.SCREEN_HEIGHT, 50):
                pygame.draw.line(self.screen, config.GRID_COLOR, (0, y), (config.SCREEN_WIDTH, y))

        for triangle in self.triangles:
            triangle.draw(self.screen)
        
        msg_surface = self.font.render(self.message, True, config.TEXT_COLOR)
        msg_y_pos = config.UI_Y_POSITION + (config.INPUT_BOX_HEIGHT - msg_surface.get_height()) // 2
        self.screen.blit(msg_surface, (config.UI_X_PADDING, msg_y_pos))

        input_box_x = config.UI_X_PADDING + msg_surface.get_width() + config.UI_SPACING
        self.input_rect.x = input_box_x

        pygame.draw.rect(self.screen, config.INPUT_BOX_COLOR, self.input_rect)
        pygame.draw.rect(self.screen, config.TEXT_COLOR, self.input_rect, 2)

        text_surface = self.font.render(self.input_text, True, config.INPUT_TEXT_COLOR)
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

        if self.game_over:
            game_over_surface = self.alert_font.render(self.message, True, config.TEXT_COLOR, config.BACKGROUND_COLOR)
            text_rect = game_over_surface.get_rect(center=(config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT/2))
            self.screen.blit(game_over_surface, text_rect)

        pygame.display.flip()

    def run(self):
        """El bucle principal del juego."""
        self.start_new_round()
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(config.FPS)
        pygame.quit()
