import pytest
from liberty.parser import parse_liberty
from liberty.types import *
from boltsta import calculate_clk2q_delay, extract_cell_pin_mapping
from boltsta.readers import parse_liberty_file

@pytest.fixture(scope="module")
def valid_cell_pin_mapping():
    library = parse_liberty_file("tests/sky130_fd_sc_hd__ff_100C_1v65.lib")
    cells_info = extract_cell_pin_mapping(library)
    return cells_info


def test_calculate_clk2q_delay_rise(valid_cell_pin_mapping):
    trans_delay,clk2q_delay = calculate_clk2q_delay(
        cell_timing_data=valid_cell_pin_mapping,
        cell_name="sky130_fd_sc_hd__dfrtp_2",
        output_capacitance=0.376292,
        output_pin_name="Q_CLK",
        input_transition_time=0.010,
        )
    assert trans_delay == pytest.approx(1.4934162)
    assert clk2q_delay == pytest.approx(1.2778603)

def test_calculate_clk2q_delay_negative_output_capacitance(valid_cell_pin_mapping):
    with pytest.raises(ValueError):
        calculate_clk2q_delay(
            cell_timing_data=valid_cell_pin_mapping,
            cell_name="sky130_fd_sc_hd__dfrtp_2",
            output_capacitance=-0.376292,
            output_pin_name="Q_CLK",
            input_transition_time=0.010,
        )


def test_calculate_clk2q_delay_negative_input_transition_time(valid_cell_pin_mapping):
    with pytest.raises(ValueError):
        calculate_clk2q_delay(
        cell_timing_data=valid_cell_pin_mapping,
        cell_name="sky130_fd_sc_hd__dfrtp_2",
        output_capacitance=0.376292,
        output_pin_name="Q_CLK",
        input_transition_time=-0.010,
    )

def test_calculate_clk2q_delay_invalid_cell_name(valid_cell_pin_mapping):
    with pytest.raises(ValueError):
        calculate_clk2q_delay(
            cell_timing_data=valid_cell_pin_mapping,
            cell_name="sky130_fd_sc_hd__dfrtp_2_invalid",
            output_capacitance=0.376292,
            output_pin_name="Q_CLK",
            input_transition_time=0.010,
        )

def test_calculate_clk2q_delay_invalid_output_pin_name(valid_cell_pin_mapping):
    with pytest.raises(ValueError):
        calculate_clk2q_delay(
            cell_timing_data=valid_cell_pin_mapping,
            cell_name="sky130_fd_sc_hd__dfrtp_2",
            output_capacitance=0.376292,
            output_pin_name="Q_CLK_invalid",
            input_transition_time=0.010,
        )

def test_calculate_clk2q_delay_last(valid_cell_pin_mapping):
    trans_delay,clk2q_delay = calculate_clk2q_delay(
        cell_timing_data=valid_cell_pin_mapping,
        cell_name="sky130_fd_sc_hd__sdfbbn_1",
        output_capacitance=0.1977640,
        output_pin_name="Q_CLK_N",
        input_transition_time=0.01,
        )
    assert trans_delay == pytest.approx(0.8731816)
    assert clk2q_delay == pytest.approx(1.0873294)



if __name__ == '__main__':
    pytest.main()
