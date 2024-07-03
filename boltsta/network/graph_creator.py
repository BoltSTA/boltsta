import networkx as nx
import matplotlib.pyplot as plt
from ..readers.verilog_reader import (
    preprocess_verilog, parse_modified_verilog, extract_input_output_ports,
    extract_input_output_pins_of_cells, modify_input_pins,
    extract_mod_input_pins, extract_unique_internal_nodes, find_partial_match
)


# * 1 MAIN FUNCTION HERE!!
def build_digraph(
        ast, internal_connections, input_list, output_list, port_to_node_to_instance,
        mod_input_pins):
    """
    The core function that builds the graph representing the netlist.
    It uses the internal connections to build the graph and the information
    in the internal_connections list to build the nodes and edges.

    Args:
        ast (ast): the netlist handler
        internal_connections (list): list containing unique
        internal connections, the module (cell) name
        and the name of the pin making the connection
        (e.g. this a connection between two gates
        with X from OR output and
        A from AND to OR input: _1_, AND, _2_, OR, X_A)
        input_list (list): list containing inputs of the design.
        output_list (list): list containing outputs of the design.
        port_to_node_to_instance (dict): mapping ports to
        instance names for efficient connection search

    Returns:
        g1 (nx.DiGraph): the graph representing the netlist.
        pos (dict): the positions of the nodes in the graph.
        node_cells (dict): the cells of the nodes in the graph.
        edge_labels (dict): the labels of the edges in the graph.
    """
    g1 = nx.DiGraph()
    inputs = find_partial_match(port_to_node_to_instance.keys(), input_list)
    outputs = find_partial_match(port_to_node_to_instance.keys(), output_list)
    for port in inputs:
        instance_info = port_to_node_to_instance.get(port, None)
        if instance_info:
            for inst in instance_info:
                instance_name, module_name, in_pin = inst
                g1.add_node(instance_name, cell=module_name)
                g1.add_node(port, cell="Input")
                g1.add_edge(port, instance_name, input_pin=in_pin)
        else:
            g1.add_node(port, cell="Input")
    for port in outputs:
        instance_info = port_to_node_to_instance.get(port, None)
        if instance_info:
            for inst in instance_info:
                instance_name, module_name, out_pin = inst
                g1.add_node(instance_name, cell=module_name)
                g1.add_node(port, cell="Output")
                if (out_pin in mod_input_pins):
                    g1.add_edge(port, instance_name, input_pin=out_pin)
                else:
                    g1.add_edge(instance_name, port)
        else:
            g1.add_node(port, cell="Output")
    for conn1, module1, conn2, module2, in_pin in internal_connections:
        g1.add_node(conn1, cell=module1)
        g1.add_node(conn2, cell=module2)
        g1.add_edge(conn1, conn2, input_pin=in_pin)

    pos = nx.spring_layout(g1)
    node_cells = nx.get_node_attributes(g1, "cell")
    edge_labels = nx.get_edge_attributes(g1, 'input_pin')

    return g1, pos, node_cells, edge_labels


# 2
def draw_graph(g1, pos, node_cells, edge_labels):
    """
    A utility function that draws the graph if visualization needed.

    Args:
        g1 (nx.DiGraph): the graph representing the netlist.
        pos (dict): the positions of the nodes in the graph.
        node_cells (dict): the cells of the nodes in the graph.
        edge_labels (dict): the labels of the edges in the graph.
    """
    nx.draw(g1, pos, node_color="lightblue", node_size=800, font_size=10)
    nx.draw_networkx_edge_labels(g1, pos, edge_labels=edge_labels)
    for node, (x, y) in pos.items():
        plt.text(
            x, y, f"{node}, {node_cells[node]}", fontsize=9, ha="center",
            va="center"
        )
    plt.show()


# 3
def print_node_predecessors_successors(g1):
    """
    A utility function that prints the predecessors and successors of each
    node.

    Args:
        g1 (nx.DiGraph): the graph
    """
    for node in g1.nodes():
        # List all of the predecessors and successors of the current node
        pres = list(g1.predecessors(node))
        sucs = list(g1.successors(node))
        # Print the current node
        print(f'current node = {node} : {g1.nodes[node]}')

        # Iterating over the predecessors of the current node and adjusting
        # their weight
        for pre in pres:
            if pre != []:
                # printing the cell names of predecessor and current
                print(f'{pre} , {g1.nodes[pre]} --> {node} , {g1.nodes[node]}')
                # printing edge value
                pre_conn_input_pin = g1.get_edge_data(pre, node)
                print(f'previous edge input_pin = {pre_conn_input_pin} \n')

        # Iterating over the successors of the current node and adjusting their
        # weight
        for suc in sucs:
            if suc != []:
                # printing the cell names of current and successor
                print(f'{node} , {g1.nodes[node]} --> {suc} , {g1.nodes[suc]}')
                # printing edge value
                suc_conn_input_pin = g1.get_edge_data(node, suc)
                print(f'successor edge attr = {suc_conn_input_pin} \n')


# 4
def graph_creation_func(file_path):
    """
    Takes the Verilog netlist file path, preprocesses it, parses the
    modified Verilog, extracts input and output ports, input and output pins
    of cells, and internal nets. Modifies input pins in the abstract syntax
    tree (AST), extracts modified input pins, extracts unique internal nodes
    and their connections, builds a directed graph (digraph) representing
    internal connections of basic gates/components (AND, OR, Full adder).

    Args:
    - file_path1 (str): Path to the Verilog netlist file.

    Returns:
    - input_list (list): List of input ports.
    - output_list (list): List of output ports.
    - g1 (networkx.DiGraph): Directed graph representing internal connections of the design.
    """
    modified_file = preprocess_verilog(file_path)
    ast = parse_modified_verilog(modified_file)

    input_list, output_list = extract_input_output_ports(ast)

    # Deleted design internal nets function and merged it with
    # this function
    input_pins, output_pins, nets = extract_input_output_pins_of_cells(ast)

    ast = modify_input_pins(ast, input_pins, output_pins)
    mod_input_pins, port_to_node_to_instance = extract_mod_input_pins(ast)

    internal_connections = extract_unique_internal_nodes(
        ast, mod_input_pins, port_to_node_to_instance
    )

    G, pos, node_cells, edge_labels = build_digraph(ast, internal_connections,
                                                    input_list, output_list,
                                                    port_to_node_to_instance,
                                                    mod_input_pins)
    # discuss if the input, output lists are even needed
    return G
