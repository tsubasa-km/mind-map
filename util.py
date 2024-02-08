import pygame as pg
import copy


class Mouse:
    _is_pressed = [False,False,False]
    @classmethod
    def update(cls):
        """毎フレーム最後に更新
        """
        cls._is_pressed = copy.deepcopy(pg.mouse.get_pressed())
    @classmethod
    def up(cls):
        return [b and not a for b,a in zip(cls._is_pressed,pg.mouse.get_pressed())]
    @classmethod
    def down(cls):
        return [not b and a for b,a in zip(cls._is_pressed,pg.mouse.get_pressed())]
    @classmethod
    def pressed(cls):
        return copy.deepcopy(pg.mouse.get_pressed())

def resize_surface(surface:pg.Surface,height=None,width=None)->pg.Surface:
    if height and width:
        value = pg.transform.scale(surface,(width,height))
    elif height:
        value = pg.transform.scale(surface,(height*surface.get_width()//height, surface.get_height()))
    elif width:
        value = pg.transform.scale(surface,(surface.get_width()), height*surface.get_height()//width)
    else:
        raise ValueError()
    return value