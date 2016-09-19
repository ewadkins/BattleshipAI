
import random;

def printMap(m):
    print();
    for i in range(len(m)):
        print(m[i]);

def choose(board, lengths):
    height = len(board);
    width = len(board[0]);

    possibilityMap = [[0 for x in range(width)] for y in range(height)];
    randomMap = [[0 for x in range(width)] for y in range(height)];

    # Guarantees a higher chance of choosing a location adjacent to a known ship than choosing a random location
    squareLengthsSum = sum(lengths) ** 2;

    # Generate decision map
    for length in lengths:
        for i in range(height):
            for j in range(width):
                left = 1;
                top = 1;
                right = 1;
                bottom = 1;
                for k in range(1, length):
                    if (j - k >= 0 and j - k < width and (board[i][j - k] == 0 or board[i][j - k] == 1)):
                        left += 1;
                    else:
                        break;
                for k in range(1, length):
                    if (i - k >= 0 and i - k < height and (board[i - k][j] == 0 or board[i - k][j] == 1)):
                        top += 1;
                    else:
                        break;
                for k in range(1, length):
                    if (j + k >= 0 and j + k < width and (board[i][j + k] == 0 or board[i][j + k] == 1)):
                        right += 1;
                    else:
                        break;
                for k in range(1, length):
                    if (i + k >= 0 and i + k < height and (board[i + k][j] == 0 or board[i + k][j] == 1)):
                        bottom += 1;
                    else:
                        break;

                if (board[i][j] == 1):
                    for k in range(1, left):
                        if (board[i][j - k] == 0):
                            possibilityMap[i][j - k] += squareLengthsSum * min(left - k, right);
                    for k in range(1, top):
                        if (board[i - k][j] == 0):
                            possibilityMap[i - k][j] += squareLengthsSum * min(top - k, bottom);
                    for k in range(1, right):
                        if (board[i][j + k] == 0):
                            possibilityMap[i][j + k] += squareLengthsSum * min(right - k, left);
                    for k in range(1, bottom):
                        if (board[i + k][j] == 0):
                            possibilityMap[i + k][j] += squareLengthsSum * min(bottom - k, top);
                elif (board[i][j] == 0):
                    if (length == 1):
                        possibilityMap[i][j] += 1;
                    for k in range(1, left):
                        possibilityMap[i][j] += min(left - k, right);
                    for k in range(1, top):
                        possibilityMap[i][j] += min(top - k, bottom);
                    for k in range(1, right):
                        possibilityMap[i][j] += min(right - k, left);
                    for k in range(1, bottom):
                        possibilityMap[i][j] += min(bottom - k, top);

    #printMap(possibilityMap);

    chosen = None;

    maxValue = 0;
    locations = [];
    for i in range(height):
        for j in range(width):
            if (possibilityMap[i][j] > maxValue):
                maxValue = possibilityMap[i][j];
                locations = [(i, j)];
            elif (possibilityMap[i][j] == maxValue):
                locations.append((i, j));

    chosen = locations[random.randrange(0, len(locations))];

    return chosen;

def getName():
    return "Eric";