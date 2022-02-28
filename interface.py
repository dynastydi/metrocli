import os
import pytube as pt

intro = 'welcome to pytube! currently we only support the london tube.\nplease visit our github if you\'d like to contribute to our development.\n'
about = 'pytube uses Stanfords 1968 A* search algorithm to choose the best possible path.\nit relies on euclidean distance between stops, rather than timetables.\nas such pytube will not always be the most practical real-world journey planner.\nthe default mode adds a penalty for each line change - use the -d flag to calculate pure distance efficiency.'

def init():
    print(intro)

    pt.start = interpret('start station: ')
    pt.destination = interpret('destination station: ')

    print(f"\n{ pt.stations[pt.start][2] } to { pt.stations[pt.destination][2] }:\n")
    pt.search()
    pt.exhibit()

def interpret(text):
    valid = False
    while not valid:
        converse = input(text)
        try: 
            out = int(converse)
            valid = True
        except ValueError:
            print("oops! input not a number or valid string. please try again.")
    return out

def 
