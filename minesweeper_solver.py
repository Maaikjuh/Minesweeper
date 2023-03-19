from DecodeDemcon3 import mineField
import pandas as pd
import numpy as np


width = mineField.BEGINNER_FIELD['width']
height = mineField.BEGINNER_FIELD['height']
nr_mines = mineField.BEGINNER_FIELD['number_of_mines']

mine_array = [[-1]*width for i in range(height)]
mine_array = np.zeros([width, height])

mine_field = mineField.MineField(width = width, height = height, number_of_mines= nr_mines)

#initial guess
#row, column, guess_change
queue = pd.DataFrame({'row': [0], 'column': [0], 'guess_change': [1]})

for index, row in queue.iterrows():
    x = row['row']
    y = row['column']
    adjecent_mines = mine_field.sweep_cell(x, y)

    neighbours = []
    for ad_rows in [x-1, x, x+1]:
        for ad_col in [y-1, y, y+1]:
            if (ad_rows >= 0) & (ad_rows <= height) & (ad_col >= 0) & (ad_col <= width) & (ad_rows != x or ad_col != y):
                neighbours.append([ad_rows, ad_col])
    nr_neighbours = len(neighbours)
    bom_change = 1 - adjecent_mines/nr_neighbours

    for neighbour_i in neighbours:
        if len(queue[queue[queue['row'] == 0]['column'] == -1]) != 0:
            
        queue['coord'].append(neighbour_i)
        queue['guess_change']


