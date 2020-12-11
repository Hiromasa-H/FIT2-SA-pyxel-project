import pyxel
import math
import random
from perlin_noise import PerlinNoise
#https://pypi.org/project/perlin-noise/
map_size = 200

class Player:
  def __init__(self):
    self.x = 100
    self.y = 100
    self.hp = 10
    self.moving = False
    self.shield_center = 180 #degrees
    self.shield_size = 45  #degrees. actual size will be twice this amount
    self.speed = 2
    self.shield = [[0,0] for _ in range(self.shield_size*2-1)]
    self.moving = False

  def upright(self):
    self.y -= self.speed
    self.x += self.speed
    self.moving = True

  def upleft(self):
    self.y -= self.speed
    self.x -= self.speed
    self.moving = True

  def downright(self):
    self.y += self.speed
    self.x += self.speed
    self.moving = True

  def downleft(self):
    self.y += self.speed
    self.x -= self.speed
    self.moving = True

  def up(self):
    self.y -= self.speed
    self.moving = True

  def down(self):
    self.y += self.speed
    self.moving = True

  def left(self):
    self.x -= self.speed
    self.moving = True

  def right(self):
    self.x += self.speed
    self.moving = True

  def move_shield(self,mouse_x,mouse_y):
    # lx = int(self.x - mouse_x )
    lx = int(mouse_x - self.x )
    ly = int(self.y - mouse_y )
    # ly = int(mouse_y - self.y)  
    # print(lx)
    if lx != 0:
      if lx > 0 and ly > 0: #第1象限
        self.shield_center = math.degrees(math.atan( ly / lx ))
      elif lx == 0 and ly > 0:
        self.shield_center = 90
      elif lx < 0 and ly > 0:#第2象限
        self.shield_center = 180 + math.degrees(math.atan( ly / lx ))
      elif lx < 0 and ly == 0:
        self.shield_center = 180
      elif lx < 0 and ly < 0:#第3象限
        self.shield_center = 180 + math.degrees(math.atan( ly / lx ))
      elif lx == 0 and ly < 0:
        self.shield_center = 270
      elif lx > 0 and ly < 0:#第4象限
        self.shield_center = 360 + math.degrees(math.atan( ly / lx ))
      else:
        self.shield_center = 0

    # print(self.shield_center)

      # self.shield_center = int(math.tan( ly / lx ))


    # else:
    #   self.shield_center = int(math.tan( 1 ))




  def draw_shield(self):

    shield_start  = self.shield_center - self.shield_size
    shield_end    = self.shield_center + self.shield_size - 1 
    # print(self.shield)
    
    # print(len(self.shield))
    # print(len(range(math.floor(shield_start),math.floor(shield_end))))

    s_index = 0
    for a in range(int(shield_start),int(shield_end)):
      b = math.radians(a)
      if 0 <= a%90 < 90:
        sx = self.x+15*math.cos(b)
        sy = self.y-15*math.sin(b)
      elif 90 <= a%90 < 180:
        sx = self.x-15*math.cos(b)
        sy = self.y-15*math.sin(b)
      elif 180 <= a%90 < 270:
        sx = self.x-15*math.cos(b)
        sy = self.y+15*math.sin(b)
      elif 270 <= a%90 < 360:
        sx = self.x+15*math.cos(b)
        sy = self.y+15*math.sin(b)
      self.shield[s_index] = ([sx,sy])
      # pyxel.pset(self.x+15*math.cos(b), self.y-15*math.sin(b), 9)
      # pyxel.line(self.x+14*math.cos(b), self.y-14*math.sin(b), self.x+15*math.cos(b), self.y-15*math.sin(b), 9)
      s_index += 1
    for s in self.shield[:len(self.shield)-1]:
      color = 7
      pyxel.pset(s[0], s[1], color)
      pyxel.pset(s[0]-1, s[1]-1, color)
      pyxel.pset(s[0]+1, s[1]-1, color)
      pyxel.pset(s[0]+1, s[1]+1, color)
      pyxel.pset(s[0]-1, s[1]+1, color)
      
      # if s[0] > 0 and s[1] > 0:
      #   pyxel.pset(s[0], s[1], 9)
      # elif s[0] < 0 and s[1] > 0:
      #   pyxel.pset(s[0], s[1], 9)
      # elif s[0] < 0 and s[1] < 0:
      #   pyxel.pset(s[0], s[1], 9)
      # elif s[0] > 0 and s[1] < 0:
      #   pyxel.pset(s[0], s[1], 9)


      

  # def deflect(self):


class Enemy:
  def __init__(self,x,y):
    global map_size
    # self.x = random.choice([random.randint(25,50),random.randint(map_size-50,map_size-25)])
    # self.y = random.choice([random.randint(25,50),random.randint(map_size-50,map_size-25)])
    self.x = x
    self.y = y
    self.noise = PerlinNoise(octaves = 10,seed = random.randint(1,100))
    self.noise_resolution = 100
    # self.noise_map = [[self.noise([i/noise_resolution,j/noise_resolution]) for i in range(1,noise_resolution)] for j in range(1,noise_resolution)]
    # self.noise_map = [[self.noise([i/self.noise_resolution, i/self.noise_resolution]) for i in range(self.noise_resolution)]]
    self.noise_index = 0

  def move(self):
    global map_size
    # print(self.noise_map[0][self.noise_index])
    noise = self.noise(self.noise_index/self.noise_resolution)
    noise2 = self.noise((self.noise_resolution-self.noise_index)/self.noise_resolution)
    self.noise_index +=1
    if self.noise_index == self.noise_resolution:
      self.noise_index = 0

    self.x += int(10*noise)
    self.y += int(10*noise2)

    if self.x >= map_size:
      self.x = map_size#-= 2*int(10*noise)
    elif self.x <= 0:
      self.x = 0
    elif self.y >= map_size:
      self.y =map_size#-= 2*int(10*noise2)
    elif self.y <= 0:
      self.y = 0

  def shoot(self,player_pos):
    px, py = player_pos
    vx = (px - self.x)
    vy = (py - self.y)
    vx = vx / max(abs(vx),abs(vy))
    vy = vy / max(abs(vx),abs(vy))

    # dx = (px - self.x) / abs(px - self.x +1)
    # dy = (py - self.y) / abs(py - self.y +1)

    projectile = Projectile(self.x+5, self.y+5, vx,vy)
    return projectile
    


class Projectile:
  def __init__(self,x,y,vx,vy,speed = 1):
    self.x = x
    self.y = y
    self.vx = vx
    self.vy = vy
    self.speed = speed

  def move(self):
    global map_size
    if self.x < 0:
      self.x = 0
      self.vx *= -1
    elif self.x > map_size:
      self.x = map_size
      self.vx *= -1
    elif self.y < 0:
      self.y = 0
      self.vy *= -1
    elif self.y > map_size:
      self.y = map_size
      self.vy *= -1

    
    self.x += self.vx
    self.y += self.vy
