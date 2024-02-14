import pygame as pg
import sys

from components.entity import EntityManager,Entity
from components.connector import ConnectorManager,Connector
from components.relationship import RelationshipManager,Relationship
from util import Mouse

class Main:
    SCREEN_SIZE = (1000,700)
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode(self.SCREEN_SIZE)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if (event.key == pg.K_n and
                        pg.key.get_mods() & pg.KMOD_CTRL):
                        EntityManager.createEntity(*pg.mouse.get_pos(),"")
                    if (Entity.edited):
                        EntityManager.insert(event)
            self.loop()
            Mouse.update()
            pg.display.update()

    def loop(self):
        self.screen.fill((200,200,200))
        EntityManager.update(self.screen)
        ConnectorManager.update(self.screen)
        RelationshipManager.update(self.screen)

Main()