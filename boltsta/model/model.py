from typing import Dict, Tuple
from ..utils import *


def calculate_combinational_delay(
    cell_pin_mapping: Dict[str, Dict[str, Dict[str, Dict[str, float]]]],
    cell_name: str,
    input_pin_name: str,
    input_transition_time: float,
    transition_type: str,
    output_capacitance: float,
    timing_sense: str,
) -> Tuple[float, float, str]:
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
        tuple: The total delay including the effect of output load capacitance and the transition type.

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
        transition_type == "fall" and timing_sense in {"positive_unate", "non_unate"}
    ) or (transition_type == "rise" and timing_sense == "negative_unate"):
        # Calculate falling edge delay
        fall_transition_delay, cell_fall_delay = calculate_falling_edge_delay(
            timing_data, input_transition_time, output_capacitance
        )
        return fall_transition_delay, cell_fall_delay, "fall"
    else:
        # Calculate rising edge delay
        rise_transition_delay, cell_rise_delay = calculate_rising_edge_delay(
            timing_data, input_transition_time, output_capacitance
        )
        return rise_transition_delay, cell_rise_delay, "rise"


def calculate_stage_delay(
    path: list,
    path_attribute: list,
    stage_index: int,
    transition_time: float,
    transition_type: str,
    cells_info: dict,
    library: str,
) -> tuple:
    """
    Calculate the delay for a specific stage in the path.

    Parameters:
    path (list): A list representing the sequence of cells and pins in the path.
    path_attribute (list): A list representing the attributes of each pin in the path.
    stage_index (int): The current stage index.
    transition_time (float): The input transition time at the current stage.
    transition_type (str): The transition type ("rise" or "fall").
    cells_info (dict): A dictionary containing cell timing information.
    library (str): The name of the library containing the cell data.

    Returns:
    tuple: Updated transition time, delay for the current stage, and updated transition type.
    """
    output_capacitance = get_output_capacitance(
        cell_name=path[stage_index + 2].split(",")[1],
        output_pin_name=path_attribute[stage_index + 1],
        library=library,
    )
    timing_sense_type = get_timing_sense(
        cell_name=path[stage_index + 1].split(",")[1],
        input_pin_name=path_attribute[stage_index],
        cells_info=cells_info,
    )
    transition_time, delay_combinational, transition_type = (
        calculate_combinational_delay(
            cell_pin_mapping=cells_info,
            cell_name=path[stage_index + 1].split(",")[1],
            input_pin_name=path_attribute[stage_index],
            transition_type=transition_type,
            timing_sense=timing_sense_type,
            output_capacitance=output_capacitance,
            input_transition_time=transition_time,
        )
    )
    return transition_time, delay_combinational, transition_type


def path_delay_function(
    path: list,
    path_attribute: list,
    initial_transition: float,
    cells_info: dict,
    library: str,
) -> float:
    """
    Calculate the propagation delay for a given path in a circuit.

    Parameters:
    path (list): A list representing the sequence of cells and pins in the path.
    path_attribute (list): A list representing the attributes of each pin in the path.
    initial_transition (float): The initial transition time at the input of the path.
    cells_info (dict): A dictionary containing cell timing information.
    library (str): The name of the library containing the cell data.

    Returns:
    float: The total propagation delay for the given path.
    """
    propagation_delay = 0  # Initialize total propagation delay

    # Loop through each stage in the path except the last one
    for stage_index in range(len(path) - 1):
        # Initialize transition type and transition time at the start of the path
        if stage_index == 0:
            transition_time = initial_transition
            transition_type = "rise"

        # Check if the next cell is the last one in the path
        is_last_stage = path[stage_index + 2] == path[-1]

        # Calculate the delay for the current stage
        transition_time, delay_combinational, transition_type = calculate_stage_delay(
            path=path,
            path_attribute=path_attribute,
            stage_index=stage_index,
            transition_time=transition_time,
            transition_type=transition_type,
            cells_info=cells_info,
            library=library,
        )

        # Add the delay of the current stage to the total propagation delay
        propagation_delay += delay_combinational

        if is_last_stage:
            break  # Exit the loop since we've reached the last stage

    return propagation_delay


def calculate_clk2q_delay(
    cell_timing_data: dict[str, dict[str, dict[str, dict[str, float]]]],
    cell_name: str,
    output_capacitance: float,
    output_pin_name: str = "Q_CLK",
    input_transition_time: float = 0.15,
) -> tuple:
    """
    Calculates the clock-to-Q delay for a given sequential cell.

    Parameters:
        cell_timing_data (dict): A dictionary mapping cell names to their timing data.
        cell_name (str): The name of the cell for which delay is being calculated.
        output_pin_name (str): The name of the output pin (default is Q_CLK).
        input_transition_time (float, optional): The input transition time. Default is 0.05.
        output_capacitance (float, optional): The output capacitance.

    Returns:
        tuple or None: The rise/fall delay and cell rise/fall delay, or None if cell name or output pin name not found.
    """

    # Check if the cell name exists in the mapping
    if cell_name in cell_timing_data:
        cell_data = cell_timing_data[cell_name]

        # Ensure the output pin name is either Q_CLK or Q_CLK_N
        if output_pin_name not in cell_data:
            output_pin_name = "Q_CLK_N"
        # Check if the adjusted output pin name exists for the given cell
        if output_pin_name in cell_data:
            timing_data = cell_data[output_pin_name]
            timing_type = timing_data["timing_type"]

            if timing_type == "rising_edge":
                return calculate_rising_edge_delay(
                    timing_data, input_transition_time, output_capacitance
                )
            else:  # falling edge
                return calculate_falling_edge_delay(
                    timing_data, input_transition_time, output_capacitance
                )
    return None


