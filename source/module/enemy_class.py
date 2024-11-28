import pyxel

class Enemy:
    def __init__(self, x, y, pos, ｔ):
        self.x = x
        self.y = y
        self.cx = x
        self.cy = y
        self.pos = pos
        self.angle = 1
        self.atk_count = 0
        self.type = t
        #グリーンスライム
        if self.type == 1:
            self.move_timer = pyxel.rndi(60, 90)
            self.range = 40
            self.atk = 1
            self.hp = 25
            self.exp = 10
        #スケルトン
        elif self.type == 2:
            self.move_timer = pyxel.rndi(40, 60)
            self.range = 20
            self.atk = 2
            self.hp = 40 
            self.exp = 20           
        #グリーンリザード
        elif self.type == 3:
            self.move_timer = pyxel.rndi(40, 60)
            self.range = 20
            self.atk = 2
            self.hp = 40 
            self.exp = 20                       
        self.cannot_move = [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
                             (5, 1), (6, 1), (7, 1), (8, 1), (9, 1),
                             (11, 1)]

    def update(self):
        pass

    def move_ctl(self, px, py):
        xd = abs(self.x - px)
        xdd = self.x - px
        yd = abs(self.y - py)
        ydd = self.y - py
        if xd < self.range or yd < self.range:
            pass
        else:
            return pyxel.rndi(1, 4)
        
        if self.type in (1, 2, 3):
            if xd > yd:
                if xdd > 0:
                    return 2
                else:
                    return 1
            else:
                if ydd > 0:
                    return 3
                else:
                    return 4
        

    def chk_cell(self, c):
        print(c)
        if c in self.cannot_move:
            return False
        else:
            return True