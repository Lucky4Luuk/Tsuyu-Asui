#brainfuck interpreter from: https://github.com/pocmo/Python-Brainfuck/ thank you x)

def brainfuck_evaluate(code):
    code     = brainfuck_cleanup(list(code))
    bracemap = brainfuck_buildbracemap(code)

    cells, codeptr, cellptr, result = [0], 0, 0, ""

    while codeptr < len(code):
        command = code[codeptr]

        if command == ">":
            cellptr += 1
            if cellptr == len(cells): cells.append(0)

        if command == "<":
            cellptr = 0 if cellptr <= 0 else cellptr - 1

        if command == "+":
            cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0

        if command == "-":
            cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255

        if command == "[" and cells[cellptr] == 0: codeptr = bracemap[codeptr]
        if command == "]" and cells[cellptr] != 0: codeptr = bracemap[codeptr]
        if command == ".": result += chr(cells[cellptr]) #sys.stdout.write(chr(cells[cellptr]))
        if command == ",": return ", is not supported yet!" #cells[cellptr] = ord(getch.getch())

        codeptr += 1

    return result

def brainfuck_cleanup(code):
    return ''.join(filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], code))

def brainfuck_buildbracemap(code):
    temp_bracestack, bracemap = [], {}

    for position, command in enumerate(code):
        if command == "[": temp_bracestack.append(position)
        if command == "]":
            start = temp_bracestack.pop()
            bracemap[start] = position
            bracemap[position] = start
    return bracemap
