import re
import pytest
from boltsta.readers import preprocess_verilog, parse_modified_verilog


def remove_whitespace(text):
    """Remove all whitespace characters from the given text."""
    return re.sub(r'\s+', '', text) 

@pytest.mark.parametrize("verilog_file, expected_ast", [
    ("tests/test_readers/test.v", "Netlist([Module(DigCt, ['IN', 'CLK', 'OUT1', 'OUT2', 'OUT3'], [InputDeclaration(IN [4:0]), InputDeclaration(CLK), OutputDeclaration(OUT1), OutputDeclaration(OUT2), OutputDeclaration(OUT3), NetDeclaration(CLK), NetDeclaration(D__0), NetDeclaration(D__1), NetDeclaration(D__2), NetDeclaration(_0_), NetDeclaration(_1_), ModuleInstance(sky130_fd_sc_hd__or3b_2, _2_, {'A': 'IN__0', 'B': 'IN__1', 'C_N': 'IN__2', 'X': '_1_'}), ModuleInstance(sky130_fd_sc_hd__buf_1, _3_, {'A': '_1_', 'X': 'D__0'}), ModuleInstance(sky130_fd_sc_hd__or3b_2, _4_, {'A': 'IN__2', 'B': 'IN__4', 'C_N': 'IN__3', 'X': '_0_'}), ModuleInstance(sky130_fd_sc_hd__buf_1, _5_, {'A': '_0_', 'X': 'D__2'}), ModuleInstance(sky130_fd_sc_hd__nand2_2, _6_, {'A': 'IN__1', 'B': 'IN__2', 'Y': 'D__1'}), ModuleInstance(sky130_fd_sc_hd__dfxtp_2, _7_, {'CLK': 'CLK', 'D': 'D__2', 'Q': 'OUT3'}), ModuleInstance(sky130_fd_sc_hd__dfxtp_2, _8_, {'CLK': 'CLK', 'D': 'D__1', 'Q': 'OUT2'}), ModuleInstance(sky130_fd_sc_hd__dfxtp_2, _9_, {'CLK': 'CLK', 'D': 'D__0', 'Q': 'OUT1'})])])"),
    ("tests/test_readers/test2.v", "Netlist([Module(AnotherModule, ['A', 'B', 'CLK', 'C', 'D'], [InputDeclaration(A), InputDeclaration(B), InputDeclaration(CLK), OutputDeclaration(C), OutputDeclaration(D), NetDeclaration(CLK), NetDeclaration(D1), NetDeclaration(D2), ModuleInstance(sky130_fd_sc_hd__and2_2, _1_, {'A': 'A', 'B': 'B', 'X': 'D1'}), ModuleInstance(sky130_fd_sc_hd__buf_1, _2_, {'A': 'D1', 'X': 'D2'}), ModuleInstance(sky130_fd_sc_hd__dfxtp_2, _3_, {'CLK': 'CLK', 'D': 'D2', 'Q': 'C'}), ModuleInstance(sky130_fd_sc_hd__dfxtp_2, _4_, {'CLK': 'CLK', 'D': 'D1', 'Q': 'D'})])])")
])
def test_parse_modified_verilog(verilog_file, expected_ast):
    """
    Test case for parse_modified_verilog function.

    Args:
        verilog_file (str): Path to the Verilog file to parse.
        expected_ast (str): Expected Abstract Syntax Tree (AST) in string format.

    Asserts:
        Compares the cleaned actual AST with the cleaned expected AST.
    """
    content = preprocess_verilog(verilog_file)  # Preprocess Verilog file content
    actual_ast = str(parse_modified_verilog(content))  # Parse the modified Verilog content
    actual_ast_cleaned = remove_whitespace(actual_ast)  # Remove whitespace for comparison
    expected_ast_cleaned = remove_whitespace(expected_ast)  # Clean expected AST
    assert actual_ast_cleaned == expected_ast_cleaned  # Assert equal after cleaning

if __name__ == '__main__':
    pytest.main()