#!/usr/bin/python3

# Libs
import pddlpy


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

if __name__ == "__main__":
    domprob = get_domprob('pddl/domain-maze.pddl', 'pddl/problem-maze1.pddl')
    print_infos(domprob)
