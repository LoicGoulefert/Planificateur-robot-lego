#! /usr/bin/python3

# Libs

# Other


class Node():
    """docstring for Node"""
    def __init__(self, state, parent):
        self.state = state
        self.children = []
        self.parent = parent

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
                new_node = Node(new_state, self)
                # I still need to add the move in the action
                action = inst.operator_name
                self.children.append((new_node, action))


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

        # TODO fonction is_goal
        if is_goal(subtree_root, goal):
            print("j'ai trouvé")
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
        row = meta[state]
        if len(row) == 2:
            state = row[0]
            action = row[1]
            action_list.append(action)
        else:
            break

    action_list.reverse()
    return action_list


def is_goal(node, goal):
    return goal in node.state


def convert_to_tuple_set(set_of_atom):
    s = set()
    for atom in set_of_atom:
        s.add(tuple(atom.predicate))
    return s
