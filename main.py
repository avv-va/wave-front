import wave
from shapely.geometry import Polygon
from grid import Grid
from wavefront import Wavefront

def get_obstacles_polygon_world2():
    w_o_1 = Polygon([(-6, -6), (25, -6), (25, -5), (-6, -5)])
    w_o_2 = Polygon([(-6, 5), (30, 5), (30, 6), (-6, 6)])
    w_o_3 = Polygon([(-6, -5), (-5, -5), (-5, 5), (-6, 5)])
    w_o_4 = Polygon([(4, -5), (5, -5), (5, 1), (4, 1)])
    w_o_5 = Polygon([(9, 0), (10, 0), (10, 5), (9, 5)])
    w_o_6 = Polygon([(14, -5), (15, -5), (15, 1), (14, 1)])
    w_o_7 = Polygon([(19, 0), (20, 0), (20, 5), (19, 5)])
    w_o_8 = Polygon([(24, -5), (25, -5), (25, 1), (24, 1)])
    w_o_9 = Polygon([(29, 0), (30, 0), (30, 5), (29, 5)])
    w_o_1_ = w_o_1.union(w_o_2).union(w_o_3).union(w_o_4).union(w_o_5).union(w_o_6).union(w_o_7).union(w_o_8).union(w_o_9)
    return [w_o_1_]


def initalize_world2():
    x_range = (-7, 36)
    y_range = (-7, 7)
    start = (0, 0)
    goal = (35, 0)
    obstacles = get_obstacles_polygon_world2()
    return start, goal, obstacles, x_range, y_range


def get_obstacles_polygon_world1():
    w_o_1 = Polygon([(1, 1), (2, 1), (2, 5), (1, 5)])
    w_o_2 = Polygon([(3, 3), (4, 3), (4, 12), (3, 12)])
    w_o_3 = Polygon([(3, 12), (12, 12), (12, 13), (3, 13)])
    w_o_4 = Polygon([(12, 5), (13, 5), (13, 13), (12, 13)])
    w_o_5 = Polygon([(6, 5), (12, 5), (12, 6), (6, 6)])
    w_o_2_ = w_o_2.union(w_o_3).union(w_o_4).union(w_o_5)
    return [w_o_1, w_o_2_]


def initalize_world1():
    x_range = (-1, 14)
    y_range = (-1, 14)
    start = (0, 0)
    goal = (10, 10)
    obstacles = get_obstacles_polygon_world1()
    return start, goal, obstacles, x_range, y_range


if __name__ == '__main__':
    start, goal, obstacles, x_range, y_range = initalize_world1()
    # start, goal, obstacles, x_range, y_range = initalize_world2()
    
    grid = Grid(start, goal, obstacles, x_range, y_range)
    wavefront = Wavefront(grid)
    wavefront.find_path()
    wavefront.print_valued_grid()
