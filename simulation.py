# Basic 2-player game of Battleship, with each player in their own distinct region.

import random;
import time;

# Import player controllers
import eric;
import testplayer;

def fill(board, n, start, end):
    for i in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
        for j in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
            board[i][j] = n;
    return board;

def genShips(board, lengths, playerIndex):
    def isLegal(ship):
        for i in range(min(ship[0][0], ship[1][0]), max(ship[0][0], ship[1][0]) + 1):
            for j in range(min(ship[0][1], ship[1][1]), max(ship[0][1], ship[1][1]) + 1):
                if (board[i][j] != 0):
                    return False;
        return True;

    height = len(board);
    width = len(board[0]);
    ships = [];
    for length in lengths:
        count = 0;
        ship = None;
        while (ship == None and count < width * height * 20):
            count += 1;
            x = random.randrange(0, width);
            y = random.randrange(0, height);
            if (random.randrange(0, 2) == 0): # vertical
                if (random.randrange(0, 2) and y - (length - 1) >= 0):
                    ship = ((y, x), (y - (length - 1), x), playerIndex, length);
                elif (y + (length - 1) < height):
                    ship = ((y, x), (y + (length - 1), x), playerIndex, length);
            else: # horizontal
                if (random.randrange(0, 2) and x - (length - 1) >= 0):
                    ship = ((y, x), (y, x - (length - 1)), playerIndex, length);
                elif (x + (length - 1) < width):
                    ship = ((y, x), (y, x + (length - 1)), playerIndex, length);
            if (ship != None and isLegal(ship) == False):
                ship = None;
        if (ship == None):
            print("Board creation failed!");
            raise "Board creation failed";
            exit();
        fill(board, playerIndex + 1, ship[0], ship[1]);
        ships.append(ship);
    return ships;

def printMap(m):
    print();
    print("".join(['-' for i in range(len(m[0]) * 3 + 4)]));
    for i in range(len(m)):
        string = "| ";
        for j in range(len(m[i])):
            if (m[i][j] != 0):
                string += " " + str(m[i][j]) + " ";
            else:
                string += "   ";
        string += " |"
        print(string);
    print("".join(['-' for i in range(len(m[0]) * 3 + 4)]));

def printPlayerMap(m):
    print();
    print("".join(['-' for i in range(len(m[0]) * 3 + 4)]));
    for i in range(len(m)):
        string = "| ";
        for j in range(len(m[i])):
            if (m[i][j] == 0):
                string += "   ";
            elif (m[i][j] == 1):
                string += " X ";
            elif (m[i][j] == 2):
                string += " # ";
            elif (m[i][j] == -1):
                string += " - ";
            elif (m[i][j] == 7):
                string += " * ";
        string += " |"
        print(string);
    print("".join(['-' for i in range(len(m[0]) * 3 + 4)]));


def run(players, width, height, lengths, delay=0, display=False):

    # Master board (0 = empty, # = player #, -# = hit player #)
    # Player boards (-1 = not found, 0 = not checked, 1 = found, 2 = found entire ship, 7 = your ship)
    boards = [];
    playerBoards = [];
    for _ in range(len(players)):
        playerBoards.append([[0 for x in range(width)] for y in range(height)]);
        boards.append([[0 for x in range(width)] for y in range(height)]);

    ships = [];
    for i in range(len(boards)):
        playerShips = genShips(boards[i], lengths, i);
        ships = ships + playerShips;

    if (display):
        for p in range(len(players)):
            print("\nPlayer " + str(p + 1) + " (" + players[p].getName() +") board:")
            printMap(boards[p]);
        print("\n==============================");
        print("Starting game");
        print("==============================");

    def winner():
        player = ships[0][2];
        for ship in ships:
            if (ship[2] != player):
                return False;
        return True;

    rounds = 0;
    while (not winner()):
        rounds += 1;
        if (display):
            print("\n============ Round " + str(rounds) + " ============");
        for p in range(len(players)):
            if (winner()):
                break;
            if (display):
                print("\n* Player " + str(p + 1) + " (" + players[p].getName() +")");
            enemyShips = [];
            enemyLengths = [];
            for ship in ships:
                if (ship[2] != p):
                    enemyShips.append(ship);
                    enemyLengths.append(ship[3]);
            chosen = players[p].choose(playerBoards[p], enemyLengths);
            for b in range(len(players)):
                if (b != p):
                    board = boards[b];
                    if (board[chosen[0]][chosen[1]] == 0):
                        playerBoards[p][chosen[0]][chosen[1]] = -1;
                    elif (abs(board[chosen[0]][chosen[1]]) != p + 1):
                        #for p2 in range(len(players)):
                        #    playerBoards[p2][chosen[0]][chosen[1]] = 1;
                        playerBoards[p][chosen[0]][chosen[1]] = 1;
                        if (board[chosen[0]][chosen[1]] > 0):
                            board[chosen[0]][chosen[1]] *= -1;
                            target = None;
                            sunk = True;
                            for enemyShip in enemyShips:
                                for i in range(min(enemyShip[0][0], enemyShip[1][0]), max(enemyShip[0][0], enemyShip[1][0]) + 1):
                                    for j in range(min(enemyShip[0][1], enemyShip[1][1]), max(enemyShip[0][1], enemyShip[1][1]) + 1):
                                        if (i == chosen[0] and j == chosen[1]):
                                            target = enemyShip;
                            if (target != None):
                                for i in range(min(target[0][0], target[1][0]), max(target[0][0], target[1][0]) + 1):
                                    for j in range(min(target[0][1], target[1][1]), max(target[0][1], target[1][1]) + 1):
                                        if (board[i][j] > 0):
                                            sunk = False;
                            if (target != None and sunk):
                                if (display):
                                    print("Player " + str(target[2] + 1) + " (" + players[target[2]].getName() + ") lost a ship of length " + str(target[3]));
                                ships.remove(target);
                                for i in range(min(target[0][0], target[1][0]), max(target[0][0], target[1][0]) + 1):
                                    for j in range(min(target[0][1], target[1][1]), max(target[0][1], target[1][1]) + 1):
                                        playerBoards[p][i][j] = 2;

            if (display):
                printPlayerMap(playerBoards[p]);
        time.sleep(delay);

    if (display):
        print("\n==============================");
        print("Player " + str(ships[0][2] + 1) + " (" + players[ships[0][2]].getName() + ") wins!");
        print("==============================");
    return (ships[0][2], rounds);

#######################################################################

numRounds = 1;
players = [eric, testplayer];
width = 10;
height = 10;
lengths = [5, 4, 3, 3, 2];
delay = 1.0;
display = True;

assert len(players) == 2;
total = 0;
winnerCount = [0 for player in players];
for i in range(numRounds):
    print(str(i + 1) + " / " + str(numRounds));
    success = False;
    while (not success):
        try:
            winnerIndex, rounds = run(players, width, height, lengths, delay, display);
            winnerCount[winnerIndex] += 1;
            total += rounds;
            success = True;
        except:
            raise;

print();
for p in range(len(players)):
    print("Player " + str(p + 1) + " (" + players[p].getName() + ") had " + str(winnerCount[p]) + " wins");
print("Avg. win on round " + str(total // numRounds));