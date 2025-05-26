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

class Recital(Object3D):
    def __init__(self, light_sources):
        super().__init__()
        chair_leather_material = LambertMaterial(
            texture=Texture("images/chair-leather.jpg"),
            number_of_light_sources=light_sources
        )
        wood_material = LambertMaterial(
            texture=Texture("images/dark-wood.jpg"),
            number_of_light_sources=light_sources
        )
        wood_dark_material = LambertMaterial(
            texture=Texture("images/dark-wood.jpg"),
            number_of_light_sources=light_sources
        )
        red_curtain_material = LambertMaterial(
            texture=Texture("images/red-curtain.jpg"),
            number_of_light_sources=light_sources
        )
        wood_tilling_material = LambertMaterial(
            texture=Texture("images/wood-tilling.jpg"),
            number_of_light_sources=light_sources
        )


        cadeiras_geometry = FileGeometry(file="./objects/recital/cadeiras.obj")
        self.cadeiras = Mesh(geometry=cadeiras_geometry, material=chair_leather_material)
        self.add(self.cadeiras)

        chao_geometry = FileGeometry(file="./objects/recital/chao.obj")
        self.chao = Mesh(geometry=chao_geometry, material=wood_tilling_material)
        self.add(self.chao)

        cortina_esquerda_geometry = FileGeometry(file="./objects/recital/cortina_esquerda.obj")
        self.cortina_esquerda = Mesh(geometry=cortina_esquerda_geometry, material=red_curtain_material)
        self.add(self.cortina_esquerda)

        cortina_direita_geometry = FileGeometry(file="./objects/recital/cortina_direita3.obj")
        self.cortina_direita = Mesh(geometry=cortina_direita_geometry, material=red_curtain_material)
        self.add(self.cortina_direita)

        palco_geometry = FileGeometry(file="./objects/recital/palco.obj")
        self.palco = Mesh(geometry=palco_geometry, material=wood_material)
        self.add(self.palco)

        escadas_esquerda_geometry = FileGeometry(file="./objects/recital/escadas_esquerda.obj")
        self.escadas_esquerda = Mesh(geometry=escadas_esquerda_geometry, material=wood_material)
        self.add(self.escadas_esquerda)

        escadas_direita_geometry = FileGeometry(file="./objects/recital/escadas_direita.obj")
        self.escadas_direita = Mesh(geometry=escadas_direita_geometry, material=wood_material)
        self.add(self.escadas_direita)

        parede_esquerda_geometry = FileGeometry(file="./objects/recital/parede_esquerda.obj")
        self.parede_esquerda = Mesh(geometry=parede_esquerda_geometry, material=wood_dark_material)
        self.add(self.parede_esquerda)

        parede_direita_geometry = FileGeometry(file="./objects/recital/parede_direita.obj")
        self.parede_direita = Mesh(geometry=parede_direita_geometry, material=wood_dark_material)
        self.add(self.parede_direita)

        teto_geometry = FileGeometry(file="./objects/recital/teto.obj")
        self.teto = Mesh(geometry=teto_geometry, material=wood_tilling_material)
        self.add(self.teto)


    def update(self, delta_t_ms):
        delta_t_ms = delta_t_ms
