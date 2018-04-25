#!/usr/bin/python3

# Libs
import pddlpy
from time import time

# Others
from graphs import Node, create_root, dijkstra_search
from graphs import convert_to_tuple_set
from client import send_data
from parser import path_to_string, goals_to_string
from parser import robots_coord_to_string, build_message


def get_domprob(domain_path, problem_path):
    """Returns the domain problem"""
    return pddlpy.DomainProblem(domain_path, problem_path)


def print_infos(domprob):
    """Debug function"""
    print("Infos :")
    print("Initial state :")
    initial_state = domprob.initialstate()
    print(initial_state)
    print("Operators list :")
    op_list = list(domprob.operators())
    print(op_list)
    print("Goals :")
    goals = domprob.goals()
    print(goals)


if __name__ == "__main__":
    # print("Configuration du planner : ")
    # domain = input("Chemin du fichier domaine pddl :")
    # problem = input("Chemin du fichier probleme pddl :")

    # print("Configuration du client :")
    # IPAdr = input("IP : ")
    # port = int(input("Port : "))
    maze_pb = int(input("Quel fichier de probleme ? (1, 2 ou 3) :"))
    if maze_pb == 3:
        file = "m1.txt"
    else:
        file = "test.txt"
    domprob = get_domprob('pddl/domain-maze.pddl', 'pddl/problem-maze{}.pddl'.format(maze_pb))
    # domprob = get_domprob(domain, problem)
    goal = convert_to_tuple_set(domprob.goals())
    initial_state = convert_to_tuple_set(domprob.initialstate())
    op_list = list(domprob.operators())

    root = create_root(domprob)

    t0 = time()
    path = dijkstra_search(root, goal, op_list, domprob)
    t1 = time()
    print("dijkstra_search : {}s".format(t1 - t0))

    print("Path : ")
    print(path)
    print("Number of nodes explored: {}".format(len(Node.all_children)))

    if path is None:
        print("No path found.")
    else:
        goal_str = goals_to_string(goal)
        robots_str = robots_coord_to_string(initial_state)
        path_str = path_to_string(path)

        message = build_message(file, goal_str, "", robots_str, path_str)

        send_data(message)
        # send_data(message, IPAdr, port)
