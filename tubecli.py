import math
import interface as intf

start = None
destination = None

radius = 6371       # The earth's approximate radius in km.

def init(path):
    load(path)
    intf.init()

def load(path):
    global stations, lines, connections
    stations = dictify('data/stations.csv')
    lines = dictify('data/lines.csv')
    connections = connectify('data/connections.csv')

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
    book[None] = [None, None, None]
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
            book[keyA] = { keyB : datA }
        else:
            book[keyA][keyB] = datA
        if keyB not in book:
            book[keyB] = { keyA : datA }
        else:
            book[keyB][keyA] = datA
    return book


# take lat+long and return cartesian coordinates.
def cart(lat, long):
    x = radius*math.cos(math.radians(lat))*math.cos(math.radians(long))
    y = radius*math.cos(math.radians(lat))*math.sin(math.radians(long))
    z = radius*math.sin(math.radians(lat))
    return (x, y, z)

# take lat+long of two points and return approximate direct distance.
def dist(a, b):
    
    ca = cart(a[0], a[1])
    cb = cart(b[0], b[1])

    # euclidian distance between sets of cartesian coordinates:
    # d**2 = (xa-xb)**2 + (ya-yb)**2 + (za-zb)**2
    
    return math.sqrt((ca[0] - cb[0])**2 + (ca[1] - cb[1])**2 + (ca[2] - cb[2])**2)

def search():
    global chain, history, changes  # new globals
    current = start
    goal = stations[destination][:2]
    line = None
    g = 0
    chain = {}                      # reset globals
    history = {}
    changes = {}
    while current != destination: 
        options = list(connections[current].keys())
        this = stations[current][:2]
        for each in options:
            if each not in chain and each not in history:
                h = dist(goal, stations[each][:2])
                d = dist(this, stations[each][:2])
                f = d + g + h
                line = connections[current][each]
                chain.update({ each : f })
                history[each] = [ current ]
                changes[each] = [ line ]
                if current in history:
                    history[each] += history[current]
                    changes[each] += changes[current]
        choice = min(chain, key=chain.get)
        g += dist(stations[current][:2], stations[choice][:2])
        chain.pop(choice)
        current = choice
    
def extract():
    stops = history[destination][::-1]
    journey = changes[destination][::-1]
    stops.append(destination)
    journey.append(None)
    linelist = []
    count = 0
    index = 0
    last = None
    line = None
    colour = None
    for each in journey:
        if each != last:
            index += count
            name = stations[stops[index]][2]
            line = lines[last][0]
            colour = lines[last][1]
            linelist.append((name, line, count, colour))
            count = 0
        last = each
        count += 1
    return linelist

def exhibit():
    linelist = extract()
    last = (linelist[0][0])
    for l in linelist[1:]:
        print(f"\u001b[0m{ last }\x1B[38;5;{ l[3] }m{ ' -'*(l[2]-1) } > \u001b[0m{ l[0] } \x1B[38;5;{ l[3] }m({ l[1] })")
        last = l[0]

