import pytest
from boltsta import calculate_combinational_delay, extract_cell_pin_mapping 
from boltsta.readers import parse_liberty_file


@pytest.fixture(scope="module")
def valid_cell_pin_mapping():
    library = parse_liberty_file("tests/sky130_fd_sc_hd__ff_100C_1v65.lib")
    cells_info = extract_cell_pin_mapping(library)
    return cells_info


def test_calculate_combinational_delay_fall(valid_cell_pin_mapping):
    trans_delay, cell_delay, trans_type = calculate_combinational_delay(
        valid_cell_pin_mapping,  
        "sky130_fd_sc_hd__buf_8",
        "X_A",
        0.01,
        "fall",
        0.0005,
        "positive_unate",
    )
    assert trans_delay == pytest.approx(0.0158805)
    assert cell_delay == pytest.approx(0.0711852)
    assert trans_type == "fall"


def test_calculate_combinational_delay_rise(valid_cell_pin_mapping):
    trans_delay, cell_delay, trans_type = calculate_combinational_delay(
        valid_cell_pin_mapping,  
        "sky130_fd_sc_hd__buf_8",
        "X_A",
        0.01,
        "rise",
        0.0005,
        "positive_unate",
    )
    assert trans_delay == pytest.approx(0.0160397)
    assert cell_delay == pytest.approx(0.0531370)
    assert trans_type == "rise"


def test_calculate_combinational_delay_negative_unate(valid_cell_pin_mapping):
    trans_delay, cell_delay, trans_type = calculate_combinational_delay(
        valid_cell_pin_mapping,  
        "sky130_fd_sc_hd__buf_8",
        "X_A",
        0.01,
        "rise",
        0.0005,
        "negative_unate",
    )
    assert trans_delay == pytest.approx(0.0158805)
    assert cell_delay == pytest.approx(0.0711852)
    assert trans_type == "fall"

# def test_calculate_combinational_delay_zero_load(valid_cell_pin_mapping):
#     trans_delay, cell_delay, trans_type = calculate_combinational_delay(
#         valid_cell_pin_mapping,  
#         "sky130_fd_sc_hd__buf_8",
#         "X_A",
#         0.0,
#         "rise",
#         0.0,
#         "negative_unate",
#     )
#     assert trans_delay == pytest.approx(0.0158805)
#     assert cell_delay == pytest.approx(0.0711852)
#     assert trans_type == "fall"


def test_calculate_combinational_delay_invalid_cell(valid_cell_pin_mapping):
    with pytest.raises(ValueError):
        calculate_combinational_delay(
            valid_cell_pin_mapping,  # Use the dictionary directly
            "invalid_cell_name",
            "X_A",
            0.01,
            "rise",
            0.0005,
            "negative_unate",
        )


def test_calculate_combinational_delay_invalid_pin(valid_cell_pin_mapping):
    with pytest.raises(ValueError):
        calculate_combinational_delay(
            valid_cell_pin_mapping, 
            "sky130_fd_sc_hd__buf_8",
            "A",
            0.01,
            "rise",
            0.0005,
            "negative_unate",
        )


def test_calculate_combinational_delay_negative_load(valid_cell_pin_mapping):
    with pytest.raises(ValueError):
        calculate_combinational_delay(
            valid_cell_pin_mapping,     
            "sky130_fd_sc_hd__buf_8",
            "X_A",
            0.01,
            "rise",
            -0.0005,
            "negative_unate",
        )


def test_calculate_combinational_delay_negative_input_trans(valid_cell_pin_mapping):
    with pytest.raises(ValueError):
        calculate_combinational_delay(
            valid_cell_pin_mapping,     
            "sky130_fd_sc_hd__buf_8",
            "X_A",
            -0.01,
            "rise",
            0.0005,
            "negative_unate",
        )


if __name__ == '__main__':
    pytest.main()
