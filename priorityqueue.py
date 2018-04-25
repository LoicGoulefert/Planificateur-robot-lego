#! /usr/bin/python3

# Libs

# Other


class PriorityQueue:

    def __init__(self):
        self.queue = list()

    def insert(self, node):
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
        # remove the first node from the queue
        return self.queue.pop(0)

    def size(self):
        return len(self.queue)
