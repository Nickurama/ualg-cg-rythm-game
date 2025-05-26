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
    ANIMATION_TIME_MS = 1000

    DRUM_WOBBLE_SPEED = 0.0008

    DRUM_ANIMATION_FRAME_0 = 0
    DRUM_ANIMATION_FRAME_1 = 250
    DRUM_ANIMATION_FRAME_2 = 750

    STICK_ROTATION_SPEED = 0.0008

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
        self.main_cylinder = Mesh(geometry=main_cylinder_geometry, material=wood_dark_material)

        cylinder_0 = FileGeometry(file="./objects/caixa/cylinder_0.obj")
        self.cylinder_0 = Mesh(geometry=cylinder_0, material=iron_material)

        cylinder_1 = FileGeometry(file="./objects/caixa/cylinder_1.obj")
        self.cylinder_1 = Mesh(geometry=cylinder_1, material=iron_material)

        cylinder_2 = FileGeometry(file="./objects/caixa/cylinder_2.obj")
        self.cylinder_2 = Mesh(geometry=cylinder_2, material=iron_material)

        cylinder_3 = FileGeometry(file="./objects/caixa/cylinder_3.obj")
        self.cylinder_3 = Mesh(geometry=cylinder_3, material=iron_material)

        cylinder_4 = FileGeometry(file="./objects/caixa/cylinder_4.obj")
        self.cylinder_4 = Mesh(geometry=cylinder_4, material=iron_material)

        cylinder_5 = FileGeometry(file="./objects/caixa/cylinder_5.obj")
        self.cylinder_5 = Mesh(geometry=cylinder_5, material=iron_material)

        cylinder_6 = FileGeometry(file="./objects/caixa/cylinder_6.obj")
        self.cylinder_6 = Mesh(geometry=cylinder_6, material=iron_material)

        cylinder_7 = FileGeometry(file="./objects/caixa/cylinder_7.obj")
        self.cylinder_7 = Mesh(geometry=cylinder_7, material=iron_material)

        stick_0 = FileGeometry(file="./objects/caixa/stick_0.obj", center=True, shift_center=[-0.5, 0.5, 0.0])
        self.stick_0 = Mesh(geometry=stick_0, material=wood_material)

        stick_1 = FileGeometry(file="./objects/caixa/stick_1.obj", center=True, shift_center=[0.5, 0.5, 0.0])
        self.stick_1 = Mesh(geometry=stick_1, material=wood_material)

        skin = FileGeometry(file="./objects/caixa/skin.obj")
        self.skin = Mesh(geometry=skin, material=skin_material)

        self.drum = Object3D()
        self.drum.add(self.main_cylinder)
        self.drum.add(self.cylinder_0)
        self.drum.add(self.cylinder_1)
        self.drum.add(self.cylinder_2)
        self.drum.add(self.cylinder_3)
        self.drum.add(self.cylinder_4)
        self.drum.add(self.cylinder_5)
        self.drum.add(self.cylinder_6)
        self.drum.add(self.cylinder_7)
        self.drum.add(self.skin)
        self.add(self.drum)

        self.stick_0.set_position([-0.8, 1.1, 0.0])
        self.stick_1.set_position([0.8, 1.1, 0.0])


        self.add(self.stick_0)
        self.add(self.stick_1)

        #self.stick_0.set_position
        self.drum_initial_matrix = self.drum.local_matrix
        self.stick_0_initial_matrix = self.stick_0.local_matrix
        self.stick_1_initial_matrix = self.stick_1.local_matrix

        self.elapsed = 0

    def update(self, delta_t_ms):
        self.elapsed += delta_t_ms
        if self.elapsed > self.ANIMATION_TIME_MS:
            self.drum.local_matrix = self.drum_initial_matrix
            self.stick_0.local_matrix = self.stick_0_initial_matrix
            self.stick_1.local_matrix = self.stick_1_initial_matrix
            self.elapsed = 0
        elif self.elapsed > self.DRUM_ANIMATION_FRAME_2:
            self.drum.rotate_z(-delta_t_ms * self.DRUM_WOBBLE_SPEED)
            self.stick_0.rotate_z(-delta_t_ms * self.STICK_ROTATION_SPEED, local=True)
            self.stick_1.rotate_z(-delta_t_ms * self.STICK_ROTATION_SPEED, local=True)
            # self.drum.set_position([self.drum.local_position[0], self.drum.local_position[1] - delta_t_ms * self.BASE_JUMP_SPEED, self.drum.local_position[2]])
        elif self.elapsed > self.DRUM_ANIMATION_FRAME_1:
            self.drum.rotate_z(delta_t_ms * self.DRUM_WOBBLE_SPEED)
            self.stick_0.rotate_z(delta_t_ms * self.STICK_ROTATION_SPEED, local=True)
            self.stick_1.rotate_z(delta_t_ms * self.STICK_ROTATION_SPEED, local=True)
            # self.drum.set_position([self.drum.local_position[0], self.drum.local_position[1] + delta_t_ms * self.BASE_JUMP_SPEED, self.drum.local_position[2]])
        elif self.elapsed > self.DRUM_ANIMATION_FRAME_0:
            self.drum.rotate_z(-delta_t_ms * self.DRUM_WOBBLE_SPEED)
            self.stick_0.rotate_z(-delta_t_ms * self.STICK_ROTATION_SPEED, local=True)
            self.stick_1.rotate_z(-delta_t_ms * self.STICK_ROTATION_SPEED, local=True)
            # self.drum.set_position([self.drum.local_position[0], self.drum.local_position[1] - delta_t_ms * self.BASE_JUMP_SPEED, self.drum.local_position[2]])