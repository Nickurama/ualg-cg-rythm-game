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

class Guitarra(Object3D):
    ANIMATION_TIME_MS = 1000

    GUITARRA_WOBBLE_SPEED = 0.0018

    GUITARRA_ANIMATION_FRAME_0 = 0
    GUITARRA_ANIMATION_FRAME_1 = 250
    GUITARRA_ANIMATION_FRAME_2 = 750

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
        strings_material = LambertMaterial(
            texture=Texture("images/white.jpg"),
            number_of_light_sources=light_sources
        )

        main_body_geometry = FileGeometry(file="./objects/guitarra/main_body.obj")
        self.main_body = Mesh(geometry=main_body_geometry, material=wood_dark_material)

        guitarra_strings = FileGeometry(file="./objects/guitarra//guitarra_strings.obj")
        self.guitarra_strings = Mesh(geometry=guitarra_strings, material=strings_material)

        black_parts = FileGeometry(file="./objects/guitarra/black_parts.obj")
        self.black_parts = Mesh(geometry=black_parts, material=wood_dark_material)

        self.guitarra = Object3D()
        self.guitarra.add(self.main_body)
        self.guitarra.add(self.guitarra_strings)
        self.guitarra.add(self.black_parts)
        self.add(self.guitarra)

        self.guitarra_initial_matrix = self.guitarra.local_matrix

        self.elapsed = 0

    def update(self, delta_t_ms):
        self.elapsed += delta_t_ms
        if self.elapsed > self.ANIMATION_TIME_MS:
            self.guitarra.local_matrix = self.guitarra_initial_matrix
            self.elapsed = 0
        elif self.elapsed > self.GUITARRA_ANIMATION_FRAME_2:
            self.guitarra.rotate_y(-delta_t_ms * self.GUITARRA_WOBBLE_SPEED)
            # self.guitarra.set_position([self.guitarra.local_position[0], self.guitarra.local_position[1] - delta_t_ms * self.BASE_JUMP_SPEED, self.guitarra.local_position[2]])
        elif self.elapsed > self.GUITARRA_ANIMATION_FRAME_1:
            self.guitarra.rotate_y(delta_t_ms * self.GUITARRA_WOBBLE_SPEED)
            # self.guitarra.set_position([self.guitarra.local_position[0], self.guitarra.local_position[1] + delta_t_ms * self.BASE_JUMP_SPEED, self.guitarra.local_position[2]])
        elif self.elapsed > self.GUITARRA_ANIMATION_FRAME_0:
            self.guitarra.rotate_y(-delta_t_ms * self.GUITARRA_WOBBLE_SPEED)
            # self.guitarra.set_position([self.guitarra.local_position[0], self.guitarra.local_position[1] - delta_t_ms * self.BASE_JUMP_SPEED, self.guitarra.local_position[2]])

