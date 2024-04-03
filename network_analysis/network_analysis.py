'''
Network analysis module:
The first side of the project which builds a networkx Directed graph
representing the digital circuit in hand.

Steps of the code:
 1. reads the verilog netlist and modifies it to be compatible with the
verilog_parser package.
 2. Extracting unique internal nodes to build the nodes from them by:
   1-Getting all nets in the design (including inputs and outputs) and
     storing them in "nets" list.
   2-Extracting the internal connections only (i.e. exclude inputs and outputs)
 3. Building the graph from the extracted connections in the circuit.
'''

from verilog_parser.parser import parse_verilog
import re
import os
import networkx as nx
import matplotlib.pyplot as plt


def modify_file(file_path: str):
    '''
    Manipulates the verilog file to work with the verilog_parser package
    and returns the netlist as a class of classes.

    Args:
        file_path (str): the path to the verilog netlist file to be
        represented.

    Returns:
        ast: the class of classes used for parsing all info needed for graph.

    '''

    with open(file_path, "r") as file:
        content = file.read()

    # Remove backslashes before port names
    content = content.replace("\\", "")

    # Replace . with ___ between two identifiers
    content = re.sub(r"(?<=\w)\.(?=\w)", "___", content)

    # Replace wire datatype with modified wire names
    content = re.sub(r"\bwire\s+(\w+)\[(\d+)\]", r"wire \1__\2", content)

    # Write the modified content to a new file and read it
    with open("modified_file.v", "w") as file:
        file.write(content)
    ast = parse_verilog(open("modified_file.v").read())
    os.remove("./modified_file.v")
    return ast


def extract_internal_nets(ast) -> list:
    '''
    Extracts all internal nodes from the verilog netlist and returns them as a
    list of the connections making these nets.

    Args:
        ast (ast): the class of classes used for parsing all info needed for
        graph.

    Returns:
        internal_connections: a list of all internal nodes in the circuit.

    '''

    # 1-Getting all nets in the design (including inputs and outputs) and
    # storing them in "nets" list.
    # 2-Extracting the internal connections (i.e. exclude inputs and outputs)
    nets = [declaration.net_name for declaration in
            ast.modules[0].net_declarations]
    internal_nodes = set(nets) - set(ast.modules[0].port_list)

    # Mapping ports to instance names for efficient connection search
    port_to_instance = {}
    for instance in ast.modules[0].module_instances:
        for port, node in instance.ports.items():
            port_to_instance.setdefault(node, []).append(
                (instance.instance_name, instance.module_name)
            )

    # Making internal connections for the graph
    internal_connections = []
    for k in internal_nodes:
        connections = port_to_instance.get(k, [])
        for i, (conn1, module1) in enumerate(connections):
            for conn2, module2 in connections[i + 1:]:
                internal_connections.append([conn1, module1, conn2, module2])

    return internal_connections


def build_graph(internal_connections: list) -> nx.DiGraph:
    '''
    Builds the networkx graph from the extracted internal connections
    and draws the graph of the netlist.

    Args:
        internal_connections (list): a list of all internal nodes in the
        circuit.

    Returns:
        g: the networkx graph representing the circuit.

    '''

    # 3. Third code section: Building the DiGraph
    g = nx.DiGraph()
    for conn1, module1, conn2, module2 in internal_connections:
        g.add_node(conn1, cell=module1)
        g.add_node(conn2, cell=module2)
        g.add_edge(conn1, conn2)

    # Drawing the graph for illustrtion only
    pos = nx.spring_layout(g)
    node_cells = nx.get_node_attributes(g, "cell")
    nx.draw(g, pos, node_color="lightblue", node_size=800, font_size=10)
    for node, (x, y) in pos.items():
        plt.text(x, y, f"{node}, {node_cells[node]}", fontsize=9, ha="center"
                 , va="center")
    plt.show()
    return g
