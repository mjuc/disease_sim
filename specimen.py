import random

# Possible states of each specimen wellbeing
# C - sick
# Z - infected
# ZD - recovering
# ZZ - healthy
wellbeing=['C','Z','ZD','ZZ']
gender=['M','F']
reproduction_boudaries=[16,60]

class Specimen:
    #coordinates of specimen on simulation board
    x=0
    y=0
    #speed of movement
    v=[0,0]
    #state of health
    state=''
    #gender
    g=''
    #age
    age=1
    #level of immunity for disease
    immunity=0
    #age of last change of state of health parameter
    last_set_age=0
    #is still alive -> should be displayed on board
    alive=True
    #max immunity for age group of specimen
    max_immunity=0
    #others interacted with during turn
    interacted_with=[]
    #borders of board -> to set coordinates of children
    screen_borders=[]
    
    def Specimen(self):
          self.alive=True
            
    def __init__(self):
        #set random age
        self.age=random.randrange(1,99)
        #set health state with likelihoods: 70% ZZ, 10% ZD, 10% Z, 10% C
        s=random.randrange(0,100)
        if s <= 70:
            self.state='ZZ'
        elif s > 70 and s <= 80:
            self.state='ZD'
        elif s > 80 and s <= 90:
            self.state='Z'
        elif s > 90 and s <=100:
            self.state='C'
        #set random gender
        self.g=random.choice(gender)
        #set level of immunity for each age group: 0 to 3 for 0-15/70-100 4 to 6 for 40-70 and 6-10 for 16-40
        if ((self.age > 0 and self.age < 15) or (self.age >=70 and self.age<=100)):
            self.max_immunity=3
            self.immunity=random.randrange(0,3) #possibility of instant death
        elif (self.age >= 40 and self.age <70):
            self.max_immunity=6
            self.immunity=random.randrange(4,6)
        elif (self.age >= 15 and self.age < 40):
            self.max_immunity=10
            self.immunity=random.randrange(7,10)
    
    def setCoordinates(self,screen_x,screen_y):
        #set random coordinates on simulation board
        self.x=random.randrange(0,screen_x)
        self.y=random.randrange(0,screen_y)
        self.screen_borders.append(screen_x)
        self.screen_borders.append(screen_y)
        
    def setSpeed(self):
        #set random speed of movement represented as two-element vector
        self.v[0]=random.randrange(-3,3)
        self.v[1]=random.randrange(-3,3)
        #check if generated speed will result in hitting the border
        self.checkWall(self.screen_borders[0],self.screen_borders[1])
        
    def move(self):
        #change coordinates according to speed of movement
        self.x+=self.v[0]
        self.y+=self.v[1]
    
    def checkWall(self,screen_x,screen_y):
        #check if current speed of movement will result in hitting the border
        #if so change it
        if(self.x+self.v[0] >= screen_x or self.y+self.v[1] == screen_y or self.x+self.v[0] <= 0 or self.y+self.v[1] <= 0):
            self.setSpeed()
        
    def getOlder(self):
        #increment age of specimen
        self.age+=1
        #if age group is changed generate new level of immunity according to new group
        if self.age==15:
            self.max_immunity=10
            self.immunity=random.randrange(7,10)
        elif self.age==40:
            self.max_immunity=6
            self.immunity=random.randrange(4,6)
        elif self.age==70:
            self.max_immunity=3
            self.immunity=random.randrange(0,3)
        #if specimen is too old or immunity level reached 0 kill specimen
        if self.age == 120 or self.immunity==0:
            self.alive=False
        #adapt immunity level according to current state
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
        #append list of interactions in current turn for both specimen
        self.interacted_with.append((s.x,s.y))
        s.interacted_with.append((self.x,self.y))
        #execute interactions according to state of health of both specimen
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
        #for each specimen on board check if in contact; execute interactions; reproduce if possible
        for s in boardState:
            if (s.x,s.y) not in self.interacted_with:
                if ((s.x == self.x+1) and (s.y == self.y or s.y == self.y+1 or s.y == self.y-1)):
                    self.infect(s)
                    if(s.g != self.g):
                        if self.age>=reproduction_boudaries[0] and self.age<=reproduction_boudaries[1]:
                            if s.age>=reproduction_boudaries[0] and s.age<=reproduction_boudaries[1]:
                                temp=Specimen()
                                temp.setSpeed()
                                temp.setCoordinates(self.screen_borders[0],self.screen_borders[1])
                                temp.state='ZZ'
                                children.append(temp)
                                del(temp)   
                elif ((s.x == self.x-1) and (s.y == self.y or s.y == self.y+1 or s.y == self.y-1)):
                    self.infect(s)
                    if(s.g != self.g):
                        if self.age>=reproduction_boudaries[0] and self.age<=reproduction_boudaries[1]:
                            if s.age>=reproduction_boudaries[0] and s.age<=reproduction_boudaries[1]:
                                temp=Specimen()
                                temp.setSpeed()
                                temp.setCoordinates(self.screen_borders[0],self.screen_borders[1])
                                temp.state='ZZ'
                                children.append(temp)
                                del(temp)
                elif ((s.x == self.x) and (s.y == self.y+1 or s.y == self.y-1)):
                    self.infect(s)
                    if(s.g != self.g):
                        if self.age>=reproduction_boudaries[0] and self.age<=reproduction_boudaries[1]:
                            if s.age>=reproduction_boudaries[0] and s.age<=reproduction_boudaries[1]:
                                temp=Specimen()
                                temp.setSpeed()
                                temp.setCoordinates(self.screen_borders[0],self.screen_borders[1])
                                temp.state='ZZ'
                                children.append(temp)
                                del(temp)
        return children
    
    def clean(self):
        #clean list of interactions after turn
        self.interacted_with=[]