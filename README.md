# Minesweeper
This minesweeper solver solves the mine field provided by MineField Object of the DecodeDemcon3 challenge: https://github.com/JeroenVerberneDemcon/DecodeDemcon3.

The solver iteratively sweeps through the mine field by revealing cells with the lowest probability of being a mine and flagging cells that must for certain be a mine. 
The solver works on the following three principles:
- for each cell that's revealed, calculate the probability for it's neighbours for being a mine. If the probability is 0.0, the neighbouring cell is safe and is revealed as well. If the probability is 1.0, the cell is flagged as a mine. The probability for all unrevealed cells in the field is calculated by the mine density 

If no cell in the field has a probability of either 0.0 or 1.0, the solver tries to deduce the cell states:
- deduce whether a unrevealed cell must be a mine. If the cell is not a mine, another cell must be a mine which is shared with a neighbouring revealed cell, which would thereby have too many adjacent mines
- deduce whether a unrevealed cell cannot be a mine. If the cell is a mine, a revealed cell will have reached it's number of adjacent mines, but thereby another revealed cell cannot reach it's number of adjacent mines

If after these steps still no cell can be found with a probability of either 0.0 or 1.0, the solver reveales the cell with the lowest probability of being a mine. 

After the solver has either succeeded or failed, a figure is generated with all the cells it has revealed and all the mines it has flagged.
