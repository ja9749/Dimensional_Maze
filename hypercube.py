import itertools
import numpy as np

class Hypercube:
    def __init__(self, dim_num):
        print("\ndim_num", dim_num)

        line_vertices = list(itertools.product([0.999, -0.999], repeat=dim_num))
        temp_vertices = list(itertools.product([0.9999, -0.9999], repeat=dim_num))

        wall_vertices = []
        wall_line_vertices = []
        for i in range(0, 2 * dim_num):
            wall_vertices.append([])
            wall_line_vertices.append([])
            for vertex in temp_vertices:
                if ((i & 1) and (vertex[i >> 1] < 0)) \
                or (not (i & 1) and (vertex[i >> 1] > 0)):
                    wall_vertices[i].append(vertex)
                    wall_line_vertices[i].append(vertex)

        wall_edges = []
        wall_surfaces_vertices = []
        wall_surface_edges = []
        wall_cube_vertices = []
        wall_cube_edges = []
        vertices = wall_vertices[0]

        edges = []
        line_edges = []
        surfaces_vertices = []
        surface_edges = []
        line_surfaces_vertices = []
        line_surface_edges = []
        cube_vertices = []
        cube_edges = []

        edge_combo = [(i, j) for i in range(0, len(vertices))
                             for j in range(i + 1, len(vertices))]

        for (i, j) in edge_combo:
            if np.sum(np.array(vertices[i]) != np.array(vertices[j])) == 1:
                edges.append((i, j))

        line_edge_combo = [(i, j) for i in range(0, len(line_vertices))
                             for j in range(i + 1, len(line_vertices))]

        for (i, j) in line_edge_combo:
            if np.sum(np.array(line_vertices[i]) != np.array(line_vertices[j])) == 1:
                line_edges.append((i, j))

        surface_combo = [(i, j, k, l) for i in range(0, len(vertices))
                                      for j in range(i + 1, len(vertices))
                                      for k in range(j + 1, len(vertices))
                                      for l in range(k + 1, len(vertices))]

        for (i, j, k, l) in surface_combo:
            if np.sum(np.array(vertices[i]) != np.array(vertices[j])) == 1 \
            and np.sum(np.array(vertices[i]) != np.array(vertices[k])) == 1 \
            and np.sum(np.array(vertices[l]) != np.array(vertices[j])) == 1 \
            and np.sum(np.array(vertices[l]) != np.array(vertices[k])) == 1:
                surfaces_vertices.append((i, j, l, k))
                surface_edges.append((edges.index((i, j)),
                                    edges.index((i, k)),
                                    edges.index((j, l)),
                                    edges.index((k, l))))

        line_surface_combo = [(i, j, k, l) for i in range(0, len(line_vertices))
                                      for j in range(i + 1, len(line_vertices))
                                      for k in range(j + 1, len(line_vertices))
                                      for l in range(k + 1, len(line_vertices))]

        for (i, j, k, l) in line_surface_combo:
            if np.sum(np.array(line_vertices[i]) != np.array(line_vertices[j])) == 1 \
            and np.sum(np.array(line_vertices[i]) != np.array(line_vertices[k])) == 1 \
            and np.sum(np.array(line_vertices[l]) != np.array(line_vertices[j])) == 1 \
            and np.sum(np.array(line_vertices[l]) != np.array(line_vertices[k])) == 1:
                line_surfaces_vertices.append((i, j, l, k))
                line_surface_edges.append((line_edges.index((i, j)),
                                    line_edges.index((i, k)),
                                    line_edges.index((j, l)),
                                    line_edges.index((k, l))))

        cube_combo = [(i, j, k, l, m, n, o, p) for i in range(0, len(vertices))
                                               for j in range(i + 1, len(vertices))
                                               for k in range(j + 1, len(vertices))
                                               for l in range(k + 1, len(vertices))
                                               for m in range(l + 1, len(vertices))
                                               for n in range(m + 1, len(vertices))
                                               for o in range(n + 1, len(vertices))
                                               for p in range(o + 1, len(vertices))]

        count = 0
        for (i, j, k, l, m, n, o, p) in cube_combo:
            if np.sum(np.array(vertices[i]) != np.array(vertices[j])) == 1 \
            and np.sum(np.array(vertices[i]) != np.array(vertices[k])) == 1 \
            and np.sum(np.array(vertices[l]) != np.array(vertices[j])) == 1 \
            and np.sum(np.array(vertices[l]) != np.array(vertices[k])) == 1 \
            and np.sum(np.array(vertices[m]) != np.array(vertices[n])) == 1 \
            and np.sum(np.array(vertices[m]) != np.array(vertices[o])) == 1 \
            and np.sum(np.array(vertices[p]) != np.array(vertices[n])) == 1 \
            and np.sum(np.array(vertices[p]) != np.array(vertices[o])) == 1 \
            and np.sum(np.array(vertices[i]) != np.array(vertices[j])) == 1 \
            and np.sum(np.array(vertices[i]) != np.array(vertices[m])) == 1 \
            and np.sum(np.array(vertices[n]) != np.array(vertices[j])) == 1 \
            and np.sum(np.array(vertices[n]) != np.array(vertices[m])) == 1 \
            and np.sum(np.array(vertices[i]) != np.array(vertices[k])) == 1 \
            and np.sum(np.array(vertices[i]) != np.array(vertices[m])) == 1 \
            and np.sum(np.array(vertices[o]) != np.array(vertices[k])) == 1 \
            and np.sum(np.array(vertices[o]) != np.array(vertices[m])) == 1 \
            and np.sum(np.array(vertices[l]) != np.array(vertices[j])) == 1 \
            and np.sum(np.array(vertices[l]) != np.array(vertices[p])) == 1 \
            and np.sum(np.array(vertices[n]) != np.array(vertices[j])) == 1 \
            and np.sum(np.array(vertices[n]) != np.array(vertices[p])) == 1 \
            and np.sum(np.array(vertices[l]) != np.array(vertices[k])) == 1 \
            and np.sum(np.array(vertices[l]) != np.array(vertices[p])) == 1 \
            and np.sum(np.array(vertices[o]) != np.array(vertices[k])) == 1 \
            and np.sum(np.array(vertices[o]) != np.array(vertices[p])) == 1:
                count += 1
                cube_vertices.append((i, j, k, l, m, n, o, p))
                cube_edges.append((
                    edges.index((i, j)),
                    edges.index((i, k)),
                    edges.index((i, m)),
                    edges.index((j, l)),
                    edges.index((j, n)),
                    edges.index((k, l)),
                    edges.index((k, o)),
                    edges.index((l, p)),
                    edges.index((m, n)),
                    edges.index((m, o)),
                    edges.index((n, p)),
                    edges.index((o, p)),
                ))

        self.vertices = wall_vertices
        self.line_vertices = line_vertices
        self.edges = edges
        self.line_edges = line_edges
        self.surfaces_vertices = surfaces_vertices
        self.surface_edges = surface_edges
        self.line_surfaces_vertices = line_surfaces_vertices
        self.line_surface_edges = line_surface_edges
        self.cube_vertices = cube_edges
        self.cube_edges = cube_edges