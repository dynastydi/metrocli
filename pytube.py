import math

def data(inp):
    inp = inp.replace('"', '')
    if inp.isdigit():
        inp = int(inp)
    else: 
        try:
            inp = float(inp)
        except ValueError:
            pass
    return inp

def dictify(csv):
    inp = open(csv, 'r').read().split('\n')
    book = {}
    for line in inp[1:-1]:
        splat = list(map(data, line.split(',')))
        book[splat[0]] = splat[1:4]
    return book

def connectify(csv):
    inp = open(csv, 'r').read().split('\n')
    book = {}
    for line in inp[1:-1]:
        splat = list(map(data, line.split(',')))
        keyA = splat[0]
        keyB = splat[1]
        datA = splat[2]
        if keyA not in book:
            book[keyA] = {keyB : datA}
        else:
            book[keyA][keyB] = datA
        if keyB not in book:
            book[keyB] = {keyA : datA}
        else:
            book[keyB][keyA] = datA
    return book

# take 2D coordinates as tuples or lists and return distance.
def dist(a, b):
    # d**2 = (xa-xb)**2 + (ya-yb)**2
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def search(start, destination, stations, connections, lines):
    current = start
    goal = stations[destination][:2]
    line = None
    g = 0
    chain = {}
    expired = []
    history = {}
    printer = ""
    name = ""
    while current != destination: 
        options = list(connections[current].keys())
        this = stations[current][:2]
        for each in options:
            if each not in chain and each not in expired:
                h = dist(goal, stations[each][:2])
                d = dist(this, stations[each][:2])
                #if line != connections[current][each]: distance *= 2
                f = d + g + h
                line = connections[current][each]
                chain.update({each : f})
                history.update({each : [current, line]})
        choice = min(chain, key=chain.get)
        val = min(chain.values())
        g += dist(stations[current][:2], stations[choice][:2])
        chain.pop(choice)
        expired.append(choice)
        current = choice
    path = []
    changes = []
    while current != start:
        path.append(current)
        changes.append(history[current][1])
        current = history[current][0]
    
    path.append(start)
    path.reverse()
    changes.reverse()
    return path, changes

def crochet(inputs, stations, lines):
    path = inputs[0]
    changes = inputs[1]
    line = changes[0]
    station = path[0]
    printer = ' '
    i = 0
    while i < len(changes):
        name = stations[path[i]][2]
        colour = lines[changes[i]][2]
        if changes[i] == changes[i-1]:
            printer += '- '
        else:
            print(f"\u001b[0m{name}\x1B[38;5;{colour}m{printer}> \u001b[0m{stations[path[i+1]][2]} \x1B[38;5;{colour}m({lines[changes[i]][0]})")
            printer = ' '
        i += 1

        #if line == connections[current][choice]:
        #    printer += "-"
        #else:
        #    if line is not None:
        #        colour = lines[line][2]
        #        print(f"\x1B[38;5;{15}m{name}\x1B[38;5;{colour}m{printer}> \x1B[38;5;{15}m{stations[current][2]} \x1B[38;5;{colour}m({lines[line][0]})")
        #    name = stations[current][2]
        #    printer = " "
        #    line = connections[current][choice]
