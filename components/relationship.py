import pygame as pg
import copy
from typing import Any

_Connector = Any

class Relationship:
    relationships = []
    def __init__(self,connector:list[_Connector]|_Connector) -> None:
        if type(connector) not in [list,tuple]:
            self.connected_connectors = connector
            self.start = [None,None]
            self.end = [None,None]
            self._is_one_harf = True
            self.calc_position()
            return
        self.connected_connectors = connector
        self.start = [None,None]
        self.end = [None,None]
        self._is_one_harf = False
        self.calc_position()
        self.relationships.append(self)

    def calc_position(self):
        if self._is_one_harf:
            c = self.connected_connectors
            self.start[0],self.end[0] = [c.x + c.size//2, pg.mouse.get_pos()[0]]
            self.start[1],self.end[1] = [c.y + c.size//2, pg.mouse.get_pos()[1]]
        else:
            self.start[0],self.end[0] = [c.x + c.size//2 for c in self.connected_connectors]
            self.start[1],self.end[1] = [c.y + c.size//2 for c in self.connected_connectors]

    def draw(self,screen:pg.Surface):
        pg.draw.line(screen,(0,0,0),self.start,self.end,1)

class RelationshipManager:
    @staticmethod
    def createRelationship(connectors:list[_Connector]):
        Relationship(connectors)
    @staticmethod
    def selecting(connector:_Connector,screen:pg.Surface):
        Relationship(connector).draw(screen)
    @staticmethod
    def update(screen:pg.Surface):
        for r in Relationship.relationships:
            r.calc_position()
            r.draw(screen)