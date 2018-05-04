#!/usr/bin/python3

# Libs
import pddlpy
from time import time

# Others
from graphs import Node, create_root, dijkstra_search
from graphs import convert_to_tuple_set  # , breadth_first_search
from client import send_data
from parser import path_to_string, goals_to_string
from parser import robots_coord_to_string, build_message
from bitvector import convert_to_bv, set_robot_list


def get_domprob(domain_path, problem_path):
    """Returns the domain problem"""
    return pddlpy.DomainProblem(domain_path, problem_path)


def get_nb_robots(initial_state):
    """Returns the number of robots in the maze.
    This function is specific to maze planning problems.
    """
    res = 0
    for s in initial_state:
        if s[0] == 'at':
            res += 1
    return res


def get_robot_list(initial_state):
    """Returns a list containing the names of the robots,
    sorted alphabetically.
    """
    res = list()
    for s in initial_state:
        if s[0] == 'at':
            res.append(s[1])
    res.sort()
    return res


def get_width_and_height(pddl_problem_file):
    """Returns the width and height of the maze.
    This function is specific to maze planning problems.
    """
    with open(pddl_problem_file) as f:
        first_line = f.readline()
        second_line = f.readline()
        width = int(first_line.strip('; \n'))
        height = int(second_line.strip('; \n'))
        return width, height


def configure_planner():
    """Returns the domain and problem files, and the
    configuration (ip and port) for the client.
    """
    print("Configuration du planner : ")
    domain = input("Chemin du fichier domaine pddl :")
    problem = input("Chemin du fichier probleme pddl :")

    print("Configuration du client :")
    IPAdr = input("IP : ")
    port = int(input("Port : "))
    return domain, problem, IPAdr, port


def main():
    # domain, problem, IPAdr, port = configure_planner()
    maze_pb = int(input("Quel fichier de probleme ? (1, 2 ou 3) :"))
    if maze_pb == 3:
        file = "m1.txt"
    else:
        file = "test.txt"
    problem_file = 'pddl/problem-maze{}.pddl'.format(maze_pb)
    domprob = get_domprob('pddl/domain-maze.pddl', problem_file)
    goal = convert_to_tuple_set(domprob.goals())
    initial_state = convert_to_tuple_set(domprob.initialstate())

    # ********************Test BV********************************
    nb_robots = get_nb_robots(initial_state)
    width, height = get_width_and_height(problem_file)
    set_robot_list(initial_state)
    init_bv = convert_to_bv(initial_state, nb_robots, width, height)
    goal_bv = convert_to_bv(goal, nb_robots, width, height)

    # ***********************************************************

    root = create_root(init_bv)

    t0 = time()
    path = dijkstra_search(root, goal_bv, domprob, nb_robots, width, height)
    t1 = time()
    print("dijkstra_search : {}s".format(t1 - t0))
    print("Number of nodes explored: {}".format(len(Node.all_children)))

    if path is None:
        print("No path found.")
    else:
        # Sending path to simulator
        goal_str = goals_to_string(goal)
        robots_str = robots_coord_to_string(initial_state)
        path_str = path_to_string(
            path, get_robot_list(initial_state), width*height, width)
        message = build_message(file, goal_str, "", robots_str, path_str)
        send_data(message)
        # send_data(message, IPAdr, port)

if __name__ == "__main__":
    main()
