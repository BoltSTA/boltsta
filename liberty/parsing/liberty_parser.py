from liberty.parser import parse_liberty
from liberty.types import *
from ..utils import concatenate_pins

# Function to parse Liberty file and extract content
def parse_liberty_file(liberty_file_path: str) -> dict:
    """
    Parse the Liberty file and extract its content.

    Args:
        liberty_file_path (str): Path to the Liberty file.

    Returns:
        dict: Parsed data from the Liberty file.
    """
    # Read Liberty file content
    with open(liberty_file_path, "r") as f:
        liberty_content = f.read()

    # Parse the Liberty content
    parsed_data = parse_liberty(liberty_content)

    return parsed_data

# Function to extract cell names and pins from the Liberty library
def extract_cell_pin_mapping(library: str) -> dict:
    """
    Extracts cell names along with their respective pin names from the Liberty library.

    Args:
        library (LibertyLibrary): Parsed Liberty library.

    Returns:
        dict: Dictionary where keys are cell names and values are dictionaries of input pins with timing information.
    """
    cell_pin_mapping = {}

    # Loop through all cells in the library
    for cell_group in library.get_groups("cell"):
        cell_name = cell_group.args[0]
        input_pins_with_timing = {}

        # Loop through all pins of the cell
        for pin_group in cell_group.get_groups("pin"):
            pin_name = pin_group.args[0]

            # Loop through timing tables for this pin
            for timing_group in pin_group.get_groups("timing"):
                related_pin = timing_group["related_pin"]
                full_pin_name = concatenate_pins(pin_name, related_pin)
                timing = select_timing_group(pin_group, related_pin=related_pin)
                input_pins_with_timing[full_pin_name] = timing

        # Store cell name and its input pins with timing information in the dictionary
        cell_pin_mapping[cell_name] = input_pins_with_timing

    return cell_pin_mapping
