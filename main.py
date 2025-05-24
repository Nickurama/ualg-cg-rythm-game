#!/usr/bin/python3
import pathlib
import sys
import math

from material.surface import SurfaceMaterial
from core.base import Base
from core_ext.camera import Camera
from core_ext.mesh import Mesh
from core_ext.renderer import Renderer
from core_ext.scene import Scene
from core_ext.texture import Texture
from extras.movement_rig import MovementRig
from geometry.sphere import SphereGeometry
from geometry.geometry import Geometry
from light.ambient import AmbientLight
from light.directional import DirectionalLight
from light.point import PointLight
from material.flat import FlatMaterial
from material.lambert import LambertMaterial
from material.phong import PhongMaterial
from material.basic import BasicMaterial
from circle import Circle


class Example(Base):
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.set_position([0, 0, 6])
        # self.rig.set_position([0, 0, 0.5])
        self.scene.add(self.rig)


        # Lighting
        ambient_light = AmbientLight(color=[0.1, 0.1, 0.1])
        directional_light = DirectionalLight(color=[3.0, 3.0, 3.0], direction=[-1, -1, -2])
        point_light1 = PointLight(color=[0.9, 0, 0], position=[4, 0, 0])
        point_light2 = PointLight(color=[0, 0.9, 0], position=[-4, 0, 0])
        self.scene.add(ambient_light)
        self.scene.add(directional_light)
        self.scene.add(point_light1)
        self.scene.add(point_light2)

        basecolor_material = BasicMaterial()

        # lighted materials with a color
        flat_material = FlatMaterial(
            property_dict={"baseColor": [0.2, 0.5, 0.5]},
            number_of_light_sources=4
        )
        lambert_material = LambertMaterial(
            property_dict={"baseColor": [0.2, 0.5, 0.5]},
            number_of_light_sources=4
        )
        phong_material = PhongMaterial(
            property_dict={"baseColor": [0.2, 0.5, 0.5]},
            number_of_light_sources=4
        )


        # lighted spheres with a color
        sphere_geometry = SphereGeometry()
        sphere_left_top = Mesh(sphere_geometry, flat_material)
        sphere_left_top.set_position([-2.5, 1.5, 0])
        sphere_center_top = Mesh(sphere_geometry, lambert_material)
        sphere_center_top.set_position([0, 1.5, 0])
        sphere_right_top = Mesh(sphere_geometry, phong_material)
        sphere_right_top.set_position([2.5, 1.5, 0])

        # lighted materials with a texture
        textured_flat_material = FlatMaterial(
            texture=Texture("images/grid.jpg"),
            number_of_light_sources=4
        )
        textured_lambert_material = LambertMaterial(
            texture=Texture("images/grid.jpg"),
            number_of_light_sources=4
        )
        textured_phong_material = PhongMaterial(
            texture=Texture("images/grid.jpg"),
            number_of_light_sources=4
        )


        # lighted spheres with a texture
        sphere_left_bottom = Mesh(sphere_geometry, textured_flat_material)
        sphere_left_bottom.set_position([-2.5, -1.5, 0])
        sphere_center_bottom = Mesh(sphere_geometry, textured_lambert_material)
        sphere_center_bottom.set_position([0, -1.5, 0])
        sphere_right_bottom = Mesh(sphere_geometry, textured_phong_material)
        sphere_right_bottom.set_position([2.5, -1.5, 0])

        self.scene.add(sphere_left_top)
        self.scene.add(sphere_center_top)
        self.scene.add(sphere_right_top)
        self.scene.add(sphere_left_bottom)
        self.scene.add(sphere_center_bottom)
        self.scene.add(sphere_right_bottom)


        # testing
        circle = Circle(x=2.0, y=1.5, z=3.0, radius=0.1, res=25, r=1.0, g=0.0, b=1.0)

        self.scene.add(circle)




    def update(self):
        speed = -0.01
        # self.circle_rig.translate(0, speed, 0)
        # self.rig.rotate_y(math.pi * speed * self.delta_time, False);
        # self.rig.update(self.input, self.delta_time)
        self.renderer.render(self.scene, self.camera)

# Instantiate this class and run the program
Example(screen_size=[800, 600]).run()
