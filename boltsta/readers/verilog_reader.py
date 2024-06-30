import re  # Regular expressions library for pattern matching and string manipulation
import os  # OS library for file handling operations
import numpy as np  # NumPy library for numerical operations and array handling
from verilog_parser.parser import parse_verilog  # Importing a Verilog parser from an external module

def preprocess_verilog(file_path):
    """
    Preprocesses the verilog netlist file to make it compatible
    with the external imported parser, by removing backslashes
    before port names, replacing '.' with '___' between two identifiers,
    and replacing wire datatype with modified wire names.

    Args:
        file_path (str): Path to the netlist.v file.

    Returns:
        str: Preprocessed verilog file content.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If there is an error reading the file.
    """
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")  # Raise an error if the file is not found

        # Try to open and read the file content
        with open(file_path, "r") as file:
            content = file.read()  # Read the content of the file
            if not isinstance(content, str) or not content:
                raise ValueError("The netlist must be a non-empty file.")  # Raise an error if file is not valid

        # Remove backslashes before port names
        content = content.replace("\\", "")  # Replace all backslashes with an empty string

        # Replace '.' between two identifiers with '___'
        content = re.sub(r"(?<=\w)\.(?=\w)", "___", content)  # Replace '.' between word characters with '___'

        # Replace identifier[index].identifier with identifier__index___identifier
        content = re.sub(r"(\w+)\[(\d+)\]\.(\w+)", r"\1__\2___\3", content)  # Handle array indices with dot notation

        # Replace identifier[index] with identifier__index
        content = re.sub(r"(\w+)\[(\d+)\]", r"\1__\2", content)  # Handle array indices without dot notation

        return content  # Return the preprocessed Verilog content

    except Exception as e:
        raise IOError(f"Error processing the file {file_path}: {e}")  # Raise an error if there is an issue processing the file

def parse_modified_verilog(content):
    """
    Writes the modified contents of the netlist into a new
    .v file. Then parses this file using the imported parser
    and returns the handler (AST) of the modified verilog file.

    Args:
        content (str): Preprocessed verilog file content.

    Returns:
        object: The AST of the modified verilog file.

    Raises:
        ValueError: If the content is not a non-empty string.
        IOError: If there is an error parsing the file.
    """
    try:
        # Check if content is a non-empty string
        if not isinstance(content, str) or not content:
            raise ValueError("The content must be a non-empty string.")  # Raise an error if content is not valid

        # Create and open a new file called "modified_file.v" in write mode
        with open("modified_file.v", "w") as file:
            # Write the modified content to this file
            file.write(content)  # Write the preprocessed content to a new file

        # Parse the content of the new file using the verilog parser
        ast = parse_verilog(open("modified_file.v").read())  # Parse the file to generate AST

        return ast  # Return the AST for further processing

    except Exception as e:
        raise IOError(f"Error parsing the modified Verilog content: {e}")  # Raise an error if parsing fails

    finally:
        # Ensure the temporary file is removed after parsing
        if os.path.exists("modified_file.v"):
            os.remove("modified_file.v")  # Clean up by removing the temporary file

def extract_input_output_ports(ast):
    """
    Extracts the input and output ports of the design.

    Args:
        ast (object): The netlist handler (AST).

    Returns:
        tuple: A tuple containing two lists - input_list and output_list.

    Raises:
        ValueError: If the AST structure is invalid.
    """
    try:
        # Check if AST is of expected structure
        if not hasattr(ast, 'modules') or not ast.modules:
            raise ValueError("Invalid Netlist structure.")  # Raise an error if the AST structure is not valid

        # Initialize empty lists to store input and output ports
        input_list = []  # List to hold input ports
        output_list = []  # List to hold output ports

        # Loop through input declarations in the AST and add them to input_list
        for i in ast.modules[0].input_declarations:
            input_list.append(i.net_name)  # Append each input port name to the list

        # Loop through output declarations in the AST and add them to output_list
        for o in ast.modules[0].output_declarations:
            output_list.append(o.net_name)  # Append each output port name to the list

        return input_list, output_list  # Return the input and output port lists

    except Exception as e:
        raise ValueError(f"Error extracting input and output ports: {e}")  # Raise an error if there is an issue extracting ports

