import os
import tubecli as tc
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

intro = 'welcome to tubecli! this is a simple data-driven tool for navigating the london tube.\nplease visit our github if you\'d like to contribute to our development.\n'
about = 'tubecli uses Stanfords 1968 A* search algorithm to choose the best possible path.\nit relies on an approximation of the direct distance between stops in three-dimensional space.\ntimetables, closures and the earth\'s deviation from spherical symmetry are among the factors not taken into account by this method.\nas such tubecli will not always be the most practical real-world journey planner.'

def init():
    global finder, names
    finder = { value[2] : key for key, value in tc.stations.items() }
    names = list(finder.keys())
    print(intro)

    tc.start = interpret('start station: ')
    tc.destination = interpret('destination station: ')

    print(f"\n{ tc.stations[tc.start][2] } to { tc.stations[tc.destination][2] }:\n")
    tc.search()
    tc.exhibit()

def interpret(text):
    valid = False
    while not valid:
        interpretee = input(text)
        if not interpretee.isdigit():
            if not interpretee in names:
                comparisons = { key : similar(key, interpretee) for key in names }
                answered = False
                while not answered:
                    best = max(comparisons, key=comparisons.get)
                    if comparisons[best] >= 0.5:
                        ans = input(f'did you mean {best}? (y/n) ')
                        if ans == 'y' or ans == 'Y':
                            answered = True
                            valid = True
                            return finder[best]
                        elif ans == 'n' or ans == 'N':
                            comparisons.pop(best)
                    else:
                        print('oops! couldn\'t figure that out. try again.')
                        answered = True
        elif int(interpretee) in tc.stations:
            valid = True
            return int(interpretee)
        else:
            print('not a valid station number :(')
 
