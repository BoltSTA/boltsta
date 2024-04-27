from ..utils import interpolate_2d_formula

# Function to calculate combinational delay
def calculate_delay_combinational(
    cell_pin_mapping: dict[str, dict[str, dict[str, dict[str, float]]]],
    cell_name: str,
    input_pin_name: str,
    input_transition_time: float,
    transition_type: str,
    output_capacitance: float,
    timing_sense: str,
) -> float:
    """
    Calculates the combinational delay for a given cell, input pin, and input transition parameters.

    Parameters:
        cell_pin_mapping (dict): A dictionary mapping cell names to their timing data.
        cell_name (str): The name of the cell for which delay is being calculated.
        input_pin_name (str): The name of the input pin of the cell.
        input_transition_time (float): The transition time of the input signal.
        transition_type (str): The type of transition ('fall' or 'rise').
        output_capacitance (float): The output load capacitance.
        timing_sense (str): The timing sense parameter.

    Returns:
        float: The total delay including the effect of output load capacitance.

    Raises:
        ValueError: If cell name or input pin name is not found.
        ValueError: If input_transition_time or output_capacitance is negative.
    """
    # Validate input parameters
    if input_transition_time < 0 or output_capacitance < 0:
        raise ValueError(
            "Input transition time and output capacitance must be non-negative."
        )

    # Check if the cell name exists in the mapping
    if cell_name not in cell_pin_mapping:
        raise ValueError(f"Cell name '{cell_name}' not found in the cell pin mapping.")

    cell_data = cell_pin_mapping[cell_name]

    # Check if the input pin name exists for the given cell
    if input_pin_name not in cell_data:
        raise ValueError(
            f"Input pin name '{input_pin_name}' not found for cell '{cell_name}'."
        )

    timing_data = cell_data[input_pin_name]

    if (
        transition_type == "fall"
        and (timing_sense == "positive_unate" or timing_sense == "non_unate")
    ) or (transition_type == "rise" and timing_sense == "negative_unate"):
        # Interpolate falling edge delay
        fall_transition_data = timing_data.get_group("fall_transition")
        cell_fall = timing_data.get_group("cell_fall")
        fall_transition_delay = interpolate_2d_formula(
            fall_transition_data.get_array("index_1"),
            fall_transition_data.get_array("index_2"),
            fall_transition_data.get_array("values"),
            input_transition_time,
            output_capacitance,
        )
        cell_fall_data = interpolate_2d_formula(
            cell_fall.get_array("index_1"),
            cell_fall.get_array("index_2"),
            cell_fall.get_array("values"),
            input_transition_time,
            output_capacitance,
        )
        return fall_transition_delay + cell_fall_data
    else:
        # Interpolate rising edge delay
        rise_transition_data = timing_data.get_group("rise_transition")
        cell_rise = timing_data.get_group("cell_rise")
        rise_transition_delay = interpolate_2d_formula(
            rise_transition_data.get_array("index_1"),
            rise_transition_data.get_array("index_2"),
            rise_transition_data.get_array("values"),
            input_transition_time,
            output_capacitance,
        )
        cell_rise_data = interpolate_2d_formula(
            cell_rise.get_array("index_1"),
            cell_rise.get_array("index_2"),
            cell_rise.get_array("values"),
            input_transition_time,
            output_capacitance,
        )
        return rise_transition_delay + cell_rise_data



