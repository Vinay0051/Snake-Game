import pygame
import random
import os
pygame.mixer.init()

pygame.init()

#colors 
# grey=(233,210,229)
white=(255,255,255)
grey=(80,80,80)
green=(0,255,0)
blue=(0,0,255)

#creating window
screen_width=800
screen_height=500
gamewindow=pygame.display.set_mode((screen_width, screen_height))

#welcome image
wlimg=pygame.image.load("wel2.jpg")
wlimg = pygame.transform.scale(wlimg,(screen_width,screen_height)).convert_alpha()

# # background image
# bgimg=pygame.image.load("back.jpg")
# bgimg = pygame.transform.scale(bgimg,(screen_width,screen_height)).convert_alpha()

# game over image
gvimg=pygame.image.load("gameover.webp")
gvimg = pygame.transform.scale(gvimg,(screen_width,screen_height)).convert_alpha()


#game title
pygame.display.set_caption("Snake Game")
pygame.display.update()



clock=pygame.time.Clock()
font=pygame.font.SysFont(None,55)




def text_screen(text,color,x,y):
    screen_text= font.render(text,True,color)
    gamewindow.blit(screen_text,[x,y])

def plot_snake(gamewindow,color,snk_list,snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gamewindow,color,[x,y,snake_size,snake_size])

def welcome():
    exit_game = False
    while not exit_game :
        #background color
        gamewindow.fill(grey)
        gamewindow.blit(wlimg,(0,0))
        #title and instructions
        text_screen('Welcome To Snake Game', blue ,40,160 )
        text_screen('Press SpaceBar To Play', blue , 60,200 )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    pygame.mixer.music.load('back.mp3')
                    pygame.mixer.music.play()
                    gameloop()

        pygame.display.update()
        clock.tick(60)

# game loop
def gameloop():

    # game specific variables
    exit_game=False
    game_over=False
    snake_x=45
    velocity_x=0
    velocity_y=0
    snake_y=45

    score=0
    init_velocity=5

    food_x=random.randint(20,screen_width/2)
    food_y=random.randint(20,screen_height/2)

    snake_size=20
    fps=60
    snk_list=[]
    snk_length=1

    #check if highscore file exists
    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt","w") as f:
            f.write("0");
    with open("highscore.txt","r") as f:
        highscore=f.read()

    while not exit_game:
        if game_over:
            with open("highscore.txt","w") as f:
                f.write(str(highscore))
            gamewindow.fill(white)
            gamewindow.blit(gvimg,(0,0))
            text_screen("Press Enter To Continue",green,170,450)
            
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game=True
                if event.type==pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN :
                        welcome()
        else:    
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game=True 
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RIGHT or event.key==pygame.K_d:
                        velocity_x=init_velocity
                        velocity_y=0

                    if event.key==pygame.K_LEFT or event.key==pygame.K_a:
                        velocity_x= - init_velocity
                        velocity_y=0
                    
                    if event.key==pygame.K_UP or event.key==pygame.K_w:
                        velocity_y= - init_velocity
                        velocity_x=0
                    
                    if event.key==pygame.K_DOWN or event.key==pygame.K_s:
                        velocity_y=init_velocity
                        velocity_x=0

                    if event.key==pygame.K_q:
                        score+=50

            snake_x+=velocity_x
            snake_y+=velocity_y

            if abs(snake_x-food_x)<15 and abs(snake_y-food_y)<15:
                score+=10
                pygame.mixer.music.load('point.mp3')
                pygame.mixer.music.play()
                food_x=random.randint(20,screen_width/2)
                food_y=random.randint(20,screen_height/2)
                snk_length+=5
                if score>int(highscore):
                    highscore = score

            gamewindow.fill(grey)
            # gamewindow.blit(bgimg,(0,0))
            text_screen("Score: "+str(score)+"  High Score: "+str(highscore),white,5,5)
            pygame.draw.rect(gamewindow,green,[food_x,food_y,snake_size,snake_size])
            
            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)
            
            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over=True
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over=True
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()

            plot_snake(gamewindow,blue,snk_list,snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

pygame.mixer.music.load('welcome.mp3')
pygame.mixer.music.play()
welcome()