import pygame, random
from typing import Any
pygame.init()

width,height = (800,600) #this is short for width=800 and height=600
screen = pygame.display.set_mode((width,height)) #sets up the window
score_font = pygame.font.Font("score_font.ttf",60)




def spawn_word():
    '''global words
    wordStr = random.choice(words).strip()
    return TypingGameWord(wordStr)'''
    global words
    wordStr = random.choice(words).strip()
    while len(wordStr) >= 4 :
            wordStr= random.choice(words).strip()
    return TypingGameWord(wordStr)

def spawn_word2():
    '''global words
    wordStr = random.choice(words).strip()
    return TypingGameWord(wordStr)'''
    global words
    wordStr = random.choice(words).strip()
    while len(wordStr) < 4 or len(wordStr) > 6 :
            wordStr= random.choice(words).strip()
    return TypingGameWord(wordStr)
#def ez():
    

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
        global speed, running,score, extra_words, currentword
        speedCoefficient = len(self.originalWord)
        if speedCoefficient < len(currentword.originalWord):
            speedCoefficient = len(currentword.originalWord)
        if speedCoefficient < 5:
            speedCoefficient = 5
        old_top = self.rect.top
        self.rect.top += speed / speedCoefficient
        if old_top < height/4 and self.rect.top >= height/4:
            if a == 1: 
                extra_words.append(spawn_word())
            elif a == 2:
                extra_words.append(spawn_word2())
        if self.rect.bottom >= height:
            screen.fill((0,0,0))
            score_end = score_font.render("YOU LOSE \n YOUR SCORE:"+ str(score), True, (0,255,0))
            choice1 = score_font.render("PRESS 'Y' TO CONTINUE", True, (0,255,0))
            choice2 = score_font.render("-'N' TO QUIT", True, (0,255,0))
            #print ("YOU LOSE! Your score is:",score)
            screen.blit(score_end,(70,130))
            screen.blit(choice1,(100,330))
            screen.blit(choice2,(200,430))
            pygame.display.flip()
            pygame.time.delay(10000)
            running = False
            
    
   

stop = False
running = True
speed = 10
wordfile = open('words.txt', 'r')
words = wordfile.readlines()
a = 0
#ez_word =[]
#mid_word = []
#hard_word = []
extra_words = []
wordfile.close()
score = 0
currentword = Any

background = pygame.image.load("background.png").convert()

clock = pygame.time.Clock()

def game(a):
    global currentword,score,running
    if  a == 1:
            currentword = spawn_word()
    elif a == 2:
            currentword = spawn_word2()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False #stops the program
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False #stops the program
            else:
                if currentword.checkLetter(event.unicode): #event.unicode is the letter the user typed
                    speed += 1
                    score += 100
                    if len(extra_words) > 0:
                        lowestwordindex = 0
                        for i in range(len(extra_words)):
                            if extra_words[i].rect.bottom > extra_words[lowestwordindex].rect.bottom:
                                lowestwordindex = i
                        currentword = extra_words.pop(lowestwordindex)
                        
                    else:
                        if a == 1:
                            currentword = spawn_word()
                        elif a == 2:
                            currentword = spawn_word2()
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

while running: #the main loop
    clock.tick(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False #stops the program
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False #stops the program
            else:
                if event.key == pygame.K_1:
                    a = 1
                elif event.key == pygame.K_2:
                    a = 2
    game(a)
    
pygame.quit() #fix the program breaking in IDLE