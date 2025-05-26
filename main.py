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
from recital import Recital
from castanholas import Castanholas


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
        self.scene.add(ambient_light)
        self.directional_light = DirectionalLight(color=[0.5, 0.5, 0.5], direction=[-1, -1, -2])
        self.directional_light.set_position([0, 0, 0])
        self.scene.add(self.directional_light)

        # Scenario
        recital = Recital(light_sources=2)
        recital.rotate_y(math.pi)
        recital.set_position([0, -4, -10])
        self.scene.add(recital)

        # Instrumentos
        caixa = Caixa(light_sources=2)
        caixa.set_position([2.1, -1.2, -10])
        self.scene.add(caixa)

        castanholas = Castanholas(light_sources=2)
        castanholas.set_position([-1.7, -1.1, -10])
        self.scene.add(castanholas)

        # Beatmap Player
        self.bm_player = BmPlayer("beatmaps/recital.bm", self.scene)
        self.game_ui = UI()
        self.menu_ui = MenuUI()
        self.highscore_ui = HighscoreUI(0)

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
        # self.after_clock_ms = -1
        # self.update_main_menu = False
        # self.beatmap_ended = False
        # self.close_game_ui = False
        # self.update_highscore = True

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

        # renderer
        self.renderer.render(self.scene, self.camera)

# Instantiate this class and run the program
Example(screen_size=[1200, 900]).run()
