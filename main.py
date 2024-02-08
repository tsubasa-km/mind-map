import pygame as pg
import sys

from components.entity import Entity, EntityManager
from util import Mouse

class Main:
    SCREEN_SIZE = (1000,700)
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode(self.SCREEN_SIZE)
        EntityManager.createEntity(100,200,"こんにちは1")
        EntityManager.createEntity(100,400,"こんにちは2")
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            self.loop()
            Mouse.update()
            pg.display.update()

    def loop(self):
        self.screen.fill((200,200,200))
        EntityManager.updateEntities(self.screen)

Main()