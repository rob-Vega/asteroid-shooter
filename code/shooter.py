import pygame, sys, time
from random import randint, uniform

def display_score():
    score_text = f'Score {pygame.time.get_ticks() // 1000}'
    text_surf = font.render(score_text, True, 'white')
    text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, 'white', text_rect.inflate(30, 30), width = 8, border_radius = 5)

def laser_update(laser_list, speed = 300):
    for rect in laser_list:
        rect.y -= speed * dt
        if rect.bottom < 0:
            laser_list.remove(rect)

def laser_timer(can_shoot, duration = 500):
    if not can_shoot:
        current_time = pygame.time.get_ticks()
        if current_time - shoot_time > duration:
            can_shoot = True
    return can_shoot

def meteor_update(meteor_list, speed = 400):
    for meteor_tuple in meteor_list:
        direction = meteor_tuple[1]
        meteor_rect = meteor_tuple[0]
        meteor_rect.center += direction * speed * dt
        if meteor_rect.top > WINDOW_HEIGHT:
            meteor_list.remove(meteor_tuple)

# game init
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Asteroid Shooter',)

clock = pygame.time.Clock()

game_active = False

# bg import 
bg_surf = pygame.image.load('../graphics/background.png').convert()

# ship import
ship_surf = pygame.image.load('../graphics/ship.png').convert_alpha()
ship_rect = ship_surf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

pygame.display.set_icon(ship_surf)

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

meteor_surf = pygame.image.load('../graphics/meteor.png').convert_alpha()
meteor_list = []

# meteor timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 300)

pygame.time.set_timer(pygame.USEREVENT, 1000)

# import sound
laser_sound = pygame.mixer.Sound('../sounds/laser.ogg')
laser_sound.set_volume(0.1)
explosion_sound = pygame.mixer.Sound('../sounds/explosion.wav')
explosion_sound.set_volume(0.1)
backgorund_music = pygame.mixer.Sound('../sounds/music.wav')
backgorund_music.set_volume(0.1)
backgorund_music.play(loops = -1)

while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True


        if event.type == pygame.MOUSEBUTTONDOWN and can_shoot and game_active:
            laser_rect = laser_surf.get_rect(midbottom = ship_rect.midtop)
            laser_list.append(laser_rect)

            # timer
            can_shoot = False
            shoot_time = pygame.time.get_ticks()

            # play laser sound 
            laser_sound.play()
        
        if event.type == meteor_timer and game_active:
            meteor_rect = meteor_surf.get_rect(midbottom = (randint(-100, WINDOW_WIDTH + 100), randint(-100, -50)))

            # create random direction
            direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)

            meteor_list.append((meteor_rect, direction))

    # framerate limit
    dt = clock.tick(120) / 1000

    display_surface.blit(bg_surf, (0, 0))

    if game_active:
        # mouse input
        ship_rect.center = pygame.mouse.get_pos()

        print(time.time())

        # update
        laser_update(laser_list)
        meteor_update(meteor_list)
        can_shoot = laser_timer(can_shoot)

        # meteor ship collision
        for meteor_tuple in meteor_list:
            meteor_rect = meteor_tuple[0]
            if ship_rect.colliderect(meteor_rect):
                game_active = False

        # laser meteor collision
        for meteor_tuple in meteor_list:
            meteor_rect = meteor_tuple[0]
            for laser_rect in laser_list:
                if laser_rect.colliderect(meteor_rect):
                    laser_list.remove(laser_rect)
                    meteor_list.remove(meteor_tuple)
                    explosion_sound.play()

        # drawing
        for rect in laser_list:
            display_surface.blit(laser_surf, rect)

        for meteor_tuple in meteor_list:
            display_surface.blit(meteor_surf, meteor_tuple[0])

        display_score()

        display_surface.blit(ship_surf, ship_rect)
    else:
        # drawing
        display_surface.blit(scaled_ship_surf, scaled_ship_rect)
        display_surface.blit(start_text_surf, start_text_rect)

        meteor_list.clear()
        pass

    # update display surface
    pygame.display.update()
