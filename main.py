import pygame
import time
import random
 
pygame.init()
 
white = (255, 255, 255)
grey = (255,255,200)
space_grey = (100,100,100)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0,255,0)

snake_block = 30
snake_speed = 5
 
dis_width = 30*snake_block
dis_height = 30*snake_block
 
dis = pygame.display.set_mode((dis_width+400, dis_height))
pygame.display.set_caption('Snake Game by Edureka')
 
clock = pygame.time.Clock()
 
font_style = pygame.font.SysFont(None, 30)

foody = 0
foodx = 0

width_snake = 1
arr_snake = []   

class snake:

    def __init__(self,name,color,pos,counter):
        self.name = name
        self.life = True
        self.color = color
        self.arr_snake = []
        self.arr_snake.append(pos)
        self.width_snake = 5
        self.arr_eye = [[0 for i in range(11)] for i in range(11)]
        self.purpose = True
        self.patience = 0
        self.counter = counter

 
def message(msg, color , pos=3):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width/pos, dis_height/pos])

def mymessage(msg,color,posx,posy):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [posx+900, posy])

def random_food():
    global foodx,foody
    
    #foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10
    #foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10 +10
    foody = random.randrange(0, dis_height, snake_block) 
    foodx = random.randrange(0, dis_width, snake_block) 

def snake_eye():
    arr = [[0 for i in range(11)] for i in range(11)]
    print(arr)
    return arr
 
def gameLoop():  # creating a function
    global foodx,foody,width_snake

    game_over = False
    game_close = False
 
    x1 = dis_width / 2
    y1 = dis_height / 2
 
    x1_change = 0
    y1_change = 0
 
    
    while not game_over:
 
        while game_close == True:
            dis.fill(white)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
 
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                game_over = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_SPACE:
                    y1_change = 0
                    x1_change = 0
 
        # if neuro.controll == True:
        #     if neuro.controll == "left":
        #         x1_change = -snake_block
        #         y1_change = 0
        #     elif neuro.controll == "right":
        #         x1_change = snake_block
        #         y1_change = 0
        #     elif neuro.controll == "up":
        #         y1_change = -snake_block
        #         x1_change = 0
        #     elif neuro.controll == "down":
        #         y1_change = snake_block
        #         x1_change = 0         
 
     
        # телепортация
        if x1 > dis_width-snake_block*2  or x1 < 0 or y1 > dis_height-snake_block*2  or y1 < 0:
            #game_close = True
            print("работает")

            if x1 > dis_width-snake_block:
                x1 = 0

            if x1 < 0 :
                x1 = dis_width

            if y1 > dis_height-snake_block:
                y1 = 0

            if y1 < 0 :
                y1 = dis_height
         
        #for i in range(len(arr_snake)):
        arr_snake.insert(0,[x1,y1])
        
        if len(arr_snake) > width_snake:
            del arr_snake[-1]
         
        x1 += x1_change
        y1 += y1_change

        # Главный рендер игры
        dis.fill(grey)
        pygame.draw.rect(dis, white, [0, 0, dis_width, dis_height])
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
               
        for i in range(len(arr_snake)):
            pygame.draw.rect(dis, space_grey, [arr_snake[i][0], arr_snake[i][1], snake_block, snake_block])
        
        pygame.draw.rect(dis, red, [x1, y1, snake_block, snake_block])
        
        # рендер надписей
        mymessage("еда: "+str(foodx)+" "+str(foody), black, 10,10)
        mymessage("голова: "+str(x1)+" "+str(y1), black, 10,30)

        # рендер зрения
        eye_snake = snake_eye()
        for i in range(len(eye_snake)):
            for k in range(len(eye_snake[i])):
                
                pygame.draw.rect(dis, white, [910+(snake_block*k), 70+(snake_block*i), snake_block, snake_block])
                pygame.draw.rect(dis, black, [910+(snake_block*k), 70+(snake_block*i), snake_block, snake_block],1)

        # Главный рендер
        pygame.display.update()
        
        # проверка на еду    
        if x1 == foodx and y1 == foody:
            print("Yummy!!")
            random_food()
            width_snake += 1           
 
        clock.tick(snake_speed)
 
    pygame.quit()
    quit()


snake_eye()
random_food() 
gameLoop()