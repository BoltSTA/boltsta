def get_timing_sense(cells_info, cell_name, input_pin_name):
    """
    Get the timing sense of a cell input pin.

    Args:
        cell_name (str): The name of the cell.
        input_pin_name (str): The name of the input pin.

    Returns:
        str: The timing sense of the input pin.
    """
    # Check if the cell name exists in the mapping
    if cell_name in cells_info:
        cell_data = cells_info[cell_name]
        # Check if the input pin name exists for the given cell
        if input_pin_name in cell_data:
            timing_data = cell_data[input_pin_name]
            # Get the timing sense of the input pin
            timing_sense = timing_data["timing_sense"]
            return timing_sense
    return None

