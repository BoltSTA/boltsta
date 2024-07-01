import pytest
from boltsta.readers import preprocess_verilog
from boltsta.readers import parse_modified_verilog
from boltsta.readers import extract_mod_input_pins
from boltsta.readers import modify_input_pins


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


@pytest.mark.parametrize("expected_mod_input_pins, expected_port_to_node_to_instance", [
    # Test case 1
    (['Y_B', 'Q_D', 'X_B', 'X_C_N', 'Y_A', 'Q_CLK', 'X_A'], {
        'IN__0': [('_2_', 'sky130_fd_sc_hd__or3b_2', 'X_A')],
        'IN__1': [('_2_', 'sky130_fd_sc_hd__or3b_2', 'X_B'),
                  ('_6_', 'sky130_fd_sc_hd__nand2_2', 'Y_A')],
        'IN__2': [('_2_', 'sky130_fd_sc_hd__or3b_2', 'X_C_N'),
                  ('_4_', 'sky130_fd_sc_hd__or3b_2', 'X_A'),
                  ('_6_', 'sky130_fd_sc_hd__nand2_2', 'Y_B')],
        '_1_': [('_2_', 'sky130_fd_sc_hd__or3b_2', 'X'),
                ('_3_', 'sky130_fd_sc_hd__buf_1', 'X_A')],
        'D__0': [('_3_', 'sky130_fd_sc_hd__buf_1', 'X'),
                 ('_9_', 'sky130_fd_sc_hd__dfxtp_2', 'Q_D')],
        'IN__4': [('_4_', 'sky130_fd_sc_hd__or3b_2', 'X_B')],
        'IN__3': [('_4_', 'sky130_fd_sc_hd__or3b_2', 'X_C_N')],
        '_0_': [('_4_', 'sky130_fd_sc_hd__or3b_2', 'X'),
                ('_5_', 'sky130_fd_sc_hd__buf_1', 'X_A')],
        'D__2': [('_5_', 'sky130_fd_sc_hd__buf_1', 'X'),
                 ('_7_', 'sky130_fd_sc_hd__dfxtp_2', 'Q_D')],
        'D__1': [('_6_', 'sky130_fd_sc_hd__nand2_2', 'Y'),
                 ('_8_', 'sky130_fd_sc_hd__dfxtp_2', 'Q_D')],
        'CLK': [('_7_', 'sky130_fd_sc_hd__dfxtp_2', 'Q_CLK'),
                ('_8_', 'sky130_fd_sc_hd__dfxtp_2', 'Q_CLK'),
                ('_9_', 'sky130_fd_sc_hd__dfxtp_2', 'Q_CLK')],
        'OUT3': [('_7_', 'sky130_fd_sc_hd__dfxtp_2', 'Q')],
        'OUT2': [('_8_', 'sky130_fd_sc_hd__dfxtp_2', 'Q')],
        'OUT1': [('_9_', 'sky130_fd_sc_hd__dfxtp_2', 'Q')]})
])
def test_extract_mod_input_pins(setup_test_data, expected_mod_input_pins,
                                expected_port_to_node_to_instance):
    """
    Test function for extract_mod_input_pins.

    Args:
        setup_test_data (fixture): Fixture providing the modified Verilog AST.
        expected_mod_input_pins (list): Expected list of modified input pins.

    Asserts:
        Compares actual_mod_input_pins with expected_mod_input_pins.
    """
    ast = setup_test_data
    actual_mod_input_pins, actual_port_to_node_to_instance = extract_mod_input_pins(ast)
    assert sorted(actual_mod_input_pins) == sorted(expected_mod_input_pins)
    assert actual_port_to_node_to_instance == expected_port_to_node_to_instance


if __name__ == '__main__':
    pytest.main()
