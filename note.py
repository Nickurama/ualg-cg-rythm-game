from material.surface import SurfaceMaterial
from material.texture import TextureMaterial
from core_ext.texture import Texture
from core_ext.mesh import Mesh
from extras.movement_rig import MovementRig
from geometry.geometry import Geometry
from geometry.rectangle import RectangleGeometry
from utils import Utils

class Note(MovementRig):
    def __init__(self, x=0.0, y=0.0, z=0.0, radius=1.0, res=25, texture="",
                 r=1.0, g=1.0, b=1.0, spawn_time=0, lane=0):
        # geometry
        position_data, uv_data = Utils.makeCircleAndUvs(0.0, 0.0, 0.0, radius, res)
        geometry = Geometry()
        geometry.add_attribute("vec3", "vertexPosition", position_data)
        geometry.add_attribute("vec2", "vertexUV", uv_data)

        # color (if no texture)
        # color_data = Utils.fillColor(r, g, b, res * 3)
        # geometry.add_attribute("vec3", "vertexColor", color_data)

        # texture
        # if texture == "":
        #     material = SurfaceMaterial(property_dict={"useVertexColors": True})
        # else:
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