import math
from material.surface import SurfaceMaterial
from material.texture import TextureMaterial
from core_ext.texture import Texture
from core_ext.mesh import Mesh
from core_ext.object3d import Object3D
from geometry.geometry import Geometry
from geometry.rectangle import RectangleGeometry
from text import Text
from utils import Utils
from typing import List, Tuple
import csv

class HighscoreUI(Object3D):
    HIGHSCORES_FILE = "highscores.high"
    TITLE_TEXT = "HIGHSCORES"
    TITLE_POS_PERCENT_X = 0.5
    TITLE_POS_PERCENT_Y = 0.9
    TITLE_SIZE = 0.3

    TITLE_PADDING = 0.3
    PADDING = 0.1
    SCORE_SIZE = 0.2

    TOTAL_SCORES = 8


    def __init__(self):
        super().__init__()

        self.title_pos = Utils.percentToRelative([self.TITLE_POS_PERCENT_X, self.TITLE_POS_PERCENT_Y])
        self.title = Text(self.TITLE_TEXT, self.title_pos[0], self.title_pos[1], self.TITLE_SIZE, centered=True)
        self.highscores = self.create_highscore_text()

        self.add(self.title)

    def create_highscore_text(self):
        highscores = self.load_highscores(self.HIGHSCORES_FILE)
        highscores = sorted(highscores, key=lambda x: -int(x[1]))
        count = 0
        for highscore in highscores:
            if count > self.TOTAL_SCORES - 1:
                return
            user = highscore[0]
            score = int(highscore[1])
            user_text = Text(user, self.title_pos[0] - self.title.width / 2,
                             self.title_pos[1] - self.title.height / 2 - self.TITLE_PADDING - count * (self.SCORE_SIZE + self.PADDING),
                             self.SCORE_SIZE, align_right=False)
            score_text = Text(score, self.title_pos[0] + self.title.width / 2,
                             self.title_pos[1] - self.title.height / 2 - self.TITLE_PADDING - count * (self.SCORE_SIZE + self.PADDING),
                             self.SCORE_SIZE, align_right=True)
            self.add(user_text)
            self.add(score_text)
            count += 1


    @staticmethod
    def load_highscores(file):
        data = []
        with open(file, 'r') as file:
            reader = csv.reader(file)
            data = [row for row in reader]

        return data

    @staticmethod
    def write_highscore(file, name, score: int):
        highscores = HighscoreUI.load_highscores(HighscoreUI.HIGHSCORES_FILE)
        highscores.append([name, str(score)])
        highscores = sorted(highscores, key=lambda x: -int(x[1]))
        with open(file, 'w', newline="\n") as file:
            writer = csv.writer(file)
            writer.writerows(highscores)



    def update(self, input):
        return input.is_mouse_left_down()
