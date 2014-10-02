import sys
import random
import os
import termios
import fcntl

def getch():
  fd = sys.stdin.fileno()

  oldterm = termios.tcgetattr(fd)
  newattr = termios.tcgetattr(fd)
  newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
  termios.tcsetattr(fd, termios.TCSANOW, newattr)

  oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
  fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

  try:        
    while 1:            
      try:
        c = sys.stdin.read(1)
        break
      except IOError: pass
  finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
  return c

class tile:
  def __init__(self,data):#data is a list of strings. The list number is the y and the string numb is the x
    self.map = data
    self.width = len(self.map[0])
    self.height = len(self.map)
  def returnBlock(self,x,y):
    return self.map[y][x]
  def writeBlock(self,x,y,block):
    self.map[y][x] = block
  def renderView(self):
    for y in range(self.height):
      for x in range(self.width):
        sys.stdout.write(self.returnBlock(x,y))
      print ""
      
class level_map:
  def __init__(self,tile_map):
    self.tile_map = tile_map
    self.height = len(tile_map)*tile_map[0][0].height
    self.width = len(tile_map[0])*tile_map[0][0].width
    self.tileWidth = tile_map[0][0].width
    self.tileHeight = tile_map[0][0].height
    self.compMap = []
    for y in range(self.height):
      self.compMap.append([])
      for x in range(self.width):
        self.compMap[y].append([])

    for y in range(self.height):
      for x in range(self.width):
        self.compMap[y][x] = self.compBlock(x,y)
  def compBlock(self,x,y):
    return self.tile_map[y/(self.tileHeight)][x/self.tileWidth].returnBlock((x%self.tileWidth),(y%self.tileHeight))
  def returnBlock(self,x,y):
    return self.compMap[y][x]
  def writeBlock(self,x,y,block):
    self.compMap[y][x] = block
  def renderView(self):
    for y in range(self.height):
      for x in range(self.width):
        sys.stdout.write(self.returnBlock(x,y))
      print ""
  



#This is awful
with open('tile1.txt','r') as file:
  map1 = file.readlines()

nremove = 0
for item in map1:
  map1[nremove] = map1[nremove].strip()
  map1[nremove] = list(map1[nremove])
  nremove += 1


with open('tile2.txt','r') as file:
  map2 = file.readlines()

nremove = 0 
for item in map2:
  map2[nremove] = map2[nremove].strip()
  map2[nremove] = list(map2[nremove])
  nremove += 1
  
with open('tile3.txt','r') as file:
  map3 = file.readlines()
  
nremove = 0  
for item in map3:
  map3[nremove] = map3[nremove].strip()
  map3[nremove] = list(map3[nremove])
  nremove += 1


#map1 is a list
testTile = tile(map1)
testTile2 = tile(map2)
testTile3 = tile(map3)

#worst code ever
def randTile():
  what = random.randint(0,2)
  if what == 0:
    return testTile
  if what == 1:
    return testTile2
  if what == 2:
    return testTile3
  
tileMap = []


genHeight = int(raw_input("What should the height be?"))
#genHeight = 1
genWidth = int(raw_input("What should the width be?"))
#genWidth = 1

for y in range(genHeight):
  tileMap.append([])
  for x in range(genWidth):
    tileMap[y].append([])

for y in range(genHeight):
  for x in range(genWidth):
    tileMap[y][x] = randTile()
    

testLevel = level_map(tileMap)

print testLevel.renderView()


Yviewdist = 45
Xviewdist = 90

#This part makes sure you spawn on a space as oppused to a wall
spotisspace = False
while not spotisspace:
  Xpos=random.randint(0,testLevel.width-1)
  Ypos=random.randint(0,testLevel.height-1)
  if (testLevel.returnBlock(Xpos,Ypos) == "."):
    spotisspace=True
    

while True:
  for y in range(Yviewdist):
    for x in range(Xviewdist):
      if (x == Xviewdist/2 and y == Yviewdist/2):
        sys.stdout.write("C")
      else:
        if ((Xpos-(Xviewdist/2)+x)<0 or (Xpos-(Xviewdist/2)+x)>testLevel.width-1) or ((Ypos-(Yviewdist/2)+y)<0 or (Ypos-(Yviewdist/2)+y)>testLevel.height-1):
          output = "="
        else:
          output = testLevel.returnBlock(Xpos-(Xviewdist/2)+x,Ypos-(Yviewdist/2)+y)
        sys.stdout.write(str(output))
    print
    

  testLevel.writeBlock(Xpos,Ypos,"X")
  print "Enter move direction (W,S,A,D)"
  move = getch()
  os.system('clear')
  if (move.lower() == 'w'):
    if (testLevel.returnBlock(Xpos,Ypos-1) == "."):
     Ypos = Ypos - 1
    elif (testLevel.returnBlock(Xpos,Ypos-1) == "X"):
      print "There is a Wall there."
  if (move.lower() == 's'):
    if (testLevel.returnBlock(Xpos,Ypos+1)== "."):
     Ypos = Ypos + 1
    elif (testLevel.returnBlock(Xpos,Ypos+1)== "X"):
      print "There is a Wall there."

  if (move.lower() == 'd'):
    if (testLevel.returnBlock(Xpos+1,Ypos) == "."):
     Xpos = Xpos + 1
    elif (testLevel.returnBlock(Xpos+1,Ypos) == "X"):
      print "There is a Wall there."

  if (move.lower() == 'a'):
    if (testLevel.returnBlock(Xpos-1,Ypos) == "."):
     Xpos = Xpos - 1
    elif (testLevel.returnBlock(Xpos-1,Ypos) == "X"):
      print "There is a Wall there."
