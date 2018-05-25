#!/usr/bin/python3

# Libs
import pddlpy
from time import time

# Others
from graphs import Node, create_root, dijkstra_search
from graphs import convert_to_tuple_set
from client import send_data, send_object
from parser import path_to_string, goals_to_string
from parser import robots_coord_to_string, build_message
from bitvector import convert_to_bv, set_robot_list

"""How it works :
1) Config of pddl files + IP, port
2) Get info from pddl files (domprob, init_state...)
3) Build and send conf_list to simulator
4) Convert these infos into bitvectors
5) Search for a solution in state graph
6) Parse solution to send it to the simulator
"""


def get_domprob(domain_path, problem_path):
    """Returns the DomainProblem object from pddlpy.

    Parameters:
        domain_path: string, path of the domain file
        problem_path: string, path of the problem file
    """
    return pddlpy.DomainProblem(domain_path, problem_path)


def get_nb_robots(initial_state):
    """Returns the number of robots in the maze.
    This function is specific to maze planning problems.

    Parameters:
        initial_state: set of tuples ('at', 'X', 'c-0-0')
    """
    res = 0
    for s in initial_state:
        if s[0] == 'at':
            res += 1
    return res


def get_robot_list(initial_state):
    """Returns a list containing the names of the robots,
    sorted alphabetically.

    Parameters:
        initial_state: set of tuples ('at', 'X', 'c-0-0')
    """
    res = list()
    for s in initial_state:
        if s[0] == 'at':
            res.append(s[1])
    res.sort()
    return res


def build_config_list(initial_state, op_list, domprob):
    """Build the list of all preconditions that can be true.

    Parameters:
        initial_state: set of tuples ('at', 'X', 'c-0-0')
        op_list: list of strings, the names of the operators
        domprob: DomainProblem object from pddlpy
    """
    res = initial_state.copy()
    for op in op_list:
        ground_op = domprob.ground_operator(op)
        for gop in ground_op:
            for e_pos in gop.effect_pos:
                res.add(e_pos)
    return list(res)


def get_width_and_height(problem_file):
    """Returns the width and height of the maze.
    This function is specific to maze planning problems.

    Parameters:
        problem_file: string, path to pddl problem file
    """
    with open(problem_file) as f:
        first_line = f.readline()
        second_line = f.readline()
        width = int(first_line.strip('; \n'))
        height = int(second_line.strip('; \n'))
        return width, height


def configure_planner():
    """Returns the domain and problem files, and the
    configuration (ip and port) for the client.
    """
    print('Configuration du planner : ')
    domain = input('Chemin du fichier domaine pddl :')
    problem = input('Chemin du fichier probleme pddl :')

    print('Configuration du client :')
    IPAdr = input('IP : ')
    port = int(input('Port : '))
    return domain, problem, IPAdr, port


def search(f, params, timer=True):
    """Search for a solution using 'f' function.
    Returns a path if a solution is found, else None.

    Parameters:
        f : search function name
        params: a tuple of parameters
    """
    t0 = time()
    path = f(*params)
    if timer:
        print('Search duration: {}s'.format(time() - t0))
    print('Number of nodes explored: {}\n'.format(len(Node.all_children)))
    return path


def main():
    # domain, problem, IPAdr, port = configure_planner()
    maze_pb = int(input('Wich problem file should we use ?'
                        ' (0,1,2,3 ou 4) :'))

    # Loading PDDL datas
    problem_file = 'pddl/problem-maze{}.pddl'.format(maze_pb)
    domprob = get_domprob('pddl/domain-maze.pddl', problem_file)
    goal = convert_to_tuple_set(domprob.goals())
    initial_state = convert_to_tuple_set(domprob.initialstate())
    op_list = list(domprob.operators())

    # Init bitvectors
    nb_robots = get_nb_robots(initial_state)
    width, height = get_width_and_height(problem_file)
    set_robot_list(initial_state)
    init_bv = convert_to_bv(initial_state, nb_robots, width, height)
    goal_bv = convert_to_bv(goal, nb_robots, width, height)
    root = create_root(init_bv)
    params = (root, goal_bv, init_bv, domprob, nb_robots, width, height)

    # Creating and sending config list
    conf_list = build_config_list(initial_state, op_list, domprob)
    print('[PLANNER]Sending conf list')
    send_object(conf_list)

    # Searching for a path
    path = search(dijkstra_search, params)

    if path is None:
        print('No path found.')
    else:
        # Parsing datas
        goal_str = goals_to_string(goal)
        robots_str = robots_coord_to_string(initial_state)
        path_str = path_to_string(
            path, get_robot_list(initial_state), width*height, width)
        message = build_message(goal_str, "", robots_str, path_str)
        # Sending path to the simulator
        print('[PLANNER]Sending path')
        send_object(path)
        print('[PLANNER]Sending datas')
        send_data(message)
        # send_data(message, IPAdr, port)

if __name__ == "__main__":
    main()
