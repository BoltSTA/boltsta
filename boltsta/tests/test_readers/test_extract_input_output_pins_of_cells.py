import pytest
from boltsta.readers import preprocess_verilog
from boltsta.readers import parse_modified_verilog
from boltsta.readers import extract_input_output_pins_of_cells


@pytest.fixture(scope="module")
def setup_verilog_data():
    """
    Fixture to setup Verilog data for test_extract_input_output_pins_of_cells.

    Returns:
        AST: Parsed and modified Verilog Abstract Syntax Tree (AST).
    """
    content = preprocess_verilog("tests/test_readers/test.v")
    ast = parse_modified_verilog(content)
    return ast


@pytest.mark.parametrize("expected_input_pins, expected_output_pins, expected_nets", [
    # Test case 1
    (['B', 'C_N', 'CLK', 'D', 'A', 'RESET_B'], ['Q', 'X', 'Y', 'Q'],
     ['IN__0', 'IN__1', 'IN__2', '_1_', '_1_', 'D__0', 'IN__2', 'IN__4', 'IN__3', '_0_', '_0_',
      'D__2', 'IN__1', 'IN__2', 'D__1', 'CLK', 'D__2', 'OUT3',
      'CLK', 'D__1', 'OUT2', 'CLK', 'D__0', 'OUT1'])
])
def test_extract_input_output_pins_of_cells(setup_verilog_data, expected_input_pins,
                                            expected_output_pins, expected_nets):
    """
    Test function for extract_input_output_pins_of_cells.

    Args:
        setup_verilog_data (fixture): Fixture providing the modified Verilog AST.
        expected_input_pins (list): Expected list of input pins.
        expected_output_pins (list): Expected list of output pins.

    Asserts:
        Compares actual_input_pins and actual_output_pins with expected_input_pins
          and expected_output_pins respectively.
    """
    ast = setup_verilog_data
    actual_input_pins, actual_output_pins, actual_nets = extract_input_output_pins_of_cells(ast)
    assert sorted(actual_input_pins) == sorted(expected_input_pins)
    assert sorted(actual_output_pins) == sorted(expected_output_pins)
    assert sorted(actual_nets) == sorted(expected_nets)


if __name__ == '__main__':
    pytest.main()