# Function to calculate sequentail delay
def calculate_delay_sequential(
    cell_pin_mapping: dict[str, dict[str, dict[str, dict[str, float]]]],
    cell_name: str,
    input_pin_name: str,
    output_pin_name: str,
    transition_type: str,
    input_transition_time: float,
    output_capacitance: float,
    related_pin_transition: float,
    constrained_pin_transition: float,
    timing_sense: str,
) -> float:
    """
    Calculates the sequential delay for a given cell, input pin, and input transition parameters.

    Parameters:
        cell_pin_mapping (dict): A dictionary mapping cell names to their timing data.
        cell_name (str): The name of the cell for which delay is being calculated.
        input_pin_name (str): The name of the input pin of the cell.
        output_pin_name (str): The name of the output pin of the cell.
        transition_type (str): The type of transition ('fall' or 'rise').
        input_transition_time (float): The input transition time.
        output_capacitance (float): The output load capacitance.
        related_pin_transition (float): The transition time of the input signal.
        constrained_pin_transition (float): The output load capacitance.
        timing_sense (str): The timing sense parameter.

    Returns:
        float or None: The total delay including the effect of output load capacitance, or None if cell name or input pin name not found.
    """
    # Check if the cell name exists in the mapping
    if cell_name in cell_pin_mapping:
        cell_data = cell_pin_mapping[cell_name]
        # Check if the input pin name exists for the given cell
        if input_pin_name in cell_data:
            timing_data = cell_data[input_pin_name]
            # Check if transition type is 'rise'
            if transition_type == "rise" or (
                transition_type == "fall" and timing_sense == "negative_unate"
            ):
                setup_rise_data = timing_data.get_group("rise_constraint")
                # Interpolate setup rise data
                required_setup = interpolate_2d_formula(
                    setup_rise_data.get_array("index_1"),
                    setup_rise_data.get_array("index_2"),
                    setup_rise_data.get_array("values"),
                    related_pin_transition,
                    constrained_pin_transition,
                )
            else:
                setup_fall_data = timing_data.get_group("fall_constraint")
                # Interpolate setup fall data
                required_setup = interpolate_2d_formula(
                    setup_fall_data.get_array("index_1"),
                    setup_fall_data.get_array("index_2"),
                    setup_fall_data.get_array("values"),
                    related_pin_transition,
                    constrained_pin_transition,
                )
        # Check if the output pin name exists for the given cell
        if output_pin_name in cell_data:
            timing_data = cell_data[output_pin_name]
            # Check if transition type is 'fall'
            if transition_type == "fall" or (
                transition_type == "rise" and timing_sense == "negative_unate"
            ):
                # Interpolate falling edge delay
                fall_data = timing_data.get_group("cell_fall")
                fall_transition_data = timing_data.get_group("fall_transition")
                fall_delay = interpolate_2d_formula(
                    fall_transition_data.get_array("index_1"),
                    fall_transition_data.get_array("index_2"),
                    fall_transition_data.get_array("values"),
                    input_transition_time,
                    output_capacitance,
                )
                # Interpolate cell fall delay
                cell_fall_delay = interpolate_2d_formula(
                    fall_data.get_array("index_1"),
                    fall_data.get_array("index_2"),
                    fall_data.get_array("values"),
                    input_transition_time,
                    output_capacitance,
                )
                # Calculate total delay including output load capacitance effect
                total_delay = fall_delay + cell_fall_delay
                if total_delay > required_setup:
                    print(total_delay)
                    print(required_setup)
                else:
                    return total_delay
            else:
                # Interpolate rising edge delay
                rise_data = timing_data.get_group("cell_rise")
                rise_transition_data = timing_data.get_group("rise_transition")
                rise_delay = interpolate_2d_formula(
                    rise_transition_data.get_array("index_1"),
                    rise_transition_data.get_array("index_2"),
                    rise_transition_data.get_array("values"),
                    input_transition_time,
                    output_capacitance,
                )
                # Interpolate cell rise delay
                cell_rise_delay = interpolate_2d_formula(
                    rise_data.get_array("index_1"),
                    rise_data.get_array("index_2"),
                    rise_data.get_array("values"),
                    input_transition_time,
                    output_capacitance,
                )
                # Calculate total delay including output load capacitance effect
                total_delay = rise_delay + cell_rise_delay
                if total_delay > required_setup:
                    print(required_setup)
                else:
                    return total_delay
    return None
