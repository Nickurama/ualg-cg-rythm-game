from core_ext.object3d import Object3D
from material.texture import TextureMaterial
from core_ext.texture import Texture
from core_ext.mesh import Mesh
from geometry.rectangle import RectangleGeometry
from core_ext.scene import Scene

class VFX:
    PERFECT_VFX_FILE = "images/perfect_vfx.png"
    GOOD_VFX_FILE = "images/good_vfx.png"
    OK_VFX_FILE = "images/ok_vfx.png"
    # MISS_VFX_FILE = "images/miss_vfx.png"
    MISS_VFX_FILE = "images/miss.png"
    VFX_LINGER_TIME_MS = 300

    def __init__(self, width, height, scene: Scene):
        self.geometry = RectangleGeometry(width, height);
        self.tiny_geometry = RectangleGeometry(width * 0.5, height * 0.15)
        self.width = width
        self.height = height
        self.scene = scene

        self.vfx_list = []
        self.remove_list = []

    def update(self, delta_t_ms):
        for vfx in self.vfx_list:
            vfx[2].set_alpha(vfx[1] / self.VFX_LINGER_TIME_MS)
            vfx[1] = vfx[1] - delta_t_ms
            if vfx[1] <= 0:
                self.remove_list.append(vfx)
        self.trigger_remove()

    def remove_all(self):
        for vfx in self.vfx_list:
            self.scene.remove(vfx[0])
        self.vfx_list = []

    def trigger_remove(self):
        for vfx in self.remove_list:
            self.vfx_list.remove(vfx)
            self.scene.remove(vfx[0])
        self.remove_list = []

    def create_perfect_vfx(self, x, y):
        texture = TextureMaterial(texture=Texture(self.PERFECT_VFX_FILE))
        mesh = Mesh(self.geometry, texture)
        mesh.set_position([x, y, 3.0])
        self.scene.add(mesh)
        self.vfx_list.append([mesh, self.VFX_LINGER_TIME_MS, texture])

    def create_good_vfx(self, x, y):
        texture = TextureMaterial(texture=Texture(self.GOOD_VFX_FILE))
        mesh = Mesh(self.geometry, texture)
        mesh.set_position([x, y, 3.0])
        self.scene.add(mesh)
        self.vfx_list.append([mesh, self.VFX_LINGER_TIME_MS, texture])

    def create_ok_vfx(self, x, y):
        texture = TextureMaterial(texture=Texture(self.OK_VFX_FILE))
        mesh = Mesh(self.geometry, texture)
        mesh.set_position([x, y, 3.0])
        self.scene.add(mesh)
        self.vfx_list.append([mesh, self.VFX_LINGER_TIME_MS, texture])

    def create_miss_vfx(self, x, y):
        texture = TextureMaterial(texture=Texture(self.MISS_VFX_FILE))
        mesh = Mesh(self.tiny_geometry, texture)
        mesh.set_position([x, y, 4.0])
        self.scene.add(mesh)
        self.vfx_list.append([mesh, self.VFX_LINGER_TIME_MS, texture])