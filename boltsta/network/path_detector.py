from collections import deque
from .graph_creator import graph_creation_func
from .fanout import get_fanout_dict
import networkx as nx


# 1
def create_adjacency_dict(G, cell_attr_name):
    """
    Creates an adjacency dictionary for path detection in a graph.

    The keys of the dictionary are all the nodes in the graph,
    and the values are lists of the very next nodes connected to the key node
    (the next level directly).
    Each node and its neighbors are represented in the format 'node,cell_attr_value'.

    Parameters:
    G (networkx.Graph): The graph representing the design.
    cell_attr_name (str): The name of the attribute to be concatenated with the node name.

    Returns:
    dict: An adjacency dictionary with nodes and their direct neighbors.
    """
    adjacency_dict = {}
    for node in G.nodes():
        node_attrs = G.nodes[node]
        node_info = f"{node},{node_attrs[cell_attr_name]}"
        adjacency_dict[node_info] = [
            f"{neighbor},{G.nodes[neighbor][cell_attr_name]}" for neighbor in G.neighbors(node)
        ]
    return adjacency_dict

# Helper functions for find_all_paths_non_rec_pro


def set_targets(targets_file_name, mode, output_ports=None):
    """
    Sets the targets based on the specified mode.

    Args:
        targets_file_name (str): The filename containing all possible substrings
        that may be in the targets.
        mode (str): The mode of operation ('IR', 'RR', 'RO').
        output_ports (list, optional): List of output ports (only required if mode is 'RO').

    Returns:
        list: A list of target strings.
    """
    targets = []
    if mode == 'RR' or mode == 'IR':
        with open(targets_file_name, "r") as f:
            for line in f:
                line = line.strip()  # Remove whitespaces, new line characters
                targets.append(line)
        targets = list(set(targets))
    elif mode == 'RO':
        if output_ports is None:
            raise ValueError("Output ports must be provided for mode 'RO'.")
        targets = output_ports
    else:
        raise ValueError("Invalid mode. Supported modes are 'IR', 'RR', 'RO'.")

    return targets


def set_source_nodes(adjacency_dict, mode, targets, input_ports=None, targets_file_name=None):
    """
    Sets the source nodes based on the specified mode and targets.

    Args:
        adjacency_dict (dict): Dictionary representing adjacency information.
        mode (str): Mode of operation ('RR', 'RO', 'IR').
        targets (list): List of target nodes or patterns.
        input_ports (list, optional): List of input ports (for 'IR' mode).
        targets_file_name (str, optional): File containing target patterns (for 'RO' mode).

    Returns:
        list: List of source nodes based on the mode.
    """
    source_nodes = []

    if mode == 'RR':
        source_nodes = [
            node for node in adjacency_dict.keys() if any(target in node for target in targets)
        ]
    elif mode == 'RO':
        regs = []
        with open(targets_file_name, "r") as f:
            for line in f:
                line = line.strip()  # Remove whitespaces, new line characters
                regs.append(line)
        regs = list(set(regs))
        source_nodes = [
            node for node in adjacency_dict.keys()
            if any(target in node for target in regs) and len(adjacency_dict[node]) < 3
        ]
    elif mode == 'IR':
        source_nodes = input_ports
    else:
        raise ValueError("Invalid mode. Supported modes are 'IR', 'RR', 'RO'.")

    return source_nodes


def find_paths_BFS(adjacency_dict, source_nodes, targets, show_steps=False):
    """
    Finds all paths from source nodes to targets in a network.

    Args:
        adjacency_dict (dict): Dictionary representing adjacency information.
        source_nodes (list): List of source nodes to start path finding.
        targets (list): List of target strings to search for in paths.
        show_steps (bool, optional): If True, prints all the steps values. Defaults to False.

    Returns:
        list: A list of lists containing all the possible paths found.
    """
    all_paths = []  # List to store all found paths

    # Iterate over each source node identified based on the mode
    for source in source_nodes:
        visited_paths = set()  # Set to track visited paths to avoid cycles
        queue = deque([(source, [source])])
        # Initialize queue with the current source node and its path

        # Breadth-First Search (BFS) loop to explore paths
        while queue:
            node, path = queue.popleft()  # Dequeue the current node and its path
            visited_paths.add(tuple(path))  # Add the current path to visited_paths

            neighbors = adjacency_dict[node]  # Get neighbors of the current node

            # Iterate over each neighbor of the current node
            for neighbor in neighbors:
                # Check if the neighbor contains any of the targets
                if any(target in neighbor for target in targets):
                    if tuple(path + [neighbor]) not in visited_paths:
                        all_paths.append(path + [neighbor])
                        # Append the complete path to all_paths
                # Check if the neighbor is not already in the current path (to avoid cycles)
                elif neighbor not in path:
                    new_path = path + [neighbor]  # Create a new path by appending the neighbor
                    if tuple(new_path) not in visited_paths:
                        queue.append((neighbor, new_path))
                        # Enqueue the neighbor with its new path
                        visited_paths.add(tuple(new_path))  # Mark the new path as visited

    if show_steps:
        print(f'total number of paths: {len(all_paths)}')  # Print total number of paths found

    return all_paths  # Return the list of all found paths


