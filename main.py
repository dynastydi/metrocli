import os
import pytube as pt


path = __file__[:-7]

stations = pt.dictify(f'{path}data/stations.csv')
lines = pt.dictify(f'{path}data/lines.csv')
connections = pt.connectify(f'{path}data/connections.csv')

start = int(input("start station: "))
destination = int(input("destination station: "))

print(f"\n{stations[start][2]} to {stations[destination][2]}:\n")

inputs = pt.search(start, destination, stations, connections, lines)
pt.crochet(inputs)
