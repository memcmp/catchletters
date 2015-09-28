import pyglet
import cocos
import os
import string
import random

from cocos.actions import *

here = os.path.abspath(os.path.dirname(__file__))
images = os.path.join(here, 'sprites')

import pyglet.resource
pyglet.resource.path = [images]
pyglet.resource.reindex()


def width():
    return cocos.director.director.window.width


def height():
    return cocos.director.director.window.height


class CatchLetters(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self, cat_layer, letter_layer):
        super(CatchLetters, self).__init__(255, 255, 255, 255)
        self.cat_layer = cat_layer
        self.letter_layer = letter_layer
        self.wrong_answ = 0
        self.true_answ = 0
        self.schedule(self.move_letter)

        # 0 = finished; 1 = running
        self.game_state = 1
        self.keys_after_finished = 0

    def on_text(self, key):
        if self.game_state >= 1:
            if self.letter_layer.random_letter == key:
                self.letter_layer.update()
                self.cat_layer.next_cat()
                self.true_answ += 1
            else:
                self.wrong_answ += 1
                if self.wrong_answ >= 3:
                    self.cat_layer.show_dead_cat()
                    self.game_state = -1
            if self.true_answ >= 6:
                self.cat_layer.show_happy_cat()
                self.letter_layer.remove(self.letter_layer.text)
                self.game_state = 0

    def move_letter(self, dt):
        if self.game_state >= 1:
            if self.letter_layer.text.position[1] >= height():
                self.cat_layer.show_dead_cat()
            else:
                self.letter_layer.text.do(MoveBy((0, 50), duration=0.4))


class LetterDisplay(cocos.layer.Layer):

    def __init__(self):
        super(LetterDisplay, self).__init__()
        self.move_step = 10
        self.move_speed = 0.1
        self.text = cocos.text.Label('', font_size=40, x=100, y=0, color=(0, 0, 0, 255))
        self.update()
        self.add(self.text)

    def update(self):
        self.random_letter = random.choice(string.ascii_letters.lower())
        self.text.element.text = self.random_letter


class CatDisplay(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):
        super(CatDisplay, self).__init__()
        self.cat_paths = ['cat_dance_01', 'cat_dance_02', 'cat_dance_03', 'cat_dance_04']
        self.catidx = -1
        self.cat = None
        self.next_cat()
        self.finished = False

    def next_cat(self):
        self.catidx += 1
        if self.catidx == len(self.cat_paths):
            self.catidx = 0
        if self.cat:
            self.remove(self.cat)
        self.cat = cocos.sprite.Sprite(self.cat_paths[self.catidx] + '.png')
        self.cat.position = width() / 2, height() / 2
        self.cat.scale = 1
        self.add(self.cat)

    def show_dead_cat(self):
        self.finished = True
        self.remove(self.cat)
        self.cat = cocos.sprite.Sprite('cat_dead.png')
        self.cat.position = width() / 2, height() / 2
        self.cat.scale = 2
        self.add(self.cat)

    def show_happy_cat(self):
        self.finished = True
        self.remove(self.cat)
        self.cat = cocos.sprite.Sprite('happy_cat.png')
        self.cat.position = width() / 2, height() / 2
        self.cat.scale = 0.3
        self.add(self.cat)

    def on_key_release(self, key, modifiers):
        if self.finished is True and (key == pyglet.window.key.ENTER or
                                key == pyglet.window.key.SPACE):
            run()


class CatchLettersGame():

    def __init__(self, exit_callback):
        self.cat = CatDisplay()
        self.letter = LetterDisplay()
        self.scene = CatchLetters(self.cat, self.letter, exit_callback)

    def main_scene(self):
        return cocos.scene.Scene(self.scene, self.letter, self.cat)


def run():
    cat = CatDisplay()
    letter = LetterDisplay()
    main_scene = CatchLetters(cat, letter)
    cocos.director.director.run(cocos.scene.Scene(main_scene, letter, cat))


def main():
    cocos.director.director.init(width=800, height=640)
    run()

if __name__ == '__main__':
    main()
