import math
from material.surface import SurfaceMaterial
from material.texture import TextureMaterial
from core_ext.texture import Texture
from core_ext.mesh import Mesh
from core_ext.object3d import Object3D
from geometry.geometry import Geometry
from geometry.rectangle import RectangleGeometry

class HighscoreUI(Object3D):
    def __init__(self):
        super().__init__()

    def update(self):
        return False
