from geometry.geometry import Geometry
from core.obj_reader import my_obj_reader as my_obj_reader


class FileGeometry(Geometry):
    def __init__(self, width=1, height=1, depth=1, file=""):
        super().__init__()

        position_data, uv_data, normal_data = my_obj_reader(file)
        
        self.add_attribute("vec3", "vertexPosition", position_data)
        self.add_attribute("vec2", "vertexUV", uv_data)
        self.add_attribute("vec3", "vertexNormal", normal_data)
        self.add_attribute("vec3", "faceNormal", normal_data)
        print(len(position_data))
        print(len(uv_data))
        print(len(normal_data))