def find_all_paths_non_rec_pro(adjacency_dict,
                               targets_file_name: str,
                               mode: str = 'RR',
                               show_steps: int = False):
    """
    Finds all paths from source nodes to targets in a networkx graph based on the specified mode.

    Args:
        adjacency_dict (dict): Dictionary containing node information and its neighbors.
        targets_file_name (str):
        The filename containing all possible substrings that may be in the targets.
        mode (str, optional): The mode of operation ('IR', 'RR', 'RO'). Defaults to 'RR'.
        show_steps (int, optional): If True, prints all the steps values. Defaults to False.

    Returns:
        list: A list of lists containing all the possible paths.
    """

    if show_steps:
        print(f'step1 adj_dict = {adjacency_dict}\n')
        print(f'adj_dict_keys -> {adjacency_dict.keys()}')

    # initialize input, ouptut ports
    input_ports = None
    output_ports = None
    # Mode setup for 'IR' and 'RO'
    if mode != 'RR':
        adjacency_dict_keys = adjacency_dict.keys()
        if mode == 'IR':
            input_ports = [key for key in adjacency_dict_keys if 'Input' in key]
        elif mode == 'RO':
            output_ports = [key for key in adjacency_dict_keys if 'Output' in key]

    # setting target nodes
    targets = []
    targets = set_targets(targets_file_name, mode, output_ports)
    if show_steps:
        print(f'step2 targets = {targets}\n')

    # setting the source nodes:
    source_nodes = []
    source_nodes = set_source_nodes(adjacency_dict, mode, targets, input_ports, targets_file_name)
    if show_steps:
        print(f'step3 source nodes = {source_nodes}\n with count of: {len(source_nodes)}')

    # main function in here
    all_paths = []
    all_paths = find_paths_BFS(adjacency_dict, source_nodes, targets, show_steps)

    return all_paths  # Return the list of all found paths


# 3
# function that creates a list of lists holding the "input_pins" attribute for each path
def get_input_attr(G, paths):
    """
    get_input_attr function takes all the predetermined paths in the graph,
    detects the edges of each path, and retrieves the 'input_pin' attribute 
    for each edge in the paths.

    arguments:
    paths: list of paths, where each path is a list of node pairs in string format (e.g., "A,B")

    output:
    all_attr_list: list of lists holding the 'input_pin' attribute for each edge in the paths
    """
        # getting the edges first, in order to get the input attr later
    def get_path_edges(all_paths):
        """
        get_path_edges function takes all the predetermined paths in the graph,
        then detects the edges of each path.

        arguments:
        all_paths: all the paths extracted from the graph

        output: list of lists containing tuples representing the edges for each path
        """
        path_pairs = []

        for path in all_paths:
            pairs = [(path[j].split(',')[0], path[j+1].split(',')[0]) for j in range(len(path)-1)]
            path_pairs.append(pairs)

        return path_pairs
        # inline function
    get_attr_list = lambda G, edge_list, attr: [G[edge[0]][edge[1]].get(attr, None) for edge in edge_list]

    paths_edges = get_path_edges(paths)
    all_attr_list = []
    for path in paths_edges:
        attr_list = get_attr_list(G, path, 'input_pin')
        all_attr_list.append(attr_list)
    return all_attr_list


# 4 main function
def all_paths_info(G):
    """
    Extracts and returns all types of paths (reg-reg, in-reg, and reg-out)
    and their attributes from the graph.

    This function identifies and extracts different types of paths in the given
    graph G. It finds reg-reg, in-reg, and reg-out paths and retrieves their
    attributes. The function relies on helper functions `find_all_paths_non_rec_pro`
    and `get_input_attr` to accomplish these tasks.

    The adjacency dictionary used in this function is structured as follows:
    - The keys are all the nodes in the graph, in the format 'node,cell_type'.
    - The values are lists of the very next nodes connected to the key node
      (the next level directly),
      each in the format 'node,cell_type'.

    Parameters:
    G : networkx.Graph
        The input graph from which paths are to be extracted.

    Returns:
    tuple:
        reg_reg : list
            List of reg-reg paths.
        rr_attr_list : list
            List of attributes for reg-reg paths.
        in_reg : list
            List of in-reg paths.
        ir_attr_list : list
            List of attributes for in-reg paths.
        reg_out : list
            List of reg-out paths.
        ro_attr_list : list
            List of attributes for reg-out paths.
        adjacency_dict : dict
            The adjacency dictionary with nodes and their direct neighbors.
    """
    targets_file_name = 'ff_names.txt'
    adjacency_dict = create_adjacency_dict(G, 'cell')
    reg_reg = find_all_paths_non_rec_pro(adjacency_dict, targets_file_name, 'RR')
    in_reg = find_all_paths_non_rec_pro(adjacency_dict, targets_file_name, 'IR')
    reg_out = find_all_paths_non_rec_pro(adjacency_dict, targets_file_name, 'RO')

    rr_attr_list = get_input_attr(G, reg_reg)
    ir_attr_list = get_input_attr(G, in_reg)
    ro_attr_list = get_input_attr(G, reg_out)

    return reg_reg, rr_attr_list, in_reg, ir_attr_list, reg_out, ro_attr_list, adjacency_dict


# 5
def graph_path_handler(file_path: str):
    """
    COMBO function combines the graph creation and path detection processes.

    This function reads a file to create a graph, extracts all types of paths
    and their attributes using the provided functions from `graph_creation`
    and `path_detection` modules, and returns the extracted information.

    Arguments:
    file_path: str - The path to the input file used for creating the graph.

    Returns:
    tuple:
        rr - List of reg-reg paths
        rr_atr_list - List of attributes for reg-reg paths
        ir - List of in-reg paths
        ir_atr_list - List of attributes for in-reg paths
        ro - List of reg-out paths
        ro_atr_list - List of attributes for reg-out paths
    """
    G = graph_creation_func(file_path)
    rr, rr_atr_list, ir, ir_atr_list, ro, ro_atr_list, adjacency_dict = all_paths_info(G)
    fanout_dict = get_fanout_dict(G, adjacency_dict)

    return rr, rr_atr_list, ir, ir_atr_list, ro, ro_atr_list, fanout_dict