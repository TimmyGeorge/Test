from typing import Self

class Node:
    def __init__(self, parent : Self, action : str, state : str):
        self.parent : Self = parent
        self.action : str = action
        self.state : str = state

class QueueFrontier:
    def __init__(self, initial_node : Node = None):
        self.queue : list[Node] = []
        if initial_node != None:
            self.add([initial_node])
    def is_empty(self) -> bool:
        return len(self.queue) == 0
    def add(self, nodes : list[Node])->None:
        if len(nodes) == 0:
            return
        for node in nodes:
            self.queue.append(node)
    def remove(self) -> Node:
        if self.is_empty():
            raise IndexError("trying to remove a node from an empty frontier".title())
        node : Node = self.queue[0]
        self.queue = self.queue[1:]
        return node
    def contains(self, state : str) ->bool:
        queue_of_removed_nodes : QueueFrontier = QueueFrontier()
        found_state : bool = False
        while not(self.is_empty()) and not(found_state):
            node : Node = self.remove()
            queue_of_removed_nodes.add([node])
            if node.state == state:
                found_state = True
        while not(queue_of_removed_nodes.is_empty()):
            node = queue_of_removed_nodes.remove()
            self.add([node])
        return found_state
        