def calculate_constraint_time(
    cell_name: str,
    checking_type: str,
    input_pin: str,
    library_name: str,
    constrained_pin_transition: float,
    related_pin_transition: float,
) -> float:
    """
    Calculates the setup or hold time for a given cell.

    Parameters:
        cell_name (str): The name of the cell for which constraints are being calculated.
        checking_type (str): The type of checking ('setup_checking' or 'hold_checking').
        input_pin (str): The name of the input pin of the cell (D_CLK, D_CLK_N).
        library_name (str): The name of the library containing the cell.
        constrained_pin_transition (float): Transition time of the constrained pin.
        related_pin_transition (float): Transition time of the related pin.

    Returns:
        float: The setup or hold time for the given cell.

    Raises:
        ValueError: If the cell name or input pin name is not found.
    """

    # Retrieve timing information for the specified cell, input pin, and checking type
    timing_information = get_constraint_timing(
        input_pin_name=input_pin,
        cell_name=cell_name,
        library_name=library_name,
        checking_type=checking_type,
    )

    # Get the timing type (e.g., setup_rising, hold_rising)
    timing_type = timing_information["timing_type"]

    # Determine the appropriate constraint data group based on checking type and timing type
    if checking_type == "hold_checking":
        if timing_type == "hold_rising":
            constraint_data = timing_information.get_group("rise_constraint")
        else:
            constraint_data = timing_information.get_group("fall_constraint")
    else:  # setup_checking
        if timing_type == "setup_rising":
            constraint_data = timing_information.get_group("rise_constraint")
        else:
            constraint_data = timing_information.get_group("fall_constraint")

    # Interpolate the constraint time based on transition times
    constraint_time = interpolate_constraint_time(
        constraint_data, related_pin_transition, constrained_pin_transition
    )

    return constraint_time


def check_timing(
    paths: list[list[str]],
    paths_attributes: list[list[str]],
    cells_info: dict[str, dict[str, dict[str, dict[str, float]]]],
    library: str,
    clock_period: float = 1.8,
    input_transition_time: float = 0.15,
) -> list[str]:
    """
    Check timing for the given paths to find setup time violations.

    Parameters:
    paths (list[list[str]]): List of paths where each path is a list of strings representing the sequence of cells.
    paths_attributes (list[list[str]]): List of paths' attributes where each attribute corresponds to a path.
    cell_pin_mapping (dict): A dictionary mapping cell names to their timing data.
    cells_info (dict): A dictionary containing cell information.
    library (str): The name of the library containing the cell data.
    clock_period (float): The clock period for timing analysis.
    input_transition_time (float): The initial input transition time.

    Returns:
    list[str]: List of paths with setup time violations.
    """
    setup_violations = []
    # Loop through each path and its corresponding attributes
    for path, path_attr in zip(paths, paths_attributes):
        print(path)
        if path_attr[0] == None:
            continue
        sequential_output_capacitance = get_output_capacitance(
            cell_name=path[1].split(",")[1],
            output_pin_name=path_attr[0],
            library=library,
        )
        # Calculate clock-to-Q delay for the source flip-flop
        transition_type, clock_to_q_delay = calculate_clk2q_delay(
            cell_timing_data=cells_info,
            cell_name=path[0].split(",")[
                1
            ],  # Assuming the cell name is in the second part
            input_transition_time=input_transition_time,
            output_capacitance=sequential_output_capacitance,
        )

        # Calculate the data arrival time for the entire path
        total_delay = path_delay_function(
            path=path,
            path_attribute=path_attr,
            initial_transition=transition_type,
            cells_info=cells_info,
            library=library,
        )

        # Update the data arrival time with clock-to-Q delay
        data_arrival_time = total_delay + clock_to_q_delay

        # Calculate setup time for the destination flip-flop
        setup_delay = calculate_constraint_time(
            cell_name=path[-1].split(",")[
                1
            ],  # Assuming the destination cell is the last element
            checking_type="setup_checking",
            input_pin="D",
            library_name=library,
            constrained_pin_transition=0.15,
            related_pin_transition=0.15,
        )
        print(data_arrival_time)
        # Perform setup time check
        if data_arrival_time > clock_period - setup_delay:
            setup_violations.append(
                (path, path[-1])
            )  # Append the path and the destination flip-flop

    return setup_violations
