import pygame
import time
import random

pygame.init()

dis = pygame.display.set_mode((900,620))
pygame.display.set_caption('Умная змейка')

clock = pygame.time.Clock()

#font_style = pygame.font.SysFont(None,30)

block = 10

row = 60
col = 60

arr_world = [['0' for i in range(col)] for i in range(row)]
arr_food = [['0' for i in range(col)] for i in range(row)]
arr_wall = [['0' for i in range(col)] for i in range(row)]


#рисуем рамки мира

for row_wall in range(len(arr_wall)):
	for col_wall in range(len(arr_wall[row_wall])):
		if row_wall <= 0 or row_wall >= row-1 :
			arr_wall[row_wall][col_wall] = '2'
		else:
			if col_wall <= 0 or col_wall >= col-1:
				arr_wall[row_wall][col_wall] = '2'	

arr_eye = [[0 for i in range(11)] for i in range(11)]
arr_mouse = [[0 for i in range(11)] for i in range(11)]
arr_neuro = [[0 for i in range(11)] for i in range(11)]


# Все для змей
width_snake_1 = 3
width_snake_2 = 3
arr_snake_1 =[]
arr_snake_2 =[]

arr_eye_snake_1 = [[0 for i in range(11)] for i in range(11)]
arr_eye_snake_2 = [[0 for i in range(11)] for i in range(11)]
#print(arr_world)

speed_world = 5

white = (255,255,255)
grey = (200,200,200)
space_gray = (150,150,150)
red = (255,0,0)
green = (0,255,0)
purpur = (255,0,255)
black=(0,0,0)

font_size = 10
font_style = pygame.font.SysFont(None, font_size)

font_style_2 = pygame.font.SysFont(None, 20)

tmp_arr =[] 


with open('neuro_bez_d_2.csv','rb') as f:
    data = f.read()
    arr_tmp = str(data).split('\\r\\n')
    for i in range(len(arr_tmp)):
    	line = arr_tmp[i].split(';')
    	tmp_arr.append(line)

tmp_arr[0][0]= tmp_arr[0][0].split("'")[1]

neuro = tmp_arr.copy()

tmp_arr.clear()

with open('neuro_wall.csv','rb') as f:
    data = f.read()
    arr_tmp = str(data).split('\\r\\n')
    for i in range(len(arr_tmp)):
    	line = arr_tmp[i].split(';')
    	tmp_arr.append(line)

tmp_arr[0][0]= tmp_arr[0][0].split("'")[1]

neuro_wall = tmp_arr.copy()


last_go = 0

x1_old = 0
y1_old = 0
time_step = 0


all_snake_arr = []

