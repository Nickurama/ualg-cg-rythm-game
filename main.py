#!/usr/bin/python3
import pathlib
import sys
import math
import pygame
import os
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
from geometry.box import BoxGeometry
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
from menu_ui import MenuUI
from highscore_ui import HighscoreUI
from text import Text
from utils import Utils
from caixa import Caixa
from guitarra import Guitarra
from recital import Recital
from castanholas import Castanholas
from core_ext.object3d import Object3D


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
        self.everything = Object3D()
        ambient_light = AmbientLight(color=[0.01, 0.01, 0.01])
        self.everything.add(ambient_light)
        #self.scene.add(ambient_light)


        self.directional_light1 = DirectionalLight(color=[0.3, 0.3, 0.3])
        self.directional_light1.set_position([0, 6, -12.0])
        #self.directional_light1.look_at([0.0, -1.0, -12.0])
        self.everything.add(self.directional_light1)
        #self.scene.add(self.directional_light1)


        self.directional_light3 = DirectionalLight(color=[0.3, 0.3, 0.3])
        self.directional_light3.set_position([0, 6, -3.0])
        self.directional_light3.look_at([-3.0, 0.0, -12.0])
        self.everything.add(self.directional_light3)
        #self.scene.add(self.directional_light3)

        rotation = 0.3

        # Scenario
        self.recital = Recital(light_sources=3)
        self.recital.rotate_y(math.pi)
        self.recital.set_position([0, -4, -10])
        #self.scene.add(self.recital)
        self.everything.add(self.recital)
        # Instrumentos
        self.instruments = Object3D()
        self.caixa = Caixa(light_sources=3)
        self.caixa.set_position([-2.0, -1.2, -12])
        self.instruments.add(self.caixa)
        #self.scene.add(self.caixa)

        self.castanholas = Castanholas(light_sources=3)
        self.castanholas.set_position([-5.6, -1.1, -12])
        self.castanholas.scale(0.5)
        self.instruments.add(self.castanholas)
        #self.scene.add(self.castanholas)

        self.guitarra = Guitarra(light_sources=3)
        self.guitarra.set_position([1.6, -1.1, -12])
        self.guitarra.rotate_y(-90)
        self.guitarra.scale(0.6)
        self.instruments.add(self.guitarra)

        #self.instruments.rotate_x(rotation)
        #self.scene.add(self.instruments)
        self.everything.add(self.instruments)
        self.scene.add(self.everything)
        self.everything.rotate_x(rotation)
        self.everything.rotate_y(1.1)
        self.everything.set_position([8, 2, -5])
        #self.scene.add(self.guitarra)

        # Beatmap Player
        self.bm_player = BmPlayer("beatmaps/recital.bm", self.scene)
        self.game_ui = UI()
        self.menu_ui = MenuUI()
        self.highscore_ui = HighscoreUI(0)

        # setup
        self.scene.add(self.menu_ui)


        self.last_time_ns = time.perf_counter_ns()
        self.fps_sum = 0
        self.fps_count = 0
        self.ms_seconds_counter = 0
        self.fps = 0

        self.after_clock_ms = -1
        self.update_main_menu = True
        self.beatmap_ended = False
        self.close_game_ui = False
        self.update_highscore = False

    def update(self):
        # metrics
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


        # main update loop
        is_player_active = self.bm_player.started
        self.bm_player.update(curr_time_ns, delta_t_ms, self.input)
        if (is_player_active and not self.bm_player.started):
            self.beatmap_ended = True
            self.after_clock_ms = 0
        if self.beatmap_ended:
            tmp = self.after_clock_ms
            self.after_clock_ms += delta_t_ms
            if (tmp <= 2000 and self.after_clock_ms > 2000):
                self.close_game_ui = True
                self.beatmap_ended = False

        if self.close_game_ui:
            self.close_game_ui = False
            self.scene.remove(self.game_ui)
            self.update_highscore = True
            HighscoreUI.write_highscore(HighscoreUI.HIGHSCORES_FILE, Utils.get_username(), int(self.bm_player.score))
            self.highscore_ui = HighscoreUI(self.bm_player.score)
            self.scene.add(self.highscore_ui)

        if self.bm_player.started or self.after_clock_ms <= 2000:
            self.game_ui.update(self.fps, self.bm_player.combo, int(self.bm_player.score), self.scene)

        if self.update_main_menu:
            play = self.menu_ui.update(self.input)
            if play:
                self.update_main_menu = False
                self.scene.remove(self.menu_ui)
                self.bm_player.start(time.perf_counter_ns())
                self.scene.add(self.game_ui)

        if self.update_highscore:
            should_continue = self.highscore_ui.update(self.input)
            if should_continue:
                self.update_highscore = False
                self.scene.remove(self.highscore_ui)
                self.update_main_menu = True
                self.scene.add(self.menu_ui)

        self.caixa.update(delta_t_ms)
        self.guitarra.update(delta_t_ms)
        self.castanholas.update(delta_t_ms)

        # renderer
        self.renderer.render(self.scene, self.camera)

# Instantiate this class and run the program
Example(screen_size=[1200, 900]).run()
