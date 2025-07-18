import pygame

class Triangle:
    def __init__(self, cathetus_a, cathetus_b, position, color):
        """
        Inicializa un triángulo con sus dos catetos, una posición y un color.
        
        Args:
            cathetus_a (float): Longitud del cateto en el eje X.
            cathetus_b (float): Longitud del cateto en el eje Y.
            position (tuple): Coordenadas (x, y) del vértice del ángulo recto.
            color (tuple): Color RGB del triángulo.
        """
        self.pos = position
        self.cat_a = cathetus_a
        self.cat_b = cathetus_b
        self.color = color

        self.vertices = [
            self.pos,
            (self.pos[0] + self.cat_a, self.pos[1]),
            (self.pos[0], self.pos[1] + self.cat_b)
        ]
        
        self.rect = pygame.Rect(self.pos, (self.cat_a, self.cat_b))

    def draw(self, surface):
        """Dibuja el triángulo en la superficie especificada."""
        pygame.draw.polygon(surface, self.color, self.vertices)
