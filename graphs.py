#! /usr/bin/python3

# Libs

# Other


class Node():
    all_children = set()
    """docstring for Node"""
    def __init__(self, state):
        self.state = state
        self.children = []

    def __str__(self):
        res = str(self.state)
        res += "\nNumber of children : "
        res += str(len(self.children))
        return res

    def build_children(self, ground_op_set):
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
        for child in cls.all_children:
            if child.state == state:
                return child
        new_child = Node(state)
        cls.all_children.add(new_child)
        return new_child


def create_root(domprob):
    seen_states = []
    root = Node(convert_to_tuple_set(domprob.initialstate()))
    seen_states.append(root.state)
    op_list = list(domprob.operators())
    build_graph(root, op_list, seen_states, domprob)
    return root


def build_graph(node, op_list, seen_states, domprob):
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
    return goal.issubset(node.state)


def convert_to_tuple_set(set_of_atom):
    s = set()
    for atom in set_of_atom:
        s.add(tuple(atom.predicate))
    return s
