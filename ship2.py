import pygame, os, pyautogui, random
pygame.font.init()
pygame.mixer.init() #mixer is used for sound
print(pyautogui.size())
WIDTH, HEIGHT = pyautogui.size()
sw, sh = WIDTH // 12, HEIGHT // 12
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ship shooting")

#loading the sound
# bullethitsound = pygame.mixer.music.load("Grenade+1.mp3")
# bullethitsound2 = pygame.mixer.music.load("Grenade+2.mp3") 
bsound1 = pygame.mixer.Sound("Grenade+1.mp3")
bsound2 = pygame.mixer.Sound("Grenade+2.mp3")
bsound1.set_volume(0.3)
bsound2.set_volume(0.3)
sound = pygame.mixer.find_channel()
# bulletsound = pygame.mixer.music.set_volume(0.5)
# bulletsound2 = pygame.mixer.music.set_volume(0.5)
bg = pygame.image.load("bg.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
yship = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("images\ship22.png"),(sw, sh)),-180)
rship = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("images\ship11.png"),(sw, sh)),90)
BORDER = pygame.Rect(WIDTH / 2 - 50, 0, 20, HEIGHT)
speed = 20
print(pygame.USEREVENT)
RED_hit = pygame.USEREVENT + 1
YELLOW_hit = pygame.USEREVENT + 2
font1 = pygame.font.SysFont("Arial", 30)
font2 = pygame.font.SysFont("Arial", 60)
gamestate = "start"


def red_movement(keypressed,red):
    if keypressed [pygame.K_LEFT] and red.x > BORDER.x + BORDER.width:
        red.x -= speed
    if keypressed [pygame.K_RIGHT] and red.x + sh < WIDTH :
        red.x += speed  
    if keypressed [pygame.K_DOWN] and red.y + sw < HEIGHT:
        red.y += speed
    if keypressed [pygame.K_UP] and red.y > 0 :
        red.y -= speed   

def yel_movement(keypressed,yel):
    if keypressed [pygame.K_a] and yel.x > 0:
        yel.x -= speed
    if keypressed [pygame.K_d] and yel.x + sh < BORDER.x :
        yel.x += speed  
    if keypressed [pygame.K_s] and yel.y + sw < HEIGHT:
        yel.y += speed
    if keypressed [pygame.K_w] and yel.y > 0 :
        yel.y -= speed   
        
def handle_bullets(rbullet, ybullet, RED, YELLOW):
    for b in rbullet:
        b.x -= 10
        if b.x < 0:
            rbullet.remove(b)
        if b.colliderect(YELLOW):
            pygame.event.post(pygame.event.Event(YELLOW_hit))
            rbullet.remove(b)
        for y in ybullet:
            if y.colliderect(b):
                ybullet.remove(y)
                rbullet.remove(b)
    for y in ybullet:
        y.x += 10
        if y.x > WIDTH:
            ybullet.remove(y)
        if y.colliderect(RED):
            pygame.event.post(pygame.event.Event(RED_hit))
            ybullet.remove(y)
        



def draw_screen(RED, YELLOW, rbullet, ybullet, rscore, yscore, winner):
    screen.blit(bg, (0,0))
    screen.blit(yship, (YELLOW.x, YELLOW.y ))
    screen.blit(rship, (RED.x, RED.y))
    pygame.draw.rect(screen, "black", BORDER)
    for i in rbullet:
        pygame.draw.rect(screen, "red", i)
    # pygame.draw.rect(screen, "red", RED)
    # pygame.draw.rect(screen, "yellow", YELLOW)
    for i in ybullet:
        pygame.draw.rect(screen, "yellow", i)
    
    rtext = font1.render("score:"+ str(rscore), 1, "white")
    screen.blit(rtext,(WIDTH - 120,20))
    ytext = font1.render("score:"+ str(yscore), 1, "white")
    screen.blit(ytext,(20,20))
    if gamestate == "start":
        stext = font1.render("use the arrow keys ⬅️⬆️⬇️➡️ for the red ship (right) and wasd ⌨️ for the yellow ship (left).", 1, "white")
        stext2 = font1.render("press right shift key to shoot ☄️ , the left ship is autoshooting.", 1, "white")
        stext3 = font1.render("to get the score, you must hit 💥 the other ship.", 1, "white")
        stext4 = font1.render("press space to start ⭐", 1, "white")
        screen.blit(stext, (WIDTH / 3, HEIGHT / 3))
        screen.blit(stext2, (WIDTH / 3, HEIGHT / 3 + 100))
        screen.blit(stext3, (WIDTH / 3, HEIGHT / 3 + 200))
        screen.blit(stext4, (WIDTH / 3, HEIGHT / 3 + 300))
    if gamestate == "end":
        etext = font1.render("game over 🙂 press start to play again", 1, "white")
        wtext = font1.render("winner=" + winner, 1, "white")
        screen.blit(wtext, (WIDTH /3, HEIGHT /3))
        screen.blit(etext, (WIDTH /3, HEIGHT /3 - 100))
    pygame.display.update()
    
def main():
    RED = pygame.Rect(WIDTH - 200, HEIGHT / 2, sh, sw)
    YELLOW = pygame.Rect(50, HEIGHT / 2, sh, sw)
    rbullet = []
    ybullet = []
    rscore = 0
    yscore = 0
    winner = ""
    run = True
    while run:
        for e in pygame.event.get():
            global gamestate
            if e.type == pygame.QUIT:
                pygame.quit()
                run = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RSHIFT and gamestate == "play":
                    b = pygame.Rect(RED.x, RED.y + RED.height / 2, 20, 10)
                    rbullet.append(b)
                    # bullethitsound2.play()
                    sound.play(bsound2)
                if e.key == pygame.K_SPACE:
                    gamestate = "play"
                    rscore = 0
                    yscore = 0
                    winner = ""
                    rbullet = []
                    ybullet = []
                    RED.x, RED.y = WIDTH - 200, HEIGHT / 2
                    YELLOW.x, YELLOW.y = 50, HEIGHT / 2
                
                    
            if e.type == RED_hit:
                sound.play(bsound1)
                yscore += 1  
            if e.type == YELLOW_hit:
                sound.play(bsound2)
                rscore += 1 
        if gamestate == "play":
            if random.randint(1,50) < 3:
                b = pygame.Rect(YELLOW.x + YELLOW.width, YELLOW.y + YELLOW.height / 2, 20, 10)
                ybullet.append(b)
                # bullethitsound.play()
            
            if rscore >= 10:
                winner = "red player wins!"
            if yscore >= 10:
                winner = "yellow player wins!"
            if winner:
                gamestate = "end"
            # print(len(rbullet))
            keypressed = pygame.key.get_pressed()  
            red_movement(keypressed, RED)
            yel_movement(keypressed, YELLOW)
            handle_bullets(rbullet, ybullet, RED, YELLOW)
            
        draw_screen(RED, YELLOW, rbullet, ybullet, rscore, yscore, winner)  
main()