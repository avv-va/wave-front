from shapely.geometry import Polygon
import matplotlib.pyplot as plt


class Grid:
    class Cell:
        START = 0
        GOAL = 1
        FREE = 2
        OBS = -1

    def __init__(self, start, goal, obstacles, x_range, y_range, grid_size=0.25) -> None:
        self.grid_size = grid_size
        

        # Making sure everything starts from zero
        x_range_c = (0, x_range[1] - x_range[0])
        y_range_c = (0, y_range[1] - y_range[0])
        start_c = (start[0] - x_range[0], start[1] - y_range[0])
        goal_c = (goal[0] - x_range[0], goal[1] - y_range[0])
        obstacles_c = []
        for obstacle in obstacles:
            coord = list(zip(*obstacle.exterior.coords.xy))
            coord_c = []
            for xy in coord:
                xy_c = (xy[0] - x_range[0], xy[1] - y_range[0])
                coord_c.append(xy_c)
            obstacles_c.append(Polygon(coord_c))
            
        

        self.start_index = self.get_map_indx(start_c[0], start_c[1])
        self.goal_index = self.get_map_indx(goal_c[0], goal_c[1])

        self.map = self.construct_map(start_c, goal_c, obstacles_c, x_range_c, y_range_c)
        self.map_row_size = len(self.map)
        self.map_column_size = len(self.map[0])

    def get_cell_coord_from_map_idx(self, x, y):
        x_left, y_bottom = x/4, y/4
        x_right, y_top = x/4 + self.grid_size, y/4 + self.grid_size
        coord = [(x_left, y_top), (x_left, y_bottom),
                 (x_right, y_bottom), (x_right, y_top)]
        coord.append(coord[0])
        return coord

    def get_map_indx(self, x, y):
        return 4 * x, 4 * y

    def cell_intersects_with_obstacles(self, cell_poly, obstacles):
        for obs in obstacles:
            if cell_poly.intersects(obs):
                return True
        return False

    def construct_map(self, start, goal, obstacles, x_range, y_range):
        grid_map = []

        x_range_map = self.get_map_indx(x_range[0], x_range[1])
        y_range_map = self.get_map_indx(y_range[0], y_range[1])

        for x in range(x_range_map[0], x_range_map[1]):
            row = []
            for y in range(y_range_map[0], y_range_map[1]):
                coord = self.get_cell_coord_from_map_idx(x, y)
                cell = Polygon(coord)

                if self.cell_intersects_with_obstacles(cell, obstacles):
                    row.append(self.Cell.OBS)
                else:
                    row.append(self.Cell.FREE)
            grid_map.append(row)

        grid_map[self.start_index[0]][self.start_index[1]] = self.Cell.START
        grid_map[self.goal_index[0]][self.goal_index[1]] = self.Cell.GOAL

        return grid_map

    def print_grid(self):
        for x in range(self.map_row_size):
            for y in range(self.map_column_size):
                coord = self.get_cell_coord_from_map_idx(x, y)
                xs, ys = zip(*coord)
                if self.map[x][y] == self.Cell.OBS:
                    plt.plot(xs, ys, color='red')
                elif self.map[x][y] == self.Cell.FREE:
                    plt.plot(xs, ys, color='yellow')
                elif self.map[x][y] == self.Cell.GOAL:
                    plt.fill(xs, ys, color='green')
                elif self.map[x][y] == self.Cell.START:
                    plt.fill(xs, ys, color='blue')
        # plt.show()
        # plt.savefig("figure.png")
