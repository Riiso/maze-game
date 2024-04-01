import heapq
import time
import threading

class Node: # A class to represent a node
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):    # Override the default equals method
        return self.position == other.position

    def __lt__(self, other):    # For the heap queue to work with the lowest f value, we need to override the less than operator
        return self.f < other.f
    
    def __hash__(self): # Hash based on the node's unique position
        return hash(self.position)

def astar_threaded(maze, start, collectibles, end, callback):
    def run_astar():
        path = astar_collectibles(maze, start, collectibles, end)   # Run the original astar function
        callback(path)  # Call the callback with the result

    threading.Thread(target=run_astar).start()  # Start the astar function in a new thread

def dijkstra_threaded(maze, start, collectibles, end, callback):
    def run_dijkstra():
        path = dijkstra(maze, start, collectibles, end) # Run the original dijkstra function
        callback(path)  # Call the callback with the result

    threading.Thread(target=run_dijkstra).start()   # Start the dijkstra function in a new thread

def astar(maze, start, end, start_time, shortest_path_so_far=float('inf')):    # A* algorithm to find path from start to end

    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    open_list = []  # For nodes to be evaluated
    closed_list = []    # Nodes already evaluated

    heapq.heapify(open_list)
    heapq.heappush(open_list, start_node)

    while len(open_list) > 0:   # Loop until you find the end

        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        if current_node == end_node:    # Path found
            path = []
            current = current_node
            while current is not None:  # Trace back the path
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Generate children
            if time.time() - start_time > 5:  # Limit search time to 5 second
                print("A* time limit exceeded, returning part of path.")
                return []  # Return None for the target position and an empty list for the path if time limit is exceeded    

            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])    # Get node position

            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:    # Make sure within range
                continue

            if maze[node_position[0]][node_position[1]] not in [0, 3, 4, 5, 6, 7]:  # Make sure walkable terrain
                continue

            new_node = Node(current_node, node_position)  # Create new node

            children.append(new_node)

        for child in children:

            if child in closed_list:    # Child is on the closed list
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Early break if the current path cost exceeds the shortest path found so far
            if child.f > shortest_path_so_far:
                print("A* path cost exceeded shortest path found so far.")
                continue  # Skip this child as it cannot possibly lead to a shorter path

            if len([open_node for open_node in open_list if child == open_node and child.g > open_node.g]) > 0: # Child is already in the open list and has a higher g value
                continue

            heapq.heappush(open_list, child)    # Add the child to the open list

    return None  # No path found

def astar_collectibles(maze, start, collectibles, end): # A* algorithm to find path to collectibles and end
    start_time = time.time()  # Start timing
    path = []
    current_position = start

    collectibles = [tuple(collectible) for collectible in collectibles] # Ensure collectibles are tuples

    while len(collectibles) > 0:
        closest_collectible, closest_path = find_closest_collectible(maze, current_position, collectibles, start_time)  # Find closest collectible
        if closest_path:
            path += closest_path if not path else closest_path[1:]  # Exclude the starting point of each segment after the first to avoid duplicate positions
            current_position = closest_collectible
            collectibles.remove(closest_collectible)
        else:
            break  # Break the loop if no path to a collectible is found
  
    if current_position != end: # If current position is not the end, find path from current position to end
        final_path = astar(maze, current_position, end, start_time)
        if final_path:
            path += final_path[1:]  # Exclude the starting point of the final segment to avoid duplicate positions
    elapsed_time = time.time() - start_time  # Calculate elapsed time
    print(f"A* found path in {elapsed_time:.5f} seconds.")
    return path

def find_closest_collectible(maze, start, collectibles, start_time):    # Find the closest collectible to the start position
    closest_collectible = None
    closest_path = []
    shortest_distance = float('inf')    # Initialize shortest distance to infinity

    for collectible in collectibles:
        path = astar(maze, start, collectible, start_time, shortest_distance)
        if path:
            if len(path) < shortest_distance:
                closest_collectible = collectible
                closest_path = path
                shortest_distance = len(path)
        else:
            print("No path found to collectible", collectible)

    if closest_collectible is None:
        print("No closest collectible found. This could be due to maze configuration or collectibles' positioning.")
    
    return closest_collectible, closest_path

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def dijkstra_path(maze, start, targets, start_time):    # Dijkstra algorithm to find path from start to any target  
    start_node = Node(None, start)
    start_node.g = 0

    open_list = []  # For nodes to be evaluated
    heapq.heappush(open_list, (0, start_node))  # Add the start node to the open list

    visited = set() # Nodes already evaluated

    while open_list:    # Loop until you find the target
        current_g, current_node = heapq.heappop(open_list)  # Get the current node

        if current_node.position in targets:
            path = []
            target_position = current_node.position
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return target_position, path[::-1]  # Return both the target position and the path

        visited.add(current_node.position)  # Add the current node to the visited set

        for direction in [(0, -1), (0, 1), (-1, 0), (1, 0)]:    # Generate children
            if time.time() - start_time > 5:  # Limit search time to 5 second
                print("Dijkstra time limit exceeded, try A* instead.")
                return None, []  # Return None for the target position and an empty list for the path if time limit is exceeded
            neighbor_pos = (current_node.position[0] + direction[0], current_node.position[1] + direction[1])
            if 0 <= neighbor_pos[0] < len(maze) and 0 <= neighbor_pos[1] < len(maze[0]) and maze[neighbor_pos[0]][neighbor_pos[1]] in [0, 3, 4, 5, 6, 7] and neighbor_pos not in visited:   # Make sure within range and walkable terrain
                neighbor_node = Node(current_node, neighbor_pos)
                neighbor_g = current_g + 1
                heapq.heappush(open_list, (neighbor_g, neighbor_node))

    return None, []  # Return None for the target position and an empty list for the path if no path was found

def dijkstra(maze, start, collectibles, end):   # Dijkstra algorithm to find path to collectibles and end
    start_time = time.time()  # Start timing
    path = []
    current_position = start
    targets = set(collectibles + [end])  # Use a set for efficient look-up

    while targets:  # Loop until all targets are found
        target_position, shortest_path = dijkstra_path(maze, current_position, targets, start_time) # Find the shortest path to any target
        if shortest_path:
            path += shortest_path if not path else shortest_path[1:]    # Exclude the starting point of each segment after the first to avoid duplicate positions
            current_position = target_position
            targets.discard(target_position)  # Remove the found target
        else:
            print("Could not find path to any remaining target.")
            break
    elapsed_time = time.time() - start_time  # Calculate elapsed time
    print(f"Dijkstra found path in {elapsed_time:.5f} seconds.")
    return path