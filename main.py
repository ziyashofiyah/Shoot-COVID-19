import pygame
from pygame.locals import *
import math
from random import randint


# INISIALISASI
pygame.init()
running = True
#Ukuran Background
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("SHOOT COVID-19")
icon = pygame.image.load('assets/virus11.png').convert_alpha()
pygame.display.set_icon(icon)
#posisi shooter
shooterpos = [100, 100]
#score
score = 0 
panahan = []
#keyboard arah shooter
keys = {
    "top": False, 
    "bottom": False,
    "left": False,
    "right": False 
}
#inisialisasi virus
virus_timer = 200 # waktu kemunculan tiap 0,2 detik
viruses = [[width, 100]] # list yang menampung koordinat musuh
#inisialisasi nyawa
health_point = 194 
countdown_timer = 90000 
#inisialisasi game over
exitcode = 0
EXIT_CODE_GAME_OVER = 0
EXIT_CODE_WIN = 1
#inisialisasi font
game_font = pygame.font.Font('04B_19.ttf',20)


#FUNCTION
def background_display():
    for x in range(int(width/background.get_width()+1)):
        for y in range(int(height/background.get_height()+1)):
            screen.blit(background, (x*100, y*100))

def mouse_button():
    global angle, new_playerpos
    mouse_position = pygame.mouse.get_pos()
    angle = math.atan2(mouse_position[1] - (shooterpos[1]+32), mouse_position[0] - (shooterpos[0]+26))
    player_rotation = pygame.transform.rotate(shooter, 360 - angle * 57.29)
    new_playerpos = (shooterpos[0] - player_rotation.get_rect().width / 2, shooterpos[1] - player_rotation.get_rect().height / 2)
    screen.blit(player_rotation, new_playerpos)

def bullet_display ():
     for bullet in panahan:
        panah_index = 0
        velx=math.cos(bullet[0])*10
        vely=math.sin(bullet[0])*10
        bullet[1]+=velx
        bullet[2]+=vely
        if bullet[1] < -64 or bullet[1] > width or bullet[2] < -64 or bullet[2] > height:
            panahan.pop(panah_index)
        panah_index += 1
        # draw the arrow
        for projectile in panahan:
            new_arrow = pygame.transform.rotate(panah, 360-projectile[0]*57.29)
            screen.blit(new_arrow, (projectile[1], projectile[2]))
  
def score_display():
	if running:
		score_surface = game_font.render(f'Score: {int(score)}' ,True,(255,255,255))
		score_rect = score_surface.get_rect(center = (320,30))
		screen.blit(score_surface,score_rect)
	else:
		score_surface = game_font.render(f'Score: {int(score)}' ,True,(255,255,255))
		score_rect = score_surface.get_rect(center = (320,30))
		screen.blit(score_surface,score_rect)


# ASSETS GAME
#gambar background
background = pygame.image.load('assets/grass.png')
#gambar shooter
shooter = pygame.image.load('assets/shooter.png').convert_alpha()
#gambar obat
obat = pygame.image.load('assets/Obat.png').convert_alpha()
obat = pygame.transform.scale(obat,(80,80))
#gambar panah
panah = pygame.image.load("assets/bullet.png").convert_alpha()
#gambar virus
virus_img = pygame.image.load("assets/virus.png")
#gambar nyawa
healthbar = pygame.image.load("assets/healthbar.png")
health = pygame.image.load("assets/health.png")
#display game over
gameover = pygame.image.load("assets/gameover.png")
youwin = pygame.image.load("assets/youwin.png")


#Looping Utama
while(running):
    background_display()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: clicked = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            panahan.append([angle, new_playerpos[0]+32, new_playerpos[1]+32])
        #keyboad untuk menggerakan shooter
        if event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                keys["top"] = True
            elif event.key == K_LEFT:
                keys["left"] = True
            elif event.key == K_DOWN:
                keys["bottom"] = True
            elif event.key == K_RIGHT:
                keys["right"] = True
        if event.type == pygame.KEYUP:
            if event.key == K_UP:
                keys["top"] = False
            elif event.key == K_LEFT:
                keys["left"] = False
            elif event.key == K_DOWN:
                keys["bottom"] = False
            elif event.key == K_RIGHT:
                keys["right"] = False

    screen.blit(obat, (5, 20))
    screen.blit(obat, (5, 140))
    screen.blit(obat, (5, 260))
    screen.blit(obat, (5, 380))
    
    mouse_button()
    bullet_display()
    
    #waktu musuh muncul
    virus_timer -= 1
    if virus_timer == 0:
        # buat musuh baru
        viruses.append([width, randint(50, height-32)])
        # waktu keluar virus random
        virus_timer = randint(1, 100)
    index = 0
    for virus in viruses:
        # musuh bergerak dengan kecepatan 5 pixel ke kiri
        virus[0] -= 5
        # hapus musuh saat mencapai batas layar sebelah kiri
        if virus[0] < -64:
            viruses.pop(index)
        #collition antara obat dan virus
        virus_rect = pygame.Rect(virus_img.get_rect())
        virus_rect.top = virus[1] # ambil titik y 
        virus_rect.left = virus[0] # ambil titik x
        # benturan virus dengan obat
        if virus_rect.left < 64:
            viruses.pop(index)
            health_point -= randint(5,20)
        index_panah = 0
        for bullet in panahan:
            bullet_rect = pygame.Rect(panah.get_rect())
            bullet_rect.left = bullet[1]
            bullet_rect.top = bullet[2]
            # benturan anak panah dengan virus
            if virus_rect.colliderect(bullet_rect):
                score += 1
                viruses.pop(index)
                panahan.pop(index_panah)
            index_panah += 1
        index += 1
    #gambar virus ke layar
    for virus in viruses:
        screen.blit(virus_img, virus)
        
    #gambar nyawa
    screen.blit(healthbar, (5,5))
    for hp in range(health_point):
        screen.blit(health, (hp+8, 8))

    # 6.4 - Draw clock
    minutes = int((countdown_timer-pygame.time.get_ticks())/60000) # 60000 itu sama dengan 60 detik
    seconds = int((countdown_timer-pygame.time.get_ticks())/1000%60)
    time_text = "{:02}:{:02}".format(minutes, seconds)
    clock = game_font.render(time_text, True, (255,255,255))
    textRect = clock.get_rect()
    textRect.topright = [635, 5]
    screen.blit(clock, textRect)

    score_display()
    pygame.display.update()

    #arah pergerakan shooter
    if keys["top"]:
        shooterpos[1] -= 5 # kurangi nilai y
    elif keys["bottom"]:
        shooterpos[1] += 5 # tambah nilai y 
    if keys["left"]:
        shooterpos[0] -= 5 # kurangi nilai x
    elif keys["right"]:
        shooterpos[0] += 5 # tambah nilai x

    #game over
    if pygame.time.get_ticks() > countdown_timer:
        running = False
        exitcode = EXIT_CODE_WIN
    if health_point <= 0:
        running = False
        exitcode = EXIT_CODE_GAME_OVER

#menang atau kalah
if exitcode == EXIT_CODE_GAME_OVER:
    screen.blit(gameover, (0, 0))
else:
    screen.blit(youwin, (0, 0))

# Tampilkan score
text = game_font.render("Score: {}".format(score), True, (255, 255, 255))
textRect = text.get_rect()
textRect.centerx = screen.get_rect().centerx
textRect.centery = screen.get_rect().centery + 24
screen.blit(text, textRect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.update()
