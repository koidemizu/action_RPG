
class Player:
    def __init__(self, x, y, pos):
        self.x = x
        self.y = y
        self.cx = x
        self.cy = y
        self.pos = pos
        self.angle = 4
        self.level = 1
        self.exp = 0
        self.atk_count = 0
        self.atk_count_base = 10
        self.hp = 100
        self.atk = 1
        self.dfn = 1
        self.move_count_base = 5
        self.move_count = 0
        self.cannot_move = [(0, 1), (1, 1), (2, 1), (3, 1), (5, 1), (6, 1), (7, 1), (8, 1),
                            (11, 1)]
    
    def set_move_count(self):
        self.move_count = self.move_count_base

    def set_atk_count(self):
        self.atk_count = self.atk_count_base

    def update(self):
        if self.atk_count > 0:
            self.atk_count -= 1
        if self.move_count > 0:
            self.move_count -= 1

    def chk_cell(self, c):
        print(c)
        if self.move_count > 0:
            return False
        elif self.atk_count > 0:
            return False
        else:
            if c in self.cannot_move:
                return False
            else:
                return True
        
class Player_atk:
    def __init__(self, x, y, ang, pos):
        self.x = x
        self.y = y
        self.cx = x
        self.cy = y - 3
        self.angle = ang
        self.pos = pos
        if self.angle == 2:
            self.cx -= 11            
            self.pos -= 1
        elif self.angle == 1:
            self.cx += 21
            self.pos += 1
        elif self.angle == 3:
            self.cx += 20
            self.cy -= 10
            self.pos -= 254
        elif self.angle == 4:
            self.cx -= 0
            self.cy += 14
            self.pos += 254            
        
        self.atk_count = 10
    
    def update(self):
        self.atk_count -= 1
