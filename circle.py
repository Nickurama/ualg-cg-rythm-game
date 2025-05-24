import math
from material.surface import SurfaceMaterial
from core_ext.mesh import Mesh
from extras.movement_rig import MovementRig
from geometry.geometry import Geometry

class Circle(MovementRig):
    def __init__(self, x=0.0, y=0.0, z=0.0, radius=1.0, res=25, r=1.0, g=1.0, b=1.0):
        geometry = Geometry()
        position_data = Circle.makeCircle(0.0, 0.0, 0.0, radius, res);
        geometry.add_attribute("vec3", "vertexPosition", position_data)
        color_data = Circle.fillColor(r, g, b, res * 3)
        geometry.add_attribute("vec3", "vertexColor", color_data)
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
        self.mesh = Mesh(geometry, material)
        super().__init__()
        self.add(self.mesh)
        self.set_position([x, y, z])

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
