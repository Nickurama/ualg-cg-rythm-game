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

class UI(Object3D):
    DEBUG = False

    PERFECT_POS = -1.30
    PERFECT_RANGE = 0.10
    GOOD_RANGE = 0.20
    OK_RANGE = 0.40

    POSX_0 = -1.2
    POSX_1 = -0.4
    POSX_2 = 0.4
    POSX_3 = 1.2

    TEXT_PADDING = 0.8
    TEXT_FPS_SIZE = 0.1
    TEXT_COMBO_SIZE = 0.2
    TEXT_SCORE_SIZE = 0.2

    TEXT_COMBO = "x"
    TEXT_SCORE = ""

    TEXT_FPS_Y = 1.7
    TEXT_FPS_X = 2.3
    TEXT_COMBO_Y = -1.5
    TEXT_COMBO_X = -2.3
    TEXT_SCORE_Y = 1.7
    TEXT_SCORE_X = -2.3

    def __init__(self):
        super().__init__()
        perfect_line = self.create_perfect_line(self.PERFECT_POS)
        perfect_range0, perfect_range1 = self.create_range(self.PERFECT_POS, self.PERFECT_RANGE)
        good_range0, good_range1 = self.create_range(self.PERFECT_POS, self.GOOD_RANGE)
        ok_range0, ok_range1 = self.create_range(self.PERFECT_POS, self.OK_RANGE)
        lane0, lane1, lane2 = self.create_lanes()
        self.fps_text = Text("", self.TEXT_FPS_X, self.TEXT_FPS_Y, self.TEXT_FPS_SIZE, self.TEXT_PADDING, True)
        self.combo_text = Text("", self.TEXT_COMBO_X, self.TEXT_COMBO_Y, self.TEXT_COMBO_SIZE, self.TEXT_PADDING)
        self.score_text = Text("", self.TEXT_SCORE_X, self.TEXT_SCORE_Y, self.TEXT_SCORE_SIZE, self.TEXT_PADDING)

        self.add(self.fps_text)
        self.add(self.combo_text)
        self.add(self.score_text)
        self.add(perfect_line)
        if (self.DEBUG):
            self.add(perfect_range0)
            self.add(perfect_range1)
            self.add(good_range0)
            self.add(good_range1)
            self.add(ok_range0)
            self.add(ok_range1)
        self.add(lane0)
        self.add(lane1)
        self.add(lane2)
        self.set_position([0, 0, 0])


    def create_perfect_line(self, pos):
        geometry = RectangleGeometry(3.1, 0.05);
        color_data = Utils.fillColor(0.9, 0.9, 0.9, geometry.vertex_count)
        geometry.add_attribute("vec3", "vertexColor", color_data)
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
        mesh = Mesh(geometry, material)
        mesh.set_position([0.0, pos, 3.0])
        return mesh

    def create_range(self, pos, range):
        geometry = RectangleGeometry(3.5, 0.01);
        color_data = Utils.fillColor(0.7, 0.7, 0.7, geometry.vertex_count)
        geometry.add_attribute("vec3", "vertexColor", color_data)
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
        mesh = Mesh(geometry, material)
        mesh2 = Mesh(geometry, material)
        mesh.set_position([0.0, pos - range, 3.0])
        mesh2.set_position([0.0, pos + range, 3.0])
        return mesh, mesh2
    
    def create_lanes(self):
        geometry = RectangleGeometry(0.005, 3.5);
        color_data = Utils.fillColor(0.7, 0.7, 0.7, geometry.vertex_count)
        geometry.add_attribute("vec3", "vertexColor", color_data)
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
        mesh0 = Mesh(geometry, material)
        mesh1 = Mesh(geometry, material)
        mesh2 = Mesh(geometry, material)
        mesh0.set_position([(self.POSX_0 + self.POSX_1) / 2.0, 0.0, 3.0])
        mesh1.set_position([(self.POSX_1 + self.POSX_2) / 2.0, 0.0, 3.0])
        mesh2.set_position([(self.POSX_2 + self.POSX_3) / 2.0, 0.0, 3.0])
        return mesh0, mesh1, mesh2

    def update(self, fps, combo, score, scene):
        self.fps_text.update(fps)
        self.combo_text.update(f"{combo}{self.TEXT_COMBO}")
        self.score_text.update(f"{self.TEXT_SCORE}{score}")

    def create_text_obj(self, text, padding, size, x, y, align_right=False):
        text_obj = Object3D()
        counter = 0
        total_size = 0
        for char in str(text):
            geometry = RectangleGeometry(size, size);
            material = TextureMaterial(texture=Texture(f"images/font/font_{char}.png"))
            mesh = Mesh(geometry, material)
            mesh.set_position([(size / 2.0) + counter * padding * size, -size / 2.0, 0.0])
            counter += 1
            text_obj.add(mesh)
        total_size += counter * size * padding
        if align_right:
            text_obj.set_position([x - total_size, y, 3.0])
        else:
            text_obj.set_position([x, y, 3.0])
        return text_obj