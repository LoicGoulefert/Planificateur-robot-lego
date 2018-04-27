#! /usr/bin/python3

# Libs

# Others
from BitVector import BitVector

"""This module is an interface between the pddlpy lib
and a bitvector representation of states.

All functions in this module will get informations from
the pddlpy lib and convert those into sets of bitvectors.
"""


class GroundOpBV():
    """This object will replace the objects
    returned by domprob.ground_op(op).
    """
    def __init__(self, instance, nb_robots, width, height):
        self.precondition_pos = convert_to_bv(instance.precondition_pos,
                                              nb_robots,
                                              width,
                                              height)
        self.precondition_neg = convert_to_bv(instance.precondition_neg,
                                              nb_robots,
                                              width,
                                              height)
        self.effect_pos = convert_to_bv(instance.effect_pos,
                                        nb_robots,
                                        width,
                                        height)
        self.effect_neg = convert_to_bv(instance.effect_neg,
                                        nb_robots,
                                        width,
                                        height)


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


def convert_to_bv(state, nb_robots, width, height):
    """Converts a PDDL state into a bit-vector"""
    robots_seen = 0  # Keeps track of the number of robots seen
    nb_cells = width * height
    offset = nb_cells * nb_robots  # To skip the 'header' of the BV
    init_state_bv = BitVector(size=offset + nb_cells*nb_cells)

    for s in state:
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


def get_ground_operator(ground_op, nb_robots, width, height):
    """Converts a ground_operator set into
    a set of GroundOpBV.
    """
    ground_op_bv = set()
    for inst in ground_op:
        ground_op_bv.add(GroundOpBV(inst, nb_robots, width, height))
    return ground_op_bv


if __name__ == '__main__':
    pass
