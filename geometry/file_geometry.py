from geometry.geometry import Geometry
from core.obj_reader import my_obj_reader as my_obj_reader
import math


class FileGeometry(Geometry):
    def __init__(self, file="", center=False, shift_center=[0.0, 0.0, 0.0]):
        super().__init__()

        position_data, uv_data, normal_data = my_obj_reader(file)

        if center:
            shifted_position_data = []
            count = len(position_data)
            avg_x = (math.fsum(v[0] for v in position_data) / count) + shift_center[0]
            avg_y = (math.fsum(v[1] for v in position_data) / count) + shift_center[1]
            avg_z = (math.fsum(v[2] for v in position_data) / count) + shift_center[2]
            for vertex in position_data:
                shifted_position_data.append([
                    vertex[0] - avg_x,
                    vertex[1] - avg_y,
                    vertex[2] - avg_z,
                ])
            self.add_attribute("vec3", "vertexPosition", shifted_position_data)
        else:
            self.add_attribute("vec3", "vertexPosition", position_data)
        
        self.add_attribute("vec2", "vertexUV", uv_data)
        self.add_attribute("vec3", "vertexNormal", normal_data)
        self.add_attribute("vec3", "faceNormal", normal_data)