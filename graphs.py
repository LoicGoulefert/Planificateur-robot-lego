#! /usr/bin/python3

# Libs
# from time import time
# Other
from priorityqueue import PriorityQueue
from bitarray import bitarray
from bitvector import get_ground_operator
import sys


class Node():
    """This class represents a node of the graph.
    Each node is identified by its state, and can build
    its own children depending on the different states it
    can reach.

    The class variable all_children stores the different states
    (e.g. the different nodes) that were seen during
    the creation of a graph.
    """
    all_children = set()

    def __init__(self, state):
        self.state = state
        self.children = []  # Will store a tuple (state, action)
        self.priority = None  # Priority used in Dijkstra search

    def __str__(self):
        res = str(self.state)
        res += "\nNumber of children : "
        res += str(len(self.children))
        return res

    def build_children(self, ground_op_set):
        """Builds the children of the current node.

        A child is created if its state has never been seen
        (e.g. it is not in all_children set). Otherwise, the "new"
        child is appended to the node's children list, but is not
        created.

        Parameter:
            ground_op_set: set of all possible actions per operator.
        """
        length = len(self.state)
        zero_bv = bitarray(length)
        zero_bv.setall(False)
        for inst in ground_op_set:
            if (inst.precondition_pos & self.state) == inst.precondition_pos \
               and (inst.precondition_neg & self.state) == zero_bv:
                # Create new state
                new_state = (self.state | inst.effect_pos) & (~inst.effect_neg)
                # Extract move details
                header_size = inst.width * inst.height * inst.nb_robots
                padding = bitarray(length - header_size)
                padding.setall(False)
                move_details = new_state[:header_size]
                move_details.extend(padding)
                action = (inst.operator_name, move_details)
                self.children.append((self.get_node_from_state(new_state),
                                      action))

    def get_node_from_state(cls, state):
        """Returns a node representing the 'state'.

        If this node already exists in the graph,
        returns it. Else, returns a new node and
        register it in the all_children set.

        Parameter:
            state: bitvector representing a state of the maze.
        """
        for child in cls.all_children:
            if child.state == state:
                return child
        new_child = Node(state)
        cls.all_children.add(new_child)
        return new_child


def create_root(initial_state):
    """Create the root of a graph.

    Parameter:
        initial_state: bitvector representing the
                        initial state of the maze.
    """
    root = Node(initial_state)
    root.priority = 0
    return root


def dijkstra_search(root, goal, init, domprob, nb_robots, width, height):
    """Dijkstra search of a solution in a graph.
    Returns a path if there is any.

    The priority of each node represent the cost
    (if each action costs 1) to go from the root
    to the node.

    Parameters:
        root: Node object, the root of the state graph we're
              searching and building at the same time.
        goal: bitvector, the state we're searching.
        init: bitvector, the initial state of the maze.
        domprob: Domain-Problem object from the pddlpy lib.
        nb_robots: integer, the number of robots in the maze.
        width, height: integers, the dimensions of the maze.
    """
    # Priority queue
    pqueue = PriorityQueue()
    # an empty set to maintain visited nodes
    closed_set = set()
    # a dictionary for path formation
    meta = dict()  # key -> (parent state, action to reach child)
    # Operator list
    op_list = list(domprob.operators())

    # initialize
    pqueue.insert(root)

    meta[root] = (None, None)
    ground_op_bv = get_ground_operator(
        op_list, domprob, init, nb_robots, width, height)
    print("Taille de ground_op : {}".format(len(ground_op_bv[0])))

    while not pqueue.empty():
        subtree_root = pqueue.dequeue()
        current_priority = subtree_root.priority

        if is_goal(subtree_root, goal):
            return construct_path(subtree_root, meta)

        # Create current node's children
        for op in ground_op_bv:
            subtree_root.build_children(op)

        for (child, action) in subtree_root.children:
            # The node has already been processed, so skip over it
            if child in closed_set:
                continue

            # The child is not enqueued to be processed,
            # so enqueue this level of children to be expanded
            if child not in pqueue.queue:
                child.priority = current_priority + 1
                # Update the path
                meta[child] = (subtree_root, action)
                # Enqueue this node
                pqueue.insert(child)

            closed_set.add(subtree_root)


