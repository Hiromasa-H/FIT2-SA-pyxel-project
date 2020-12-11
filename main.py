import pyxel
import math
import random
from classes import *

map_size = 200

class App:
  def __init__(self,debug=False):
    global map_size
    self.enemies=[Enemy(random.randint(25,50),random.randint(25,50)),
    Enemy(random.randint(25,50),random.randint(map_size-50,map_size-25)),
    Enemy(random.randint(map_size-50,map_size-25),random.randint(25,50)),
    Enemy(random.randint(map_size-50,map_size-25),random.randint(map_size-50,map_size-25))]
    self.projectiles = []
    self.player = Player()
    self.debug = debug
    self.frame = 60 #start at 60 or -1
    self.run = False
    pyxel.init(map_size, map_size, caption="mini-project",fps=60)
    pyxel.load("test.pyxres")
    pyxel.run(self.update, self.draw)


       
  def update(self):

    if not self.run:
      if pyxel.btnp(pyxel.KEY_SPACE):
        self.run = True
     
    if self.run:
      self.frame += 1

      #move player
      if pyxel.btn(pyxel.KEY_W) and pyxel.btn(pyxel.KEY_R):
        self.player.upright()
      elif pyxel.btn(pyxel.KEY_W) and pyxel.btn(pyxel.KEY_A):
        self.player.upleft()
      elif pyxel.btn(pyxel.KEY_S) and pyxel.btn(pyxel.KEY_D):
        self.player.downright()
      elif pyxel.btn(pyxel.KEY_S) and pyxel.btn(pyxel.KEY_A):
        self.player.downleft()
      elif pyxel.btn(pyxel.KEY_W):
        self.player.up()
      elif pyxel.btn(pyxel.KEY_A):
        self.player.left()
      elif pyxel.btn(pyxel.KEY_S):
        self.player.down()
      elif pyxel.btn(pyxel.KEY_D):
        self.player.right()
      else:
        self.player.moving = False

      #move shield
      if self.player.moving == False:
        self.player.move_shield(pyxel.mouse_x,pyxel.mouse_y)

      #move enemies and shoot
      for enemy in self.enemies:
        enemy.move()
        if self.frame % 120 == 0 and len(self.projectiles) < 8:
          self.projectiles.append(enemy.shoot([self.player.x,self.player.y]))
          #spawn enemies
        if self.frame % 40 == 0 and len(self.enemies) < 4:
          if random.random() < 0.7:
            x = random.choice([random.randint(25,50),random.randint(map_size-50,map_size-25)])
            y = random.choice([random.randint(25,50),random.randint(map_size-50,map_size-25)])
            pyxel.circb(x,y,5,8)
        # if self.frame % 80 == 0:
            self.enemies.append(Enemy(x,y))


      #check for collisions. wait for 6 frames before checking, as the enemies tend to collide into their own bullets.
      if self.frame % 120 >= 18:
        self.collide()

      
      self.collide_shield()

      #move projectiles
      if len(self.projectiles) > 0:
        for projectile in self.projectiles:
          projectile.move()



    


  def collide(self):
    for projectile in self.projectiles:
      for enemy in self.enemies:
        if enemy.x-5 <= projectile.x <= enemy.x+5 and enemy.y-5 <= projectile.y <= enemy.y+5:
          self.enemies.remove(enemy)
          self.projectiles.remove(projectile)
          #self.explosions.append(Explosion)
          # print("hit")
      # for s in self.player.shield:
      #   # print(s)
      # # pyxel.pset(s[0], s[1], 9)
      # # pyxel.pset(s[0]-1, s[1]-1, 9)
      # # pyxel.pset(s[0]+1, s[1]-1, 9)
      # # pyxel.pset(s[0]+1, s[1]+1, 9)
      # # pyxel.pset(s[0]-1, s[1]+1, 9)
      #   if s[0]-3 <= projectile.x <= s[0]+3 and s[1]-3 <= projectile.y <= s[1]+3:#shield_hit(s[0],s[1],projectile.x,projectile.y):
      #     # print(projectile.vx)
      #     projectile.vx *= -1
      #     projectile.vy *= -1
      #     print("shield hit")
      #     # print(projectile.vx)

      # if self.player.x-5 <= projectile.x <= self.player.x+5 and  self.player.y-5 <= projectile.y <= self.player.y+5:
      #   self.run = False
      #   # print("game over")

  def collide_shield(self):
    for projectile in self.projectiles:
      if self.player.moving == False: 
        for s in self.player.shield:
            if s[0]-3 <= projectile.x <= s[0]+3 and s[1]-3 <= projectile.y <= s[1]+3:#shield_hit(s[0],s[1],projectile.x,projectile.y):
              # print(projectile.vx)
              projectile.vx *= -1
              projectile.vy *= -1
              # print("shield hit")

      if self.player.x-5 <= projectile.x <= self.player.x+5 and  self.player.y-5 <= projectile.y <= self.player.y+5:
        self.run = False
          # print("game over")


  def shield_hit(sx,sy,px,py):
    flag = False
    if sx-2 <= px <= sx+2 and sy-2 <= py <= sy+2:
      flag = True
    return flag


    






        

  def draw(self):
    # pyxel.cls(7) 
    pyxel.cls(0)     
    # print(self.player.moving)

    if not self.run:
      pyxel.text(map_size/2, map_size/2, "MiniGame", 7)
      pyxel.text(map_size/2, map_size/2 + 5, "space key to start", 7)
     
    if self.run:
      pyxel.circ(self.player.x, self.player.y, 5, 6)
      pyxel.circ(self.player.x, self.player.y, 4, 7)
      if self.player.moving == False: 
        self.player.draw_shield()

      for enemy in self.enemies:
        # pyxel.blt(16,16,)
        pyxel.circ(enemy.x, enemy.y, 5, 8)
        pyxel.circ(enemy.x, enemy.y, 3, 0)
        pyxel.circ(enemy.x, enemy.y, 1, 8)

      for projectile in self.projectiles:
        pyxel.circ(projectile.x, projectile.y, 2, 9)
        pyxel.circ(projectile.x, projectile.y, 1, 7)

      pyxel.circ(pyxel.mouse_x, pyxel.mouse_y, 1, 6)
      pyxel.pset(pyxel.mouse_x, pyxel.mouse_y,7)



      if self.debug:
        pyxel.line(self.player.x, self.player.y, pyxel.mouse_x, pyxel.mouse_y,1)
        pyxel.line(pyxel.mouse_x, self.player.y, pyxel.mouse_x, pyxel.mouse_y,3)
        pyxel.line(self.player.x, self.player.y, pyxel.mouse_x, self.player.y,2)
        pyxel.text(5, 5, f'xlen: {pyxel.mouse_x - self.player.x}', 0)
        pyxel.text(5, 15, f'ylen: {self.player.y -pyxel.mouse_y}', 0)
        pyxel.text(5, 25, f'degrees: {self.player.shield_center}', 0)
        pyxel.text(5, 35, f'start: {self.player.shield_center - 45}', 0)
        pyxel.text(5, 45, f'end: {self.player.shield_center + 45}', 0)
        pyxel.text(5, 55, f'rad: {math.radians(self.player.shield_center)}', 0)
      
     





if __name__ == "__main__":
  App(debug=False)

