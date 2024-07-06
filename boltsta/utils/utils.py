import numpy as np
from liberty.types import *
from tabulate import tabulate


# Function to concatenate pin name and related pin with an underscore
def concatenate_pins(pin_name: str, related_pin: str) -> str:
    """
    Concatenates pin name and related pin with an underscore.

    Args:
        pin_name (str): Name of the pin.
        related_pin (str): Name of the related pin.

    Returns:
        str: Concatenated string of pin name and related pin with an underscore.
    """
    # Convert EscapedString objects to regular strings
    pin_name = str(pin_name)
    related_pin = str(related_pin)
    # Remove double quotes from pin names
    pin_name = pin_name.strip('"')
    related_pin = related_pin.strip('"')
    return f"{pin_name}_{related_pin}"


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


# Function to interpolate 2D data using a provided formula
def interpolate_2d_formula(
    index_1_values: list,
    index_2_values: list,
    table_values: np.ndarray,
    x0: float,
    y0: float,
) -> float:
    """
    Interpolates 2D data using the formula in the Static Timing Analysis for
    Nanometer Designs A Practical Approach book .

    Parameters:
        index_1_values (list): Values of index_1.
        index_2_values (list): Values of index_2.
        table_values (np.ndarray): Corresponding table values.
        x0 (float): Target value of index_1 for interpolation.
        y0 (float): Target value of index_2 for interpolation.

    Returns:
        float: Interpolated value using the provided formula.
    """
    # Find the nearest index values
    x1, x2 = find_nearest_index(index_1_values[0], x0)
    y1, y2 = find_nearest_index(index_2_values[0], y0)

    # Calculate interpolation parameters
    x01 = (x0 - x1) / (x2 - x1)
    x20 = (x2 - x0) / (x2 - x1)
    y01 = (y0 - y1) / (y2 - y1)
    y20 = (y2 - y0) / (y2 - y1)

    # Find corresponding table values using numpy.where()
    (i1,) = np.where(index_1_values[0] == x1)
    (i2,) = np.where(index_2_values[0] == y1)
    T11 = table_values[i1, i2]

    (i2,) = np.where(index_2_values[0] == y2)
    T12 = table_values[i1, i2]

    (i1,) = np.where(index_1_values[0] == x2)
    (i2,) = np.where(index_2_values[0] == y1)
    T21 = table_values[i1, i2]

    (i2,) = np.where(index_2_values[0] == y2)
    T22 = table_values[i1, i2]

    # Perform interpolation using the provided formula
    interpolated_value = (
        x20 * y20 * T11 + x20 * y01 * T12 + x01 * y20 * T21 + x01 * y01 * T22
    )

    return interpolated_value


# Function to find the two nearest values in an array to a given value
def find_nearest_index(arr: list, value: float) -> tuple:
    """
    Find the two nearest values in an array to a given value.

    Parameters:
        arr (list): Array of values.
        value (float): Target value.

    Returns:
        tuple: The two nearest values.
    """
    idx = (np.abs(np.array(arr) - value)).argsort()[:2]
    return arr[idx[0]], arr[idx[1]]


def calculate_rising_edge_delay(
    timing_data: dict, input_transition_time: float, output_capacitance: float
) -> tuple:
    """
    Calculates the rising edge delay for a given timing data.

    Parameters:
        timing_data (dict): The timing data for the rising edge.
        input_transition_time (float): The input transition time.
        output_capacitance (float): The output capacitance.

    Returns:
        tuple: The rise delay and cell rise delay.
    """
    cell_rise_data = timing_data.get_group("cell_rise")
    rise_transition_data = timing_data.get_group("rise_transition")

    # Calculate rise transition delay
    rise_transition_delay = interpolate_2d_formula(
        rise_transition_data.get_array("index_1"),
        rise_transition_data.get_array("index_2"),
        rise_transition_data.get_array("values"),
        input_transition_time,
        output_capacitance,
    )

    # Calculate cell rise delay
    cell_rise_delay = interpolate_2d_formula(
        cell_rise_data.get_array("index_1"),
        cell_rise_data.get_array("index_2"),
        cell_rise_data.get_array("values"),
        input_transition_time,
        output_capacitance,
    )

    return rise_transition_delay, cell_rise_delay


def calculate_falling_edge_delay(
    timing_data: dict, input_transition_time: float, output_capacitance: float
) -> tuple:
    """
    Calculates the falling edge delay for a given timing data.

    Parameters:
        timing_data (dict): The timing data for the falling edge.
        input_transition_time (float): The input transition time.
        output_capacitance (float): The output capacitance.

    Returns:
        tuple: The fall delay and cell fall delay.
    """
    cell_fall_data = timing_data.get_group("cell_fall")
    fall_transition_data = timing_data.get_group("fall_transition")

    # Calculate fall transition delay
    fall_transition_delay = interpolate_2d_formula(
        fall_transition_data.get_array("index_1"),
        fall_transition_data.get_array("index_2"),
        fall_transition_data.get_array("values"),
        input_transition_time,
        output_capacitance,
    )

    # Calculate cell fall delay
    cell_fall_delay = interpolate_2d_formula(
        cell_fall_data.get_array("index_1"),
        cell_fall_data.get_array("index_2"),
        cell_fall_data.get_array("values"),
        input_transition_time,
        output_capacitance,
    )

    return fall_transition_delay, cell_fall_delay


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


