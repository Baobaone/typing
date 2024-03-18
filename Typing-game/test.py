import pygame, random
import sys
from pygame.locals import *
pygame.init()

white =(255, 255, 255)
Chu =  (100, 149, 237)
Nen =  (255, 255, 255)
green = (0,255,0)
Black =(0,   0   ,0  )
pause = False
width,height = (800,600) #this is short for width=800 and height=600
screen = pygame.display.set_mode((width,height)) #sets up the window
score_font = pygame.font.Font("score_font.ttf",60)
font = pygame.font.Font(None, 36)
textSurface = font.render('Moi chon', True, Chu, Nen)
sw = False
fns = False


def spawn_word():
    global words
    wordStr = random.choice(words).strip()
    return TypingGameWord(wordStr)

class TypingGameWord(pygame.sprite.Sprite):
    "Represents a word that the user will have to type"
    
    def __init__(self, word):
        global width
        pygame.sprite.Sprite.__init__(self) #initialize it as a pygame sprite
        self.font = pygame.font.Font("font.ttf",40) #make the font we'll write the word in
        self.originalWord = word
        self.word = word
        self.image = self.font.render(self.word, True, (255,255,255))
        self.rect = self.image.get_rect()
        self.rect.bottom = 0 #start the word just above the screen
        self.rect.centerx = random.randint(int(self.rect.width/2),int(width-self.rect.width/2))
        
    def checkLetter(self, letter):
        "Checks a letter that the player typed.  Returns true if the word is empty, otherwise false."
        if letter == self.word[0]:
            self.word = self.word[1:]
            self.updateSurface()
        return self.word == ""
    
    def updateSurface(self):
        "Updates self.image to match the text of the word."
        self.image = self.font.render(self.word, True, (255,255,255))
        right = self.rect.right
        bottom = self.rect.bottom
        self.rect = self.image.get_rect()
        self.rect.right = right
        self.rect.bottom = bottom

    def update(self):
        global height
        "Called every frame to update the state of the word."
        global speed, running,score, extra_words, currentword,fns,fix
        speedCoefficient = len(self.originalWord)
        if speedCoefficient < len(currentword.originalWord):
            speedCoefficient = len(currentword.originalWord)
        if speedCoefficient < 5:
            speedCoefficient = 5
        old_top = self.rect.top
        self.rect.top += speed / speedCoefficient
        if old_top < height/4 and self.rect.top >= height/4:
            extra_words.append(spawn_word())
        if self.rect.bottom >= height:
            running = not running
            fix = not fix
            fns = not fns
            finish()
            
fix = False
def finish():
    global fns, score, running, fix, score_font,check
    if fix:
        screen.fill((0,0,0))
        pygame.display.flip()
        while fns: 
            score_end1 = score_font.render("YOU LOSE", True, (0,255,0))
            score_end2 = score_font.render("YOUR SCORE:"+ str(score), True, (0,255,0))
            choice1 = score_font.render("PRESS 'Y' TO CONTINUE", True, (0,255,0))
            choice2 = score_font.render("-'N' TO QUIT", True, (0,255,0))
            #print ("YOU LOSE! Your score is:",score)
            screen.blit(score_end1,(270,130))
            screen.blit(score_end2,(220,230))
            screen.blit(choice1,(100,330))
            screen.blit(choice2,(200,430))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() #stops the program
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        check = True
                        reset()
                        fns = not fns
                        fix = not fix
                    elif event.key == pygame.K_n:
                        sys.exit()
                        

stop = False
running = False
speed = 20
check = True

