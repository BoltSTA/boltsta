import re
import os
import numpy as np
from verilog_parser.parser import parse_verilog

# 1
def preprocess_verilog(file_path):
    """
    Preprocesses the verilog netlist file to make it compatible
    with the external imported parser, by removing backslashes
    before port names, replacing . with ___ between two identifiers,
    and replacing wire datatype with modified wire names.

    Args:
        file_path (str): Path to the netlist.v file.

    Returns:
        content (str): Preprocessed verilog file content.

    """
    with open(file_path, "r") as file:
        content = file.read()

    # Remove backslashes before port names
    content = content.replace("\\", "")

    # Replace . with ___ between two identifiers
    content = re.sub(r"(?<=\w)\.(?=\w)", "___", content)
    content = re.sub(r"(\w+)\[(\d+)\]\.(\w+)", r"\1__\2___\3", content)

    # Replace wire datatype with modified wire names
    content = re.sub(r"(\w+)\[(\d+)\]", r"\1__\2", content)

    return content


# 2
def parse_modified_verilog(content):
    """
    Writes the modified contents of the netlist into a new
    .v file. Then parses this file using the imported parser
    and returns the handler (ast) of the modified verilog
    file.

    Args:
        content (str): Preprocessed verilog file content.

    Returns:
        ast (ast): The netlist handler (ast) of the modified verilog
        file.
    """
    with open("modified_file.v", "w") as file:
        file.write(content)
    ast = parse_verilog(open("modified_file.v").read())
    os.remove("./modified_file.v")
    return ast


# 3
def extract_input_output_ports(ast):
    """
    Extracts the input and output ports of the design

    Args:
        ast (ast): the netlist handler

    Returns:
        input_list (list): list containing inputs
        output_list (list): list containing outputs
    """
    input_list = []
    output_list = []
    for i in ast.modules[0].input_declarations:
        input_list.append(i.net_name)

    for o in ast.modules[0].output_declarations:
        output_list.append(o.net_name)

    return input_list, output_list


# 4
def extract_input_output_pins_of_cells(ast):
    """
    Extracts the input and output pins of the design
    cells, they are to be used in STA calculation.

    Args:
        ast (ast): the netlist handler

    Returns:
        input_pins (list): list containing cells' input
        pins.
        output_pins (list): list containing cells' output
        pins.
    """
    input_pins = []
    output_pins = []
    for inst in ast.modules[0].module_instances:
        a = list(inst.ports.keys())
        output_pins.append(a[-1])
        for i in np.arange(len(a) - 1):
            input_pins.append(a[i])
            a[i] = a[-1] + "_" + a[i]
    input_pins = list(set(input_pins))
    output_pins = list(set(output_pins))

    # Adding an exception for registers' output 'Q' and input 'RESET_B'
    # as they are swapped in the netlist (i.e. 'RESET_B' is the last pin)
    if "Q" in input_pins:
        input_pins.remove("Q")
    input_pins.append("RESET_B")
    if "RESET_B" in output_pins:
        output_pins.remove("RESET_B")
    output_pins.append("Q")

    return input_pins, output_pins


# 5
def extract_design_internal_nets(ast):
    """
    Extracts the design internal nets (nodes).

    Args:
        ast (ast): the netlist handler

    Returns:
        nets (list): list containing design internal nets.
    """
    nets = []
    for instance in ast.modules[0].module_instances:
        for port, node in instance.ports.items():
            nets.append(str(node))
    return nets


# 6
def modify_input_pins(ast, input_pins, output_pins):
    """
    Modifies the input pins of the design cells (A -> X_A).
    This modification is made to facilitate the STA calculation
    and to pass the modified graph to the STA function.

    Args:
        ast (ast): the netlist handler
        input_pins (list): list containing cells' input
        output_pins (list): list containing cells' output

    Returns:
        ast (ast): the netlist handler with modified input pins.
    """
    module = ast.modules[0]
    for instance in module.module_instances:
        connections = instance.ports
        modified_connections = {}
        output_pin = list(connections.keys())[-1]
        if output_pin == "RESET_B":
            output_pin = "Q"
        for key in connections:
            if key in input_pins:
                if output_pin in output_pins:
                    prefix = output_pin + "_"
                else:
                    prefix = key[-1] + "_"
                modified_connections[prefix + key] = connections[key]
            else:
                modified_connections[key] = connections[key]
        instance.ports = modified_connections
    return ast


# 7
def extract_mod_input_pins(ast):
    """
    Extracts the modified input pins of the design cells.
    This is done again to remove the output 'Q' from these
    modified inputs and deal with the correct version of
    the cells' input pins.

    Args:
        ast (ast): the netlist handler

    Returns:
        mod_input_pins (list): list containing cells' modified
        input pins.
    """
    mod_input_pins = []
    for inst in ast.modules[0].module_instances:
        a = list(inst.ports.keys())
        for i in np.arange(len(a) - 1):
            mod_input_pins.append(a[i])
            a[i] = a[-1] + "_" + a[i]
    mod_input_pins = list(set(mod_input_pins))
    if "Q" in mod_input_pins:
        mod_input_pins.remove("Q")
    return mod_input_pins


# 8
def extract_unique_internal_nodes(ast, mod_input_pins):
    """
    Extracts the unique internal connections of the
    verilog design. These connections are to be used to build
    the graph representing the verilog design. Also builds an
    important dict (port_to_node_to_instance) which binds ports
    to the design cells to make searching for nodes
    efficient.

    Args:
        ast (ast): the netlist handler
        mod_input_pins (list): list containing cells' modified
        input pins.

    Returns:
        internal_connections (list): list containing unique
        internal connections, the module (cell) name
        and the name of the pin making the connection
        (e.g. this a connection between two gates
        with X from OR output and
        A from AND to OR input: _1_, AND, _2_, OR, X_A)
        port_to_node_to_instance (dict): mapping ports to
        instance names for efficient connection search
    """
    all_signals = [
        declaration.net_name for declaration in ast.modules[0].net_declarations
    ]
    internal_nodes = set(all_signals) - set(ast.modules[0].port_list)

    port_to_node_to_instance = {}
    for instance in ast.modules[0].module_instances:
        for port, node in instance.ports.items():
            port_to_node_to_instance.setdefault(str(node), []).append(
                (instance.instance_name, instance.module_name, port)
            )

    internal_connections = []
    for k in internal_nodes:
        connections = port_to_node_to_instance.get(k, [])
        for i, (conn1, module1, port1) in enumerate(connections):
            for conn2, module2, port2 in connections[i + 1:]:
                if port1 in mod_input_pins and port2 in mod_input_pins:
                    continue
                if port2 == "Q":
                    internal_connections.append([conn2, module2, conn1,
                                                 module1, port1])
                else:
                    internal_connections.append([conn1, module1, conn2,
                                                 module2, port2])
    return internal_connections, port_to_node_to_instance


# 9
def find_partial_match(nets, input_list):
    """
    A utility function used to find partial matches
    between two given lists and returns a new list
    with the matching elements.

    Args:
        nets (list): list containing design internal nets.
        input_list (list): list containing inputs of the design.

    Returns:
        output (list): list containing elements present in both lists.
    """
    pattern = "|".join(
        r"\b{}(?:__[0-9]+)?\b".format(re.escape(item)) for item in input_list
    )
    regex = re.compile(pattern)
    output = set(regex.findall(" ".join(nets)))
    return output