def get_output_capacitance(
    fanout,
    library: str,
) -> float:
    """
    Retrieve the output capacitance for a given set of cells and their output pins.

    Parameters:
        fanout (list): A list representing the sequence of cells and their output pins in the format 'prefix,cell_name,output_pin'.
        library (str): The name of the library containing the cell data.

    Returns:
        float: The total output capacitance of the specified pins.

    Raises:
        KeyError: If the specified pin or cell is not found in the library.
    """
    capacitance = 0
    # Iterate through each cell in the fanout list
    for cell in fanout:
        output_pin_name = cell.split(",")[2]
        cell_name = cell.split(",")[1]
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
        capacitance += output_capacitance

    return capacitance


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


def interpolate_constraint_time(
    constraint_data, related_pin_transition, constrained_pin_transition
) -> float:
    """
    Interpolates the constraint time based on transition times.

    Parameters:
        constraint_data: The data group containing constraint values.
        related_pin_transition (float): Transition time of the related pin.
        constrained_pin_transition (float): Transition time of the constrained pin.

    Returns:
        float: Interpolated constraint time.
    """
    return interpolate_2d_formula(
        constraint_data.get_array("index_1"),
        constraint_data.get_array("index_2"),
        constraint_data.get_array("values"),
        related_pin_transition,
        constrained_pin_transition,
    )


def generate_timing_report(
    delays: dict,
    output_file: str,
    clock_rise_edge: float = 0.0,
    clock_network_delay: float = 0.0,
    clock_uncertainty: float = 0.3,
    clock_period: float = 10.0,
):
    """
    Generates a timing report for the given delays using the tabulate library and writes it to a text file.

    Args:
        delays (dict): A dictionary where keys are path identifiers (e.g., "path1") and values
                       are dictionaries mapping cell names to their delays.
        output_file (str): The file path where the timing report will be written.
        clock_rise_edge (float): Delay of clock rise edge.
        clock_network_delay (float): Delay of clock path.
        clock_uncertainty (float): Clock uncertainty.
        clock_period (float): Clock period.

    Returns:
        None
    """

    with open(output_file, "w") as file:
        # Iterate over each path and its cell delays
        for path_key, cells_delay in delays.items():
            if not cells_delay:
                continue  # Skip empty paths

            # Check if cells_delay has valid keys
            cell_keys = list(cells_delay.keys())
            if not cell_keys:
                continue

            startpoint = cell_keys[0].split(",")[0]
            endpoint = cell_keys[-1].split(",")[0]

            # Print start and end points
            print(
                f"Startpoint: {startpoint} (rising edge-triggered flip-flop clocked by core_clock)",
                file=file,
            )
            print(
                f"Endpoint: {endpoint} (rising edge-triggered flip-flop clocked by core_clock)",
                file=file,
            )
            print("Path Group: core_clock", file=file)
            print("Path Type: max\n", file=file)

            headers = ["Point", "Incr", "Path"]
            table = []

            # Initial conditions
            path_delay = 0.00

            # Add initial clock conditions to the table
            table.append(
                [
                    "clock CLKM (rise edge)",
                    f"{clock_rise_edge:.4f}",
                    f"{clock_rise_edge:.4f}",
                ]
            )
            table.append(
                [
                    "clock network delay (ideal)",
                    f"{clock_network_delay:.4f}",
                    f"{clock_network_delay:.4f}",
                ]
            )

            # Iterate over cells in the path (excluding the last cell)
            items_to_iterate = list(cells_delay.items())[:-1]
            for index, (cell, delay) in enumerate(items_to_iterate):
                if index == 0:  # Special handling for the first cell
                    modified_name = f"{cell_keys[0].split(',')[0]}/Clk2Q"
                    table.append(
                        [modified_name, f"{delay:.4f}", f"{path_delay + delay:.4f}"]
                    )
                else:
                    table.append(
                        [
                            cell.split(",")[0] + "/" + cell.split(",")[1],
                            f"{delay:.4f}",
                            f"{path_delay + delay:.4f}",
                        ]
                    )
                path_delay += delay

            # Add data arrival time to the table
            table.append(["data arrival time", "", f"{path_delay:.4f}"])

            # Calculate and add data required time to the table
            table.append(
                [
                    "clock period (rise edge)",
                    f"{clock_period:.4f}",
                    f"{clock_period:.4f}",
                ]
            )
            data_required_time = clock_period - clock_network_delay
            table.append(
                [
                    "clock network delay (ideal)",
                    f"{clock_network_delay:.4f}",
                    f"{data_required_time:.4f}",
                ]
            )
            data_required_time -= clock_uncertainty
            table.append(
                [
                    "clock uncertainty",
                    f"{-clock_uncertainty:.4f}",
                    f"{data_required_time:.4f}",
                ]
            )

            # Adjust data required time for setup time
            setup_time = cells_delay[cell_keys[-1]]
            data_required_time -= setup_time
            table.append(
                ["setup_time", f"{-setup_time:.4f}", f"{data_required_time:.4f}"]
            )

            # Add final data required and arrival times to the table
            table.append(["----------------------------", "-------", "--------"])
            table.append(["data required time", "", f"{data_required_time:.4f}"])
            table.append(["data arrival time", "", f"{-path_delay:.4f}"])
            table.append(["----------------------------", "-------", "--------"])

            # Calculate and add slack to the table
            slack = data_required_time - path_delay
            slack_status = "MET" if slack >= 0 else "VIOLATE"
            table.append([f"slack ({slack_status})", "", f"{slack:.4f}"])

            # Print the table using tabulate
            file.write(tabulate(table, headers, tablefmt="simple"))
            file.write("\n\n")
