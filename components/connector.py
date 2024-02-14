import pygame as pg
from typing import Any

from components.relationship import RelationshipManager
from util import Mouse

_Entity = Any

class Connector:
    connectors = []
    target_selecting = False
    def __init__(self,parent_entity:_Entity,direction) -> None:
        self.size = 15
        self.parent_entity = parent_entity
        self.direction = direction
        self.x:int
        self.y:int
        self.calc_position()
        self._visible = False
        self._target_selecting = False
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
        self._visible = visible if visible != None else not self._visible

    def hook_up(self,screen):
        if (self.get_rect().collidepoint(*pg.mouse.get_pos()) and
            Mouse.down()[0] and not Connector.target_selecting):
            self._target_selecting = True
            Connector.target_selecting = True
            return

        if self._target_selecting:
            RelationshipManager.selecting(self, screen)

        if (self.get_rect().collidepoint(*pg.mouse.get_pos()) and
            Mouse.down()[0] and Connector.target_selecting):
            for c in Connector.connectors:
                if not c._target_selecting:continue
                c._target_selecting = False
                Connector.target_selecting = False
                RelationshipManager.createRelationship([self,c])
                break
        
        if (Mouse.down()[2] and self._target_selecting):
            self._target_selecting = False
            Connector.target_selecting = False

    def get_rect(self)->pg.Rect:
        return pg.Rect(self.x,self.y,self.size,self.size)

    def get_visibility(self)->bool:
        return self._visible

    def draw(self, screen):
        if not self._visible:return
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
            c.hook_up(screen)
            c.calc_position()
            c.draw(screen)
    @staticmethod
    def toggleVisibility(connectors:list[Connector],visible:bool=None):
        for c in connectors:c.toggle_visibility(visible)
    @staticmethod
    def collideMouse(connectors:list[Connector]) -> bool:
        value = any([c.get_visibility() and c.get_rect().collidepoint(*pg.mouse.get_pos()) for c in connectors])
        return value