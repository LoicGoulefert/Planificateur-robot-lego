#! /usr/bin/python3

# Libs
# from time import time
# Other
from priorityqueue import PriorityQueue
from BitVector import BitVector
from bitvector import get_ground_operator


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

        The 'ground_op_set' parameter is a set of all possible actions
        per operator.
        """
        for inst in ground_op_set:
            # print("precond_pos=", inst.precondition_pos)
            # print("state=", self.state)
            # print("res precond_pos & state=", inst.precondition_pos & self.state)
            # print("neg=", inst.precondition_neg)
            # print("res neg ^ state=", inst.precondition_neg ^ self.state)
            zero_bv = BitVector(size=len(inst.precondition_pos))
            # print("and => ", (inst.precondition_pos & self.state) == inst.precondition_pos)
            # print("xor => ", ~(inst.precondition_neg & self.state) == ~zero_bv)
            # print("~zero => ", ~zero_bv)
            # print("\n")
            #input()
            if (inst.precondition_pos & self.state) == inst.precondition_pos \
               and ~(inst.precondition_neg & self.state) == ~zero_bv:
                # Creating new state
                new_state = (self.state | inst.effect_pos) & (~inst.effect_neg)
                # t2 = time()
                header = new_state[:inst.width * inst.height * inst.nb_robots]
                move_details = header | zero_bv
                action = (inst.operator_name, move_details)
                # t3 = time()
                self.children.append((self.get_node_from_state(new_state),
                                      action))
                # print(move_details)
                # input()

    def get_node_from_state(cls, state):
        """Returns a node representing the 'state'.

        If this node already exists in the graph,
        returns it. Else, returns a new node and
        register it in the all_children set.
        """
        for child in cls.all_children:
            if child.state == state:
                return child
        new_child = Node(state)
        cls.all_children.add(new_child)
        return new_child


def create_root(initial_state):
    """Create the root of a graph"""
    root = Node(initial_state)
    root.priority = 0
    return root


def breadth_first_search(root, goal, op_list, domprob):
    """Breadth first search of a solution
    in a graph. Returns a path if there is any.
    """
    # FIFO open set
    open_set = []
    # an empty set to maintain visited nodes
    closed_set = set()
    # a dictionary for path formation
    meta = dict()  # key -> (parent state, action to reach child)

    # initialize
    open_set.append(root)

    meta[root] = (None, None)

    while open_set != []:
        subtree_root = open_set.pop(0)

        if is_goal(subtree_root, goal):
            return construct_path(subtree_root, meta)

        # Create current node's children
        for op in op_list:
            subtree_root.build_children(domprob.ground_operator(op))

        for (child, action) in subtree_root.children:

            # The node has already been processed, so skip over it
            if child in closed_set:
                continue

            # The child is not enqueued to be processed,
            # so enqueue this level of children to be expanded
            if child not in open_set:
                # Update the path
                meta[child] = (subtree_root, action)
                # Enqueue this node
                open_set.append(child)

            closed_set.add(subtree_root)


def dijkstra_search(root, goal, domprob, nb_robots, width, height):
    """Dijkstra search of a solution in a graph.
    Returns a path if there is any.

    The priority of each node represent the cost
    (if each edge weights 1) to go from the root
    to the node.
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
    ground_op_bv = get_ground_operator(op_list, domprob, nb_robots, width, height)

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
                # Set priority level of the child
                child.priority = current_priority + 1
                # Update the path
                meta[child] = (subtree_root, action)
                # Enqueue this node
                pqueue.insert(child)

            closed_set.add(subtree_root)


def construct_path(state, meta):
    """Builds the action list of the solution path
    found by breadth_first_search function.
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
    """Returns true if 'node' is a goal,
    false otherwise.
    """
    return goal & node.state == goal


def convert_to_tuple_set(set_of_atom):
    """Converts a set of Atom (from the pddlpy lib)
    to a set of tuple, because we can't compare Atoms.
    """
    s = set()
    for atom in set_of_atom:
        s.add(tuple(atom.predicate))
    return s
