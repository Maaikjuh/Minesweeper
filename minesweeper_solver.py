from DecodeDemcon3 import mineField
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


width = mineField.BEGINNER_FIELD['width']
height = mineField.BEGINNER_FIELD['height']
nr_mines = mineField.BEGINNER_FIELD['number_of_mines']

mine_array = [[-1]*width for i in range(height)]
# mine_array = np.zeros([width, height])

mine_field = mineField.MineField(width = width, height = height, number_of_mines= nr_mines)

# mine_figure, mine_ax = plt.subplots(


class SortedItems:
    def __init__(self, coord: tuple, prob: float):
        self.coordinate = coord
        self.probability = prob   
        self.bomb_flagged = False
        self.safe_flagged = False
        self.nr_surrounding_bombs = 0

 class PriorityQueue:
    def __init__(self):
        self.items = []

    def sortComparatorByProb(self, item):
        return item.probability

    def enqueue(self, item):
        self.items.append(item)
        self.items.sort(key=self.sortComparatorByProb)

    def dequeue(self):
        return self.items.pop(0)

    def addToQueue(self, coord: tuple, prob: float):
        for element in queue.items:
            if element.coordinate == coord:
                element.probability += prob          
                return
        element = SortedItems(coord, prob)
        self.enqueue(element)


# plotter = plotMineField(mine_array)
# plotter.showMinefield()

queue = PriorityQueue()
first_cell_guess = SortedItems((0,0), 0)
queue.enqueue(first_cell_guess)

for item in queue.items:
    x = item.coordinate[0]
    y = item.coordinate[1]
    print(x,y)

    if item.probability < 1.0:
        try:
            adjecent_mines = mine_field.sweep_cell(x, y)
            removed_item = queue.dequeue()
            # plotter.updateArrayValue(removed_item, adjecent_mines)
        except Exception:
            print("I failed.. :c")
            break

        neighbours = []
        for ad_rows in [x-1, x, x+1]:
            for ad_col in [y-1, y, y+1]:
                if (ad_rows >= 0) & (ad_rows <= height) & (ad_col >= 0) & (ad_col <= width) & (ad_rows != x or ad_col != y):
                    neighbours.append((ad_rows, ad_col))
        nr_neighbours = len(neighbours)
        bom_change = adjecent_mines/nr_neighbours

        for neighbour_i in neighbours:
            queue.addToQueue(neighbour_i, bom_change)

        # plotter.showMinefield()

    else:
        print('bom?')


        



