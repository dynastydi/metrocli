import math
import interface as intf

start = None        # set empty globals.
destination = None

radius = 6371       # the earth's approximate radius in km.

def init(path):     # initialise interface and load data.
    load(path)
    intf.init()



def load(path):     # take install / execution path and find data.
    global stations, lines, connections
    stations = dictify('data/stations.csv')
    lines = dictify('data/lines.csv')
    connections = connectify('data/connections.csv')

def data(inp):      # decides how to parse.
    inp = inp.replace('"', '')
    if inp.isdigit():
        inp = int(inp)
    else: 
        try:
            inp = float(inp)
        except ValueError:
            pass
    return inp

def dictify(csv):   # generic csv -> dict function. 
    inp = open(csv, 'r').read().split('\n')
    book = {}
    for line in inp[0:-1]:
        splat = list(map(data, line.split(',')))
        book[splat[0]] = splat[1:]
    return book

def connectify(csv):# more involved dict function for adjacent connections.
    inp = open(csv, 'r').read().split('\n')
    book = {}
    for line in inp[0:-1]:
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


def cart(lat, long):# find rough cartesian coords from lat & long. 
    x = radius*math.cos(math.radians(lat))*math.cos(math.radians(long))
    y = radius*math.cos(math.radians(lat))*math.sin(math.radians(long))
    z = radius*math.sin(math.radians(lat))
    return (x, y, z) 

def dist(a, b):     # find euclidian distance from lat & long.
    
    ca = cart(a[0], a[1])
    cb = cart(b[0], b[1])

    # euclidian distance between sets of cartesian coordinates:
    # d**2 = (xa-xb)**2 + (ya-yb)**2 + (za-zb)**2
    
    return math.sqrt((ca[0] - cb[0])**2 + (ca[1] - cb[1])**2 + (ca[2] - cb[2])**2)

def search():       # standard A* search function.
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
    
def extract():      # take relevant info about best path from searched data.
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
            if last is not None: 
                line = lines[last][0]
                colour = lines[last][1]
            linelist.append((name, line, count, colour))
            count = 0
        last = each
        count += 1
    return linelist

def exhibit():      # present extracted info.
    linelist = extract()
    last = (linelist[0][0])
    for l in linelist[1:]:
        print(f"\u001b[0m{ last }\x1B[38;5;{ l[3] }m{ ' -'*(l[2]-1) } > \u001b[0m{ l[0] } \x1B[38;5;{ l[3] }m({ l[1] })")
        last = l[0]

