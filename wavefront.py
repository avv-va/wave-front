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

    def get_neighbours_not_obs(self, map_idx):
        x, y = map_idx[0], map_idx[1]
        n_right = (x + 1, y)
        n_left = (x - 1, y)
        n_top = (x, y + 1)
        n_bottom = (x, y - 1)

        neighbours = []
        for neighbour in [n_right, n_left, n_top, n_bottom]:
            n_x, n_y = neighbour[0], neighbour[1]

            if n_x >= 0 and n_y < self.grid.map_column_size and self.grid.map[n_x][n_y] !=  Grid.Cell.OBS:
                neighbours.append(neighbour)

        return neighbours

    def find_path(self):
        value = 2
        finished = False

        print("start")
        while not finished:
            for x in range(self.grid.map_row_size):
                for y in range(self.grid.map_column_size):
                    
                    if self.valued_grid[x][y] == value:
                        neighbours = self.get_neighbours_not_obs((x, y))
                        print(neighbours)
                        

                        for neighbour in neighbours:
                            if self.valued_grid[neighbour[0]][neighbour[1]] == 0:
                                self.valued_grid[neighbour[0]][neighbour[1]] = value
                        if self.grid.map[x][y] == Grid.Cell.START:
                            finished = True
                            break

            value += 1
        print("done!")
    

    def print_valued_grid(self):
        for x in range(self.grid.map_row_size):
            for y in range(self.grid.map_column_size):
                
                cell_center = (x/4 + 0.25/2, y/4 + 0.25/2)
                value = self.valued_grid[x][y]
                plt.text(cell_center[0], cell_center[1], value, color="black")

                coord = self.grid.get_cell_coord_from_map_idx(x, y)
                xs, ys = zip(*coord)
                if self.grid.map[x][y] == Grid.Cell.OBS:
                    plt.plot(xs, ys, color='red')
                elif self.grid.map[x][y] == Grid.Cell.FREE:
                    plt.plot(xs, ys, color='yellow')
                elif self.grid.map[x][y] == Grid.Cell.GOAL:
                    plt.fill(xs, ys, color='green')
                elif self.grid.map[x][y] == Grid.Cell.START:
                    plt.fill(xs, ys, color='blue')
        
        plt.show()
