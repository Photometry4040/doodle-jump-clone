import pygame
from player import Player
from utils import generate_platforms, check_collision, update_platforms, scroll_platforms

# Pygame 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Doodle Jump Clone")

# 색상 정의
WHITE = (255, 255, 255)

# 게임 객체 생성
all_sprites = pygame.sprite.Group()
platforms = generate_platforms(SCREEN_HEIGHT, SCREEN_WIDTH)
player = Player(SCREEN_WIDTH)

# 플레이어 초기 위치 설정 - 첫 번째 플랫폼 위에 배치
platforms_list = platforms.sprites()
if platforms_list:
    first_platform = platforms_list[0]  # generate_platforms()에서 생성된 첫 번째 플랫폼
    player.rect.centerx = first_platform.rect.centerx
    player.rect.bottom = first_platform.rect.top
    player.velocity_y = 0  # 초기 속도를 0으로 설정

# 스프라이트 그룹에 추가
all_sprites.add(player)
all_sprites.add(platforms)

# 게임 설정
clock = pygame.time.Clock()
score = 0
running = True

# 게임 루프
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키보드 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    elif keys[pygame.K_RIGHT]:
        player.move_right()
    else:
        player.stop()

    # 업데이트
    player.update()
    check_collision(player, platforms)
    
    # 스크롤링 및 점수 계산
    scroll_amount = scroll_platforms(platforms, player, SCREEN_HEIGHT, SCREEN_WIDTH)
    score += int(scroll_amount)
    
    # 플랫폼 업데이트
    update_platforms(platforms, all_sprites, SCREEN_HEIGHT, SCREEN_WIDTH)
    
    # 게임 오버 체크
    if player.rect.top > SCREEN_HEIGHT:
        running = False

    # 화면 그리기
    screen.fill(WHITE)
    all_sprites.draw(screen)
    
    # 점수 표시
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()