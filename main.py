import pytube as pt

stations = pt.dictify('data/stations.csv')
lines = pt.dictify('data/lines.csv')
connections = pt.connectify('data/connections.csv')

start = int(input("start station: "))
destination = int(input("destination station: "))

inputs = pt.search(start, destination, stations, connections, lines)
pt.crochet(inputs, stations, lines)
