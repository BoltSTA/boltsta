from utils import interpolate_2d_formula
import pytest

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


def test_calculate_rising_edge_delay():
    # Sample timing data
    timing_data = {
        "cell_rise": {
            "index_1": [0.1, 0.2, 0.3],
            "index_2": [1.0, 1.5, 2.0],
            "values": [
                [1.1, 1.2, 1.3],
                [1.4, 1.5, 1.6],
                [1.7, 1.8, 1.9]
            ]
        },
        "rise_transition": {
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

    rise_transition_delay, cell_rise_delay = calculate_rising_edge_delay(
        timing_data, input_transition_time, output_capacitance
    )

    # Manually calculate expected values
    expected_rise_transition_delay = interpolate_2d_formula(
        [0.1, 0.2, 0.3], [1.0, 1.5, 2.0],
        [[2.1, 2.2, 2.3], [2.4, 2.5, 2.6], [2.7, 2.8, 2.9]],
        input_transition_time, output_capacitance
    )

    expected_cell_rise_delay = interpolate_2d_formula(
        [0.1, 0.2, 0.3], [1.0, 1.5, 2.0],
        [[1.1, 1.2, 1.3], [1.4, 1.5, 1.6], [1.7, 1.8, 1.9]],
        input_transition_time, output_capacitance
    )

    assert rise_transition_delay == expected_rise_transition_delay
    assert cell_rise_delay == expected_cell_rise_delay

if __name__ == '__main__':
    pytest.main()



