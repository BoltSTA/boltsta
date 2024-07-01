import pytest
import re
from boltsta.readers import preprocess_verilog, parse_modified_verilog, modify_input_pins


def remove_whitespace(text):
    """Remove all whitespace characters from the given text."""
    return re.sub(r'\s+', '', text)


@pytest.fixture(scope="module")
def setup_verilog_data():
    """
    Fixture to setup Verilog data for modification testing.

    Returns:
        AST: Parsed Abstract Syntax Tree (AST) of the modified Verilog content.
    """
    content = preprocess_verilog("tests/test_readers/test.v")  # Preprocess Verilog file content
    ast = parse_modified_verilog(content)  # Parse modified Verilog content
    return ast  # Return parsed AST


@pytest.mark.parametrize("input_pins, output_pins, expected_modified_ast", [
    (['B', 'C_N', 'CLK', 'D', 'A', 'RESET_B'], ['Q', 'X', 'Y', 'Q'], "Netlist([Module(DigCt, ['IN',\
'CLK', 'OUT1', 'OUT2', 'OUT3'], [InputDeclaration(IN [4:0]), InputDeclaration(CLK), \
OutputDeclaration(OUT1), OutputDeclaration(OUT2), OutputDeclaration(OUT3), NetDeclaration(CLK), \
NetDeclaration(D__0), NetDeclaration(D__1), NetDeclaration(D__2), NetDeclaration(_0_), \
NetDeclaration(_1_), ModuleInstance(sky130_fd_sc_hd__or3b_2, _2_, {'X_A': 'IN__0', 'X_B': 'IN__1', \
'X_C_N': 'IN__2', 'X': '_1_'}), ModuleInstance(sky130_fd_sc_hd__buf_1, _3_, {'X_A': '_1_', 'X': \
'D__0'}), ModuleInstance(sky130_fd_sc_hd__or3b_2, _4_, {'X_A': 'IN__2', 'X_B': 'IN__4', 'X_C_N': \
'IN__3', 'X': '_0_'}), ModuleInstance(sky130_fd_sc_hd__buf_1, _5_, {'X_A': '_0_', 'X': 'D__2'}), \
ModuleInstance(sky130_fd_sc_hd__nand2_2, _6_, {'Y_A': 'IN__1', 'Y_B': 'IN__2', 'Y': 'D__1'}), \
ModuleInstance(sky130_fd_sc_hd__dfxtp_2, _7_, {'Q_CLK': 'CLK', 'Q_D': 'D__2', 'Q': 'OUT3'}), \
ModuleInstance(sky130_fd_sc_hd__dfxtp_2, _8_, {'Q_CLK': 'CLK', 'Q_D': 'D__1', 'Q': 'OUT2'}), \
ModuleInstance(sky130_fd_sc_hd__dfxtp_2, _9_, {'Q_CLK': 'CLK', 'Q_D': 'D__0', 'Q': 'OUT1'})])])")
])
def test_modify_input_pins(setup_verilog_data, input_pins, output_pins, expected_modified_ast):
    """
    Test case for modify_input_pins function.

    Args:
        setup_verilog_data (AST): Fixture returning parsed AST of modified Verilog content.
        input_pins (list): List of input pins to modify.
        output_pins (list): List of output pins to modify.
        expected_modified_ast (str): Expected modified AST in string format.

    Asserts:
        Compares cleaned actual modified AST with cleaned expected modified AST.
    """
    # Modify input pins in AST
    actual_modified_ast = str(modify_input_pins(setup_verilog_data, input_pins, output_pins))
    # Assert equal after cleaning
    assert remove_whitespace(actual_modified_ast) == remove_whitespace(expected_modified_ast)


if __name__ == '__main__':
    pytest.main()
