import random

def create_board(size_x, size_y, number_of_mines) :
    result = ["="*min((size_x//2 - 6), 3) + "Mine Sweeper" + "="*min((size_x//2 - 6), 3)]
    size = size_x * size_y
    cells = []
    for i in range(0, size) :
        #cells[i] = ":teb_empty:"
        cells.append("||<:teb_empty_pressed:541971761504452628>||")

    for i in range(0, number_of_mines) :
        pos = random.randint(0, size)
        cells[pos] = "||<:teb_bomb_pressed:541971761474961409>||"

    n = 0
    res = ""
    for i in range(0, size) :
        cell = cells[i]
        res += cell
        if n == size_x :
            size_y += 1
            n = 0
            #result += "\n"
            result.append(res)
            res = ""
        n += 1

    return result
