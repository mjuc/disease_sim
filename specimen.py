import random

# Possible states of each specimen wellbeing
# C - sick
# Z - infected
# ZD - recovering
# ZZ - healthy
wellbeing=['C','Z','ZD','ZZ']
gender=['M','F']
reproduction_likeliness=30
reproduction_boudaries=[16,60]

class Specimen:
    x=0
    y=0
    v=[0,0]
    state=''
    g=''
    age=1
    immunity=0
    last_set_age=0
    alive=True
    max_immunity=0
    interacted_with=[]
    
    def __init__(self):
        self.age=random(1,99)
        self.state=random(wellbeing)
        self.g=random(gender)
        if ((self.age > 0 and self.age < 15) or (self.age >=70 and self.age<=100)):
            self.max_immunity=3
            self.immunity=random(0,3) #possibility of instant death
        elif (self.age >= 40 and self.age <70):
            self.max_immunity=6
            self.immunity=random(4,6)
        elif (self.age >= 15 and self.age < 40):
            self.max_immunity=10
            self.immunity=random(7,10)
    
    def setCoordinates(self,screen_x,screen_y):
        self.x=random(0,screen_x)
        self.y=random(0,screen_y)
        
    def setSpeed(self):
        self.v[0]=random(-3,3)
        self.v[1]=random(-3,3)
        
    def move(self):
        self.x+=self.v[0]
        self.y+=self.v[1]
    
    def checkWall(self,screen_x,screen_y):
        if(self.x == screen_x or self.y == screen_y or self.x == 0 or self.y == 0):
            self.setSpeed()
        
    def getOlder(self):
        self.age+=1
        if self.age==15:
            self.max_immunity=10
            self.immunity=random(7,10)
        elif self.age==40:
            self.max_immunity=6
            self.immunity=random(4,6)
        elif self.age==70:
            self.max_immunity=3
            self.immunity=random(0,3)
        if self.age == 100 or self.immunity==0: #possibility of instant death
            self.alive=False
        if self.state=='Z':
            self.immunity-=0.1
            if (self.age-self.last_set_age == 2):
                self.state='C'
                self.last_set_age=self.age
        elif self.state=='C':
            self.immunity-=0.5
            if (self.age-self.last_set_age == 7):
                self.state='ZD'
                self.last_set_age=self.age
        elif self.state=='ZD':
            if(self.immunity+0.1<self.max_immunity):
                self.immunity+=0.1
            if (self.age-self.last_set_age == 5):
                self.state='ZZ'
                self.last_set_age=self.age
        elif self.state=='ZZ':
            if(self.immunity+0.05<self.max_immunity):
                self.immunity+=0.05
    
    def infect(self,s):
        self.interacted_with.append((s.x,s.y))
        s.interacted_with.append((self.x,self.y))
        if(s.state=='Z' and self.state=='ZZ') or (s.state=='ZZ' and self.state=='Z'):
            if s.state=='Z':
                if self.immunity<3:
                    self.state='Z'
            else:
                if s.immunity<3:
                    s.state='Z'
        elif(s.state=='C' and self.state=='ZZ') or (s.state=='ZZ' and self.state=='C'):
            if s.state=='C':
                if self.immunity<6:
                    self.state='Z'
                    self.last_set_age=self.age
                else:
                    self.immunity-=3
            else:
                if s.immunity<6:
                    s.state='Z'
                    s.last_set_age=s.age
                else:
                    s.immunity-=3
        elif(s.state=='ZD' and self.state=='ZZ') or (s.state=='ZZ' and self.state=='ZD'):
            if s.state=='ZD':
                s.immunity+=1
            else:
                self.immunity+=1
        elif(s.state=='ZZ' and self.state=='ZZ') or (s.state=='ZZ' and self.state=='ZZ'):
            if s.immunity > self.immunity:
                self.immunity=s.immunity
            elif s.immunity < self.immunity:
                s.immunity=self.immunity
            else:
                s.immunity=s.max_immunity
                self.immunity=self.max_immunity
        elif(s.state=='C' and self.state=='Z') or (s.state=='Z' and self.state=='C'):
            if s.state=='C':
                self.state='C'
                self.last_set_age=self.age
                s.last_set_age=s.age
            else:
                s.state='C'
                self.last_set_age=self.age
                s.last_set_age=s.age
        elif(s.state=='C' and self.state=='ZD') or (s.state=='ZD' and self.state=='C'):
            if s.state=='C':
                s.last_set_age=s.age
                self.state='ZD'
                self.last_set_age=self.age
            else:
                s.last_set_age=s.age
                s.s='ZD'
                self.last_set_age=self.age
        elif(s.state=='C' and self.state=='C') or (s.state=='C' and self.state=='C'):
            if s.immunity > self.immunity:
                self.immunity=s.immunity
            elif s.immunity < self.immunity:
                s.immunity=self.immunity
            s.last_set_age=s.age
            self.last_set_age=self.age
        elif(s.state=='ZD' and self.state=='Z') or (s.state=='Z' and self.state=='ZD'):
            if s.state=='ZD':
                s.immunity-=1
            else:
                self.immunity-=1
        elif(s.state=='Z' and self.state=='Z') or (s.state=='Z' and self.state=='Z'):
            s.immunity-=1
            self.immunity-=1 
    
    def checkContact(self,boardState):
        children=[]
        for s in boardState:
            if (s.x,s.y) not in self.interacted_with:
                if ((s.x == self.x+1) and (s.y == self.y or s.y == self.y+1 or s.y == self.y-1)):
                    self.infect(s)
                    if(s.g != self.g):
                        l = random(0,100)
                        if l<=reproduction_likeliness:
                            if self.age>=reproduction_boudaries[0] and self.age<=reproduction_boudaries[1]:
                                if s.age>=reproduction_boudaries[0] and s.age<=reproduction_boudaries[1]:
                                    temp=Specimen()
                                    temp.setSpeed()
                                    temp.setCoordinates()
                                    children.append(temp)
                                    del(temp)   
                elif ((s.x == self.x-1) and (s.y == self.y or s.y == self.y+1 or s.y == self.y-1)):
                    self.infect(s)
                    if(s.g != self.g):
                        l = random(0,100)
                        if l<=reproduction_likeliness:
                            if self.age>=reproduction_boudaries[0] and self.age<=reproduction_boudaries[1]:
                                if s.age>=reproduction_boudaries[0] and s.age<=reproduction_boudaries[1]:
                                    temp=Specimen()
                                    temp.setSpeed()
                                    temp.setCoordinates()
                                    children.append(temp)
                                    del(temp)
                elif ((s.x == self.x) and (s.y == self.y+1 or s.y == self.y-1)):
                    self.infect(s)
                    if(s.g != self.g):
                        l = random(0,100)
                        if l<=reproduction_likeliness:
                            if self.age>=reproduction_boudaries[0] and self.age<=reproduction_boudaries[1]:
                                if s.age>=reproduction_boudaries[0] and s.age<=reproduction_boudaries[1]:
                                    temp=Specimen()
                                    temp.setSpeed()
                                    temp.setCoordinates()
                                    children.append(temp)
                                    del(temp)
        return children