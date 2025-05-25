import math
from material.surface import SurfaceMaterial
from material.texture import TextureMaterial
from core_ext.texture import Texture
from core_ext.mesh import Mesh
from extras.movement_rig import MovementRig
from geometry.geometry import Geometry
from geometry.rectangle import RectangleGeometry

class Note(MovementRig):
    def __init__(self, x=0.0, y=0.0, z=0.0, radius=1.0, res=25, texture="",
                 r=1.0, g=1.0, b=1.0, spawn_time=0, lane=0):
        # geometry
        position_data, uv_data = Note.makeCircleAndUvs(0.0, 0.0, 0.0, radius, res)
        geometry = Geometry()
        geometry.add_attribute("vec3", "vertexPosition", position_data)
        geometry.add_attribute("vec2", "vertexUV", uv_data)

        # color (if no texture)
        color_data = Note.fillColor(r, g, b, res * 3)
        geometry.add_attribute("vec3", "vertexColor", color_data)

        # texture
        if texture == "":
            material = SurfaceMaterial(property_dict={"useVertexColors": True})
        else:
            material = TextureMaterial(texture=Texture(texture))

        self.mesh = Mesh(geometry, material)
        super().__init__()
        self.add(self.mesh)
        self.set_position([x, y, z])
        self.spawn_time = spawn_time
        self.has_reached_perfect_line = False
        self.lane = lane
        self.missed = False

    def is_within_range(self, pos, range):
        y = self.local_position[1]

        if y > (pos + range):
            return False
        if y < (pos - range):
            return False
        return True

    def is_below_range(self, pos, range):
        y = self.local_position[1]

        return y < (pos - range)

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

    @staticmethod
    def makeNormalData(n):
        data = []
        for i in range(n):
            data.append([0, 0, 1])
        return data
