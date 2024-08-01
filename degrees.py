import csv
import sys

from typing import Set
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

class Test:
    @staticmethod
    def node_test_code()->None:
        node : Node = Node(parent = None, action = "11232", state = "2123")
        print(f"{node =}")
        print(f"{node.parent =}")
        print(f"{node.action =}")
        print(f"{node.state =}")
        node2 : Node = Node(parent = node, action = "12312", state = "23421")
        print(f"{node2.parent =}")
        print(f"{node2.action =}")
        print(f"{node2.state =}")
    @staticmethod
    def test_queue_frontier()->None:
        node : Node = Node(parent = None, action = "11232", state = "2123")
        node2 : Node = Node(parent = node, action = "12312", state = "23421")
        print(f"{node =}")
        print(f"{node2 =}")
        print()
        frontier1 : QueueFrontier = QueueFrontier()
        frontier1.add([node, node2])
        print(f"{frontier1.is_empty()=}")
        print(f"{frontier1.contains('2123')=}")
        print(f"{frontier1.contains('23421')=}")
        print(f"{frontier1.contains('112322')=}")
        print(f"{frontier1.remove()=}")
        print(f"{frontier1.remove()=}")
        try:
            print(f"{frontier1.remove()=}")
        except IndexError as e:
            print(e)
        print(f"{frontier1.is_empty()=}")
        frontier2 : QueueFrontier = QueueFrontier(node)
        print()
        print(f"{frontier2.remove()=}")
    @staticmethod
    def test_solver_expand(source : str, target : str)-> list[Node]:
        initial_node : Node = Node(parent = None, action = None, state = source)
        neighbouring_nodes : list[Node] = Solver.expand(initial_node)
        print(f"{target=}")
        print(f"{initial_node.state=}")
        print("Neighbouring Actors Are:")
        for neighbouring_node in neighbouring_nodes:
            print(f"{neighbouring_node.state=} {neighbouring_node.action=}")
        return neighbouring_nodes
    @staticmethod
    def test_solver_remove_found_nodes(source : str, target : str):
        neighbouring_nodes : list[Node] = Test.test_solver_expand(source = source, target = target)
        counter = 0
        frontier : QueueFrontier = Queuefrontier(list(neighbouring_nodes)[0])
        explored_states : Set = [ list(neighbouring_nodes)[1] ]
        new_nodes : list[Node] = Solver.remove_found_nodes(nodes = neighbouring_nodes, frontier = frontier, explored_states = explored_states)
        print()
        print(f"{frontier.queue[0].state = }")
        print(f"{explored_states[0] = }")
        print("New Nodes Are")
        for new_node in new_nodes:
            print(f"{new_node.state=} {new_node.action=}")
    @staticmethod
    def test_solver_is_a_goal(source : str, success_case : bool):
        initial_node : Node = Node(parent = None, action = None, state = source)
        neighbouring_nodes : list[Node] = Solver.expand(initial_node)
        if success_case:
            target : str = list(neighbouring_nodes)[0].state
        else:
            target : str = "-_-"
        there_is_a_goal : bool = False
        goal_node : Node = None
        there_is_a_goal, goal_node = Solver.is_a_goal(neighbouring_nodes,target)
        print(f"{source=}")
        print(f"{target=}")
        print("Neighbouring Actors Are:")
        for neighbouring_node in neighbouring_nodes:
            print(f"{neighbouring_node.state=} {neighbouring_node.action=}")
        if there_is_a_goal:
            print(f"{Solver.is_a_goal(neighbouring_nodes,target)[0]=} {Solver.is_a_goal(neighbouring_nodes,target)[1].state=}")
        else:
            print(f"{Solver.is_a_goal(neighbouring_nodes,target)[0]=} {Solver.is_a_goal(neighbouring_nodes,target)[1]=}")
    @staticmethod
    def test_solver_generate_solution():
        node1 : Node = Node(parent = None, action = None, state = "A")
        node2 : Node = Node(parent = node1, action = "1", state = "B")
        node3 : Node = Node(parent = node2, action = "2", state = "C")
        node4 : Node = Node(parent = node3, action = "3", state = "D")
        solution : list[tuple[str]] = Solver.generate_solution(node4)
        print(f"{node1=} {node1.state=} {node1.action=} {node1.parent=}")
        print(f"{node2=} {node2.state=} {node2.action=} {node2.parent=}")
        print(f"{node3=} {node3.state=} {node3.action=} {node3.parent=}")
        print(f"{node4=} {node4.state=} {node4.action=} {node4.parent=}")
        print("Solution:")
        print(solution)
   
