# credits: Margarida Moura, CGr 2022
#          Sergio Jesus, CG 2024 (modified)
#
"""Read vertices from OBJ file"""
from typing import List
def my_obj_reader(filename :str) -> tuple[List, List, List]:
    """Get the vertices from the file"""
    position_list = list()
    vertices = list()
    tex_coords = list()
    tex_coords_repeated = list()
    normals = list()
    normals_repeated = list()

    with open(filename, 'r') as in_file:
        for line in in_file:
            parts = line.strip().split()
            if not parts:
                continue

            # Parse UVs
            if parts[0] == 'vt':
                tex_coords.append([float(value) for value in parts[1:3]])

            # Parse normals (nx ny nz)
            elif parts[0] == 'vn':
                normal = [float(value) for value in parts[1:4]]
                normals.append(normal)

            # Parse vertices (v x y z)
            elif parts[0] == 'v':
                vertex = [float(value) for value in parts[1:4]]  # x, y, z
                vertices.append(vertex)

            # Parse faces (f v1/vt1 v2/vt2 ...)
            elif parts[0] == 'f':
                for part in parts[1:]:
                    indices = part.split('/')
                    vertex_index = int(indices[0]) - 1
                    uv_index = int(indices[1]) - 1
                    tex_coords_repeated.append(tex_coords[uv_index])
                    position_list.append(vertices[vertex_index])
                    if (len(indices) > 2):
                        normal_index = int(indices[2]) - 1
                        normals_repeated.append(normals[normal_index])

    return position_list, tex_coords_repeated, normals_repeated

if __name__ == '__main__':
    f_in = input("File? ")
    result = my_obj_reader(f_in)
    print(result)