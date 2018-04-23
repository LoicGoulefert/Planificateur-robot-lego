#! /usr/bin/python3

# Libs

# Other


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
        self.children = []

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
        """
        for inst in ground_op_set:
            if inst.precondition_pos.issubset(self.state) \
              and inst.precondition_neg.isdisjoint(self.state):
                new_state = (self.state.union(inst.effect_pos)) \
                            .difference(inst.effect_neg)
                # appeler la f qui :
                # si le noeud + state existe, le renvoie
                # sinon, cree le noeud et l'enregistre dans all_children,
                # et le renvoie
                move_details = get_move_details(new_state)
                action = inst.operator_name, move_details[0], move_details[1]
                self.children.append((self.get_node_from_state(new_state),
                                      action))

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


def create_root(domprob):
    """Create the root of a graph, then
    recursively build the graph starting from this root.
    """
    seen_states = []
    root = Node(convert_to_tuple_set(domprob.initialstate()))
    seen_states.append(root.state)
    op_list = list(domprob.operators())
    build_graph(root, op_list, seen_states, domprob)
    return root


def build_graph(node, op_list, seen_states, domprob):
    """Recursively build the node's children until
    there are no new children created.
    """
    for op in op_list:
        node.build_children(domprob.ground_operator(op))

    # Delete nodes that we have already seen
    # node.children = [child for child in node.children
    #                  if child[0].state not in seen_states]

    # Recursive
    # Stops if current node has no new child
    for child in node.children:
        if child[0].state not in seen_states:
            seen_states.append(child[0].state)
            build_graph(child[0], op_list, seen_states, domprob)


def breadth_first_search(root, goal):
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

        for (child, action) in subtree_root.children:

            # The node has already been processed, so skip over it
            if child in closed_set:
                continue

            # The child is not enqueued to be processed,
            # so enqueue this level of children to be expanded
            if child not in open_set:
                # Faire le chemin
                meta[child] = (subtree_root, action)
                # Enqueue this node
                open_set.append(child)

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


def get_move_details(state):
    """Returns the cell coords associated
    with the 'move' action, and the robot who
    is making this move.
    """
    for s in state:
        if s[0] == 'at':
            return s[1], s[2]


def is_goal(node, goal):
    """Returns true if 'node' is a goal,
    false otherwise.
    """
    return goal.issubset(node.state)


def convert_to_tuple_set(set_of_atom):
    """Converts a set of Atom (from the pddlpy lib)
    to a set of tuple, because we can't compare Atoms.
    """
    s = set()
    for atom in set_of_atom:
        s.add(tuple(atom.predicate))
    return s
