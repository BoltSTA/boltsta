import pytest
from boltsta.readers import preprocess_verilog, parse_modified_verilog, extract_unique_internal_nodes, modify_input_pins

@pytest.fixture(scope="module")
def setup_test_data():
    """
    Fixture to setup test data for test_extract_unique_internal_nodes.

    Returns:
        tuple: Tuple containing ast (parsed modified Verilog AST) and mod_input_pins (modified input pins list).
    """
    content = preprocess_verilog("tests/test_readers/test.v")
    input_pins = ['B', 'C_N', 'CLK', 'D', 'A', 'RESET_B']
    output_pins = ['Q', 'X', 'Y', 'Q']
    ast = parse_modified_verilog(content)
    ast = modify_input_pins(ast, input_pins, output_pins)
    mod_input_pins = ['Y_B', 'Q_D', 'X_B', 'X_C_N', 'Y_A', 'Q_CLK', 'X_A']
    return ast, mod_input_pins


@pytest.mark.parametrize("expected_internal_connections, expected_port_to_node_to_instance", [
    ([['_2_', 'sky130_fd_sc_hd__or3b_2', '_3_', 'sky130_fd_sc_hd__buf_1', 'X_A'], ['_3_', 'sky130_fd_sc_hd__buf_1', '_9_', 'sky130_fd_sc_hd__dfxtp_2', 'Q_D'], ['_5_', 'sky130_fd_sc_hd__buf_1', '_7_', 'sky130_fd_sc_hd__dfxtp_2', 'Q_D'], ['_6_', 'sky130_fd_sc_hd__nand2_2', '_8_', 'sky130_fd_sc_hd__dfxtp_2', 'Q_D'], ['_4_', 'sky130_fd_sc_hd__or3b_2', '_5_', 'sky130_fd_sc_hd__buf_1', 'X_A']], {'IN__0': [('_2_', 'sky130_fd_sc_hd__or3b_2', 'X_A')], 'IN__1': [('_2_', 'sky130_fd_sc_hd__or3b_2', 'X_B'), ('_6_', 'sky130_fd_sc_hd__nand2_2', 'Y_A')], 'IN__2': [('_2_', 'sky130_fd_sc_hd__or3b_2', 'X_C_N'), ('_4_', 'sky130_fd_sc_hd__or3b_2', 'X_A'), ('_6_', 'sky130_fd_sc_hd__nand2_2', 'Y_B')], '_1_': [('_2_', 'sky130_fd_sc_hd__or3b_2', 'X'), ('_3_', 'sky130_fd_sc_hd__buf_1', 'X_A')], 'D__0': [('_3_', 'sky130_fd_sc_hd__buf_1', 'X'), ('_9_', 'sky130_fd_sc_hd__dfxtp_2', 'Q_D')], 'IN__4': [('_4_', 'sky130_fd_sc_hd__or3b_2', 'X_B')], 'IN__3': [('_4_', 'sky130_fd_sc_hd__or3b_2', 'X_C_N')], '_0_': [('_4_', 'sky130_fd_sc_hd__or3b_2', 'X'), ('_5_', 'sky130_fd_sc_hd__buf_1', 'X_A')], 'D__2': [('_5_', 'sky130_fd_sc_hd__buf_1', 'X'), ('_7_', 'sky130_fd_sc_hd__dfxtp_2', 'Q_D')], 'D__1': [('_6_', 'sky130_fd_sc_hd__nand2_2', 'Y'), ('_8_', 'sky130_fd_sc_hd__dfxtp_2', 'Q_D')], 'CLK': [('_7_', 'sky130_fd_sc_hd__dfxtp_2', 'Q_CLK'), ('_8_', 'sky130_fd_sc_hd__dfxtp_2', 'Q_CLK'), ('_9_', 'sky130_fd_sc_hd__dfxtp_2', 'Q_CLK')], 'OUT3': [('_7_', 'sky130_fd_sc_hd__dfxtp_2', 'Q')], 'OUT2': [('_8_', 'sky130_fd_sc_hd__dfxtp_2', 'Q')], 'OUT1': [('_9_', 'sky130_fd_sc_hd__dfxtp_2', 'Q')]})
])
def test_extract_unique_internal_nodes(setup_test_data, expected_internal_connections, expected_port_to_node_to_instance):
    """
    Test function for extract_unique_internal_nodes.

    Args:
        setup_test_data (fixture): Fixture providing ast and mod_input_pins.
        expected_internal_connections (list): Expected list of internal connections.
        expected_port_to_node_to_instance (dict): Expected dictionary mapping ports to nodes and instances.

    Asserts:
        Compares sorted actual_internal_connections with sorted expected_internal_connections.
        Asserts actual_port_to_node_to_instance equals expected_port_to_node_to_instance.
    """
    ast, mod_input_pins = setup_test_data
    actual_internal_connections, actual_port_to_node_to_instance = extract_unique_internal_nodes(ast, mod_input_pins)
    assert sorted(actual_internal_connections) == sorted(expected_internal_connections)
    assert actual_port_to_node_to_instance == expected_port_to_node_to_instance

if __name__ == '__main__':
    pytest.main()