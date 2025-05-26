from material.material import Material
from core.uniform import Uniform


class BasicMaterial(Material):
    def __init__(self, vertex_shader_code=None, fragment_shader_code=None, use_vertex_colors=True, alpha=1.0):
        if vertex_shader_code is None:
            vertex_shader_code = """
                uniform mat4 projectionMatrix;
                uniform mat4 viewMatrix;
                uniform mat4 modelMatrix;
                in vec3 vertexPosition;
                in vec3 vertexColor;
                out vec3 color;    
                        
                void main()
                {
                    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
                    color = vertexColor;
                }
            """
        if fragment_shader_code is None:
            fragment_shader_code = """
                uniform vec3 baseColor;
                uniform bool useVertexColors;
                uniform float alpha;
                in vec3 color;
                out vec4 fragColor;
                
                void main()
                {
                    fragColor = vec4(baseColor, alpha);
                    if (useVertexColors) 
                    {
                        fragColor = vec4(color, alpha);
                    }
                }
            """
        super().__init__(vertex_shader_code, fragment_shader_code)
        self.add_uniform("vec3", "baseColor", [1.0, 1.0, 1.0])
        self.add_uniform("float", "alpha", alpha)
        if use_vertex_colors:
            self.add_uniform("bool", "useVertexColors", False)
        self.locate_uniforms()

    def set_alpha(self, alpha):
        self.add_uniform("float", "alpha", alpha)
        self.locate_uniforms()

