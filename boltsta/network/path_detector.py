from collections import deque
from .graph_creator import graph_creation_func
import networkx as nx


#1
def find_all_paths_non_rec_pro(G, cell_attr_name: str, targets_file_name: str,mode: str = 'RR', show_steps: int = False):
    """
    Finds all paths from source nodes to targets in a networkx graph based on the specified mode.

    Args:
        G (networkx.Graph): The networkx graph.
        cell_attr_name (str): The name of the node attribute showing the cell type.
        targets_file_name (str): The filename containing all possible substrings that may be in the targets.
        mode (str, optional): The mode of operation ('IR', 'RR', 'RO'). Defaults to 'RR'.
        IR -> in-reg, RO -> reg-out, RR -> reg-reg
        show_steps (int, optional): If True, prints all the steps values. Defaults to False.

    Returns:
        list: A list of lists containing all the possible paths.
    """

    adjacency_dict = {}
    # Filling adjacency dictionary with node names concatenated with attribute values
    for node in G.nodes():
        node_attrs = G.nodes[node]
        node_info = f"{node},{node_attrs[cell_attr_name]}"
        adjacency_dict[node_info] = [
            f"{neighbor},{G.nodes[neighbor][cell_attr_name]}" for neighbor in G.neighbors(node)
        ]

    if show_steps:
        print(f'step1 adj_dict = {adjacency_dict}\n')
        print(f'adj_dict_keys -> {adjacency_dict.keys()}')

    # MODE SETUP (IR, RO)
    filter_keys_with_input = lambda keys: [key for key in keys if 'Input' in key]
    filter_keys_with_output = lambda keys: [key for key in keys if 'Output' in key]
    if mode != 'RR':
        adjacency_dict_keys = adjacency_dict.keys()
        if mode == 'IR':
            input_ports = filter_keys_with_input(adjacency_dict_keys)
        if mode == 'RO':
            output_ports = filter_keys_with_output(adjacency_dict_keys)
    
    # Set the Targets
    targets = []
    if mode == 'RR' or mode == 'IR':
        with open(targets_file_name, "r") as f:
            for line in f:
                line = line.strip()  # Remove leading and trailing whitespaces, new line characters
                targets.append(line)
        targets = list(set(targets))
    elif mode == 'RO':
        targets = output_ports
    else:
        raise ValueError("Invalid mode. Supported modes are 'IR', 'RR', 'RO'.")

    if show_steps:
        print(f'step2 targets = {targets}\n')

    # Set the source nodes
    source_nodes = []
    if mode == 'RR':
        source_nodes = [
            node for node in adjacency_dict.keys() if any(target in node for target in targets)
        ]
    elif mode == 'RO':
        regs = []
        with open(targets_file_name, "r") as f:
            for line in f:
                line = line.strip()  # Remove leading and trailing whitespaces, new line characters
                regs.append(line)
        regs = list(set(regs))
        source_nodes = [
            node for node in adjacency_dict.keys() #! check for a better cond than 3!!
            if any(target in node for target in regs) and len(adjacency_dict[node]) < 3
        ]

    elif mode == 'IR':
        source_nodes = input_ports
    else:
        raise ValueError("Invalid mode. Supported modes are 'IR', 'RR', 'RO'.")

    if show_steps:
        print(f'step3 source nodes = {source_nodes}\n with count of: {len(source_nodes)}')

    # Main function body
    all_paths = []

    for source in source_nodes:
        visited_paths = set()  # Track visited paths
        queue = deque([(source, [source])])

        while queue:
            node, path = queue.popleft()
            visited_paths.add(tuple(path))  # Add current path to visited_paths
            neighbors = adjacency_dict[node]

            for neighbor in neighbors:
                if any(target in neighbor for target in targets):
                    if tuple(path + [neighbor]) not in visited_paths:
                        all_paths.append(path + [neighbor])
                elif neighbor not in path:
                    new_path = path + [neighbor]
                    if tuple(new_path) not in visited_paths:
                        queue.append((neighbor, new_path)) 
                        visited_paths.add(tuple(new_path))  # Mark new path as visited

    print(f'total number of paths: {len(all_paths)}')
    return all_paths

# 2
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



#3 main function 
def all_paths_info(G):
    """
    Extracts and returns all types of paths (reg-reg, in-reg, and reg-out) 
    and their attributes from the graph.

    This function identifies and extracts different types of paths in the given 
    graph G. It finds reg-reg, in-reg, and reg-out paths and retrieves their 
    attributes. The function relies on helper functions `find_all_paths_non_rec_pro` 
    and `get_input_attr` to accomplish these tasks.

    Arguments:
    G : NetworkX graph
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
    """
    targets_file_name = 'ff_names.txt'
    reg_reg = find_all_paths_non_rec_pro(G, 'cell', targets_file_name, 'RR')
    in_reg = find_all_paths_non_rec_pro(G, 'cell', targets_file_name, 'IR')
    reg_out = find_all_paths_non_rec_pro(G, 'cell', targets_file_name, 'RO')

    rr_attr_list = get_input_attr(G, reg_reg)
    ir_attr_list = get_input_attr(G, in_reg)
    ro_attr_list = get_input_attr(G, reg_out)

    return reg_reg, rr_attr_list, in_reg, ir_attr_list, reg_out, ro_attr_list


# 4
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
    rr, rr_atr_list, ir, ir_atr_list, ro, ro_atr_list = all_paths_info(G)

    return rr, rr_atr_list, ir, ir_atr_list, ro, ro_atr_list