import math
from material.surface import SurfaceMaterial
from material.texture import TextureMaterial
from core_ext.texture import Texture
from core_ext.mesh import Mesh
from core_ext.object3d import Object3D
from geometry.geometry import Geometry
from geometry.rectangle import RectangleGeometry

class MenuUI(Object3D):
    TITLE_Y = 1.0

    def __init__(self):
        super().__init__()

        title = self.create_title()

        self.add(title)

        self.visible = False

    def create_title(self):
        geometry = RectangleGeometry(3.1, 0.05);
        material = SurfaceMaterial(property_dict={"useVertexColors": True})
        mesh = Mesh(geometry, material)
        mesh.set_position([0.0, self.TITLE_Y, 3.0])
        return mesh

    def update(self, fps, combo, score, scene):
        self = self
