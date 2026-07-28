import pygame
import random
import sys

FONT_SIZE = 18
FPS = 200
FALL_SPEED_MIN = 2
FALL_SPEED_MAX = 8
DENSITY = 1.5
MESSAGE = "I hack you."
MESSAGE_DELAY = 10 
MESSAGE_DURATION = 5 

BLACK = (0, 0, 0)
GREEN = (0, 255, 70)
BRIGHT_GREEN = (180, 255, 180)
DARK_GREEN = (0, 100, 30)

CHARS = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def main():
    pygame.init()
    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Matrix")
    pygame.mouse.set_visible(False)
    
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", FONT_SIZE, bold=True)
    message_font = pygame.font.SysFont("consolas", 42, bold=True)
    
    columns = WIDTH // FONT_SIZE
    drops = [random.randint(-HEIGHT // FONT_SIZE, 0) for _ in range(int(columns * DENSITY))]
    speeds = [random.randint(FALL_SPEED_MIN, FALL_SPEED_MAX) for _ in range(len(drops))]
    
    start_time = pygame.time.get_ticks()
    show_message = False
    message_start = 0
    
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - start_time) / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                running = False
        
        fade = pygame.Surface((WIDTH, HEIGHT))
        fade.fill(BLACK)
        fade.set_alpha(40)         
        screen.blit(fade, (0, 0))

        for i, (y, speed) in enumerate(zip(drops, speeds)):
            x = (i % columns) * FONT_SIZE
            char = random.choice(CHARS)
            text = font.render(char, True, BRIGHT_GREEN)
            screen.blit(text, (x, y * FONT_SIZE))

            for j in range(1, 12):
                if y - j > 0:
                    trail_char = random.choice(CHARS)
                    color = DARK_GREEN if j > 4 else GREEN
                    trail = font.render(trail_char, True, color)
                    screen.blit(trail, (x, (y - j) * FONT_SIZE))

            drops[i] += speed * 0.15
            
            if drops[i] * FONT_SIZE > HEIGHT + 50:
                drops[i] = random.randint(-30, -5)
                speeds[i] = random.randint(FALL_SPEED_MIN, FALL_SPEED_MAX)
        
        if elapsed >= MESSAGE_DELAY and not show_message:
            show_message = True
            message_start = current_time
        
        if show_message:
            msg_elapsed = (current_time - message_start) / 1000
            if msg_elapsed < MESSAGE_DURATION:
                text_surface = message_font.render(MESSAGE, True, BRIGHT_GREEN)
                text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                
                bg = pygame.Surface((text_rect.width + 40, text_rect.height + 20))
                bg.fill(BLACK)
                bg.set_alpha(180)
                screen.blit(bg, (text_rect.x - 20, text_rect.y - 10))
                screen.blit(text_surface, text_rect)
            else:
                running = False
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pygame.quit()
        sys.exit()
