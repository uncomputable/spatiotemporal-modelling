import collections
import math

from typing import List, Tuple


def distance(pos1, pos2):
    squared_distance = 0
    for i in range(0, len(pos1)):
        squared_distance += (pos1[i] - pos2[i]) ** 2
    return math.sqrt(squared_distance)


Particle1D = collections.namedtuple("Particle", ["x"])  # Wrapper
Particle2D = collections.namedtuple("Particle", ["x", "y"])  # Wrapper
Particle1D1 = collections.namedtuple("Particle", ["x", "strength0"])
Particle2D1 = collections.namedtuple("Particle", ["x", "y", "strength0"])
Particle2D2 = collections.namedtuple("Particle", ["x", "y", "strength0", "strength1"])
CellIndex1D = collections.namedtuple("CellIndex2D", ["x"])
CellIndex2D = collections.namedtuple("CellIndex2D", ["x", "y"])
Environment = collections.namedtuple("Environment", ["D", "domain_lower_bound", "domain_upper_bound",
                                                     "particle_number_per_dim", "h", "epsilon", "volume_p", "cutoff",
                                                     "cell_side", "t_max", "dt"])


class CellList:

    def __init__(self, positions):
        for pos_index, pos in enumerate(positions):
            cell_index = self.pos_get_cell_index(pos)
            self[cell_index].append(pos_index)

    def pos_get_cell_index(self, pos):
        pass

    def get_neighbour_cell_indices(self, cell_index):
        pass

    def __getitem__(self, item):
        pass


class CellList1D(CellList):

    def __init__(self, positions: List[Tuple[float]], lower_bound: int, upper_bound: int, cell_side: float):
        self.dim_width = math.floor((upper_bound - lower_bound) / cell_side) + 1
        self.cell_side = cell_side
        self.cells: List[List[int]] = [[] for _ in range(0, self.dim_width)]

        CellList.__init__(self, positions)

    def pos_get_cell_index(self, pos: Tuple[float]):
        return CellIndex1D(math.floor(pos[0] / self.cell_side))

    def get_neighbour_cell_indices(self, cell_index: CellIndex1D):
        neighbour_indices = []
        for dx in [-1, 0, 1]:
            x = cell_index.x + dx
            if 0 <= x < self.dim_width :
                neighbour_indices.append(CellIndex1D(x))
        return neighbour_indices

    def __getitem__(self, item: CellIndex1D):
        return self.cells[item.x]


class CellList2D(CellList):

    def __init__(self, positions: List[Tuple[float, float]], lower_bound: int, upper_bound: int, cell_side: float):
        self.cell_side = cell_side
        self.dim_width = math.floor((upper_bound - lower_bound) / cell_side) + 1
        self.cells: List[List[List[int]]] = [[[] for _ in range(0, self.dim_width)] for _ in range(0, self.dim_width)]

        CellList.__init__(self, positions)

    def pos_get_cell_index(self, pos: Tuple[float, float]):
        x_index = math.floor(pos[0] / self.cell_side)
        y_index = math.floor(pos[1] / self.cell_side)
        return CellIndex2D(x_index, y_index)

    def get_neighbour_cell_indices(self, cell_index: CellIndex2D):
        neighbour_indices = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                x = cell_index.x + dx
                y = cell_index.y + dy

                if 0 <= x < self.dim_width and 0 <= y < self.dim_width:
                    neighbour_indices.append(CellIndex2D(x, y))
        return neighbour_indices

    def __getitem__(self, item: CellIndex2D):
        return self.cells[item.x][item.y]


class VerletList:

    def __init__(self, positions, cell_list: CellList, cutoff: float):
        num_particles = len(positions)
        self.cells = [[] for _ in range(0, num_particles)]

        for pos_index, pos in enumerate(positions):
            cell_index = cell_list.pos_get_cell_index(pos)
            neighbour_indices = cell_list.get_neighbour_cell_indices(cell_index)

            for neighbour_index in neighbour_indices:
                for other_pos_index in cell_list[neighbour_index]:
                    other_pos = positions[other_pos_index]
                    if distance(pos, other_pos) <= cutoff:
                        self.cells[pos_index].append(other_pos_index)

    def __getitem__(self, item: int):
        return self.cells[item]
