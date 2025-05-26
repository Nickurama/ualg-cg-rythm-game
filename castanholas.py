import math
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
    ANIMATION_TIME_MS = 1000

    CASTANHOLAS_ANIMATION_FRAME_0 = 0
    CASTANHOLAS_ANIMATION_FRAME_1 = 250
    CASTANHOLAS_ANIMATION_FRAME_2 = 750

    STICK_ROTATION_SPEED = 0.0008
    TRANSLATION_SPEED = 0.0065

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

        castanhola_cima_geometry = FileGeometry(file="./objects/castanholas/castanhola_cima.obj", center=True, shift_center=[0.0, 0, 0.0])
        self.castanhola_cima = Mesh(geometry=castanhola_cima_geometry, material=wood_material_up)

        castanhola_baixo_geometry = FileGeometry(file="./objects/castanholas/castanhola_baixo.obj", center=True, shift_center=[0.0, 0.4, 0.0])
        self.castanhola_baixo = Mesh(geometry=castanhola_baixo_geometry, material=wood_material_up)

        self.castanhola_cima.set_position([-0.3, 0.3, 0.0])
        self.castanhola_baixo.set_position([-0.3, 0.3, 0.0])
        self.castanhola_cima.rotate_z(math.pi/16)
        
        self.add(self.castanhola_cima)
        self.add(self.castanhola_baixo)

        self.castanhola_cima_initial_matrix = self.castanhola_cima.local_matrix
        self.castanhola_baixo_initial_matrix = self.castanhola_baixo.local_matrix

        self.elapsed = 0

    def update(self, delta_t_ms):
        self.elapsed += delta_t_ms
        if self.elapsed > self.ANIMATION_TIME_MS:
            self.castanhola_cima.local_matrix = self.castanhola_cima_initial_matrix
            self.castanhola_baixo.local_matrix = self.castanhola_baixo_initial_matrix
            self.elapsed = 0
        elif self.elapsed > self.CASTANHOLAS_ANIMATION_FRAME_2:
            self.castanhola_cima.rotate_z(-delta_t_ms * self.STICK_ROTATION_SPEED, local=True)
            self.castanhola_baixo.rotate_z(delta_t_ms * self.STICK_ROTATION_SPEED, local=True)
            self.castanhola_cima.translate(0, -self.TRANSLATION_SPEED, 0, local=True)
            # self.drum.set_position([self.drum.local_position[0], self.drum.local_position[1] - delta_t_ms * self.BASE_JUMP_SPEED, self.drum.local_position[2]])
        elif self.elapsed > self.CASTANHOLAS_ANIMATION_FRAME_1:
            self.castanhola_cima.rotate_z(delta_t_ms * self.STICK_ROTATION_SPEED, local=True)
            self.castanhola_baixo.rotate_z(-delta_t_ms * self.STICK_ROTATION_SPEED, local=True)
            self.castanhola_cima.translate(0, self.TRANSLATION_SPEED, 0, local=True)
            # self.drum.set_position([self.drum.local_position[0], self.drum.local_position[1] + delta_t_ms * self.BASE_JUMP_SPEED, self.drum.local_position[2]])
        elif self.elapsed > self.CASTANHOLAS_ANIMATION_FRAME_0:
            self.castanhola_cima.rotate_z(-delta_t_ms * self.STICK_ROTATION_SPEED, local=True)
            self.castanhola_baixo.rotate_z(delta_t_ms * self.STICK_ROTATION_SPEED, local=True)
            self.castanhola_cima.translate(0, -self.TRANSLATION_SPEED, 0, local=True)
            # self.drum.set_position([self.drum.local_position[0], self.drum.local_position[1] - delta_t_ms * self.BASE_JUMP_SPEED, self.drum.local_position[2]])
