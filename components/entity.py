import pygame as pg
import copy

from util import Mouse
from time import time
from math import floor

class Entity:
    entities = []
    default_size = 100
    dragging = False
    def __init__(self,x:int,y:int,text:str="",color:pg.Color|tuple=(180,180,180),size:int=None) -> None:
        """_summary_

        Args:
            x (int): 画面上(screen surface)の座標
            y (int): 画面上(screen surface)の座標
            text (str, optional): 文字. Defaults to "".
            color (Color, tuple): ベースカラー. Defaults to (200,200,200).
            size (int, optional): 大きさ. Defaults to None.
        """
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.size = size if size!=None else self.default_size
        self.width = 2
        self.font = pg.font.Font("resource/font/irohamaru-Regular.ttf", 25)
        self._is_dragging = False
        self._drag_start = None
        self._drag_start_mouse = None
        self._editing = False
        Entity.entities.append(self)
    
    def __repr__(self) -> str:
        return f"{self.text} ({(self.x,self.y)})"

    def drag(self):
        rect = pg.Rect(self.x,self.y,self.size*2,self.size)
        if (rect.collidepoint(*pg.mouse.get_pos()) and
            Mouse.down()[1] and not Entity.dragging): # エンティティの上でクリックするとドラッグ状態にする
            self._drag_start = (self.x, self.y)
            self._drag_start_mouse = copy.deepcopy(pg.mouse.get_pos())
            self._is_dragging = True
            Entity.dragging = True
            for i,e in enumerate(Entity.entities):
                if e is self and i != 0: # 先頭にない場合
                    Entity.entities[0], Entity.entities[i] = Entity.entities[i], Entity.entities[0]

        if self._is_dragging and Mouse.up()[1]: # 解除
            self._is_dragging = False
            Entity.dragging = False
        if self._is_dragging: # ドラッグの処理
            D = [ p-s for p, s in zip(pg.mouse.get_pos(),self._drag_start_mouse) ]
            self.x = self._drag_start[0] + D[0]
            self.y = self._drag_start[1] + D[1]

    def draw(self,screen:pg.Surface):
        pg.draw.rect(screen,(255,255,255),
                     (self.x,self.y,self.size*2,self.size))
        pg.draw.rect(screen,self.color,
                     (self.x + self.width,
                      self.y + self.width,
                      self.size*2 - self.width*2,
                      self.size - self.width*2))
        text = self.font.render(self.text,True,(0,0,0))
        text_pos = [self.x+(self.size-text.get_size()[0]//2),
                    self.y+(self.size//2-text.get_size()[1]//2)]
        screen.blit(text,text_pos)
        pointer_pos = [s+t for s,t in zip([text.get_width()+2,0],text_pos)]
        if self._editing and time()%2 <= 1:
            pg.draw.rect(screen,(100,100,100),pointer_pos+[3,text.get_height()])


class EntityManager:
    @staticmethod
    def createEntity(*args, **kwargs) -> Entity:
        return Entity(*args, **kwargs)
    @staticmethod
    def updateEntities(screen):
        for e in Entity.entities:
            e.drag()
        for e in Entity.entities[::-1]:
            e.draw(screen)