def extract_input_output_pins_of_cells(ast):
    """
    Extracts the input and output pins of the design cells.
    These are to be used in STA calculation.

    Args:
        ast (object): The netlist handler (AST).

    Returns:
        tuple: A tuple containing two lists - input_pins and output_pins.

    Raises:
        ValueError: If the AST structure is invalid.
    """
    try:
        # Check if AST is of expected structure
        if not hasattr(ast, 'modules') or not ast.modules:
            raise ValueError("Invalid Netlist structure.")  # Raise an error if the AST structure is not valid

        # Initialize empty lists to store input and output pins
        input_pins = []  # List to hold input pins
        output_pins = []  # List to hold output pins

        # Loop through module instances in the AST
        for inst in ast.modules[0].module_instances:
            # Get a list of port names for the current instance
            a = list(inst.ports.keys())  # List of ports for the current instance
            # The last port in the list is considered an output pin
            output_pins.append(a[-1])  # Append the last port name as an output pin
            # Loop through all but the last port to consider them as input pins
            for i in np.arange(len(a) - 1):  # Loop through all ports except the last
                input_pins.append(a[i])  # Append the port name as an input pin
                # Modify the input pin name by adding the output pin as a prefix
                a[i] = a[-1] + "_" + a[i]  # Combine output pin name with input pin name

        # Remove duplicate pins by converting the lists to sets
        input_pins = list(set(input_pins))  # Remove duplicates from input pins list
        output_pins = list(set(output_pins))  # Remove duplicates from output pins list

        # Special handling for specific pins: 'Q' and 'RESET_B'
        if "Q" in input_pins:
            input_pins.remove("Q")  # Remove 'Q' from input pins if present
        input_pins.append("RESET_B")  # Ensure 'RESET_B' is in the input pins list
        if "RESET_B" in output_pins:
            output_pins.remove("RESET_B")  # Remove 'RESET_B' from output pins if present
        output_pins.append("Q")  # Ensure 'Q' is in the output pins list

        return input_pins, output_pins  # Return the input and output pin lists

    except Exception as e:
        raise ValueError(f"Error extracting input and output pins of cells: {e}")  # Raise an error if there is an issue extracting pins

def extract_design_internal_nets(ast):
    """
    Extracts the design internal nets (nodes).

    Args:
        ast (object): The netlist handler (AST).

    Returns:
        list: List containing design internal nets.

    Raises:
        ValueError: If the AST structure is invalid.
    """
    try:
        # Check if AST is of expected structure
        if not hasattr(ast, 'modules') or not ast.modules:
            raise ValueError("Invalid Netlist structure.")  # Raise an error if the AST structure is not valid

        # Initialize an empty list to store internal nets
        nets = []  # List to hold internal nets

        # Loop through module instances in the AST
        for instance in ast.modules[0].module_instances:
            # Loop through ports of the current instance and add them to nets list
            for port, node in instance.ports.items():
                nets.append(str(node))  # Append each port node to the nets list

        return nets  # Return the list of internal nets

    except Exception as e:
        raise ValueError(f"Error extracting design internal nets: {e}")  # Raise an error if there is an issue extracting nets

def modify_input_pins(ast, input_pins, output_pins):
    """
    Modifies the input pins of the design by 
    adding the corresponding output pin as a prefix.
    This modification is made to facilitate the STA calculation
    and to pass the modified graph to the STA function.
    
    Args:
        ast (ast): the netlist handler
        input_pins (list): List of input pins.
        output_pins (list): List of output pins.

    Returns:
        list: Modified input pins list.
    
    Raises:
        ValueError: If input_pins or output_pins is not a list.
    """
    try:
        if not hasattr(ast, 'modules') or not ast.modules:
            raise ValueError("Invalid Netlist structure.")  # Raise an error if the AST structure is not valid

        if not isinstance(input_pins, list) or not isinstance(output_pins, list):
            raise ValueError("input_pins and output_pins must be lists.")  # Raise an error if inputs are not valid lists
        
        # Access the first module in the AST
        module = ast.modules[0]

        # Iterate over each instance of a module (cell) in the design
        for instance in module.module_instances:
            # Get the current port connections of the instance
            connections = instance.ports
            modified_connections = {}

            # Determine the output pin of the instance
            output_pin = list(connections.keys())[-1]
            
            # Special case handling for "RESET_B" as it should not be used as the output pin
            if output_pin == "RESET_B":
                output_pin = "Q"

            # Iterate over each connection key (pin)
            for key in connections:
                if key in input_pins:
                    # If the key is an input pin, modify it with a prefix
                    if output_pin in output_pins:
                        prefix = output_pin + "_"
                    else:
                        prefix = key[-1] + "_"
                    modified_connections[prefix + key] = connections[key]
                else:
                    # If the key is not an input pin, keep it unchanged
                    modified_connections[key] = connections[key]

            # Update the ports of the instance with modified connections
            instance.ports = modified_connections

        # Return the modified AST
        return ast
    except Exception as e:
        raise Exception(f"Error in modify_input_pins: {e}")

