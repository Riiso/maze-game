import heapq

class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        # Override the default equals method
        return self.position == other.position

    def __lt__(self, other):
        # For the heap queue to work with the lowest f value, we need to override the less than operator
        return self.f < other.f
    
    def __hash__(self):
        # Hash based on the node's unique position
        return hash(self.position)

def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list and Add the start node
    heapq.heapify(open_list) 
    heapq.heappush(open_list, start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            #print("Path found:", path[::-1])
            return path[::-1]  # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] not in [0, 3, 4]:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            if child in closed_list:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            if len([open_node for open_node in open_list if child == open_node and child.g > open_node.g]) > 0:
                continue

            # Add the child to the open list
            heapq.heappush(open_list, child)

    return None  # No path found

def astar_collectibles(maze, start, collectibles, end):
    path = []
    current_position = start

    # Ensure collectibles are tuples, since your astar uses tuple positions
    collectibles = [tuple(collectible) for collectible in collectibles]

    while len(collectibles) > 0:
        # Find closest collectible
        closest_collectible, closest_path = find_closest_collectible(maze, current_position, collectibles)
        if closest_path:
            # Exclude the starting point of each segment after the first to avoid duplicate positions
            path += closest_path if not path else closest_path[1:]
            current_position = closest_collectible
            collectibles.remove(closest_collectible)
        else:
            #print("Could not find path to collectible:", closest_collectible)
            break  # Break the loop if no path to a collectible is found

    # If current position is not the end, find path from current position to end
    if current_position != end:
        #print("Finding path from current position to end:", current_position, end)
        final_path = astar(maze, current_position, end)
        if final_path:
            #print("Found path from current position to end:", final_path)
            # Exclude the starting point of the final segment to avoid duplicate positions
            path += final_path[1:]  # Ensure we're not duplicating the last collectible's position
        #else:
            #print("Could not find path from current position to end.")
    #print("Final path:", path)
    return path

def find_closest_collectible(maze, start, collectibles):
    closest_collectible = None
    closest_path = []
    shortest_distance = float('inf')

    for collectible in collectibles:
        #print("Trying to find path from", start, "to collectible at", collectible)
        path = astar(maze, start, collectible)
        if path:
            #print("Found path to collectible", collectible, ":", path)
            if len(path) < shortest_distance:
                closest_collectible = collectible
                closest_path = path
                shortest_distance = len(path)
        #else:
            #print("No path found to collectible", collectible)

    #if closest_collectible is None:
        #print("No closest collectible found. This could be due to maze configuration or collectibles' positioning.")
    return closest_collectible, closest_path

# ------------------------------------------------------------------------------------------------------------------------------------------------

def dijkstra_path(maze, start, targets):
    start_node = Node(None, start)
    start_node.g = 0

    open_list = []
    heapq.heappush(open_list, (0, start_node))

    visited = set()

    while open_list:
        current_g, current_node = heapq.heappop(open_list)

        if current_node.position in targets:
            path = []
            target_position = current_node.position
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return target_position, path[::-1]  # Return both the target position and the path

        visited.add(current_node.position)

        for direction in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            neighbor_pos = (current_node.position[0] + direction[0], current_node.position[1] + direction[1])
            if 0 <= neighbor_pos[0] < len(maze) and 0 <= neighbor_pos[1] < len(maze[0]) and maze[neighbor_pos[0]][neighbor_pos[1]] in [0, 3, 4] and neighbor_pos not in visited:
                neighbor_node = Node(current_node, neighbor_pos)
                neighbor_g = current_g + 1
                heapq.heappush(open_list, (neighbor_g, neighbor_node))

    return None, []  # Return None for the target position and an empty list for the path if no path was found

def dijkstra(maze, start, collectibles, end):
    path = []
    current_position = start
    targets = set(collectibles + [end])  # Use a set for efficient look-up

    while targets:
        target_position, shortest_path = dijkstra_path(maze, current_position, targets)
        if shortest_path:
            path += shortest_path if not path else shortest_path[1:]
            current_position = target_position
            targets.discard(target_position)  # Remove the found target
        else:
            print("Could not find path to any remaining target.")
            break

    return path

'''
#Example usage
maze = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [4, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1],
            [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1],
            [1, 0, 2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

start = (22, 2)
collectibles = [(2, 3), (5, 9), (17, 12)]
end = (2, 0)

path = dijkstra(maze, start, collectibles, end)
print(path)
'''