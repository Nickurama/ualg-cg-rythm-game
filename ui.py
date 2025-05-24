import math
from material.surface import SurfaceMaterial
from material.texture import TextureMaterial
from core_ext.texture import Texture
from core_ext.mesh import Mesh
from extras.movement_rig import MovementRig
from geometry.geometry import Geometry
from geometry.rectangle import RectangleGeometry

class UI(MovementRig):
    def __init__(self):
        perfect_line: MovementRig = self.create_perfect_line()

        # texture
        super().__init__()
        self.add(perfect_line)
        self.set_position([0, 0, 0])

    def create_perfect_line(self):
        geometry = RectangleGeometry(3.5, 0.05);
        color_data = UI.fillColor(0.9, 0.9, 0.9, geometry.vertex_count)
        geometry.add_attribute("vec3", "vertexColor", color_data)
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
        mesh = Mesh(geometry, material)
        rig = MovementRig()
        rig.add(mesh)
        rig.set_position([0.0, -1.3, 3.0])
        return rig


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
