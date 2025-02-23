import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((100, 10))
        self.image.fill((0, 128, 0))  # 초록색 플랫폼
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y