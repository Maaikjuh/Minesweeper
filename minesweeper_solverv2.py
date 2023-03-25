from DecodeDemcon3 import mineField
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import copy

ENTER_MODE = "Expert" # "Intermediate" #"Beginner" #

if ENTER_MODE == "Beginner":
    mode = mineField.BEGINNER_FIELD
elif ENTER_MODE == "Intermediate":
    mode = mineField.INTERMEDIATE_FIELD
elif ENTER_MODE == "Expert":
    mode = mineField.EXPERT_FIELD

width = mode['width']
height = mode['height']
nr_mines = mode['number_of_mines']

mine_field = mineField.MineField(width = width, height = height, number_of_mines= nr_mines)

class mineCell:
    def __init__(self, coord, prob):
        self.coordinates = coord
        self.probability = prob   
        self.bomb_flagged = False
        self.revealed = False
        self.safe_flagged = False
        self.failed = False
        self.nr_surrounding_bombs = -1
        # self.neighbours = []

    # def bom_chance(self):
    #     bom_cells = self.bom_candidates_neighbours()
    #     nr_bom_candidates = len(bom_cells)
    #     if nr_bom_candidates == 0:
    #         return 0
    #     else:
    #         bom_chance = (self.nr_surrounding_bombs - self.nr_bom_neighbours()) / nr_bom_candidates
    #         return bom_chance

    # def update_bom_probability_neighbours(self):
    #     nr_flagged_bombs = 0
    #     bom_chance = self.bom_chance()
    #     for n in self.bom_candidates_neighbours():
    #         n.probability = bom_chance
    #         if n.probability >= 1.:
    #             n.bomb_flagged = True
    #             nr_flagged_bombs += 1
    #         elif n.probability == 0.0:
    #             n.safe_flagged = True
    #     return nr_flagged_bombs

    # def bom_candidates_neighbours(self):
    #     bom_candidate_neighbours = []
    #     for n in self.neighbours:
    #         if (n.safe_flagged == False) & (n.bomb_flagged == False):
    #             bom_candidate_neighbours += [n]
    #     return bom_candidate_neighbours

    # def nr_bom_neighbours(self):
    #     bom_neighbours = 0
    #     for n in self.neighbours:
    #         if n.bomb_flagged == True:
    #             bom_neighbours += 1
    #     return bom_neighbours

  
