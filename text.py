from core_ext.object3d import Object3D
from material.texture import TextureMaterial
from core_ext.texture import Texture
from core_ext.mesh import Mesh
from geometry.rectangle import RectangleGeometry

class Text(Object3D):
    def __init__(self, text, padding, size, x, y, align_right=False):
        super().__init__()
        self.text = text
        self.padding = padding
        self.size = size
        self.x = x
        self.y = y
        self.align_right = align_right

        self.update(text)


    def update(self, text):
        if text == self.text:
            return
        self.text = text
        self._children_list = []

        counter = 0
        total_size = 0
        for char in str(text):
            geometry = RectangleGeometry(self.size, self.size);
            material = TextureMaterial(texture=Texture(f"images/font/font_{char}.png"))
            mesh = Mesh(geometry, material)
            mesh.set_position([(self.size / 2.0) + counter * self.padding * self.size, -self.size / 2.0, 0.0])
            counter += 1
            self.add(mesh)
        total_size += counter * self.size * self.padding
        if self.align_right:
            self.set_position([self.x - total_size, self.y, 3.0])
        else:
            self.set_position([self.x, self.y, 3.0])
