import sys, pygame, random

class Breakout():
   
    def main(self):
          
        xspeed = 3
        yspeed = 3
        max_lives = 5
        bat_speed = 20      
        score = 0 
        bgcolour = 0x2F, 0x4F, 0x4F  # darkslategrey        
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

        # Initialise ready for game loop
        batrect = batrect.move((width / 2) - (batrect.right / 2), height - 20)
        ballrect = ballrect.move(width / 2, height / 2)       
        lives = max_lives
        clock = pygame.time.Clock()
        pygame.key.set_repeat(1,30)       
        pygame.mouse.set_visible(0)       # turn off mouse pointer

        while True:

            # 60 frames per second
            clock.tick(60)

            # process key presses
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
        	            sys.exit()
                    if event.key == pygame.K_LEFT:                        
                        batrect = batrect.move(-bat_speed, 0)     
                        if (batrect.left < 0):                           
                            batrect.left = 0      
                    if event.key == pygame.K_RIGHT:                    
                        batrect = batrect.move(bat_speed, 0)
                        if (batrect.right > width):                            
                            batrect.right = width

            # check if bat has hit ball    
            if ballrect.bottom >= batrect.top and ballrect.bottom <= batrect.bottom and ballrect.right >= batrect.left and ballrect.left <= batrect.right:
                yspeed = -yspeed                
                               

            # move bat/ball
            ballrect = ballrect.move(xspeed, yspeed)        #muove con la velocità
            if ballrect.left < 0 or ballrect.right > width:
                xspeed = -xspeed        #modifica la velocità x facendola rimbalzare                       
            if ballrect.top < 0:
                yspeed = -yspeed        #modifica la velocità y facendola rimbalzare               
         

            # check if ball has gone past bat - lose a life
            if ballrect.top > height:
                lives -= 1
                # start a new ball
                rand = random.random()                
                if random.random() > 0.5:
                    xspeed = -xspeed           
                ballrect.center = width * random.random(), height / 3        #centro della palla                        
                if lives == 0:     #se vite == 0              
                    msg = pygame.font.Font(None,70).render("Game Over", True, (0,255,255), bgcolour)       #messaggio a fine gioco
                    msgrect = msg.get_rect()
                    msgrect = msgrect.move(width / 2 - (msgrect.center[0]), height / 3)
                    screen.blit(msg, msgrect)
                    pygame.display.flip()


                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                    	            sys.exit()
                                                                

            
            if xspeed < 0 and ballrect.left < 0:
                xspeed = -xspeed                                
               

            if xspeed > 0 and ballrect.right > width:
                xspeed = -xspeed                               

           
            # check if ball has hit wall
            # if yes yhen delete brick and change ball direction
            index = ballrect.collidelist(wall.brickrect)       #controllo collisione con mattone
            if index != -1: 
                if ballrect.center[0] > wall.brickrect[index].right or \
                   ballrect.center[0] < wall.brickrect[index].left:     #controllo collisione e modifica rimbalzo
                    xspeed = -xspeed
                else:
                    yspeed = -yspeed                
          
                wall.brickrect[index:index + 1] = []
                score += 10     #score + 10
            


            #testo per punteggio
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

            # if wall completely gone then rebuild it
            if wall.brickrect == []:              
                wall.build_wall(width)    #ricostruzione muro                           
                ballrect.center = width / 2, height / 3     
         
            screen.blit(ball, ballrect)
            screen.blit(bat, batrect)
            pygame.display.flip()

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

if __name__ == '__main__':
    br = Breakout()
    br.main()