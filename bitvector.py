#! /usr/bin/python3

# Libs
from bitarray import bitarray

# Others

"""Convert states into bitvectors.
Convert ground_op into GroundOpBV objects, meaning
it converts all preconditions and effects of a ground_op
into bitvectors.
"""

# Store the robots in alphabetical order
robot_list = list()


class GroundOpBV():
    """This object will replace the objects returned
    by domprob.ground_op(op).
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
        # C'est la qu'on veut identifier les grounp op
        self.operator_name = instance.operator_name
        self.variable_list = instance.variable_list


def set_robot_list(state):
    """Build the global variable robot_list, and sort it.

    Parameter:
        state: a pddl-like tuple of string
                ex : ('at', 'X', 'c-0-0')
    """
    for s in state:
        if s[0] == 'at':
            robot_list.append(s[1])
    robot_list.sort()


def get_coord_from_cell(cell):
    """From a string representing a cell in pddl format,
    returns the x and y coordinates.

    Parameter:
        cell: a string representing a cell.
              ex : 'c-0-0'
    """
    coord = cell.split('-')
    x, y = int(coord[1]), int(coord[2])
    return x, y


def get_index_of_cell(cell, width):
    """Returns the position of a cell in the maze.

    Parameters:
        cell: a string representing a cell ('c-0-0')
        width: an integer, the width of the maze
    """
    x, y = get_coord_from_cell(cell)
    return x*width + y


# A modifier
def convert_to_bv(state, nb_robots, width, height):
    """Converts a PDDL state into a bit-vector

    If a state has x robots, then the (number of cells + 8) * x
    first bits represent the robot's name and position.
    The next (number of cells)² bits are all of the 'allowed'
    preconditions possible for a state, with a value of 1 if a precondition
    is actually True in the pddl-style state.

    +---+---+
    | X |   |
    +---+---+ =>   1  0  0  0   0 1 1 0 0 1 0 0 1 1 0 0 1 0 1 1 0
    |   |   |       X coords         'allowed' preconditions
    +---+---+

    Parameters:
        state: a pddl-like tuple of string
        nb_robots: integer, number of robots on the maze
        width: integer, width of the maze
        height: integer, height of the maze
    """
    nb_cells = width * height
    offset = nb_cells * (nb_robots)  # To skip the 'header' of the BV
    state_bv = bitarray(offset + nb_cells*nb_cells)
    state_bv.setall(False)

    for s in state:
        if s[0] == 'at':
            # Encoding 'at' states in bitvector
            x, y = get_coord_from_cell(s[2])
            bot_index = robot_list.index(s[1])
            index = (width*x + y) + bot_index*nb_cells
            state_bv[index] = 1
        else:
            # Encoding 'allowed' states in bitvector
            c1 = get_index_of_cell(s[1], width)
            c2 = get_index_of_cell(s[2], width)
            index = c1*nb_cells + c2 + offset
            state_bv[index] = 1

    return state_bv


def get_ground_operator(op_list, domprob, init, nb_robots, width, height):
    """Converts a ground_operator set into a list of sets of GroundOpBV.
    Remove impossible operators (those whose preconditions
    will never be true).

    Parameters:
        op_list: string list, names of all operators
        domprob: Domain-Problem object from pddlpy lib
        init: bitvector representing the initial state of the maze
              + its preconditions ('allowed' and 'at')
        nb_robots: integer, number of robots in the maze
        width, height: integers, dimensions of the maze
    """
    res = list()  # A list of sets of GroundOpBV
    header_size = nb_robots * width * height
    for op in op_list:
        ground_op_bv = set()
        ground_op = domprob.ground_operator(op)
        for inst in ground_op:
            gobv = GroundOpBV(inst, nb_robots, width, height)
            # Adding possible action
            if (gobv.precondition_pos[header_size:] | init[header_size:]) \
               == init[header_size:]:
                ground_op_bv.add(gobv)
        res.append(ground_op_bv)
    return res


if __name__ == '__main__':
    pass
