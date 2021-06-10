import sys, pygame, random
import serial, time
import threading, queue
import time

q = queue.Queue()

GAME_OVER = pygame.image.load('gameOver.png')
GAME_OVER = pygame.transform.scale(GAME_OVER,(350, 350))
WIN = pygame.image.load('vittoria.png')
WIN = pygame.transform.scale(WIN ,(380, 327))

class Read_Microbit(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._running = True
      
    def terminate(self):
        self._running = False
        
    def run(self):
        #serial config
        port = "COM15"
        s = serial.Serial(port)
        s.baudrate = 115200
        while self._running:
            data = s.readline().decode() 
            acc = [float(x) for x in data[1:-3].split(",")]
            q.put(acc)
            time.sleep(0.01)


class Wall():

    def __init__(self):
        self.brick = pygame.image.load("brick.png")   #immagine mattone
        brickrect = self.brick.get_rect()
        self.bricklength = brickrect.right - brickrect.left       #lunghezza e altezza del mattone
        self.brickheight = brickrect.bottom - brickrect.top             

    def build_wall(self, width):        #funzione per costruire muro
        xpos = 0
        ypos = 60
        adj = 0
        self.brickrect = []
        for i in range (0, 52):       #52 numero di mattoni nel muro    
            if xpos > width:
                if adj == 0:
                    adj = self.bricklength / 2
                else:
                    adj = 0
                xpos = -adj
                ypos += self.brickheight
                
            self.brickrect.append(self.brick.get_rect())    
            self.brickrect[i] = self.brickrect[i].move(xpos, ypos)
            xpos = xpos + self.bricklength



def main():
        
    xspeed = 4
    yspeed = 4
    max_lives = 5
    bat_speed = 10  
    score = 0 
    bgcolour = 0x2F, 0x4F, 0x4F 
    size = width, height = 640, 480

    pygame.init()            
    screen = pygame.display.set_mode(size)
    #screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

    bat = pygame.image.load("bat.png")        #carica l'immagine della paletta
    batrect = bat.get_rect()

    ball = pygame.image.load("ball.png")      #carica l'immagine della pallina
    ball.set_colorkey((255, 255, 255))  
    ballrect = ball.get_rect()
    

    
    wall = Wall()       #muro da distruggere
    wall.build_wall(width)      #costruzione muro

    batrect = batrect.move((width / 2) - (batrect.right / 2), height - 20)
    ballrect = ballrect.move(width / 2, height / 2)       
    lives = max_lives
    clock = pygame.time.Clock()
    #pygame.key.set_repeat(1,30)      nn dovrebbe servire cancellare   
    pygame.mouse.set_visible(0)

    while True:

        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rm.terminate()
                rm.join()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    rm.terminate()
                    rm.join()
                    pygame.quit()
                    sys.exit()

        acc = q.get()
        
        if (acc[0] < -200):        #se microbit è inclinato a sinistra la piattaforma va a sinistra e viceversa
            batrect = batrect.move(-bat_speed, 0)
            screen.blit(bat, batrect)
        elif (acc[0] > 200):
            batrect = batrect.move(+bat_speed, 0)
            screen.blit(bat, batrect)
        q.task_done()

        
        
        if (batrect.left < 0):                           
            batrect.left = 0
        if (batrect.right > 640):
            batrect.right = 640

        #se la palla ha toccato la piattaforma la fa rimbalzare    
        if ballrect.bottom >= batrect.top and ballrect.bottom <= batrect.bottom and ballrect.right >= batrect.left and ballrect.left <= batrect.right:
            yspeed = -yspeed                
            

        ballrect = ballrect.move(xspeed, yspeed)        #muove con la velocità
        if ballrect.left < 0 or ballrect.right > width:
            xspeed = -xspeed        #modifica la velocità x facendola rimbalzare                       
        if ballrect.top < 0:
            yspeed = -yspeed        #modifica la velocità y facendola rimbalzare               
        

        if ballrect.top > height:
            lives -= 1
            
            rand = random.random()                
            if random.random() > 0.5:
                xspeed = -xspeed           
            ballrect.center = width * random.random(), height / 3        #centro della palla                        
            if lives == 0:             
                screen.fill(bgcolour)
                screen.blit(GAME_OVER, (145, 50))
                fnt_score = pygame.font.SysFont("Forte", 40)
                surf_txt_score = fnt_score.render("Score: " + str(score), True, (0,255,255))
                screen.blit(surf_txt_score, (260, 420))
                pygame.display.flip()


                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            rm.terminate()
                            rm.join()
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                rm.terminate()
                                rm.join()
                                pygame.quit()
                                sys.exit()
                                  
        
        if xspeed < 0 and ballrect.left < 0:
            xspeed = -xspeed                                
            

        if xspeed > 0 and ballrect.right > width:
            xspeed = -xspeed                               

        
        
        index = ballrect.collidelist(wall.brickrect)       #controllo collisione con mattone
        if index != -1: 
            print(abs(xspeed))
            if score == 100:
                xspeed = abs(xspeed) + 0.5
                yspeed = abs(yspeed) + 0.5
            elif score == 200:
                xspeed = abs(xspeed) + 0.5
                yspeed = abs(yspeed) + 0.5
            elif score == 300:
                xspeed = abs(xspeed) + 0.5
                yspeed = abs(yspeed) + 0.5
            elif score == 400:
                xspeed = abs(xspeed) + 0.5
                yspeed = abs(yspeed) + 0.5

            if ballrect.center[0] > wall.brickrect[index].right or \
                ballrect.center[0] < wall.brickrect[index].left:     #controllo collisione e modifica rimbalzo

                xspeed = -xspeed
            else:
                yspeed = -yspeed                
        
            wall.brickrect[index:index + 1] = []
            score += 10     #score + 10
                        
        #stampa punteggio
        screen.fill(bgcolour)
        fnt_score = pygame.font.SysFont("Forte", 30)
        surf_txt_score = fnt_score.render("Score: " + str(score), True, (0,255,255))
        screen.blit(surf_txt_score, (500, 10))

        #stampa vite
        fnt_lives = pygame.font.SysFont("Forte", 30)
        surf_txt_lives = fnt_lives.render("Lives: " + str(lives), True, (0,255,255))
        screen.blit(surf_txt_lives, (20, 10))

        for i in range(0, len(wall.brickrect)):
            screen.blit(wall.brick, wall.brickrect[i])    

        #se il muro è vuoto si vince
        if wall.brickrect == []:              
            screen.fill(bgcolour)
            screen.blit(WIN, (130, 50))
            fnt_score = pygame.font.SysFont("Forte", 40)
            surf_txt_score = fnt_score.render("Score: " + str(score), True, (0,255,255))
            screen.blit(surf_txt_score, (260, 390))
            pygame.display.flip()
            
            while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            rm.terminate()
                            rm.join()
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                rm.terminate()
                                rm.join()
                                pygame.quit()
                                sys.exit()
        
        screen.blit(ball, ballrect)
        screen.blit(bat, batrect)
        pygame.display.flip()





if __name__ == '__main__':
    rm = Read_Microbit()
    rm.start()
    pygame.init()
    main()
    