class Snake:

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

	def breath(self,arr_eye,auto_pilot,x1,y1,x1_change,y1_change):
		#self.arr_snake

		#print(self.name)
		# Автопилот
		if auto_pilot == True:

			out = brain(self.arr_eye,self.purpose,self.patience)

			if out == 'left':
			    x1_change = -1
			    y1_change = 0
			elif out == 'right':
			    x1_change = 1
			    y1_change = 0
			elif out == 'up':
			    y1_change = -1
			    x1_change = 0
			elif out == 'down':
			    y1_change = 1
			    x1_change = 0

		if self.life != False : 
			# Движуха змеии
			x1 = self.arr_snake[0][0]
			y1 = self.arr_snake[0][1]

			if x1 > col:		
				x1 = 0

			if x1 < 0 :		
				x1 = col-2

			if y1 > row:		
				y1 = 0

			if y1 < 0 :		
				y1 = row-2		
				
			
			x1 += x1_change
			y1 += y1_change
			
			self.arr_snake.insert(0,[x1,y1])
				
				
			#print(str(x1)+' '+str(y1))        
			self.snake_eye(x1*block,y1*block)

			if len(self.arr_snake) > self.width_snake:
				arr_wall[self.arr_snake[-1][1]][self.arr_snake[-1][0]] = '0'
				del self.arr_snake[-1]

			# if self.width_snake > 6:
			# 	self.width_snake=6

			#all_snake_arr.append(self.arr_snake)

			#print(self.name+' - '+str(self.width_snake))
			
		
		# проверка на съедение
		for row_food in range(len(arr_food)):
			for col_food in range(len(arr_food[row_food])):

				# Проверка на еду
				if self.arr_snake[0][1] == row_food and self.arr_snake[0][0] == col_food and arr_food[row_food][col_food] == '1':
					#print("ням ням!!")
					random_food()
					arr_food[row_food][col_food] = '0'
					self.width_snake += 1

				# Проверка на стену
				if self.arr_snake[0][1] == row_food and self.arr_snake[0][0] == col_food and arr_wall[row_food][col_food] == '2':
					self.life = False

				# if [self.arr_snake[0][1],self.arr_snake[0][0]] == all_snake_arr[i][k]:
				# 	self.life = False

				# if [self.arr_snake[0][1],self.arr_snake[0][0]] in [element for a_list in all_snake_arr for element in a_list]:
				# 	print('True')

		arr_wall[int(y1)][int(x1)] = '2'

	def snake_eye(self,x,y):
		block = 10

		arr = self.arr_eye

		for row in range(len(arr)):
			for col in range(len(arr[row])):


				#print(self.arr_snake.index([row,col]))
				try:
					arr[row][col] = arr_food[round(y/block)+row-5][round(x/block)+col-5]
					
					if arr_wall[round(y/block)+row-5][round(x/block)+col-5] != '0':
						arr[row][col] = arr_wall[round(y/block)+row-5][round(x/block)+col-5]

				except:
					arr[row][col] = '-1'

				for i in range(len(all_snake_arr)):
					try:					
						index = all_snake_arr[i].index([round(x/block)+col-5,round(y/block)+row-5]) 

						
						# #print(arr[5][5])
						# if arr[5][5] == '2':
						# 	self.life = False

						if index != 0:
							arr[row][col] = '2'
						
						
						# print('work')
					except:
						pass

	def render(self,dis):

		add_text_2(self.name+' - '+str(self.width_snake),self.color,self.counter[0],self.counter[1])

		for i in range(len(self.arr_snake)):
			if self.life != False:
				pygame.draw.rect(dis,self.color,[block*self.arr_snake[i][0],block*self.arr_snake[i][1],block,block])
			else:
				pygame.draw.rect(dis,grey,[block*self.arr_snake[i][0],block*self.arr_snake[i][1],block,block])

	def render_eye(self,x,y,block,neuro=None):

		#render_eye2(arr_eye_snake_1,620,20,25,neuro)

		for r in range(len(self.arr_eye)):
			for c in range(len(self.arr_eye[r])):
				pygame.draw.rect(dis,white,[block*c+x,block*r+y,block,block])

				if self.arr_eye[r][c] == '1':
					pygame.draw.rect(dis,green,[block*c+x,block*r+y,block,block])

				if self.arr_eye[r][c] == '2':
					pygame.draw.rect(dis,space_gray,[block*c+x,block*r+y,block,block])

				if self.arr_eye[r][c] == '-1':
					pygame.draw.rect(dis,purpur,[block*c+x,block*r+y,block,block])

				if neuro != None:
					neurons = neuro[r][c].split(',')

					add_text(str(neurons[0]),black,block*c+x+11,block*r+y+3)
					add_text(str(neurons[1]),black,block*c+x+11,block*r+y+18)
					add_text(str(neurons[2]),black,block*c+x+3,block*r+y+11)
					add_text(str(neurons[3]),black,block*c+x+18,block*r+y+11)
				
				pygame.draw.rect(dis,grey,[block*c+x,block*r+y,block,block],1)

				

		pygame.draw.rect(dis,self.color,[block*5+x,block*5+y,block,block])



def add_text(msg,color,posx,posy):	
	mesg = font_style.render(msg, True, color)
	dis.blit(mesg, [posx, posy])

def add_text_2(msg,color,posx,posy):	
	mesg = font_style_2.render(msg, True, color)
	dis.blit(mesg, [posx, posy])

def random_food():
	row_food = random.randrange(6,row-4)
	col_food = random.randrange(6,col-4)

	arr_food[row_food][col_food] = '1'

def brain(arr,purpose,patience):
	global last_go

	#print(tmp_arr)
	otvet=[0,0,0,0]



	for row in range(len(arr)):
		for col in range(len(arr[row])):
			
			if arr[row][col] == '1':

				for i in range(4):
					otvet[i] = otvet[i] + float(neuro[row][col].split(',')[i].split("'")[0])

			if arr[row][col] == '2':

				for i in range(4):
					otvet[i] = otvet[i] + float(neuro_wall[row][col].split(',')[i].split("'")[0])*-1

	# Если еды не видно двигаемся рандомно
	all_food = True


	for i in range(4):
		if otvet[i] != 0:
			all_food = False 

	if patience == 5 and purpose == True:
		purpose = False

	if all_food == True and purpose == False:
		go = random.randrange(1,3)
		purpose = True
	else:


		go = otvet.index(max(otvet))

		if otvet.count(max(otvet)) > 1:
			go = index_max(otvet,max(otvet))

		

	out =['up','down','left','right']

	return out[go] 

def brain2(arr):
	global last_go

	#print(tmp_arr)
	otvet=[0,0,0,0]

	print(arr)

	for row in range(len(arr)):
		for col in range(len(arr[row])):
			if arr[row][col] == '1':
				#otvet.append(neuro[row][col])
				#neuro[row][col].split(',')
				print(neuro[row][col])
				for i in range(4):
					print(i)
					otvet[i] = otvet[i] + float(neuro[row][col].split(',')[i].split("'")[0])

	#print(otvet)
	#print(otvet.index(max(otvet)))
	# resh = otvet.split(',')


	# Если еды не видно двигаемся рандомно
	all_nuul = True

	for i in range(4):
		if otvet[i] != 0:
			all_nuul = False 
	#print(all_nuul)
	if all_nuul == True:
		go = random.randrange(0,3)
	else:
		go = otvet.index(max(otvet))
	

	out =['up','down','left','right']

	return out[go]

