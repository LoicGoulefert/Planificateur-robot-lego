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
        self.nb_robots = nb_robots
        self.width = width
        self.height = height
        self.operator_name = instance.operator_name


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
    """Converts a PDDL state into a bit-vector

    If a state has x robots, then the (number of cells + 8) * x
    first bits represent the robot's name and position.
    The next (number of cells)² bits are all of the 'allowed'
    preconditions possible for a state, with a value of 1 if a precondition
    is actually True in the pddl-style state.

    +---+---+
    | X |   |
    +---+---+ => 0 1 0 1 1 0 0 0  1  0  0  0  0 1 1 0 0 1 0 0 1 1 0 0 1 0 1 1 0
    |   |   |     encoding 'X'     X coords         'allowed' preconditions
    +---+---+

    """
    robots_seen = 0  # Keeps track of the number of robots seen
    nb_cells = width * height
    offset = (nb_cells+8) * (nb_robots)  # To skip the 'header' of the BV
    state_bv = BitVector(size=offset + nb_cells*nb_cells)

    for s in state:
        if s[0] == 'at':
            x, y = get_coord_from_cell(s[2])
            # Writing robot's name
            begin = robots_seen * (nb_cells+8)
            state_bv[begin:begin+8] = BitVector(intVal=ord(s[1]), size=8)
            # Writing robot's position
            index = (width*x + y) + robots_seen*(nb_cells+8) + 8
            state_bv[index] = 1
            robots_seen += 1
        else:
            c1 = get_index_of_cell(s[1], width)
            c2 = get_index_of_cell(s[2], width)
            index = c1*nb_cells + c2 + offset
            state_bv[index] = 1

    # print(state_bv[:offset])
    # print(state_bv)
    # translate_header(state_bv[:offset], nb_robots, nb_cells)
    # input()
    return state_bv


def get_ground_operator(op_list, domprob, nb_robots, width, height):
    """Converts a ground_operator set into a set of GroundOpBV."""
    res = list()
    for op in op_list:
        ground_op_bv = set()
        ground_op = domprob.ground_operator(op)
        for inst in ground_op:
            ground_op_bv.add(GroundOpBV(inst, nb_robots, width, height))
        res.append(ground_op_bv)
    return res


# Debug
def translate_header(header, nb_robots, nb_cells):
    for i in range(nb_robots):
        begin = i*(nb_cells+8)
        end = i*(nb_cells+8)+8
        robot_name = chr(int(header[begin:end]))
        at = header[end:end+nb_cells]
        print("Robot {} at {}".format(robot_name, at))


if __name__ == '__main__':
    pass
