from liberty.types import *

def get_constraint_timing(
    input_pin_name: str, cell_name: str, library_name: str, checking_type: str
) -> dict:
    """
    Retrieves the hold timing data for a specified cell and input pin from a given library.

    Parameters:
        input_pin_name (str): The name of the input pin.
        cell_name (str): The name of the cell.
        library_name (str): The name of the library containing the cell.

    Returns:
        dict: The hold timing data for the specified input pin of the cell.

    Raises:
        ValueError: If the cell or pin is not found in the library.
    """
    # Select the cell from the specified library
    cell = select_cell(library_name, cell_name)
    if cell is None:
        raise ValueError(f"Cell '{cell_name}' not found in library '{library_name}'.")

    # Select the input pin from the selected cell
    pin = select_pin(cell, input_pin_name)
    if pin is None:
        raise ValueError(
            f"Input pin '{input_pin_name}' not found in cell '{cell_name}'."
        )

    # Get the hold timing data group from the input pin
    if checking_type == "hold_checking":
        constraint_timing_data = pin.get_groups("timing")[1]
    else:
        constraint_timing_data = pin.get_groups("timing")[0]

    return constraint_timing_data

