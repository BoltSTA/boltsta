import pytest
from boltsta.readers import preprocess_verilog, parse_modified_verilog, extract_mod_input_pins, modify_input_pins

@pytest.fixture(scope="module")
def setup_test_data():
    """
    Fixture to setup Verilog data for test_extract_mod_input_pins.

    Returns:
        AST: Parsed and modified Verilog Abstract Syntax Tree (AST).
    """
    input_pins = ['B', 'C_N', 'CLK', 'D', 'A', 'RESET_B']
    output_pins = ['Q', 'X', 'Y', 'Q']
    content = preprocess_verilog("tests/test_readers/test.v")
    ast = parse_modified_verilog(content)
    ast = modify_input_pins(ast, input_pins, output_pins)
    return ast

@pytest.mark.parametrize("expected_mod_input_pins", [
    # Test case 1
    (['Y_B', 'Q_D', 'X_B', 'X_C_N', 'Y_A', 'Q_CLK', 'X_A'])
])
def test_extract_mod_input_pins(setup_test_data, expected_mod_input_pins):
    """
    Test function for extract_mod_input_pins.

    Args:
        setup_test_data (fixture): Fixture providing the modified Verilog AST.
        expected_mod_input_pins (list): Expected list of modified input pins.

    Asserts:
        Compares actual_mod_input_pins with expected_mod_input_pins.
    """
    ast = setup_test_data
    actual_mod_input_pins = extract_mod_input_pins(ast)
    assert sorted(actual_mod_input_pins) == sorted(expected_mod_input_pins)

if __name__ == '__main__':
    pytest.main()
