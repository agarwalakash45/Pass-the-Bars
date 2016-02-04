import pygame
import random
pygame.init()       #Initialize pygame modules

display_width=350
display_height=550
block_size=15           #Size of block
bar_height=8            #Height of each bar
    
white=(255,255,255)
black=(0,0,0)
blue=(67,148,154)
green=(1,148,119)
red=(255,0,0)
purple=(86,24,125)


bars_count=15
fps=80                          #Frames per second
clock=pygame.time.Clock()

gameDisplay=pygame.display.set_mode((display_width,display_height)) #Setting display resolutions
pygame.display.set_caption("Pass the Bars")

def display_message(msg,color,font_size=25,y_position=0):                  #Method to display message on screen
    size=font_size
    font=pygame.font.SysFont("georgia",size)
    text_screen=font.render(msg,True,color)
    text_rect=text_screen.get_rect()
    text_rect.center=(display_width/2,display_height/2+y_position)
    gameDisplay.blit(text_screen,text_rect)
    
    
def create_bars(total_bars):             #Method to create bars
    bars=[]                               #[[x1,y1,l1],[x2,y2,l2],.....]
    factor=2                                #Determines factor if bar takes entire width, what factor of block size should the gap be
    i=0
    min_width=50                    #Minimum length of bar
    min_gap=50                      #Minimum gap between two bars
    max_gap=110                      #Maximum gap between two bars
    while i<total_bars:
        bar_length=random.randrange(min_width,display_width-(factor*block_size))
        bar_x=random.randrange(0,display_width-bar_length)
        if i==0:
            bar_y=random.randrange(max_gap,display_height/2)
        else:
            bar_y=bars[i-1][1]-random.randrange(min_gap,max_gap)
        bars.append([bar_x,bar_y,bar_length])
        i+=1
    return bars


def display_bars(bars):                 #Method to display bars
    for element in bars:
        gameDisplay.fill(red,[element[0],element[1],element[2],bar_height])


def bars_shift(bars,bar_shift):         #TO handle bar shifting in vertical direction
    factor=2                        #Determines factor if bar takes entire width, what factor of block size should the gap be
    min_width=50                        #Minimum length of bar
    min_gap=50                  #Minimum gap between two bars
    max_gap=110                      #Maximum gap between two bars
    i=0
    while i<len(bars):                #Increment y-position of each bar
        bars[i][1]+=bar_shift
        if bars[i][1]>display_height:
            bars[i][2]=random.randrange(min_width,display_width-(factor*block_size))
            bars[i][0]=random.randrange(0,display_width-bars[i][2])
            next_bar=(i-1)%bars_count
            bars[i][1]=bars[next_bar][1]-random.randrange(min_gap,max_gap)
            #element[1]-=(display_height+min_gap)

        i+=1

def is_safe(pos_x,pos_y,bars):          #Returns true if block is safe
    for element in bars:
        if pos_x>=element[0] and pos_x<element[0]+element[2] or pos_x+block_size>element[0] and pos_x+block_size<=element[0]+element[2]:
            if pos_y>=element[1] and pos_y<=element[1]+bar_height or pos_y+block_size>element[1] and pos_y+block_size<element[1]+bar_height:        
                return False
    return True

def game_intro():
    intro=True
    while intro:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:     #If close is clicked
                    pygame.quit()              #Exit from the game

            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_p:           #'P' pressed, start the game
                    intro=False
                elif event.key==pygame.K_q:        #'Q' pressed, quit the game
                    pygame.quit()

        gameDisplay.fill(white)
        display_message("Pass the Bars",green,50)
        display_message("Press P to play, Q to quit",black,25,80)
        pygame.display.update()
    
    
def game_play():
    gameExit=False
    gameOver=True
    pos_x=175
    pos_y=400
    move_x=0
    move_y=0
    shift_bar=1.5                 #Shifting of bars in one frame in vertical direction
    shift_block=10                #Shifting of block in one frame in horizontal direction
    global bars_count
    bars=create_bars(bars_count)

    while not gameExit:
    
        while not gameOver:          #Game Over loop

            for event in pygame.event.get():
                if event.type==pygame.QUIT:     #If close is clicked
                        pygame.quit()               #Exit from the game
                        quit()
                        
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_p:           #'P' pressed, start the game
                        bars=create_bars(bars_count)
                        pos_x=175
                        pos_y=400
                        gameOver=True
                    elif event.key==pygame.K_q:        #'Q' pressed, quit the game
                        pygame.quit()
                        quit()
                        
            gameDisplay.fill(white)
            display_message("You Crashed!!",red,50)
            display_message("Press P to play, Q to quit",black,25,75)
            pygame.display.update()


        for event in pygame.event.get():
            if event.type==pygame.QUIT:     #If close is clicked
                gameOver=True               #Exit from the game

            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RIGHT:           #Right key is pressed
                    move_x=shift_block
                elif event.key==pygame.K_LEFT:            #Left key is pressed
                    move_x=-shift_block
                elif event.key==pygame.K_UP:            #Up key is pressed
                    move_y=-shift_block
                elif event.key==pygame.K_DOWN:          #Down key is pressed
                    move_y=shift_block

            elif event.type==pygame.KEYUP:
                move_x=0
                move_y=0
                
        pos_x+=move_x
        pos_y+=move_y

        #If block moves out of the sides
        if pos_x<=0:            #Left side constraint
            pos_x=0
        elif pos_x+block_size>=display_width:           #Right side constraint
            pos_x=display_width-block_size
        elif pos_y<=0:                      #Top constraint
            pos_y=0
        elif pos_y+block_size>=display_height:          #Down constraint
            pos_y=display_height-block_size


        gameDisplay.fill(white) #Setting background as white

        display_bars(bars)

        bars_shift(bars,shift_bar)

        #To check whether block collides with any of the bars
        if not is_safe(pos_x,pos_y,bars):
            gameOver=False
        
        gameDisplay.fill(purple,[pos_x,pos_y,block_size,block_size])      #To display block
        pygame.display.update()

        clock.tick(fps)                     #frames per second

game_intro()            
game_play()
pygame.quit()           #Uninitialize pygame modules
