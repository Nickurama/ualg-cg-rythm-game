import OpenGL.GL as GL

from material.material import Material


class TextureMaterial(Material):
    def __init__(self, texture, property_dict=None, alpha=1.0):
        vertex_shader_code = """
            uniform mat4 projectionMatrix;
            uniform mat4 viewMatrix;
            uniform mat4 modelMatrix;
            in vec3 vertexPosition;
            in vec2 vertexUV;
            uniform vec2 repeatUV;
            uniform vec2 offsetUV;
            out vec2 UV;
            void main()
            {
                gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
                UV = vertexUV * repeatUV + offsetUV;
            }
        """

        fragment_shader_code = """
            uniform vec3 baseColor;
            uniform sampler2D textureSampler;
            uniform float alpha;
            in vec2 UV;
            out vec4 fragColor;
            void main()
            {
                vec4 color = vec4(baseColor, alpha) * texture(textureSampler, UV);
                if (color.a < 0.100)
                    discard;                    
                fragColor = color;
            }
        """
        super().__init__(vertex_shader_code, fragment_shader_code)
        self.add_uniform("vec3", "baseColor", [1.0, 1.0, 1.0])
        self.add_uniform("sampler2D", "textureSampler", [texture.texture_ref, 1])
        self.add_uniform("vec2", "repeatUV", [1.0, 1.0])
        self.add_uniform("vec2", "offsetUV", [0.0, 0.0])
        self.add_uniform("float", "alpha", alpha)
        self.locate_uniforms()
        # Render both sides?
        self.setting_dict["doubleSide"] = True
        # Render triangles as wireframe?
        self.setting_dict["wireframe"] = False
        # line thickness for wireframe rendering
        self.setting_dict["lineWidth"] = 1
        self.set_properties(property_dict)

    def set_alpha(self, alpha):
        self.add_uniform("float", "alpha", alpha)
        self.locate_uniforms()

    def update_render_settings(self):
        if self.setting_dict["doubleSide"]:
            GL.glDisable(GL.GL_CULL_FACE)
        else:
            GL.glEnable(GL.GL_CULL_FACE)
        if self.setting_dict["wireframe"]:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        else:
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        GL.glLineWidth(self.setting_dict["lineWidth"])
