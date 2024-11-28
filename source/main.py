import pyxel
from module import bdfrenderer as Bdf, player_class, enemy_class, button_class, event_class

class APP:
    def __init__(self):
        pyxel.init(320, 480, display_scale=2, fps=30, quit_key=pyxel.KEY_NONE,)
        pyxel.load("assets/assets.pyxres")          
        self.status_set()
        #日本語表示用        
        self.bdf = Bdf.BDFRenderer("./assets/font/umplus_j10r.bdf")        
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def status_set(self):
        self.cells = []
        self.effects = []
        self.enemys = []
        i = 0
        #プレイヤーのインスタンスをセット
        self.player = player_class.Player(0, 0, 259*2+8)     
        
        #タイルマップを走破してセルのインスタンスを作る
        for c1 in range(60):
            for c2 in range(255):
                tile = pyxel.tilemaps[0].pget(c2, c1)
                #障害物がある場合はステータスセット
                #灰色ブロック_大
                if tile == (0, 1):
                    o = 1
                    osize = (32, 32)
                #灰色ブロック_小
                elif tile == (1, 1):
                    o = 2
                    osize = (32, 32)
                #オレンジブロック_大
                elif tile == (2, 1):
                    o = 3
                    osize = (32, 32)
                #オレンジブロック_小
                elif tile == (3, 1):
                    o = 4
                    osize = (32, 32)
                #オレンジ門                                        
                elif tile == (4, 1):
                    o = 5
                    osize = (32, 32)                    
                #オレンジブロック_小_紙
                elif tile == (5, 1):
                    o = 6
                    osize = (32, 32)   
                #オレンジブロック_掲示板1
                elif tile == (6, 1):
                    o = 7
                    osize = (32, 32)   
                #オレンジブロック_掲示板2
                elif tile == (7, 1):
                    o = 8
                    osize = (32, 32)   
                #オレンジブロック_掲示板3
                elif tile == (8, 1):
                    o = 9
                    osize = (32, 32)  
                #灰色門
                elif tile == (9, 1):
                    o = 10
                    osize = (32, 32)                                                               
                #ギルド受付
                elif tile == (10, 1):
                    o = 11
                    osize = (32, 32)         
                #墓石
                elif tile == (11, 1):
                    o = 12
                    osize = (32, 32)                                             
                #地面                 
                elif tile == (0, 0):
                    o = 0
                    osize = (0, 0)      
                #黒い地面
                elif tile == (1, 0):
                    o = 99
                    osize = (0, 0)                      
                #はしご
                elif tile == (2, 0):
                    o = 98
                    osize = (0, 0)
                #敵出現タイルの場合はEnemyインスタンスをセット
                #グリーンスライム
                elif tile == (0, 2):
                    o = 0
                    osize = (0, 0)    
                    self.enemys.append(enemy_class.Enemy(0, 0, i, 1))
                #スケルトン
                elif tile == (1, 2):
                    o = 0
                    osize = (0, 0)                        
                    self.enemys.append(enemy_class.Enemy(0, 0, i, 2))                        
                #グリーンリザード
                elif tile == (2, 2):
                    o = 0
                    osize = (0, 0)                        
                    self.enemys.append(enemy_class.Enemy(0, 0, i, 3))         

                #実際のCellインスタンス作成部分
                self.cells.append(Cell(c2, c1, i, 0+c2*16, 0+c1*16, o, osize))
                i += 1
        #その他変数
        self.player_atk = []
        self.camera_x = 0
        self.camera_y = 0
        self.camera_y = 28*16
        self.chk_p_pos()
        self.chk_e_pos()
        self.dith = 1.0
        self.dith_speed = 0.1
        self.game_status = 0
        self.buttons = []
        self.buttons.append(button_class.Button(50, 385, 40, 37, 6, 1, "UP"))
        self.buttons.append(button_class.Button(50, 440, 40, 37, 6, 2, "DOWN"))
        self.buttons.append(button_class.Button(5, 412, 40, 37, 6, 3, "LEFT"))
        self.buttons.append(button_class.Button(95, 412, 40, 37, 6, 4, "RIGHT"))
        self.buttons.append(button_class.Button(245, 412, 70, 50, 8, 5, "ACTION"))
        self.buttons.append(button_class.Button(155, 412, 70, 50, 13, 6, "CANCEL"))
        self.hit_button = 0        
        self.events = event_class.Event()
        self.event_mode = True
        self.event_number = (100, 100)
        self.message = []
        self.quest_number = [1, 2, 3]
        self.quest_number_sel = 0
        self.quest_number_tgt = [0, 0]                        
        #print(self.cells)

    def update(self):        
        if self.dith < 1.0:
            self.dith += self.dith_speed        
        #コントロール部分###########################################################################################
        #マウス位置によって画面のどのボタンが押されたかを取得############
        self.hit_button = 0
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.chk_button()

        elif pyxel.btnp(pyxel.KEY_D):
             self.hit_button = 4
            
        elif pyxel.btnp(pyxel.KEY_A):
             self.hit_button = 3

        elif pyxel.btnp(pyxel.KEY_W):
             self.hit_button = 1

        elif pyxel.btnp(pyxel.KEY_S):
             self.hit_button = 2

        elif pyxel.btnp(pyxel.KEY_L):
             self.hit_button = 5

        elif pyxel.btnp(pyxel.KEY_K):
             self.hit_button = 6             
        
        #ボタンの表示更新処理########################################
        for b in self.buttons:
            b.check_tipo(self.hit_button)

        #イベントフラグによって処理分岐
        if self.event_mode == True:
            self.event_update()
        else:
            self.game_update()

    def event_update(self):
        #押されているボタンによって処理を変える#################################################
        #ギルドの受付
        if self.event_number == (5, 1):
            if self.hit_button == 4:
                pass
            elif self.hit_button == 3:
                pass
            elif self.hit_button == 1:
                pass
            elif self.hit_button == 2:
                pass
            elif self.hit_button == 5:
                self.event_mode = False
            elif self.hit_button == 6:
                pass
        #依頼掲示板1
        elif self.event_number == (6, 1):
            if self.hit_button == 4:
                pass
            elif self.hit_button == 3:
                pass
            elif self.hit_button == 1:
                pass
            elif self.hit_button == 2:
                pass
            elif self.hit_button == 5:
                self.event_mode = False
                self.quest_number_sel = self.quest_number[0]
                self.quest_number_tgt = [1, 10]
            elif self.hit_button == 6:
                self.event_mode = False
        #依頼掲示板2
        elif self.event_number == (7, 1):
            if self.hit_button == 4:
                pass
            elif self.hit_button == 3:
                pass
            elif self.hit_button == 1:
                pass
            elif self.hit_button == 2:
                pass
            elif self.hit_button == 5:
                self.event_mode = False
                self.quest_number_sel = self.quest_number[1]
                self.quest_number_tgt = [2, 1]
            elif self.hit_button == 6:
                self.event_mode = False    
        #依頼掲示板3                
        elif self.event_number == (8, 1):
            if self.hit_button == 4:
                pass
            elif self.hit_button == 3:
                pass
            elif self.hit_button == 1:
                pass
            elif self.hit_button == 2:
                pass
            elif self.hit_button == 5:
                self.event_mode = False
                self.quest_number_sel = self.quest_number[2]
                self.quest_number_tgt = [3, 10]
            elif self.hit_button == 6:
                self.event_mode = False
        #タイトルスクリーン
        elif self.event_number == (100, 100):
            if self.hit_button in (1, 2, 3, 4, 5, 6):
                self.event_number = (101, 101)
                self.dith = 0
                self.dith_speed = 0.025   
        #プロローグ1                    
        elif self.event_number == (101, 101):
            if self.hit_button in (1, 2, 3, 4, 5, 6) and self.dith >= 1:
                self.event_number = (102, 102)    
                self.dith = 0
                self.dith_speed = 0.05                   
        #プロローグ2                    
        elif self.event_number == (102, 102):
            if self.hit_button in (1, 2, 3, 4, 5, 6) and self.dith >= 1:
                self.event_number = (103, 103)    
                self.dith = 0
                self.dith_speed = 0.05                                                           
        #プロローグ3                    
        elif self.event_number == (103, 103):
            if self.hit_button in (1, 2, 3, 4, 5, 6) and self.dith >= 1:
                self.event_mode = False
                self.camera_y = 0
                self.dith = 0
                self.dith_speed = 0.05              
        else:
            pass

    def game_update(self):
        #押されているボタンによって処理を変える#################################################
        if self.hit_button == 4:
            if self.player.chk_cell(pyxel.tilemaps[0].pget(self.player.cx+1, self.player.cy)):
                self.player.set_move_count()
                self.player.pos += 1
                self.player.angle = 1
                self.chk_p_pos()
                if self.player.x >= self.camera_x + 320:
                    self.camera_x += 320                               
                    self.dith = 0
                    self.dith_speed = 0.1
            else:
                if self.events.chk_event(pyxel.tilemaps[0].pget(self.player.cx+1, self.player.cy))                    :
                    self.event_mode = True                    
                    self.event_number = pyxel.tilemaps[0].pget(self.player.cx+1, self.player.cy)

        elif self.hit_button == 3:
            if self.player.chk_cell(pyxel.tilemaps[0].pget(self.player.cx-1, self.player.cy)):
                self.player.set_move_count()
                self.player.pos -= 1
                self.player.angle = 2
                self.chk_p_pos()
                if self.player.x < self.camera_x:
                    self.camera_x -= 320                       
                    self.dith = 0    
                    self.dith_speed = 0.1
            else:
                if self.events.chk_event(pyxel.tilemaps[0].pget(self.player.cx-1, self.player.cy)):
                    self.event_mode = True
                    self.event_number = pyxel.tilemaps[0].pget(self.player.cx-1, self.player.cy)

        elif self.hit_button == 1:
            if self.player.chk_cell(pyxel.tilemaps[0].pget(self.player.cx+1, self.player.cy-1)):
                self.player.set_move_count()
                self.player.pos -= 254
                self.chk_p_pos()
                self.player.angle = 3
                if self.player.x >= self.camera_x + 320:
                    self.camera_x += 320                             
                    self.dith = 0
                    self.dith_speed = 0.1
            else:
                if self.events.chk_event(pyxel.tilemaps[0].pget(self.player.cx+1, self.player.cy-1)):
                    self.event_mode = True
                    self.event_number = pyxel.tilemaps[0].pget(self.player.cx+1, self.player.cy-1)

        elif self.hit_button == 2:
            if self.player.chk_cell(pyxel.tilemaps[0].pget(self.player.cx-1, self.player.cy+1)):
                self.player.set_move_count()
                self.player.pos += 254
                self.chk_p_pos()
                self.player.angle = 4
                if self.player.x < self.camera_x:
                    self.camera_x -= 320                       
                    self.dith = 0    
                    self.dith_speed = 0.1
            else:
                if self.events.chk_event(pyxel.tilemaps[0].pget(self.player.cx-1, self.player.cy+1)):
                    self.event_mode = True
                    self.event_number = pyxel.tilemaps[0].pget(self.player.cx-1, self.player.cy+1)

        elif self.hit_button == 5:
            if self.player.atk_count < 1:
                self.player.set_atk_count()
                self.player_atk.append(player_class.Player_atk(self.player.x, self.player.y, self.player.angle, self.player.pos))
        #############################################################################################################

        #クエストアクティブの場合ターゲット数のチェック
        if self.quest_number_sel > 0:
            #ターゲットをすべて倒していた場合はクエストクリアにする
            if self.quest_number_tgt[1] < 1:
                self.quest_number_sel = 0
        #プレイヤーのアップデート
        self.player.update()     
        #レベルアップ処理
        if self.player.exp > self.player.level*100*0.05:
            self.player.level += 1
            self.effects.append(Effect(self.player.x-3, self.player.y-8, 30, 4, "LEVEL UP"))
        #プレイヤーの攻撃マスのアップデート  
        for pa in self.player_atk:
            pa.update()
            #存在判定時間が経過したら消す
            if pa.atk_count < 1:
                self.player_atk.remove(pa)

        #敵のアップデート
        for e in self.enemys:
            #動作待ち時間が経過したら敵を動かす
            if pyxel.frame_count % e.move_timer == 0:
                t = e.move_ctl(self.player.x, self.player.y)
                self.e_move(t, e)
            #プレイヤーと同じマスに入ったら攻撃
            if e.pos == self.player.pos:
                self.player.hp -= e.atk
                self.effects.append(Effect(self.player.x, self.player.y, 2, 1))
            #プレイヤーの攻撃と同じマスに入ったらダメージ
            for pa2 in self.player_atk:
                if pa2.pos == e.pos:
                    e.hp -= self.player.atk
                    self.effects.append(Effect(e.x, e.y, 2, 2))
            #体力がなくなったら消す
            if e.hp < 1:
                #クエストアクティブの場合ターゲットだったら数を減らす
                if self.quest_number_sel > 0:
                    if e.type == self.quest_number_tgt[0]:
                        self.quest_number_tgt[1] -= 1
                self.player.exp += e.exp
                self.effects.append(Effect(e.x, e.y-8, 20, 3, e.exp))
                self.enemys.remove(e)
        #動作後の敵位置修正
        self.chk_e_pos()
    
        #エフェクトのアップデート
        for ef in self.effects:
            ef.update()
            if ef.timer < 1:
                self.effects.remove(ef)

    def chk_p_pos(self):
        for c in self.cells:
            if c.n == self.player.pos:
                self.player.x = c.x2
                self.player.y = c.y2
                self.player.cx = c.x
                self.player.cy = c.y

    def chk_e_pos(self):
        for c in self.cells:
            for e in self.enemys:
                if c.n == e.pos:
                    e.x = c.x2
                    e.y = c.y2
                    e.cx = c.x
                    e.cy = c.y          

    #押下ボタン判別関数#####################################
    def chk_button(self):
        self.hit_button = 0
        if pyxel.MOUSE_BUTTON_LEFT:
            for b in self.buttons:
                if b.check_hit(pyxel.mouse_x, pyxel.mouse_y):
                    self.hit_button = b.check_hit(pyxel.mouse_x, pyxel.mouse_y)
                else:
                    if self.hit_button > 0:
                        pass
                    else:
                        self.hit_button = 0                                       


    def e_move(self, t, e):
        if t == 1:
            if e.chk_cell(pyxel.tilemaps[0].pget(e.cx+1, e.cy)):
                e.pos += 1
                e.angle = 1                
            
        elif t == 2:
            if e.chk_cell(pyxel.tilemaps[0].pget(e.cx-1, e.cy)):
                e.pos -= 1
                e.angle = 2
                
        elif t == 3:
            if e.chk_cell(pyxel.tilemaps[0].pget(e.cx+1, e.cy-1)):
                e.pos -= 254
                
        elif t == 4:
            if e.chk_cell(pyxel.tilemaps[0].pget(e.cx-1, e.cy+1)):
                e.pos += 254
                            
    def draw(self):
        pyxel.cls(0)        
        pyxel.camera(self.camera_x, self.camera_y)
        pyxel.dither(self.dith)

        for bc in self.cells:     
            pyxel.blt(bc.x2, bc.y2, 0, 0, 0, 32, 16, 15)       

        #各セルを走破して障害物を描画_プレイヤーが入れないオブジェクト##########
        for c in self.cells:                                    
            if c.obj == 1:
                pyxel.blt(c.x2, c.y2-16, 0, 0, 96, c.o_size[0], c.o_size[1], 15)
            elif c.obj == 2:
                pyxel.blt(c.x2, c.y2-16, 0, 32, 96, c.o_size[0], c.o_size[1], 15)                
            elif c.obj == 3:
                pyxel.blt(c.x2, c.y2-16, 0, 0, 128, c.o_size[0], c.o_size[1], 15)
            elif c.obj == 4:
                pyxel.blt(c.x2, c.y2-16, 0, 32, 128, c.o_size[0], c.o_size[1], 15)                                                         
            elif c.obj == 6:
                pyxel.blt(c.x2, c.y2-16, 0, 96, 128, c.o_size[0], c.o_size[1], 15)                                                                         
            elif c.obj == 7:
                pyxel.blt(c.x2, c.y2-16, 0, 0, 160, c.o_size[0], c.o_size[1], 15)    
            elif c.obj == 8:
                pyxel.blt(c.x2, c.y2-16, 0, 32, 160, c.o_size[0], c.o_size[1], 15)          
            elif c.obj == 9:
                pyxel.blt(c.x2, c.y2-16, 0, 64, 160, c.o_size[0], c.o_size[1], 15)                                              
            elif c.obj == 11:
                pyxel.blt(c.x2, c.y2-16, 0, 128, 128, c.o_size[0], c.o_size[1], 15)               
            elif c.obj == 12:
                pyxel.blt(c.x2, c.y2-16, 0, 96, 160, c.o_size[0], c.o_size[1], 15)      
            elif c.obj == 99:                                          
                pyxel.blt(c.x2, c.y2, 0, 32, 0, 32, 16, 15)        
            elif c.obj == 98:                                          
                pyxel.blt(c.x2, c.y2, 0, 0, 16, 32, 16, 15)                                      
          
        #敵の描画###########################################################
            for e in self.enemys:
                if c.n == e.pos:
                    if e.angle == 2:
                        pyxel.blt(e.x+5, e.y-3, 1, -16 + e.type*16, 32, 16, 16, 15)  
                    elif e.angle == 1:
                        pyxel.blt(e.x+5, e.y-3, 1, -16 + e.type*16, 48, 16, 16, 15)  

        #プレイヤーの描画####################################################
            if c.n == self.player.pos:
                if self.player.angle == 2:
                    if self.player.atk_count > 0:
                        pyxel.blt(self.player.x+5, self.player.y-3, 1, 16, 0, 16, 16, 15)    
                        for p in self.player_atk:
                            pyxel.blt(p.cx, p.cy, 1, 32, 0, 16, 16, 15)                                
                    else:
                        pyxel.blt(self.player.x+5, self.player.y-3, 1, 0, 0, 16, 16, 15)
                elif self.player.angle == 1:
                    if self.player.atk_count > 0:
                        pyxel.blt(self.player.x+5, self.player.y-3, 1, 16, 16, 16, 16, 15) 
                        for p in self.player_atk:
                            pyxel.blt(p.cx, p.cy, 1, 32, 16, 16, 16, 15)    
                    else:
                        pyxel.blt(self.player.x+5, self.player.y-3, 1, 0, 16, 16, 16, 15)      
                elif self.player.angle == 3:
                    if self.player.atk_count > 0:
                        pyxel.blt(self.player.x+5, self.player.y-3, 1, 64, 16, 16, 16, 15) 
                        for p in self.player_atk:
                            pyxel.blt(p.cx, p.cy, 1, 80, 16, 16, 16, 15)    
                    else:
                        pyxel.blt(self.player.x+5, self.player.y-3, 1, 48, 16, 16, 16, 15)                              
                elif self.player.angle == 4:
                    if self.player.atk_count > 0:
                        pyxel.blt(self.player.x+5, self.player.y-3, 1, 64, 0, 16, 16, 15) 
                        for p in self.player_atk:
                            pyxel.blt(p.cx, p.cy, 1, 80, 0, 16, 16, 15)    
                    else:
                        pyxel.blt(self.player.x+5, self.player.y-3, 1, 48, 0, 16, 16, 15)            
            
            #各セルを走破して障害物を描画_プレイヤーと重ねるオブジェクト##################
            if c.obj == 5:
                pyxel.blt(c.x2, c.y2-16, 0, 64, 128, c.o_size[0], c.o_size[1], 15)                                                                       
            elif c.obj == 10:
                pyxel.blt(c.x2, c.y2-16, 0, 64, 96, c.o_size[0], c.o_size[1], 15)         
                
            #エフェクトの描画#########################################################
            for ef in self.effects:
                if ef.type == 1:
                    pyxel.blt(ef.x + 5, ef.y, 2, 0, 24, 16, 16, 15)
                elif ef.type == 2:
                    pyxel.blt(ef.x + 5, ef.y, 2, 16, 24, 16, 16, 15)    
                elif ef.type == 3:
                    pyxel.text(ef.x-1, ef.y+1, "EXP:" + str(ef.text), 1)
                    pyxel.text(ef.x, ef.y, "EXP:" + str(ef.text), 7)    
                elif ef.type == 4:
                    pyxel.text(ef.x-1, ef.y+1, str(ef.text), 1)
                    pyxel.text(ef.x, ef.y, str(ef.text), 7)                                            
        
        #各種ステータス表示部分
        pyxel.camera(0, 0)
        pyxel.rect(0, 0, 102, 8, 0)
        pyxel.rect(3, 3, self.player.hp, 6, 0)
        pyxel.rect(1, 1, self.player.hp, 6, 8)        
        pyxel.text(1, 1, str(self.player.x)+","+str(self.player.y), 8)
        pyxel.text(200, 1, str(self.quest_number_sel), 8)
        pyxel.text(105, 3, "LEVEL:"+str(self.player.level), 0)
        pyxel.text(107, 1, "LEVEL:"+str(self.player.level), 1)
        pyxel.text(106, 2, "LEVEL:"+str(self.player.level), 7)
        #クエストアクティブの場合はターゲットを表示する
        if self.quest_number_sel > 0:
            pyxel.rect(200, 0, 150, 16, 0)
            pyxel.rectb(200, 0, 150, 16, 1)
            self.bdf.draw_text(202, 2, "TARGET:", 7)                        
            pyxel.blt(245, 0, 1, -16 + self.quest_number_tgt[0]*16, 32, 16, 16, 15)
            self.bdf.draw_text(265, 2, "x " + str(self.quest_number_tgt[1]), 7)

        #コントローラー表示部分
        pyxel.rect(0, 384, 320, 100, 0)
        pyxel.rectb(0, 383, 320, 97, 1)
        for b in self.buttons:
            b.draw()
            self.bdf.draw_text(int(b.x + 5), int(b.y + (b.h/2-3)), b.caption, 0)
    
        #イベントウィンドウ
        if self.event_mode == True:            
            if self.event_number == (5, 1):
                self.message = [
                    "ここは冒険者たちのギルドです。",
                    "隣の掲示板から受注する依頼を選択してください。",
                ]
                pyxel.rect(25, 25, 260, 300, 0)
                pyxel.rectb(25, 25, 260, 300, 7)
                pyxel.rectb(25, 25, 260, 45, 7)
                self.bdf.draw_text(200, 305, "ACTION:YES", 8)
                #self.bdf.draw_text(45, 305, "CANCEL:NO", 13)
                mc = 0
                self.bdf.draw_text(180, 55, "ギルドの受付", 7)
                for m in self.message:
                    self.bdf.draw_text(45, 80 + mc*20, m, 7)
                    mc += 1
            elif self.event_number == (6, 1):
                self.message = [
                    "依頼名：グリーンスライムの討伐",
                    "目的：グリーンスライム10体の討伐",
                    "依頼人：王都探検隊の副長",
                    "我々王都探検隊は地下遺跡の調査を進めているが、",
                    "グリーンスライムによる人的被害が発生している。",
                    "探検隊には武官が少数しか随行していないため、",
                    "冒険者の手を借りたい。",
                    "遺跡のグリーンスライムを10体討伐してほしい。"
                ]
                pyxel.rect(25, 25, 260, 300, 0)
                pyxel.rectb(25, 25, 260, 300, 7)
                pyxel.rectb(25, 25, 260, 45, 7)
                self.bdf.draw_text(200, 305, "ACTION:YES", 8)
                self.bdf.draw_text(45, 305, "CANCEL:NO", 13)
                mc = 0
                self.bdf.draw_text(180, 55, "依頼掲示板", 7)
                for m in self.message:
                    self.bdf.draw_text(45, 80 + mc*20, m, 7)
                    mc += 1                    
            elif self.event_number == (7, 1):
                self.message = [
                    "依頼名：スケルトンの討伐",
                    "目的：スケルトン10体の討伐",
                    "依頼人：遺跡の行商人",
                    "私はいつも地下遺跡の墓地区画を通って",
                    "その先の『紫紺の花畑』へ行っている。",
                    "貴重な染料のもとになる植物があるのでね。",
                    "ところが最近になって墓地区画をスケルトンが",
                    "うろつくようになった。私は商人だから荒事は",
                    "苦手なんだ。",
                    "腕に自信のある冒険者の助けを借りたい。"
                ]
                pyxel.rect(25, 25, 260, 300, 0)
                pyxel.rectb(25, 25, 260, 300, 7)
                pyxel.rectb(25, 25, 260, 45, 7)
                self.bdf.draw_text(200, 305, "ACTION:YES", 8)
                self.bdf.draw_text(45, 305, "CANCEL:NO", 13)
                mc = 0
                self.bdf.draw_text(180, 55, "依頼掲示板", 7)
                for m in self.message:
                    self.bdf.draw_text(45, 80 + mc*20, m, 7)
                    mc += 1                                        
            elif self.event_number == (8, 1):
                self.message = [
                    "依頼名：グリーンリザードの討伐",
                    "目的：グリーンリザード10体の討伐",
                    "依頼人：都の武具職人",
                    "地下遺跡に生息するグリーンリザードの",
                    "討伐を依頼したい。",
                    "やつの皮革は防具の素材に最適なのだ。",
                    "キリよく10体、よろしく頼む。",                    
                ]
                pyxel.rect(25, 25, 260, 300, 0)
                pyxel.rectb(25, 25, 260, 300, 7)
                pyxel.rectb(25, 25, 260, 45, 7)
                self.bdf.draw_text(200, 305, "ACTION:YES", 8)
                self.bdf.draw_text(45, 305, "CANCEL:NO", 13)
                mc = 0
                self.bdf.draw_text(180, 55, "依頼掲示板", 7)
                for m in self.message:
                    self.bdf.draw_text(45, 80 + mc*20, m, 7)
                    mc += 1                                                            
            elif self.event_number == (100, 100):
                
                self.message = [
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",                    
                ]
                pyxel.rect(1, 1, 318, 300, 0)
                pyxel.rectb(1, 1, 318, 300, 7)
                pyxel.rectb(1, 1, 318, 45, 7)
                self.bdf.draw_text(80, 305, "...何かキーを押してください...", 7)                
                mc = 0
                self.bdf.draw_text(180, 55, "タイトル画面", 7)
                for m in self.message:
                    self.bdf.draw_text(45, 80 + mc*20, m, 7)
                    mc += 1                                                        
            elif self.event_number == (101, 101):                                                           
                self.message = [
                    "王都の地下に発見された古代の遺跡。",
                    "そこはいつのころからか財宝目当ての冒険家や、",
                    "神秘を探求する研究者の探検の場と化していた。",
                    "あなたもまた、何か見つけるべきものがあって",
                    "この地下世界の入り口までやってきた一人である。",            
                ]
                pyxel.rect(25, 195, 265, 150, 0)
                pyxel.rectb(25, 195, 265, 150, 7)
                pyxel.rectb(25, 195, 265, 45, 7)
                self.bdf.draw_text(80, 355, "...何かキーを押してください...", 7)                
                mc = 0
                #self.bdf.draw_text(180, 220, "白面の男", 7)
                for m in self.message:
                    self.bdf.draw_text(45, 250 + mc*20, m, 7)
                    mc += 1                                  
            elif self.event_number == (102, 102):
                pyxel.blt(180, 78, 1, 96, 0, 16, 16, 15)
                pyxel.blt(198, 67, 1, 0, 0, 16, 16, 15)                                                      

                self.message = [
                    "しかしあんたも物好きだね。",
                    "地下に潜るのは結構だが、今は時期が悪い。",
                    "先月案内したやつも結局行方知れずさ...。",
                    "",
                    "",
                    "",
                    "",                    
                ]
                pyxel.rect(25, 195, 265, 150, 0)
                pyxel.rectb(25, 195, 265, 150, 7)
                pyxel.rectb(25, 195, 265, 45, 7)
                self.bdf.draw_text(80, 355, "...何かキーを押してください...", 7)                
                mc = 0
                self.bdf.draw_text(180, 220, "白面の男", 7)
                #pyxel.blt(20, 200, 1, 112, 0, 32, 24)
                for m in self.message:
                    self.bdf.draw_text(45, 250 + mc*20, m, 7)
                    mc += 1                                                                                                                                                         
            elif self.event_number == (103, 103):
                pyxel.blt(143, 112, 1, 96, 0, 16, 16, 15)
                pyxel.blt(158, 125, 1, 0, 0, 16, 16, 15) 

                self.message = [
                    "まぁ私はお代がいただければそれでいいんだが...。",
                    "",
                    "さ、案内できるのはここまでだ。",
                    "あんまり深入りせずに戻ることだよ。",
                    "「命あっての物種」ともいうだろう？",
                    "",
                    "",                    
                ]
                pyxel.rect(25, 195, 265, 150, 0)
                pyxel.rectb(25, 195, 265, 150, 7)
                pyxel.rectb(25, 195, 265, 45, 7)
                self.bdf.draw_text(80, 355, "...何かキーを押してください...", 7)                
                mc = 0
                self.bdf.draw_text(180, 220, "白面の男", 7)
                for m in self.message:
                    self.bdf.draw_text(45, 250 + mc*20, m, 7)
                    mc += 1                                                                          
            else:
                pass
            

class Cell:
    def __init__(self, x, y, n, x2, y2 ,o=0, o_size=(0, 0)):
        self.x = x
        self.y = y
        self.n = n
        self.x2 = x2
        self.y2 = y2
        self.graund = 0
        self.obj = o
        self.o_size = o_size



class Effect:
    def __init__(self, x, y, t, type, txt=""):
        self.x = x
        self.y = y
        self.timer = t
        self.type = type
        self.text = txt
    
    def update(self):
        self.timer -= 1



APP()
