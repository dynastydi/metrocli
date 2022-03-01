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

    mtcl.start = interpret(input('start station: '))
    mtcl.destination = interpret(input('destination station: '))

    print(f"\n{ mtcl.stations[mtcl.start][2] } to { mtcl.stations[mtcl.destination][2] }:\n")
    mtcl.search()
    mtcl.exhibit()

def interpret(text):
    valid = False
    while not valid:
        if not text.isdigit():
            if not text in names:
                comparisons = { key : similar(key, text) for key in names if key is not None }
                best = max(comparisons, key=comparisons.get)
                if comparisons[best] >= 0.5:
                    print(f'did you mean {best}? (y/n)')
                else:
                    print('oops! couldn\'t figure that out. try again.')
                valid = True

        elif int(text) in mtcl.stations:
            return int(text)
        else:
            print('oops! input not a number or valid string. please try again.')
 
