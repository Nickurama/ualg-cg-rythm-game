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

class Caixa(Object3D):
    def __init__(self, light_sources):
        super().__init__()
        wood_material = LambertMaterial(
            texture=Texture("images/light-wood.jpg"),
            number_of_light_sources=light_sources
        )
        iron_material = LambertMaterial(
            texture=Texture("images/iron.jpg"),
            number_of_light_sources=light_sources
        )
        wood_dark_material = LambertMaterial(
            texture=Texture("images/dark-wood.jpg"),
            number_of_light_sources=light_sources
        )
        skin_material = LambertMaterial(
            texture=Texture("images/skin.jpg"),
            number_of_light_sources=light_sources
        )

        main_cylinder_geometry = FileGeometry(file="./objects/caixa/main_cylinder.obj")
        self.mesh_main_cylinder = Mesh(geometry=main_cylinder_geometry, material=wood_dark_material)
        self.add(self.mesh_main_cylinder)

        cylinder_0 = FileGeometry(file="./objects/caixa/cylinder_0.obj")
        self.mesh_cylinder_0 = Mesh(geometry=cylinder_0, material=iron_material)
        self.add(self.mesh_cylinder_0)

        cylinder_1 = FileGeometry(file="./objects/caixa/cylinder_1.obj")
        self.mesh_cylinder_1 = Mesh(geometry=cylinder_1, material=iron_material)
        self.add(self.mesh_cylinder_1)

        cylinder_2 = FileGeometry(file="./objects/caixa/cylinder_2.obj")
        self.mesh_cylinder_2 = Mesh(geometry=cylinder_2, material=iron_material)
        self.add(self.mesh_cylinder_2)

        cylinder_3 = FileGeometry(file="./objects/caixa/cylinder_3.obj")
        self.mesh_cylinder_3 = Mesh(geometry=cylinder_3, material=iron_material)
        self.add(self.mesh_cylinder_3)

        cylinder_4 = FileGeometry(file="./objects/caixa/cylinder_4.obj")
        self.mesh_cylinder_4 = Mesh(geometry=cylinder_4, material=iron_material)
        self.add(self.mesh_cylinder_4)

        cylinder_5 = FileGeometry(file="./objects/caixa/cylinder_5.obj")
        self.mesh_cylinder_5 = Mesh(geometry=cylinder_5, material=iron_material)
        self.add(self.mesh_cylinder_5)

        cylinder_6 = FileGeometry(file="./objects/caixa/cylinder_6.obj")
        self.mesh_cylinder_6 = Mesh(geometry=cylinder_6, material=iron_material)
        self.add(self.mesh_cylinder_6)

        cylinder_7 = FileGeometry(file="./objects/caixa/cylinder_7.obj")
        self.mesh_cylinder_7 = Mesh(geometry=cylinder_7, material=iron_material)
        self.add(self.mesh_cylinder_7)

        stick_0 = FileGeometry(file="./objects/caixa/stick_0.obj")
        self.mesh_stick_0 = Mesh(geometry=stick_0, material=wood_material)
        self.add(self.mesh_stick_0)

        stick_1 = FileGeometry(file="./objects/caixa/stick_1.obj")
        self.mesh_stick_1 = Mesh(geometry=stick_1, material=wood_material)
        self.add(self.mesh_stick_1)

        skin = FileGeometry(file="./objects/caixa/skin.obj")
        self.mesh_skin = Mesh(geometry=skin, material=skin_material)
        self.add(self.mesh_skin)

    def update(self, delta_t_ms):
        delta_t_ms = delta_t_ms
