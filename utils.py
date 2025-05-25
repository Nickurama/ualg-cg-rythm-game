import math

class Utils:
    MAX_X = 2.308
    MAX_Y = 1.730
    PIXELS_X = 1200
    PIXELS_Y = 900

    @staticmethod
    def collides_rectangle(point, center, width, height):
        collide_x = center[0] - (width / 2.0) <= point[0] and center[0] + (width / 2.0) >= point[0]
        collide_y = center[1] - (height / 2.0) <= point[1] and center[1] + (height / 2.0) >= point[1]
        return collide_x and collide_y

    @staticmethod
    def toPixels(coord):
        normalized_x = (coord[0] + Utils.MAX_X) / (2 * Utils.MAX_X)
        normalized_y = (coord[1] + Utils.MAX_Y) / (2 * Utils.MAX_Y)
        pixel_x = int(Utils.PIXELS_X * normalized_x)
        pixel_y = int(Utils.PIXELS_Y * (1 - normalized_y))
        return [pixel_x, pixel_y]

    @staticmethod
    def toRelative(coord):
        normalized_x = coord[0] / Utils.PIXELS_X
        normalized_y = coord[1] / Utils.PIXELS_Y
        rel_x = normalized_x * 2 * Utils.MAX_X - Utils.MAX_X
        rel_y = (1 - normalized_y) * 2 * Utils.MAX_Y - Utils.MAX_Y
        return [rel_x, rel_y]

    @staticmethod
    def fillColor(r, g, b, n):
        curr_colors = []
        for i in range(n):
            curr_colors.append([r, g, b])
        return curr_colors

    @staticmethod
    def makeCircle(x, y, z, r, n):
        angle = 2 * math.pi / n
        curr_angle = 0.0;
        curr_points = []
        for i in range(n):
            curr_x = x + r * math.cos(curr_angle)
            curr_y = y + r * math.sin(curr_angle)
            curr_z = z
            curr_points.append([curr_x, curr_y, curr_z])
            if i > 0:
                curr_points.append([x, y, z])
                curr_points.append([curr_x, curr_y, curr_z])
            curr_angle += angle
        curr_points.append(curr_points[0])
        curr_points.append([x, y, z])

        return curr_points

    @staticmethod
    def makeCircleAndUvs(x, y, z, r, n):
        angle_step = 2 * math.pi / n
        vertices = []
        uvs = []

        center_uv = [0.5, 0.5]
        center_vert = [x, y, z]

        for i in range(n):
            angle = angle_step * i

            # vertices
            px = x + r * math.cos(angle)
            py = y + r * math.sin(angle)
            pz = z

            # uvs
            uv_x = 0.5 + 0.5 * math.cos(angle)
            uv_y = 0.5 + 0.5 * math.sin(angle)

            vertices.append([px, py, pz])
            uvs.append([uv_x, uv_y])
            if i > 0:
                vertices.append(center_vert)
                uvs.append(center_uv)
                vertices.append([px, py, pz])
                uvs.append([uv_x, uv_y])

        vertices.append(vertices[0])
        uvs.append(uvs[0])
        vertices.append(center_vert)
        uvs.append(center_uv)

        return vertices, uvs

    @staticmethod
    def makeCircleRaw(x, y, z, r, n):
        angle = 2 * math.pi / n
        curr_angle = 0.0;
        curr_points = []
        for i in range(n):
            curr_x = x + r * math.cos(curr_angle)
            curr_y = y + r * math.sin(curr_angle)
            curr_z = z
            curr_points.append([curr_x, curr_y, curr_z])
            curr_angle += angle

        return curr_points
