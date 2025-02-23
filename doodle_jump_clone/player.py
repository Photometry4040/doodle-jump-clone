import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width):
        super().__init__()
        self.screen_width = screen_width
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))  # 빨간색 플레이어
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = 550  # 시작 위치
        self.velocity_y = 0
        self.velocity_x = 0
        self.jump_power = -15
        self.gravity = 0.8
        self.speed = 5
        self.is_jumping = False

    def update(self):
        # 중력 적용
        self.velocity_y += self.gravity
        
        # 떨어지기 시작할 때 점프 상태 해제
        if self.velocity_y > 0:
            self.is_jumping = False
            
        self.rect.y += self.velocity_y
        self.rect.x += self.velocity_x

        # 좌우 이동시 화면 반대편으로 나오기
        if self.rect.right < 0:
            self.rect.left = self.screen_width
        elif self.rect.left > self.screen_width:
            self.rect.right = 0

    def jump(self):
        if not self.is_jumping:  # 이미 점프 중이 아닐 때만 점프
            self.velocity_y = self.jump_power
            self.is_jumping = True

    def move_left(self):
        self.velocity_x = -self.speed

    def move_right(self):
        self.velocity_x = self.speed

    def stop(self):
        self.velocity_x = 0