#!/usr/bin/python3

# Libs
import pddlpy

# Others
from graphs import Node, create_root
from graphs import breadth_first_search, convert_to_tuple_set
from client import send_data

objectives_name = "abcdefghijklmnopqrstuvwxyz"


def get_domprob(domain_path, problem_path):
    return pddlpy.DomainProblem(domain_path, problem_path)


def print_infos(domprob):
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


def path_to_string(path):
    """Converts the path into a string
    for the client.
    """
    res = "#4"  # ID of move list
    for action in path:
        res += action[1]
        coord = action[2].split('-')
        res += " " + coord[1] + " " + coord[2]
        res += ","
    return res[:-1]  # [:-1] to delete the last ','


def goals_to_string(goals):
    """Converts the goals into a string
    for the client.
    """
    i = 0  # index for objectives name
    res = "#1"
    for goal in goals:
        coord = goal[2].split('-')
        res += objectives_name[i] + " "
        res += coord[1] + " " + coord[2] + ","
        i += 1
    return res[:-1]  # [:-1] to delete the last ','


def robots_coord_to_string(initial_state):
    res = "#3"
    for state in initial_state:
        if state[0] == 'at':
            res += state[1] + " "
            coord = state[2].split('-')
            res += coord[1] + " " + coord[2]
            res += ","
    return res[:-1]  # [:-1] to delete the last ','


def build_message(config_file,
                  obj_coord, static_obj_coord,
                  robots_coord,
                  move_list):
    message = []
    message.append("#c" + config_file)
    if obj_coord != "":
        message.append(obj_coord)
    if static_obj_coord != "":
        message.append(static_obj_coord)
    message.append(robots_coord)
    message.append(move_list)
    return message


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
