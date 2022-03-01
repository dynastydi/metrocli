import os
import metrocli as mtcl

intro = 'welcome to metrocli! currently we only support the london tube.\nplease visit our github if you\'d like to contribute to our development.\n'
about = 'metrocli uses Stanfords 1968 A* search algorithm to choose the best possible path.\nit relies on an approximation of the direct distance between stops in three-dimensional space.\ntimetables, closures and the earth\'s deviation from spherical symmetry are among the factors not taken into account by this method.\nas such metrocli will not always be the most practical real-world journey planner.\nthe default mode adds a penalty for each line change - use the -d flag to calculate pure distance efficiency.'

def init():
    print(intro)

    mtcl.start = interpret('start station: ')
    mtcl.destination = interpret('destination station: ')

    print(f"\n{ mtcl.stations[mtcl.start][2] } to { mtcl.stations[mtcl.destination][2] }:\n")
    mtcl.search()
    mtcl.exhibit()

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
 
