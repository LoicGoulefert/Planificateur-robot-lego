#!/usr/bin/python3

# Libs
import pddlpy

# Others
from graphs import Node, convert_to_tuple_set, breadth_first_search


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


def create_root(domprob):
    seen_states = []
    root = Node(convert_to_tuple_set(domprob.initialstate()), None)
    seen_states.append(root.state)
    op_list = list(domprob.operators())
    build_graph(root, op_list, seen_states, domprob)
    return root


def build_graph(node, op_list, seen_states, domprob):
    for op in op_list:
        node.build_children(domprob.ground_operator(op))

    # Delete nodes that we have already seen
    node.children = [child for child in node.children
                     if child[0].state not in seen_states]

    # Recursive
    # Stops if current node has no child
    for child in node.children:
        seen_states.append(child[0].state)
        build_graph(child[0], op_list, seen_states, domprob)


if __name__ == "__main__":
    domprob = get_domprob('pddl/domain-maze.pddl', 'pddl/problem-maze1.pddl')
    goal = domprob.goals()
    root = create_root(domprob)
    print(root.children[0][0])
    path = breadth_first_search(root, convert_to_tuple_set(goal))
    print(path)