def extract_mod_input_pins(ast):
    """
    Extracts the modified input pins of the design cells 
    by adding the corresponding output pin as a prefix.
    This is done again to remove the output 'Q' from these
    modified inputs and deal with the correct version of
    the cells' input pins.

    Args:
        ast (object): The netlist handler (AST).

    Returns:
        list: Modified input pins list.

    Raises:
        ValueError: If the AST structure is invalid.
    """
    try:
        # Check if AST is of expected structure
        if not hasattr(ast, 'modules') or not ast.modules:
            raise ValueError("Invalid Netlist structure.")  # Raise an error if the AST structure is not valid

        # Initialize an empty list to store modified input pins
        mod_input_pins = []  # List to hold modified input pins

        # Loop through module instances in the AST
        for inst in ast.modules[0].module_instances:
            # Get a list of port names for the current instance
            a = list(inst.ports.keys())  # List of ports for the current instance
            # Loop through all but the last port to consider them as input pins
            for i in np.arange(len(a) - 1):
                mod_input_pins.append(a[i])  # Append each port name to the list of modified input pins
                # Modify the input pin name by adding the output pin as a prefix
                a[i] = a[-1] + "_" + a[i]  # Combine output pin name with input pin name

        # Remove duplicate pins by converting the list to a set
        mod_input_pins = list(set(mod_input_pins))  # Remove duplicates from the modified input pins list

        # Special handling to remove 'Q' from the modified input pins
        if "Q" in mod_input_pins:
            mod_input_pins.remove("Q")  # Remove 'Q' from the modified input pins if present

        # Return the list of modified input pins
        return mod_input_pins  # Return the modified input pins list
    
    except Exception as e:
        raise Exception(f"Error in extract_mod_input_pins: {e}")

def extract_unique_internal_nodes(ast, mod_input_pins):
    """
    Extracts the unique internal connections of the
    verilog design. These connections are to be used to build
    the graph representing the verilog design. Also builds an
    important dict (port_to_node_to_instance) which binds ports
    to the design cells to make searching for nodes efficient.

    Args:
        ast (object): The netlist handler (AST).
        mod_input_pins (list): List containing cells' modified input pins.

    Returns:
        tuple: A tuple containing the list of unique internal connections and the port-to-instance mapping.

    Raises:
        ValueError: If the AST structure is invalid or mod_input_pins is not a list.
    """
    try:
        # Check if AST is of expected structure
        if not hasattr(ast, 'modules') or not ast.modules:
            raise ValueError("Invalid Netlist structure.")  # Raise an error if the AST structure is not valid

        # Check if mod_input_pins is a list
        if not isinstance(mod_input_pins, list):
            raise ValueError("Modified input pins must be a list.")  # Raise an error if mod_input_pins is not a list
        
        # Get all signal names from net declarations in the AST
        all_signals = [declaration.net_name for declaration in ast.modules[0].net_declarations]  # List of all signals

        # Get the internal nodes by excluding port names from the signal names
        internal_nodes = set(all_signals) - set(ast.modules[0].port_list)  # Internal nodes are signals not in the port list

        # Initialize a dictionary to map ports to instance names
        port_to_node_to_instance = {}  # Dictionary to map ports to instances

        # Loop through module instances in the AST
        for instance in ast.modules[0].module_instances:
            # Loop through ports of the current instance and add them to the dictionary
            for port, node in instance.ports.items():
                port_to_node_to_instance.setdefault(str(node), []).append(
                    (instance.instance_name, instance.module_name, port)  # Map port to instance and module
                )

        # Initialize a list to store internal connections
        internal_connections = []  # List to hold internal connections

        # Loop through internal nodes
        for k in internal_nodes:
            # Get the connections for the current node from the dictionary
            connections = port_to_node_to_instance.get(k, [])  # Get connections for the current node
            # Loop through the connections to find pairs of connected instances
            for i, (conn1, module1, port1) in enumerate(connections):
                for conn2, module2, port2 in connections[i + 1:]:
                    # Skip connections between input pins only
                    if port1 in mod_input_pins and port2 in mod_input_pins:
                        continue  # Skip if both ports are modified input pins
                    # Handle special case where 'Q' is an output pin
                    if port2 == "Q":
                        internal_connections.append([conn2, module2, conn1, module1, port1])  # Handle special case for 'Q'
                    else:
                        internal_connections.append([conn1, module1, conn2, module2, port2])  # Add the connection

        # Return the list of internal connections and the port-to-instance mapping
        return internal_connections, port_to_node_to_instance  # Return internal connections and port-to-instance mapping

    
    except Exception as e:
        raise Exception(f"Error in extract_unique_internal_nodes: {e}")

def find_partial_match(nets, input_list):
    """
    A utility function used to find partial matches
    between two given lists and returns a new list
    with the matching elements.

    Args:
        nets (list): List containing design internal nets.
        input_list (list): List containing inputs of the design.

    Returns:
        list: List containing elements present in both lists.

    Raises:
        ValueError: If nets is not a list or dict_keys or input_list is not list.
    """
    try:
        # Check if nets and input_list are lists
        if not isinstance(nets, list|type({}.keys())) or not isinstance(input_list, list):
            raise ValueError("Nets must be list or dict_keys and input_list must be list.")  # Raise an error if nets isn't list or dict_keys or input_list is not list
        # Create a regex pattern to match any item in input_list with optional suffixes
        pattern = "|".join(r"\b{}(?:__[0-9]+)?\b".format(re.escape(item)) for item in input_list)  # Build regex pattern
        # Compile the regex pattern
        regex = re.compile(pattern)  # Compile the regex pattern
        # Find all matches of the pattern in the concatenated string of nets
        output = set(regex.findall(" ".join(nets)))  # Find matches in the nets list

        # Return the list of matching elements
        return list(output)  # Return the list of matching elements

    
    except Exception as e:
        raise Exception(f"Error in find_partial_match: {e}")
    