class Solver:
    @staticmethod
    def is_a_goal(nodes : Set[Node], target : str) -> bool:
        for node in nodes:
            if node.state == target:
                return True, node
        return False, None
    @staticmethod
    def expand(node: Node) -> list[Node]:
        neighbouring_states : dict[str,str] = Solver.get_neighbouring_states(node.state)
        neighbouring_nodes : Set[Node] = set()
        for state, action in neighbouring_states.items():
            neighbouring_node = Node(parent = node, action = action, state = state)
            neighbouring_nodes.add(neighbouring_node)
        return neighbouring_nodes
    @staticmethod
    def remove_found_nodes(nodes : list[Node], frontier : QueueFrontier, explored_states : list[str]) -> list[Node]:
        unfound_nodes : list[node] = []
        for node in nodes:
               if not(frontier.contains(node.state)) and not(node.state in explored_states):
                   unfound_nodes.append(node)
        return unfound_nodes
    @staticmethod
    def get_neighbouring_states(input_state : str) -> list[tuple[str]]:
        action_state_pairs : list[tuple[str]] = neighbors_for_person(input_state)
        neighbouring_states : dict[str,str] = {}
        for action, state in action_state_pairs:
            if neighbouring_states.get(state,"None")=="None":
                neighbouring_states[state] = action
        return neighbouring_states
    @staticmethod
    def generate_solution(goal_node) -> list[tuple[str]]:
        path : list[tuple[str]] = []
        current_node : Node = goal_node
        while current_node.parent != None:
           path.insert(0,(current_node.action, current_node.state))
           current_node = current_node.parent
        return path

    
# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    #List Of Things to create
    #/   - Node
    #/       - parent : Node
    #/       - action : str
    #/       - state : str
    #/   - QueueFrontier
    #/       - constructor(initial_node = None : Node)
    #/       - is_empty() -> bool
    #/       - add(nodes : list[Node]) -> None
    #/       - remove() -> Node
    #/       - contains(state : str)->bool
    #   - Solver
    #/       - target
    #/       - expand(node : Node) -> list[Node]
    #/           - neighbors_for_person(state : str) #already made
    #/           - get_neighbouring_states(input_state : str) -> list[tuple[str]] #To remove duplicates
    #/           - node
    #/       - remove_found_nodes(nodes : list[Node], frontier : QueueFrontier, explored_states : list[str]) -> list[Node]
    #/       - is_a_goal(nodes : list[Node], target : str) -> bool, Node
    #/       - generate_solution(goal_node) -> list[tuple[str]]
    node : Node = None
    neighbouring_nodes : list[Node] = None
    new_nodes : list[Node] = None
    there_is_a_goal : bool = None
    goal_node : Node = None
    
    Source_Node : Node = Node(parent = None, action = None, state = source)
    frontier : QueueFrontier = QueueFrontier(Source_Node)
    explored_states : Set = set()
    while True:
        if frontier.is_empty():
           return None
        node = frontier.remove()
        explored_states.add(node.state)
        neighbouring_nodes = Solver.expand(node)             #needs to use , node
        new_nodes = Solver.remove_found_nodes(neighbouring_nodes, frontier, explored_states)
        there_is_a_goal, goal_node = Solver.is_a_goal(new_nodes, target)
        if there_is_a_goal:
            return Solver.generate_solution(goal_node)      #uses parents of goal node
        frontier.add(new_nodes)

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
