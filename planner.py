#!/usr/bin/python3

# Libs
import pddlpy

# Others
from graphs import Node, create_root
from graphs import breadth_first_search, convert_to_tuple_set
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
    domprob = get_domprob('pddl/domain-maze.pddl', 'pddl/problem-maze1.pddl')
    goal = convert_to_tuple_set(domprob.goals())
    initial_state = convert_to_tuple_set(domprob.initialstate())
    root = create_root(domprob)
    print(root.children[0][0])
    path = breadth_first_search(root, goal)
    print("Path : ")
    print(path)
    print("Number of nodes : {}".format(len(Node.all_children)))

    path_str = path_to_string(path)
    goal_str = goals_to_string(goal)
    robots_str = robots_coord_to_string(initial_state)

    message = build_message("test.txt", goal_str, "", robots_str, path_str)
    print(message)

    send_data(message)
