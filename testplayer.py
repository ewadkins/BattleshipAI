
import random;

def choose(board, lengths):
    '''
    Choose the location to attack given the board and the lengths of the remaining enemy ships.
    :param board: a 2d list of numbers indicating the status of that cell.
        (-1 = not found, 0 = not checked, 1 = found, 2 = found entire ship)
        (7 = your ship [only if using simulationMultiplayer.py since all ships are in the same region])
    :param lengths: a list containing the lengths of all remaining enemy ships.
    :return: a tuple (i, j) representing the location in board to attack.
        i is the index of the row (0 being top row) and j is index of the column (0 being left column)
    '''

    # Randomly chooses a location
    height = len(board);
    width = len(board[0]);
    return (random.randrange(0, height), random.randrange(0, width))

def getName():
    '''
    Return the name of your AI.
    :return: a string of the name of your AI.
    '''
    return "Terrible Bot";