class mineFieldArray:
    def __init__(self, width = int, height = int, bom_density= float):
        self.width = width
        self.height = height
        self.prev_bom_density = bom_density

        self.nr_flagged_bombs = 0

        self.mine_array = [[mineCell((j,i), bom_density) for j in range(width)] for i in range(height)]
        # self._find_neighbours()

        self.color_map = {1: np.array([255, 0, 0]), # red
                        2: np.array([0, 255, 0]), # green
                        3: np.array([255, 255, 255]), #blue
                        4: np.array([144, 238, 144]), #light green
                        5: np.array([119, 0, 200])} #purple
    
    # def find_neighbours(self):
    #     for r in range(0, self.height):
    #         for c in range(0, self.width):
    #             cell = self.mine_array[r][c]
    #             for h in range(r-1, r+2):
    #                 for w in range(c-1, c+2):
    #                     if ((w >= 0) & (h >= 0)) & ((w < self.width) & (h < self.height)) & (w != c or h != r):
    #                         cell.neighbours.append(self.mine_array[h][w])

    def find_cell_neighbours(self, cell):
        neighbours = []
        column = cell.coordinates[0]
        row = cell.coordinates[1]
        for h in range(row-1, row+2):
            for w in range(column-1, column+2):
                if ((w >= 0) & (h >= 0)) & ((w < self.width) & (h < self.height)) & (w != column or h != row):
                    neighbours.append(self.mine_array[h][w])
        return neighbours

    def bom_chance(self, cell):
        bom_cells = self.bom_candidates_neighbours(cell)
        nr_bom_candidates = len(bom_cells)
        if nr_bom_candidates == 0:
            return 0
        else:
            bom_chance = (cell.nr_surrounding_bombs - self.nr_bom_neighbours(cell)) / nr_bom_candidates
            return bom_chance

    def update_bom_probability_neighbours(self, cell):
        bom_chance = self.bom_chance(cell)
        for n in self.bom_candidates_neighbours(cell):
            n.probability = bom_chance
            if n.probability >= 1.:
                n.bomb_flagged = True
                self.nr_flagged_bombs += 1
            elif n.probability == 0.0:
                n.safe_flagged = True
        # return nr_flagged_bombs

    def bom_candidates_neighbours(self, cell):
        bom_candidate_neighbours = []
        for n in self.find_cell_neighbours(cell):
            if (n.safe_flagged == False) & (n.bomb_flagged == False):
                bom_candidate_neighbours += [n]
        return bom_candidate_neighbours

    def nr_bom_neighbours(self, cell):
        bom_neighbours = 0
        for n in self.find_cell_neighbours(cell):
            if n.bomb_flagged == True:
                bom_neighbours += 1
        return bom_neighbours





    def bomb_candidates(self):
        unkown_cells = []
        for row in self.mine_array:
            for cell in row:
                if (cell.safe_flagged != True) & (cell.bomb_flagged != True):
                    unkown_cells += [cell]  
        return unkown_cells 

    def un_revealed_cells(self):
        unkown_cells = []
        for row in self.mine_array:
            for cell in row:
                if (cell.revealed != True) & (cell.bomb_flagged != True):
                    unkown_cells += [cell]  
        return unkown_cells 
    
    def revealed_unsolved(self):
        '''cells whos all adjecent mines have not been found yet'''
        revealed_unsolved = []
        for row in self.mine_array:
            for cell in row:
                if (cell.revealed == True):
                    unkown_cell_bool = False
                    for n in self.find_cell_neighbours(cell):
                        if (n.safe_flagged == False) & (n.bomb_flagged == False):
                            unkown_cell_bool = True
                    if unkown_cell_bool == True:
                        revealed_unsolved += [cell]
        return revealed_unsolved

    def update_cells(self):
        for cell in self.revealed_unsolved():
            self.update_bom_probability_neighbours(cell)
        return 

    def update_bom_field_density(self):
        check_cells = self.bomb_candidates()
        if len(check_cells) > 0:
            bom_density =  (nr_mines - self.nr_flagged_bombs)/len(check_cells)
            for cell in check_cells:
                if cell.probability == self.prev_bom_density:
                    cell.probability = bom_density
            self.prev_bom_density = bom_density
    
    def try_guessing(self):
        unresolved_cells = self.revealed_unsolved()

        for cell_i in unresolved_cells:
            remaining_mines = cell_i.nr_surrounding_bombs - self.nr_bom_neighbours(cell_i)

            if remaining_mines == 1:
                mine_candidates = self.bom_candidates_neighbours(cell_i)
                coord_mine_candidates = [cell.coordinates for cell in mine_candidates]
                
                adjecent_unresolved_cells = []
                for cell_r in unresolved_cells:
                    if cell_r in self.find_cell_neighbours(cell_i):
                        adjecent_unresolved_cells += [cell_r]
                
                for cell_i_n in mine_candidates:
                    coord_cell_i_n = cell_i_n.coordinates
                    for cell_r in adjecent_unresolved_cells:
                        adjecent_unresolved_mine_candidates = self.bom_candidates_neighbours(cell_r)
                        coord_adjecent_unresolved_mine_candidates = [cell.coordinates for cell in adjecent_unresolved_mine_candidates]

                        if coord_cell_i_n not in coord_adjecent_unresolved_mine_candidates:
                            mine_fields_left = len([coord for coord in coord_adjecent_unresolved_mine_candidates if coord not in coord_mine_candidates])

                            if mine_fields_left < (cell_r.nr_surrounding_bombs - self.nr_bom_neighbours(cell_r)):
                                cell_i_n.safe_flagged = True
                                cell_i_n.probability = 0.0
                                self.update_cells()
                                return
        return

        # copy_mine_array = copy.deepcopy(self.mine_array)
        # for cell_ru in self.revealed_unsolved():
        #     for cell_ru_n in self.bom_candidates_neighbours(cell_ru):
        #         cell_ru_n.bomb_flagged = True
        #         self.update_bom_probability_neighbours(cell_ru_n)
        #         for cell_ru_2 in self.revealed_unsolved(copy_mine_array):
        #             mine_candidates = self.bom_candidates_neighbours(cell_ru_2)
        #             if (cell_ru_2.nr_surrounding_bombs - cell_ru_2.nr_bom_neighbours()) > len(mine_candidates):
        #                 #selected cell cannot be a mine
        #                 cell_ru_n.bomb_flagged = False
        #                 cell_ru_n.probability = 0.0
        #                 self.nr_flagged_bombs += self.update_cells()
        #                 return 
        #         cell_ru_n.bomb_flagged = False
        # return

    def sortComparatorByProb(self, item):
        return item.probability

    def lowest_bomb_prob(self):
        check_cells = self.un_revealed_cells()
        check_cells.sort(key= self.sortComparatorByProb)
        # if check_cells[0].probability > 0:
        #     self.try_guessing(nr_flagged_bombs)
        return check_cells
    
    def return_next_cell(self):
        if self.lowest_bomb_prob()[0].probability > 0:
            self.try_guessing()
        return self.lowest_bomb_prob()[0] 

    def plot_minefield(self, with_timer = True, title = ""):
        plot_array =  [["" for j in range(self.width)] for i in range(self.height)]
        color_array = np.ndarray(shape=(self.height, self.width, 3), dtype=int)
        for r in range(0, self.height):
            for c in range(0, self.width):
                cell = self.mine_array[r][c]
                if cell.revealed == True:
                    plot_array[r][c] = str(cell.nr_surrounding_bombs)
                    if cell.nr_surrounding_bombs == 0:
                        color_array[r][c] = self.color_map[4]
                    else:
                        color_array[r][c] = self.color_map[2]
                elif (cell.bomb_flagged == True) & (cell.failed == False):
                    plot_array[r][c] = "x"
                    color_array[r][c] = self.color_map[1]
                elif cell.failed == True:
                    plot_array[r][c] = "x"
                    color_array[r][c] = self.color_map[5]
                else:
                    plot_array[r][c] = str(round(cell.probability,2))
                    color_array[r][c] = self.color_map[3]   

        # display the plot 
        fig, ax = plt.subplots(1,1)
        ax.imshow(color_array)

        def close_event():
            plt.close() #timer calls this function after 3 seconds and closes the window 

        timer = fig.canvas.new_timer(interval = 2000) #creating a timer object and setting an interval of 3000 milliseconds
        timer.add_callback(close_event)
        # add numbers to the plot 
        # thanks to tmdavison answer here https://stackoverflow.com/a/40890587/7871710
        for i in range(0, height):
            for j in range(0, width):
                c = plot_array[i][j]
                ax.text(j, i, c, va='center', ha='center')
        if with_timer:
            timer.start()
        
        fig_title = "nr of mines found: {}/{}".format(self.nr_flagged_bombs, nr_mines)
        if title != "":
            fig_title += "\n{}".format(title)
        fig.suptitle(fig_title)

        fig.tight_layout()

        plt.show()

bom_density = nr_mines / (width * height)
field = mineFieldArray(width = width, height = height, bom_density= bom_density)
field.mine_array[0][0].probability = 0.0


title = "We won!!!"
while field.nr_flagged_bombs != nr_mines:
    item = field.return_next_cell()

    x = item.coordinates[0]
    y = item.coordinates[1]

    if item.probability > 0:
        print("guessing at ({}, {})".format(x,y))
    try:
        adjecent_mines = mine_field.sweep_cell(x, y)
        item.revealed = True
        item.safe_flagged = True
        item.nr_surrounding_bombs = adjecent_mines

    except Exception:
        print("I failed.. :c")
        item.bomb_flagged = True
        item.failed = True
        title = "We lost... :c"
        break

    field.update_bom_probability_neighbours(item)

    field.update_bom_field_density()
    field.update_cells()
    # field.plot_minefield(with_timer = False)
field.plot_minefield(with_timer = False, title = title)


