from material.flat import FlatMaterial
from material.lambert import LambertMaterial
from material.phong import PhongMaterial
from material.basic import BasicMaterial
from material.surface import SurfaceMaterial
from material.texture import TextureMaterial
from core_ext.texture import Texture
from core_ext.mesh import Mesh
from extras.movement_rig import MovementRig
from geometry.geometry import Geometry
from geometry.rectangle import RectangleGeometry
from core_ext.object3d import Object3D
from utils import Utils
from geometry.file_geometry import FileGeometry

class Castanholas(Object3D):
    def __init__(self, light_sources):
        super().__init__()
        wood_material_up = LambertMaterial(
            texture=Texture("images/wood_texture.jpg"),
            number_of_light_sources=light_sources
        )
        wood_material_down = LambertMaterial(
            texture=Texture("images/wood_texture_2.jpg"),
            number_of_light_sources=light_sources
        )

        castanhola_cima_geometry = FileGeometry(file="./objects/castanholas/castanhola_cima.obj")
        self.castanhola_cima = Mesh(geometry=castanhola_cima_geometry, material=wood_material_up)
        self.add(self.castanhola_cima)

        castanhola_baixo_geometry = FileGeometry(file="./objects/castanholas/castanhola_baixo.obj")
        self.castanhola_baixo = Mesh(geometry=castanhola_baixo_geometry, material=wood_material_up)
        self.add(self.castanhola_baixo)


    def update(self, delta_t_ms):
        delta_t_ms = delta_t_ms
