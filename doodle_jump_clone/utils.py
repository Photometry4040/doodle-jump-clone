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
        # 플레이어가 떨어지는 중이고, 플랫폼의 윗부분에 닿았을 때만 점프
        if player.velocity_y > 0:  # 떨어지는 중일 때만
            platform_top = platform.rect.top
            player_bottom = player.rect.bottom
            
            # 플랫폼 상단 부근에서 충돌했는지 확인 (약간의 여유 허용)
            if player_bottom >= platform_top and player_bottom <= platform_top + 10:
                player.rect.bottom = platform_top
                player.velocity_y = 0
                player.jump()  # 자동 점프
                return True
    return False

def update_platforms(platforms, all_sprites, screen_height, screen_width):
    # 화면 아래로 사라진 플랫폼 제거 및 새로운 플랫폼 생성
    for platform in platforms:
        if platform.rect.top > screen_height:
            platform.kill()
            
    # 새로운 플랫폼 생성 - 간격 조정
    while len(platforms) < 8:
        x = random.randint(0, screen_width - 100)
        y = random.randint(-100, -10)  # 화면 위쪽에 생성
        platform = Platform(x, y)
        platforms.add(platform)
        all_sprites.add(platform)

def scroll_platforms(platforms, player, screen_height, screen_width):
    # 화면의 1/3 지점까지 올라왔을 때 스크롤 시작
    if player.rect.top <= screen_height * 0.3:
        scroll_speed = abs(player.velocity_y)
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