def render():
	global width_snake,x1_old,y1_old,time_step
	game_over = False

	auto_pilot = False

	
	x1 = col / 2
	y1 = row / 2

	arr_snake_1.append([x1,y1])
	arr_snake_2.append([x1+10,y1])

	x1_change = 1
	y1_change = 0

	snake_1 = Snake('Зелёная',green,[10,30],[10,600])
	snake_2 = Snake('Фиолетовая',purpur,[30,30],[160,600])
	snake_3 = Snake('Чёрная',black,[50,30],[320,600])

	while not game_over:

		# управление
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				game_over = True

			if event.type == pygame.KEYDOWN:
			    if event.key == pygame.K_LEFT:
			        x1_change = -1
			        y1_change = 0
			    elif event.key == pygame.K_RIGHT:
			        x1_change = 1
			        y1_change = 0
			    elif event.key == pygame.K_UP:
			        y1_change = -1
			        x1_change = 0
			    elif event.key == pygame.K_DOWN:
			        y1_change = 1
			        x1_change = 0
			    elif event.key == pygame.K_SPACE:
			        y1_change = 0
			        x1_change = 0
			    elif event.key == pygame.K_a:
			    	auto_pilot = True
			    elif event.key == pygame.K_s:
			    	auto_pilot = False
			
			if event.type == pygame.MOUSEBUTTONUP:
				pos = pygame.mouse.get_pos()

				try:
					if arr_wall[round(pos[1]/block)][round(pos[0]/block)] == '2':
						arr_wall[round(pos[1]/block)][round(pos[0]/block)] = '0'
					else:
						arr_wall[round(pos[1]/block)][round(pos[0]/block)] = '2'
				except:
					pass
				#mouse_eye(round(pos[0]),round(pos[1]))
				#snake_eye(round(pos[0]),round(pos[1]))
				#print(pos)
		
		

		#snake(arr_snake_1,arr_eye_snake_1,auto_pilot,x1,y1,width_snake_1,x1_change,y1_change)
		#snake(arr_snake_2,arr_eye_snake_2,auto_pilot,x1,y1,width_snake_2,x1_change,y1_change)

		# body_snake(snake_1.arr_snake)
		# body_snake(snake_2.arr_snake)
		# body_snake(snake_3.arr_snake)
		
		snake_1.breath(arr_eye_snake_1, auto_pilot, x1, y1, x1_change, y1_change)
		snake_2.breath(arr_eye_snake_1, auto_pilot, x1, y1, x1_change, y1_change)
		snake_3.breath(arr_eye_snake_1, auto_pilot, x1, y1, x1_change, y1_change)
		


		dis.fill(grey)

		

		# Рендер мира
		for r in range(len(arr_world)):
			for c in range(len(arr_world[r])):
				pygame.draw.rect(dis,white,[block*c,block*r,block,block])				

				if arr_food[r][c] == '1':
					pygame.draw.rect(dis,red,[block*c,block*r,block,block])

				if arr_wall[r][c] == '2':
					pygame.draw.rect(dis,space_gray,[block*c,block*r,block,block])

				if arr_wall[r][c] == '-1':
					pygame.draw.rect(dis,purpur,[block*c,block*r,block,block])

				# рендер змеи
				# for i in range(len(arr_snake_1)):
				# 	pygame.draw.rect(dis,green,[block*arr_snake_1[i][0],block*arr_snake_1[i][1],block,block])

				# for i in range(len(arr_snake_2)):
				# 	pygame.draw.rect(dis,purpur,[block*arr_snake_2[i][0],block*arr_snake_2[i][1],block,block])				


				# сетка
				pygame.draw.rect(dis,grey,[block*c,block*r,block,block],1)

		snake_1.render(dis)
		snake_2.render(dis)
		snake_3.render(dis)

		# Рендер зрения
		snake_1.render_eye(620,20,25,neuro)	
		snake_2.render_eye(620,300,25,neuro)		
		#render_eye(arr_eye,620,20)
		#render_eye2(arr_eye_snake_1,620,20,25,neuro)
		#render_eye2(arr_eye_snake_2,620,300,25,neuro)

		#render_eye2(arr_neuro,620,300,25,neuro)
		#render_eye(arr_mouse,620,150)

		#random_food()
		#pygame.draw.rect(dis,white,[0,0,100,100])

		pygame.display.update()
		clock.tick(speed_world)

	pygame.quit()
	quit()

def index_max(arr,value):
	tmp_arr = []
	for i in range(len(arr)):
		if arr[i] == value:
			tmp_arr.append(i)
	
	return tmp_arr[random.randrange(0,len(tmp_arr))]

def body_snake(arr_snake):
	for row in range(len(arr_wall)):
		for col in range(len(arr_wall[row])):

			for i in range(len(arr_snake)):
				if arr_snake[0][1] != row and arr_snake[0][0] != col:
					if arr_snake[i][1] == row and arr_snake[i][0] == col:
						arr_wall[row][col] = '2'
				 

for i in range(70):
	random_food()

render()
