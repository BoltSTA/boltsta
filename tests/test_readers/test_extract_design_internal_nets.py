import pytest
from boltsta.readers import preprocess_verilog, parse_modified_verilog, extract_design_internal_nets

@pytest.fixture(scope="module")
def setup_verilog_data():
    """
    Fixture to setup Verilog data for test_extract_design_internal_nets.

    Returns:
        AST: Parsed and modified Verilog Abstract Syntax Tree (AST).
    """
    content = preprocess_verilog("tests/test_readers/test.v")
    ast = parse_modified_verilog(content)
    return ast

@pytest.mark.parametrize("expected_internal_nets", [
    ['IN__0', 'IN__1', 'IN__2', '_1_', '_1_', 'D__0', 'IN__2', 'IN__4', 'IN__3', '_0_', '_0_', 'D__2', 'IN__1', 'IN__2', 'D__1', 'CLK', 'D__2', 'OUT3', 'CLK', 'D__1', 'OUT2', 'CLK', 'D__0', 'OUT1']
])
def test_extract_design_internal_nets(setup_verilog_data, expected_internal_nets):
    """
    Test function for extract_design_internal_nets.

    Args:
        setup_verilog_data (fixture): Fixture providing the modified Verilog AST.
        expected_internal_nets (list): Expected list of internal nets.

    Asserts:
        Compares actual_internal_nets with expected_internal_nets.
    """
    ast = setup_verilog_data
    actual_internal_nets = extract_design_internal_nets(ast)
    assert sorted(actual_internal_nets) == sorted(expected_internal_nets)

if __name__ == '__main__':
    pytest.main()