def a_star_search(root, goal, init, domprob, nb_robots, width, height):
    """A* search of a solution in a graph.
    Returns a path if there is any.

    The priority of each node represent the cost
    (if each action costs 1) to go from the root
    to the node + the heuristic function value at current node.

    Parameters:
        root: Node object, the root of the state graph we're
              searching and building at the same time.
        goal: bitvector, the state we're searching.
        init: bitvector, the initial state of the maze.
        domprob: Domain-Problem object from the pddlpy lib.
        nb_robots: integer, the number of robots in the maze.
        width, height: integers, the dimensions of the maze.
    """
    # Priority queue
    pqueue = PriorityQueue()
    # an empty set to maintain visited nodes
    closed_set = set()
    # a dictionary for path formation
    meta = dict()  # key -> (parent state, action to reach child)
    # Operator list
    op_list = list(domprob.operators())

    # initialize
    pqueue.insert(root)

    meta[root] = (None, None)
    ground_op_bv = get_ground_operator(
        op_list, domprob, init, nb_robots, width, height)
    print("Taille de ground_op : {}".format(len(ground_op_bv[0])))
    # for opbv in ground_op_bv[0]:
    #     print(opbv.precondition_pos)

    while not pqueue.empty():
        subtree_root = pqueue.dequeue()
        current_priority = subtree_root.priority

        if is_goal(subtree_root, goal):
            return construct_path(subtree_root, meta)

        # Create current node's children
        for op in ground_op_bv:
            subtree_root.build_children(op)

        for (child, action) in subtree_root.children:
            # The node has already been processed, so skip over it
            if child in closed_set:
                continue

            # The child is not enqueued to be processed,
            # so enqueue this level of children to be expanded
            if child not in pqueue.queue:
                h = graphplan_heuristic(child.state, ground_op_bv, goal, 0, [])
                # print("A* : h = {}".format(h))
                child.priority = current_priority + 1 + h
                # Update the path
                meta[child] = (subtree_root, action)
                # Enqueue this node
                pqueue.insert(child)

            closed_set.add(subtree_root)


def construct_path(state, meta):
    """Builds the action list of a solution path.

    Parameters:
        state: bitvector, should be the goal
        meta: dict{}, containing the move-state actions
              to extract the solution path.
    """
    action_list = list()

    while True:
        if state is not None:
            row = meta[state]
        else:
            break
        if len(row) == 2:
            state = row[0]
            action = row[1]
            action_list.append(action)
        else:
            break

    action_list.reverse()
    action_list.pop(0)
    return action_list


def is_goal(node, goal):
    """Returns true if 'node' is a goal, false otherwise.

    Parameters:
        node: Node object
        goal: bitvector representing the goal we're looking for.
    """
    return goal & node.state == goal


def convert_to_tuple_set(set_of_atom):
    """Converts a set of Atom (from the pddlpy lib)
    to a set of tuple, because we can't compare Atoms.

    Parameters:
        set_of_atom: a set of Atom objects.
    """
    s = set()
    for atom in set_of_atom:
        s.add(tuple(atom.predicate))
    return s


# Marche pô
def graphplan_heuristic(state, ground_op_bv, goal, depth, seen_list):
    """Build a relaxed graphplan. This is used to compute a
    heuristic for A* search, but right now it just slow down the A* algo.

    Parameters:
        state: bitvector, the current state from which we'll build graphplan.
        ground_op_bv: list of sets of GroundOpBV objects.
        goal: bitvector, the goal we're searching.
        depth: integer, count the depth of graphplan. This is the
               value used as a heuristic.
        seen_list: list of bitvectors, to maintain visited states.
    """
    length = len(state)
    zero_bv = bitarray(length)
    zero_bv.setall(False)
    for op in ground_op_bv:
        for inst in op:
            # Check if the action is valid
            if (inst.precondition_pos & state) == inst.precondition_pos \
               and (inst.precondition_neg & state) == zero_bv:
                depth += 1
                # Create a new state with a valid action
                new_state = (state | inst.effect_pos) & (~inst.effect_neg)
                if new_state not in seen_list:
                    seen_list.append(new_state)
                    if goal & new_state == goal:
                        return depth
                    else:
                        return graphplan_heuristic(
                            new_state, ground_op_bv, goal, depth, seen_list)

    return sys.maxsize
