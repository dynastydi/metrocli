import os
import pytube as pt


path = __file__[:-7]

stations = pt.dictify(f'{path}data/stations.csv')
lines = pt.dictify(f'{path}data/lines.csv')
connections = pt.connectify(f'{path}data/connections.csv')

start = int(input("start station: "))
destination = int(input("destination station: "))

inputs = pt.search(start, destination, stations, connections, lines)
pt.crochet(inputs, stations, lines)
