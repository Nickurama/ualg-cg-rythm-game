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

class MenuUI(Object3D):
    TITLE_X = 0.0
    TITLE_Y = 1.0
    TITLE_SIZE = 0.3
    TITLE_TEXT = "O Recital Espanhol"

    PLAY_TEXT = "Jogar!"
    PLAY_X = 0.0
    PLAY_Y = -0.5
    PLAY_TEXT_SIZE = 0.2
    PLAY_BTN_W = 1.5
    PLAY_BTN_H = 0.5

    def __init__(self):
        super().__init__()

        self.title = Text(self.TITLE_TEXT, self.TITLE_X, self.TITLE_Y, self.TITLE_SIZE, centered=True)
        self.play_text = Text(self.PLAY_TEXT, self.PLAY_X, self.PLAY_Y, self.PLAY_TEXT_SIZE, centered=True)
        self.play_button = self.create_play_button(self.PLAY_X, self.PLAY_Y, self.PLAY_BTN_W, self.PLAY_BTN_H)
        self.add(self.title)
        self.add(self.play_text)
        self.add(self.play_button)
        # g = self.create_play_button(0.0, 0.0, 0.01, 0.01)
        # t = self.create_play_button(-2.308, 1.730, 0.01, 0.01)
        # self.add(g)
        # self.add(t)

        self.set_position([0, 0, 0])

    def create_play_button(self, x, y, width, height):
        geometry = RectangleGeometry(width, height);
        color_data = Utils.fillColor(1.0, 0.427, 0.416, geometry.vertex_count)
        geometry.add_attribute("vec3", "vertexColor", color_data)
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
        material.set_alpha(0.6)
        mesh = Mesh(geometry, material)
        mesh.set_position([x, y, 3.0])
        return mesh

    def clicked_play(self, mouse_pos):
        rel_mouse_pos = Utils.toRelative(mouse_pos)
        rel_btn_center = [self.PLAY_X, self.PLAY_Y]
        return Utils.collides_rectangle(rel_mouse_pos, rel_btn_center, self.PLAY_BTN_W, self.PLAY_BTN_H)
        # g = self.create_play_button(self.PLAY_X - self.PLAY_BTN_W / 2.0 - 0.01, self.PLAY_Y, 0.01, 0.01)
        # g = self.create_play_button(rel_pos[0], rel_pos[1], 0.01, 0.01)
        # self.add(g)

    def update(self, input):
        if input.is_mouse_left_down():
            if self.clicked_play(input.get_mouse_pos()):
                return True

        return False