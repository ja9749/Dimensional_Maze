import itertools
import numpy as np

class Hypercube:
    def __init__(self, dim_num):
        print("\ndim_num", dim_num)

        # line_vertices = list(itertools.product([0.999, -0.999], repeat=dim_num))
        vertices = list(itertools.product([0.9999, -0.9999], repeat=dim_num))
        inner_vertices = list(itertools.product([-0.0009, 0.0009], repeat=dim_num))

        wall_vertices = []
        for i in range(2 * dim_num):
            wall_vertices.append([])
            for j in range(len(vertices)):
                vertex = vertices[j]
                if ((i & 1) and (vertex[i >> 1] < 0)) \
                or (not (i & 1) and (vertex[i >> 1] > 0)):
                    wall_vertices[i].append(j)

        wall_edges = []
        wall_surfaces = []
        wall_cubes = []

        sample = wall_vertices[0]

        edge_combo = [(i, j) for i in range(0, len(sample))
                             for j in range(i + 1, len(sample))]

        sample_edges = []

        for (i, j) in edge_combo:
            if np.sum(np.array(vertices[sample[i]]) != np.array(vertices[sample[j]])) == 1:
                sample_edges.append((i, j))

        wall_edges = [[(wall[edge[0]], wall[edge[1]]) for edge in sample_edges] for wall in wall_vertices]

        surface_combo = [(i, j, k, l) for i in range(0, len(sample))
                                      for j in range(i + 1, len(sample))
                                      for k in range(j + 1, len(sample))
                                      for l in range(k + 1, len(sample))]

        sample_surfaces = []

        for (i, j, k, l) in surface_combo:
            if np.sum(np.array(vertices[sample[i]]) != np.array(vertices[sample[j]])) == 1 \
            and np.sum(np.array(vertices[sample[i]]) != np.array(vertices[sample[k]])) == 1 \
            and np.sum(np.array(vertices[sample[l]]) != np.array(vertices[sample[j]])) == 1 \
            and np.sum(np.array(vertices[sample[l]]) != np.array(vertices[sample[k]])) == 1:
                sample_surfaces.append((i, j, l, k))

        wall_surfaces = [[(wall[surface[0]], wall[surface[1]], wall[surface[2]], wall[surface[3]])
                         for surface in sample_surfaces] for wall in wall_vertices]

        cube_combo = [(i, j, k, l, m, n, o, p) for i in range(0, len(sample))
                                               for j in range(i + 1, len(sample))
                                               for k in range(j + 1, len(sample))
                                               for l in range(k + 1, len(sample))
                                               for m in range(l + 1, len(sample))
                                               for n in range(m + 1, len(sample))
                                               for o in range(n + 1, len(sample))
                                               for p in range(o + 1, len(sample))]

        sample_cubes = []

        count = 0
        for (i, j, k, l, m, n, o, p) in cube_combo:
            if np.sum(np.array(vertices[sample[i]]) != np.array(vertices[sample[j]])) == 1 \
            and np.sum(np.array(vertices[sample[i]]) != np.array(vertices[sample[k]])) == 1 \
            and np.sum(np.array(vertices[sample[l]]) != np.array(vertices[sample[j]])) == 1 \
            and np.sum(np.array(vertices[sample[l]]) != np.array(vertices[sample[k]])) == 1 \
            and np.sum(np.array(vertices[sample[m]]) != np.array(vertices[sample[n]])) == 1 \
            and np.sum(np.array(vertices[sample[m]]) != np.array(vertices[sample[o]])) == 1 \
            and np.sum(np.array(vertices[sample[p]]) != np.array(vertices[sample[n]])) == 1 \
            and np.sum(np.array(vertices[sample[p]]) != np.array(vertices[sample[o]])) == 1 \
            and np.sum(np.array(vertices[sample[i]]) != np.array(vertices[sample[j]])) == 1 \
            and np.sum(np.array(vertices[sample[i]]) != np.array(vertices[sample[m]])) == 1 \
            and np.sum(np.array(vertices[sample[n]]) != np.array(vertices[sample[j]])) == 1 \
            and np.sum(np.array(vertices[sample[n]]) != np.array(vertices[sample[m]])) == 1 \
            and np.sum(np.array(vertices[sample[i]]) != np.array(vertices[sample[k]])) == 1 \
            and np.sum(np.array(vertices[sample[i]]) != np.array(vertices[sample[m]])) == 1 \
            and np.sum(np.array(vertices[sample[o]]) != np.array(vertices[sample[k]])) == 1 \
            and np.sum(np.array(vertices[sample[o]]) != np.array(vertices[sample[m]])) == 1 \
            and np.sum(np.array(vertices[sample[l]]) != np.array(vertices[sample[j]])) == 1 \
            and np.sum(np.array(vertices[sample[l]]) != np.array(vertices[sample[p]])) == 1 \
            and np.sum(np.array(vertices[sample[n]]) != np.array(vertices[sample[j]])) == 1 \
            and np.sum(np.array(vertices[sample[n]]) != np.array(vertices[sample[p]])) == 1 \
            and np.sum(np.array(vertices[sample[l]]) != np.array(vertices[sample[k]])) == 1 \
            and np.sum(np.array(vertices[sample[l]]) != np.array(vertices[sample[p]])) == 1 \
            and np.sum(np.array(vertices[sample[o]]) != np.array(vertices[sample[k]])) == 1 \
            and np.sum(np.array(vertices[sample[o]]) != np.array(vertices[sample[p]])) == 1:
                count += 1
                sample_cubes.append((i, j, k, l, m, n, o, p))

        wall_cubes = [[(wall[cube[0]], wall[cube[1]], wall[cube[2]], wall[cube[3]],
                      wall[cube[4]], wall[cube[5]], wall[cube[6]], wall[cube[7]])
                      for cube in sample_cubes] for wall in wall_vertices]

        self.vertices = vertices
        self.inner_vertices = inner_vertices
        self.wall_vertices = wall_vertices
        self.wall_edges = wall_edges
        self.wall_surfaces = wall_surfaces
        self.wall_cubes = wall_cubes