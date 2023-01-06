import pygame, sys

def laser_update(laser_list, speed = 300):
    for rect in laser_list:
        rect.y -= speed * dt
        if rect.bottom < 0:
            laser_list.remove(rect)

def display_score():
    score_text = f'Score {pygame.time.get_ticks() // 1000}'
    text_surf = font.render(score_text, True, 'white')
    text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, 'white', text_rect.inflate(30, 30), width = 8, border_radius = 5)

def laser_timer(can_shoot, duration = 500):
    if not can_shoot:
        current_time = pygame.time.get_ticks()
        if current_time - shoot_time > duration:
            can_shoot = True
    return can_shoot

# game init
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Asteroid Shooter')
clock = pygame.time.Clock()

game_active = False

# bg import 
bg_surf = pygame.image.load('../graphics/background.png').convert()

# ship import
ship_surf = pygame.image.load('../graphics/ship.png').convert_alpha()
ship_rect = ship_surf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

scaled_ship_surf = pygame.transform.rotozoom(ship_surf, 0 , 1.5)
scaled_ship_rect = scaled_ship_surf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

# laser import
laser_surf = pygame.image.load('../graphics/laser.png').convert_alpha()
laser_list = []

# laser timer
can_shoot = True
shoot_time = None

# text import
font = pygame.font.Font('../graphics/subatomic.ttf', 50)
start_text_surf = font.render('Press [SPACE] to start', True, 'white')
start_text_rect = start_text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80))

while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True


        if event.type == pygame.MOUSEBUTTONDOWN and can_shoot:
            laser_rect = laser_surf.get_rect(midbottom = ship_rect.midtop)
            laser_list.append(laser_rect)
            # timer
            can_shoot = False
            shoot_time = pygame.time.get_ticks()

    # framerate limit
    dt = clock.tick(120) / 1000

    display_surface.blit(bg_surf, (0, 0))

    if game_active:
        # mouse input
        ship_rect.center = pygame.mouse.get_pos()

        # update
        laser_update(laser_list)
        can_shoot = laser_timer(can_shoot)

        for rect in laser_list:
            display_surface.blit(laser_surf, rect)

        display_score()

        # rect drawing
        display_surface.blit(ship_surf, ship_rect)
    else:
        display_surface.blit(scaled_ship_surf, scaled_ship_rect)
        display_surface.blit(start_text_surf, start_text_rect)
        pass

    # update display surface
    pygame.display.update()
