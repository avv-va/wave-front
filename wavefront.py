from tracemalloc import start
import matplotlib.pyplot as plt
from grid import Grid


class Wavefront:
    def __init__(self, grid) -> None:
        self.grid = grid
        self.valued_grid = self.init_path_grid()

    def init_path_grid(self):
        path_grid = []
        for x in range(self.grid.map_row_size):
            row = []
            for y in range(self.grid.map_column_size):
                if self.grid.map[x][y] == Grid.Cell.OBS:
                    row.append(1)
                elif self.grid.map[x][y] == Grid.Cell.GOAL:
                    row.append(2)
                else:
                    row.append(0)
            path_grid.append(row)
        return path_grid

    def get_neighbours(self, map_idx):
        x, y = map_idx[0], map_idx[1]
        n_right = (x + 1, y)
        n_left = (x - 1, y)
        n_top = (x, y + 1)
        n_bottom = (x, y - 1)

        neighbours = []
        for neighbour in [n_right, n_left, n_top, n_bottom]:
            n_x, n_y = neighbour[0], neighbour[1]
            if n_x >= 0 and n_y >= 0 and n_x < self.grid.map_row_size and n_y < self.grid.map_column_size:
                neighbours.append(neighbour)

        return neighbours

    def find_path(self):
        self.grow_wave()

        start_cell_idx = self.grid.start_index
        goal_cell_idx = self.grid.goal_index
        cell_idx = start_cell_idx

        self.path = [start_cell_idx]

        while cell_idx != goal_cell_idx:
            neighbours = self.get_neighbours((cell_idx[0], cell_idx[1]))
            current_val = self.valued_grid[cell_idx[0]][cell_idx[1]]
            for neigh in neighbours:
                neigh_val = self.valued_grid[neigh[0]][neigh[1]]
                if current_val - neigh_val == 1:
                    self.path.append(neigh)
                    cell_idx = neigh
                    break

    def grow_wave(self):
        value = 2
        finished = False
        while not finished:
            for x in range(self.grid.map_row_size):
                for y in range(self.grid.map_column_size):

                    if self.valued_grid[x][y] == value:
                        neighbours = self.get_neighbours((x, y))
                        for neighbour in neighbours:
                            if self.valued_grid[neighbour[0]][neighbour[1]] == 0:
                                self.valued_grid[neighbour[0]
                                                 ][neighbour[1]] = value + 1

                        if self.grid.map[x][y] == Grid.Cell.START:
                            finished = True
                            break

            value += 1

    def print_valued_grid(self):
        plt.rcParams.update({'font.size': 6})

        for x in range(self.grid.map_row_size):
            for y in range(self.grid.map_column_size):

                cell_center = (x/4 + 0.25/3, y/4 + 0.25/5)
                value = self.valued_grid[x][y]
                plt.text(cell_center[0], cell_center[1],
                         value, color="black", weight='bold')

                coord = self.grid.get_cell_coord_from_map_idx(x, y)
                xs, ys = zip(*coord)

                if (x, y) in self.path:
                    plt.fill(xs, ys, color='purple')

                if self.grid.map[x][y] == Grid.Cell.OBS:
                    plt.plot(xs, ys, color='red')
                elif self.grid.map[x][y] == Grid.Cell.FREE:
                    plt.plot(xs, ys, color='gray')
                elif self.grid.map[x][y] == Grid.Cell.GOAL:
                    plt.fill(xs, ys, color='green')
                elif self.grid.map[x][y] == Grid.Cell.START:
                    plt.fill(xs, ys, color='yellow')

        plt.show()
