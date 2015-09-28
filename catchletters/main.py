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

SPEED = 1000
LIVES = 5


def width():
    return cocos.director.director.window.width


def height():
    return cocos.director.director.window.height


class CatchLetters(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self):
        super(CatchLetters, self).__init__(255, 255, 255, 255)
        self.speed = SPEED
        self.cat_layer = CatDisplay()
        self.add(self.cat_layer)

        self.letters = []
        self.wrong_answ = 0
        self.true_answ = 0
        self.parallel_letters = 1
        self.mod = 5

        # 0 = finished; 1 = running
        self.game_state = 1
        self.keys_after_finished = 0
        self.schedule(self.create_letters)
        self.score = None
        self.lives = None
        self.update_score()

    def move_speed(self):
        return width() / (self.speed * 10.0)

    def create_letter(self):
        letter_layer = LetterDisplay(self.move_speed(), self)
        self.letters.append(letter_layer)
        self.add(letter_layer)

    def create_letters(self, dt):
        if len(self.letters) < self.parallel_letters:
            self.create_letter()

    def correct(self, key):
        for letter in self.letters:
            if letter.random_letter == key:
                return letter
        return None

    def remove_letter(self, letter):
        self.remove(letter)
        self.letters.remove(letter)

    def cleanup(self):
        self.parallel_letters = 0
        for letter in self.letters:
            self.remove_letter(letter)

    def on_text(self, key):
        if self.game_state >= 1:
            letter = self.correct(key)
            if letter:
                self.true_answ += 1
                self.cat_layer.next_cat()
                self.remove_letter(letter)
                self.speed += 20
                if self.true_answ % self.mod == 0:
                    self.mod += 20
                    self.parallel_letters += 1
            else:
                self.wrong_answ += 1
                self.check_finish()
        self.update_score()

    def failed(self, letter):
        self.remove_letter(letter)
        self.wrong_answ += 1
        self.check_finish()

    def update_score(self):
        if self.score:
            self.remove(self.score)
            self.remove(self.lives)
        self.score = cocos.text.Label('Score: {}'.format(self.true_answ * 100), font_size=20, x=10, y=height() - 20, color=(255, 0, 0, 255))
        self.lives = cocos.text.Label('Lives: {}'.format(LIVES - self.wrong_answ), font_size=20, x=width() - 100, y=height() - 20, color=(255, 0, 0, 255))
        self.add(self.score)
        self.add(self.lives)

    def check_finish(self):
        self.update_score()
        if self.wrong_answ >= LIVES:
            self.cleanup()
            if self.true_answ > 50:
                self.cat_layer.show_happy_cat()
            else:
                self.cat_layer.show_dead_cat()
            self.game_state = -1


class LetterDisplay(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self, speed, callback):
        super(LetterDisplay, self).__init__()
        self.callback = callback
        self.speed = speed
        self.text = cocos.text.Label('', font_size=40, x=random.randint(0, width() - 40), y=0, color=(0, 0, 0, 255))
        self.update()
        self.add(self.text)
        self.schedule(self.move_letter)

    def update(self):
        self.random_letter = random.choice(string.ascii_letters.lower())
        self.text.element.text = self.random_letter.upper()

    def move_letter(self, dt):
        if self.text.position[1] >= height():
            self.callback.failed(self)
        else:
            self.text.do(MoveBy((0, 10), duration=self.speed))


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


def run():
    main_scene = CatchLetters()
    cocos.director.director.run(cocos.scene.Scene(main_scene))


def main():
    cocos.director.director.init(width=800, height=640, resizable=False)
    run()

if __name__ == '__main__':
    main()
