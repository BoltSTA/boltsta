import pytest
from boltsta.readers import preprocess_verilog, parse_modified_verilog, extract_input_output_ports


@pytest.fixture(scope="module")
def setup_verilog_data():
    """
    Fixture to setup Verilog data for test_extract_input_output_ports.

    Returns:
        AST: Parsed and modified Verilog Abstract Syntax Tree (AST).
    """
    content = preprocess_verilog("tests/test_readers/test.v")
    ast = parse_modified_verilog(content)
    return ast


@pytest.mark.parametrize("expected_input_ports, expected_output_ports", [
    # Test case 1
    (['IN', 'CLK'], ['OUT1', 'OUT2', 'OUT3'])
])
def test_extract_input_output_ports(setup_verilog_data, expected_input_ports,
                                    expected_output_ports):
    """
    Test function for extract_input_output_ports.

    Args:
        setup_verilog_data (fixture): Fixture providing the modified Verilog AST.
        expected_input_ports (list): Expected list of input ports.
        expected_output_ports (list): Expected list of output ports.

    Asserts:
        Compares actual_input_ports and actual_output_ports with
        expected_input_ports and expected_output_ports respectively.
    """
    ast = setup_verilog_data
    actual_input_ports, actual_output_ports = extract_input_output_ports(ast)
    assert sorted(actual_input_ports) == sorted(expected_input_ports)
    assert sorted(actual_output_ports) == sorted(expected_output_ports)


if __name__ == '__main__':
    pytest.main()
