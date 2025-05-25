import math
from material.surface import SurfaceMaterial
from material.texture import TextureMaterial
from core_ext.texture import Texture
from core_ext.mesh import Mesh
from core_ext.object3d import Object3D
from geometry.geometry import Geometry
from geometry.rectangle import RectangleGeometry

class HighscoreUI(Object3D):
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
        perfect_line = self.create_perfect_line(self.PERFECT_POS)
        perfect_range0, perfect_range1 = self.create_range(self.PERFECT_POS, self.PERFECT_RANGE)
        good_range0, good_range1 = self.create_range(self.PERFECT_POS, self.GOOD_RANGE)
        ok_range0, ok_range1 = self.create_range(self.PERFECT_POS, self.OK_RANGE)
        lane0, lane1, lane2 = self.create_lanes()

        super().__init__()
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

        self.fps_counter = None
        self.last_fps = -1
        self.combo_counter = None
        self.last_combo = -1
        self.score_counter = None
        self.last_score = -1

    def create_perfect_line(self, pos):
        geometry = RectangleGeometry(3.1, 0.05);
        color_data = HighscoreUI.fillColor(0.9, 0.9, 0.9, geometry.vertex_count)
        geometry.add_attribute("vec3", "vertexColor", color_data)
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
        mesh = Mesh(geometry, material)
        mesh.set_position([0.0, pos, 3.0])
        return mesh

    def create_range(self, pos, range):
        geometry = RectangleGeometry(3.5, 0.01);
        color_data = HighscoreUI.fillColor(0.7, 0.7, 0.7, geometry.vertex_count)
        geometry.add_attribute("vec3", "vertexColor", color_data)
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
        mesh = Mesh(geometry, material)
        mesh2 = Mesh(geometry, material)
        mesh.set_position([0.0, pos - range, 3.0])
        mesh2.set_position([0.0, pos + range, 3.0])
        return mesh, mesh2
    
    def create_lanes(self):
        geometry = RectangleGeometry(0.005, 3.5);
        color_data = HighscoreUI.fillColor(0.7, 0.7, 0.7, geometry.vertex_count)
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
        if fps != self.last_fps:
            self.last_fps = fps
            if self.fps_counter != None:
                scene.remove(self.fps_counter)
            fps_text = f"{fps}"
            self.fps_counter = self.create_text_obj(fps_text, self.TEXT_PADDING, self.TEXT_FPS_SIZE, self.TEXT_FPS_X, self.TEXT_FPS_Y, True)
            scene.add(self.fps_counter)
        if combo != self.last_combo:
            self.last_combo = combo
            if self.combo_counter != None:
                scene.remove(self.combo_counter)
            combo_text = f"{combo}{self.TEXT_COMBO}"
            self.combo_counter = self.create_text_obj(combo_text, self.TEXT_PADDING, self.TEXT_COMBO_SIZE, self.TEXT_COMBO_X, self.TEXT_COMBO_Y)
            scene.add(self.combo_counter)
        if score != self.last_score:
            self.last_score = score
            if self.score_counter != None:
                scene.remove(self.score_counter)
            score_text = f"{self.TEXT_SCORE}{score}"
            self.score_counter = self.create_text_obj(score_text, self.TEXT_PADDING, self.TEXT_SCORE_SIZE, self.TEXT_SCORE_X, self.TEXT_SCORE_Y)
            scene.add(self.score_counter)

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


    @staticmethod
    def fillColor(r, g, b, n):
        curr_colors = []
        for i in range(n):
            curr_colors.append([r, g, b])
        return curr_colors

    @staticmethod
    def makeCircle(x, y, z, r, n):
        angle = 2 * math.pi / n
        curr_angle = 0.0;
        curr_points = []
        for i in range(n):
            curr_x = x + r * math.cos(curr_angle)
            curr_y = y + r * math.sin(curr_angle)
            curr_z = z
            curr_points.append([curr_x, curr_y, curr_z])
            if i > 0:
                curr_points.append([x, y, z])
                curr_points.append([curr_x, curr_y, curr_z])
            curr_angle += angle
        curr_points.append(curr_points[0])
        curr_points.append([x, y, z])

        return curr_points

    @staticmethod
    def makeCircleAndUvs(x, y, z, r, n):
        angle_step = 2 * math.pi / n
        vertices = []
        uvs = []

        center_uv = [0.5, 0.5]
        center_vert = [x, y, z]

        for i in range(n):
            angle = angle_step * i

            # vertices
            px = x + r * math.cos(angle)
            py = y + r * math.sin(angle)
            pz = z

            # uvs
            uv_x = 0.5 + 0.5 * math.cos(angle)
            uv_y = 0.5 + 0.5 * math.sin(angle)

            vertices.append([px, py, pz])
            uvs.append([uv_x, uv_y])
            if i > 0:
                vertices.append(center_vert)
                uvs.append(center_uv)
                vertices.append([px, py, pz])
                uvs.append([uv_x, uv_y])

        vertices.append(vertices[0])
        uvs.append(uvs[0])
        vertices.append(center_vert)
        uvs.append(center_uv)

        return vertices, uvs

    @staticmethod
    def makeCircleRaw(x, y, z, r, n):
        angle = 2 * math.pi / n
        curr_angle = 0.0;
        curr_points = []
        for i in range(n):
            curr_x = x + r * math.cos(curr_angle)
            curr_y = y + r * math.sin(curr_angle)
            curr_z = z
            curr_points.append([curr_x, curr_y, curr_z])
            curr_angle += angle

        return curr_points
