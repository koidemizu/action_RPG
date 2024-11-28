import pyxel

class Button:
  def __init__(self, x, y, w, h, c, t, cap=""):
      self.x = x
      self.y = y
      self.w = w
      self.h = h      
      self.c = c
      self.type = t
      self.col_cng_time = 0
      self.caption = cap
      
  def update(self):
      if self.col_cng_time > 0:
          self.col_cng_time -= 1
  
  def check_hit(self, x, y):
      if self.x <= x and (self.x + self.w) >= x:
          if self.y <= y and (self.y + self.h) >= y:
              self.col_cng_time = 7
              return self.type          

  def check_tipo(self, t):
      if t == self.type:
          self.col_cng_time = 6                     
  
  def draw(self):
      self.update()
      c = self.c
      if self.col_cng_time > 0:
          c = 1
      pyxel.rect(self.x, self.y, self.w, self.h, c)
      pyxel.rectb(self.x, self.y, self.w, self.h, 1)
      
      