def LV():

    global running,check
    screen.fill((0,0,0))
    pygame.display.flip()
    while check:
        rect1 = pygame.draw.rect(screen,white, (250,100,350,50))
        rect2 = pygame.draw.rect(screen,white, (250,200,350,50))
        rect3 = pygame.draw.rect(screen,white, (250,300,350,50))
        rect4 = pygame.draw.rect(screen,white, (250,400,350,50))
        #viết chữ
        text = font.render("Màn 1", True, green)
        screen.blit(text, (380, 110))
        text2 = font.render("Man 2", True, green)
        screen.blit(text2, (380, 210))
        text3 = font.render("Man 3", True, green)
        screen.blit(text3, (380, 310))
        text4 = font.render("Man 4", True, green)
        screen.blit(text4, (380, 410))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                check = False
            if event.type == pygame.K_ESCAPE:
                running = False
                check = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:   
                mouse_pos = pygame.mouse.get_pos()
                if rect1.collidepoint(mouse_pos):
                        running = True
                        check = False
                        return 1
                        #print("Bạn đã click vào man 1!")
                if rect2.collidepoint(mouse_pos):
                        running = True
                        check = False
                        return 2
                        #print("Bạn đã click vào man 2!")
                if rect3.collidepoint(mouse_pos):
                        running = True
                        check = False
                        return 3
                        #print("Bạn đã click vào man 3!")
                if rect4.collidepoint(mouse_pos):
                        running = True
                        check = False
                        return 4
                        #print("Bạn đã click vào man 4!")

        screen.blit(textSurface, (830, 50))
        #1
lv = LV()
if lv == 1:
    wordfile = open('word_coso.txt', 'r')
    words = wordfile.readlines()
    wordfile.close()
elif lv == 2:
    wordfile = open('word_top.txt', 'r')
    words = wordfile.readlines()
    wordfile.close()
elif lv == 3:
    wordfile = open('word_bot.txt', 'r')
    words = wordfile.readlines()
    wordfile.close()
else:
    wordfile = open('words.txt', 'r')
    words = wordfile.readlines()
    wordfile.close()

currentword = spawn_word()
extra_words = []
score = 0

background = pygame.image.load("background.png").convert()

clock = pygame.time.Clock()

count = 0

def ps():
    global pause, sw
    pause = not pause
    sw = not sw

def play():
    global running, currentword,score,speed,extra_words, pause, sw,count
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False #stops the program
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                ps()
                #running = False #stops the program
            else:
                if currentword.checkLetter(event.unicode): #event.unicode is the letter the user typed
                    if count == 9:
                        speed += 10
                        count = 0
                        score += 100
                    else:
                        count += 1
                        score += 100
                    if len(extra_words) > 0:
                        lowestwordindex = 0
                        for i in range(len(extra_words)):
                            if extra_words[i].rect.bottom > extra_words[lowestwordindex].rect.bottom:
                                lowestwordindex = i
                        currentword = extra_words.pop(lowestwordindex)
                        
                    else:
                        currentword = spawn_word()
    currentword.update()
    for i in extra_words:
        i.update()

    score_surf = score_font.render("SCORE:"+str(score), True, (0,255,0))
    
    screen.fill((0,0,0)) #clears the screen
    screen.blit(background,(0,0))
    screen.blit(score_surf,(0,530))
    for i in extra_words:
        screen.blit(i.image, i.rect)
    pygame.draw.line(screen,(111,255,122),(width/2, height),(currentword.rect.left+7, currentword.rect.bottom),14)
    screen.blit(currentword.image, currentword.rect) #draw the word
    pygame.display.flip() #apply the changes

def reset():
    global words, lv, currentword,extra_words,score,count
    lv = LV()
    if lv == 1:
        wordfile = open('word_coso.txt', 'r')
        words = wordfile.readlines()
        wordfile.close()
    elif lv == 2:
        wordfile = open('word_top.txt', 'r')
        words = wordfile.readlines()
        wordfile.close()
    elif lv == 3:
        wordfile = open('word_bot.txt', 'r')
        words = wordfile.readlines()
        wordfile.close()
    else:
        wordfile = open('words.txt', 'r')
        words = wordfile.readlines()
        wordfile.close()

    currentword = spawn_word()
    extra_words = []
    score = 0
    count = 0

while running: #the main loop
    clock.tick(20)
    if pause:
        p = score_font.render("PAUSED", True, (0,255,0))
        screen.blit(p,(300,250))
        pygame.display.flip()
        while sw:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause = not pause
                        sw = not sw
    else: 
        play()
pygame.quit() #fix the program breaking in IDLE