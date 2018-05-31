#! /usr/bin/python3

# Libs

# Other


class PriorityQueue:
    """Implementation of a priority queue."""
    def __init__(self):
        self.queue = list()

    def insert(self, node):
        """Insert a node into the priority queue,
        so that it still is ordered after the insertion.
        """
        # if queue is empty
        if self.size() == 0:
            # add the new node
            self.queue.append(node)
        else:
            # traverse the queue to find the right place for new node
            for x in range(0, self.size()):
                # if the priority of new node is greater
                if node.priority >= self.queue[x].priority:
                    # if we have traversed the complete queue
                    if x == (self.size()-1):
                        # add new node at the end
                        self.queue.insert(x+1, node)
                    else:
                        continue
                else:
                    self.queue.insert(x, node)
                    return True

    def dequeue(self):
        """Remove the first node from the queue."""
        return self.queue.pop(0)

    def size(self):
        """Returns the size of the queue."""
        return len(self.queue)

    def empty(self):
        """Returns true if the queue is empty, false otherwise."""
        return self.size() == 0
