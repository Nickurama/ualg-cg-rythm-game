#!/usr/bin/python3
import pathlib
import sys
import math
import pygame
import time

from material.surface import SurfaceMaterial
from core.base import Base
from core_ext.camera import Camera
from core_ext.mesh import Mesh
from core_ext.renderer import Renderer
from core_ext.scene import Scene
from core_ext.texture import Texture
from extras.movement_rig import MovementRig
from geometry.sphere import SphereGeometry
from geometry.rectangle import RectangleGeometry
from geometry.geometry import Geometry
from light.ambient import AmbientLight
from light.directional import DirectionalLight
from light.point import PointLight
from material.flat import FlatMaterial
from material.lambert import LambertMaterial
from material.phong import PhongMaterial
from material.basic import BasicMaterial
from note import Note
from beatmap_player import BmPlayer
from ui import UI


class Example(Base):
    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.set_position([0, 0, 6])
        self.scene.add(self.rig)


        # Lighting
        ambient_light = AmbientLight(color=[0.01, 0.01, 0.01])
        directional_light = DirectionalLight(color=[1.0, 1.0, 1.0], direction=[-1, -1, -2])
        point_light1 = PointLight(color=[0.1, 0, 0], position=[4, 0, 0])
        point_light2 = PointLight(color=[0, 0.1, 0], position=[-4, 0, 0])
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

        # self.scene.add(sphere_left_top)
        # self.scene.add(sphere_center_top)
        # self.scene.add(sphere_right_top)
        # self.scene.add(sphere_left_bottom)
        # self.scene.add(sphere_center_bottom)
        # self.scene.add(sphere_right_bottom)


        # circle1 = Note(x=-1.2, y=0.0, z=3.0, radius=0.5, res=25, texture="images/note1.png", r=0.1, g=0.0, b=0.0)
        # circle2 = Note(x=-0.4, y=0.0, z=3.0, radius=0.5, res=25, texture="images/note2.png", r=0.1, g=0.0, b=0.0)
        # circle3 = Note(x= 0.4, y=0.0, z=3.0, radius=0.5, res=25, texture="images/note3.png", r=0.1, g=0.0, b=0.0)
        # circle4 = Note(x= 1.2, y=0.0, z=3.0, radius=0.5, res=25, texture="images/note1.png", r=0.1, g=0.0, b=0.0)
        # self.scene.add(circle1)
        # self.scene.add(circle2)
        # self.scene.add(circle3)
        # self.scene.add(circle4)

        self.ui = UI()
        self.scene.add(self.ui)

        # self.bm_player = BmPlayer("beatmaps/beatmap.bm", self.scene)
        self.bm_player = BmPlayer("beatmaps/beatmap_slow.bm", self.scene)
        # self.bm_player = BmPlayer("beatmaps/beatmap_rainbow.bm", self.scene)
        self.bm_player.start(time.perf_counter_ns())

        self.last_time_ns = time.perf_counter_ns()
        self.fps_sum = 0
        self.fps_count = 0
        self.ms_seconds_counter = 0
        self.fps = 0

    def update(self):
        curr_time_ns = time.perf_counter_ns()
        delta_t_ms = int((curr_time_ns - self.last_time_ns) / 1000000)
        curr_fps = 0
        if (delta_t_ms != 0):
            curr_fps = int(1000 / delta_t_ms)
        self.fps_sum += curr_fps
        self.fps_count += 1
        self.ms_seconds_counter += delta_t_ms
        self.last_time_ns = curr_time_ns

        if (self.ms_seconds_counter >= 1000):
            self.fps = int(self.fps_sum / self.fps_count)
            self.fps_sum = 0
            self.fps_count = 0
            self.ms_seconds_counter = 0


        self.bm_player.update(curr_time_ns, self.input)
        self.ui.update(self.fps, self.scene)
        self.renderer.render(self.scene, self.camera)

# Instantiate this class and run the program
Example(screen_size=[1200, 900]).run()
