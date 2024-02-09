import pygame as pg
from typing import Any
_Entity = Any

class Connector:
    connectors = []
    def __init__(self,parent_entity:_Entity,direction) -> None:
        self.size = 15
        self.parent_entity = parent_entity
        self.direction = direction
        self.x:int
        self.y:int
        self.calc_position()
        self.visible = False
        Connector.connectors.append(self)

    def calc_position(self):
        self.y = self.parent_entity.y + self.parent_entity.size//2 - self.size//2
        if self.direction == "Left":
            self.x = self.parent_entity.x - self.size//2
        elif self.direction == "Right":
            self.x = self.parent_entity.x + self.parent_entity.size*2 - self.size//2
        else:
            ValueError()

    def toggle_visibility(self,visible:bool=None):
        """可視性の変更

        Args:
            visible (bool, optional): None->反転. Defaults to None.
        """
        self.visible = visible if visible != None else not self.visible

    def get_rect(self)->pg.Rect:
        return pg.Rect(self.x,self.y,self.size,self.size)

    def draw(self, screen):
        if not self.visible:return
        pg.draw.rect(screen,(255,255,255),
                    (self.x,self.y,self.size,self.size))
        pg.draw.rect(screen,(0,0,0),
                    (self.x,self.y,self.size,self.size),3)


class ConnectorManager:
    @staticmethod
    def createConnector(parent_entity:_Entity) -> None:
        return (Connector(parent_entity,"Left"),Connector(parent_entity,"Right"))
    @staticmethod
    def update(screen):
        for c in Connector.connectors:
            c.calc_position()
            c.draw(screen)
    @staticmethod
    def toggleVisibility(connectors:list[Connector],visible:bool=None):
        for c in connectors:c.toggle_visibility(visible)