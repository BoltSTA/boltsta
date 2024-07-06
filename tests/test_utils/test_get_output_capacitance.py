from liberty.types import *


def get_output_capacitance(
    cell_name: str,
    output_pin_name: str,
    library: str,
) -> float:
    """
    Retrieves the output capacitance for a given cell and output pin.

    Parameters:
        cell_name (str): The name of the cell for which output capacitance is being retrieved.
        output_pin_name (str): The name of the output pin (formatted as 'prefix_pin' or 'prefix_subprefix_pin').
        library (str): The name of the library containing the cell.

    Returns:
        float: The output capacitance of the specified pin.

    Raises:
        KeyError: If the specified pin or cell is not found in the library.
    """

    # Split the output pin name to determine the input pin name
    parts = output_pin_name.split("_")
    if len(parts) == 3:
        input_pin_name = f"{parts[1]}_{parts[2]}"
    else:
        input_pin_name = parts[-1]

    # Retrieve the cell from the library
    cell = select_cell(library, cell_name)

    # Retrieve the pin from the cell
    pin = select_pin(cell, input_pin_name)

    # Get the output capacitance value from the pin information
    output_capacitance = pin["capacitance"]

    return output_capacitance

