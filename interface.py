import os
import metrocli as mtcl
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

intro = 'welcome to metrocli! currently we only support the london tube.\nplease visit our github if you\'d like to contribute to our development.\n'
about = 'metrocli uses Stanfords 1968 A* search algorithm to choose the best possible path.\nit relies on an approximation of the direct distance between stops in three-dimensional space.\ntimetables, closures and the earth\'s deviation from spherical symmetry are among the factors not taken into account by this method.\nas such metrocli will not always be the most practical real-world journey planner.\nthe default mode adds a penalty for each line change - use the -d flag to calculate pure distance efficiency.'

def init():
    global finder, names
    finder = { value[2] : key for key, value in mtcl.stations.items() }
    names = list(finder.keys())
    print(intro)

    mtcl.start = interpret('start station: ')
    mtcl.destination = interpret('destination station: ')

    print(f"\n{ mtcl.stations[mtcl.start][2] } to { mtcl.stations[mtcl.destination][2] }:\n")
    mtcl.search()
    mtcl.exhibit()

def interpret(text):
    valid = False
    while not valid:
        interpretee = input(text)
        if not interpretee.isdigit():
            if not interpretee in names:
                comparisons = { key : similar(key, interpretee) for key in names if key is not None }
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
        elif int(interpretee) in mtcl.stations:
            valid = True
            return int(interpretee)
        else:
            print('not a valid station number :(')
 
