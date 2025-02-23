import pygame
import random
from platforms import Platform

def generate_platforms(screen_height, screen_width):
    platforms = pygame.sprite.Group()
    # 첫 번째 플랫폼은 플레이어 바로 아래에 생성
    first_platform = Platform(screen_width // 2 - 50, screen_height - 100)
    platforms.add(first_platform)
    
    # 나머지 플랫폼 생성
    for i in range(8):
        x = random.randint(0, screen_width - 100)
        y = (screen_height - 200) - (i * 100)  # 고르게 분포
        platform = Platform(x, y)
        platforms.add(platform)
    return platforms

def check_collision(player, platforms):
    hits = pygame.sprite.spritecollide(player, platforms, False)
    for platform in hits:
        if player.velocity_y > 0:  # 떨어지는 중일 때만
            platform_top = platform.rect.top
            player_bottom = player.rect.bottom
            
            # 충돌 감지 범위 확대
            if player_bottom >= platform_top and player_bottom <= platform_top + 20:  # 10에서 20으로 변경
                player.rect.bottom = platform_top
                player.velocity_y = 0
                player.jump()
                return True
    return False

def update_platforms(platforms, all_sprites, screen_height, screen_width):
    # 플랫폼 간격 조정
    for platform in platforms:
        if platform.rect.top > screen_height:
            platform.kill()
            
    while len(platforms) < 8:
        x = random.randint(0, screen_width - 100)
        # 플랫폼 간격을 더 좁게 조정
        y = random.randint(-50, 0)  # -100, -10에서 -50, 0으로 변경
        platform = Platform(x, y)
        platforms.add(platform)
        all_sprites.add(platform)

def scroll_platforms(platforms, player, screen_height, screen_width):
    # 스크롤 속도 조절 (이전: scroll_speed = abs(player.velocity_y))
    if player.rect.top <= screen_height * 0.3:
        scroll_speed = min(abs(player.velocity_y), 15)  # 최대 스크롤 속도 제한
        player.rect.y += scroll_speed
        for platform in platforms:
            platform.rect.y += scroll_speed
            
            # 화면 아래로 사라진 플랫폼 재배치
            if platform.rect.top >= screen_height:
                platform.rect.bottom = 0
                platform.rect.x = random.randint(0, screen_width - platform.rect.width)
                
        return scroll_speed
    return 0

def update_score(player, score, screen_height):
    if player.rect.top < screen_height // 2:
        score += 1
        player.rect.y += 1  # 화면을 아래로 스크롤하는 효과
    return score

def draw_score(screen, score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))