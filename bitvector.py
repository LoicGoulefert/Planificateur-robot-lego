#! /usr/bin/python3

# Libs

# Others
from BitVector import BitVector

"""This module is an interface between the pddlpy lib
and a bitvector representation of states.

All functions in this module will get informations from
the pddlpy lib and convert those into sets of bitvectors.
"""

# Me faut une fonction qui converti un elem d'état
# en bitvector.
# Du coup il me faut des infos sur la taille du labyrinthe...? => et oui
# nb_cells, nb_robots


def get_coord_from_cell(cell):
    """From a string representing a cell in pddl format,
    returns the x and y coordinates.
    """
    coord = cell.split('-')
    x, y = int(coord[1]), int(coord[2])
    return x, y


def get_index_of_cell(cell, width):
    """Returns the position of a cell in the maze"""
    x, y = get_coord_from_cell(cell)
    return x*width + y


def get_initial_state(initial_state, nb_robots, width, height):
    """
    """
    robots_seen = 0  # Keeps track of the number of robots seen
    nb_cells = width * height
    offset = nb_cells * nb_robots  # To skip the 'header' of the BV
    init_state_bv = BitVector(size=offset + nb_cells*nb_cells)

    for s in initial_state:
        if s[0] == 'at':
            x, y = get_coord_from_cell(s[2])
            index = (width*x + y) + robots_seen*nb_cells
            init_state_bv[index] = 1
            robots_seen += 1
        else:
            c1 = get_index_of_cell(s[1], width)
            c2 = get_index_of_cell(s[2], width)
            index = c1*nb_cells + c2 + offset
            init_state_bv[index] = 1

    return init_state_bv


def get_ground_operator(domprob, nb_robots, nb_cells):
    # ground_op_bv = BitVector(size=nb_cells*nb_robots + nb_cells*nb_cells)
    pass


if __name__ == '__main__':
    pass
