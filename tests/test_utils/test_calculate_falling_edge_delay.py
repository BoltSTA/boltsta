import pytest
import numpy as np
from utils import interpolate_2d_formula



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



def test_calculate_falling_edge_delay():
    # Sample timing data
    timing_data = {
        "cell_fall": {
            "index_1": [0.1, 0.2, 0.3],
            "index_2": [1.0, 1.5, 2.0],
            "values": [
                [1.1, 1.2, 1.3],
                [1.4, 1.5, 1.6],
                [1.7, 1.8, 1.9]
            ]
        },
        "fall_transition": {
            "index_1": [0.1, 0.2, 0.3],
            "index_2": [1.0, 1.5, 2.0],
            "values": [
                [2.1, 2.2, 2.3],
                [2.4, 2.5, 2.6],
                [2.7, 2.8, 2.9]
            ]
        }
    }

    input_transition_time = 0.15
    output_capacitance = 1.25

    fall_transition_delay, cell_fall_delay = calculate_falling_edge_delay(
        timing_data, input_transition_time, output_capacitance
    )

    # Manually calculate expected values
    expected_fall_transition_delay = interpolate_2d_formula(
        [0.1, 0.2, 0.3], [1.0, 1.5, 2.0],
        [[2.1, 2.2, 2.3], [2.4, 2.5, 2.6], [2.7, 2.8, 2.9]],
        input_transition_time, output_capacitance
    )

    expected_cell_fall_delay = interpolate_2d_formula(
        [0.1, 0.2, 0.3], [1.0, 1.5, 2.0],
        [[1.1, 1.2, 1.3], [1.4, 1.5, 1.6], [1.7, 1.8, 1.9]],
        input_transition_time, output_capacitance
    )

    assert fall_transition_delay == expected_fall_transition_delay
    assert cell_fall_delay == expected_cell_fall_delay

if __name__ == '__main__':
    pytest.main()

