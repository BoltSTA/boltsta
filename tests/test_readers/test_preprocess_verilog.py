import re
import pytest
from boltsta.readers import preprocess_verilog


def remove_whitespace(text):
    """Remove all whitespace characters from the given text."""
    return re.sub(r'\s+', '', text)     # Remove all whitespace characters


@pytest.mark.parametrize("verilog_file, expected_output", [
    ("tests/test_readers/test.v", """
    module DigCt(IN, CLK, OUT1, OUT2, OUT3);
    input [4:0] IN;
    input CLK;
    output OUT1;
    output OUT2;
    output OUT3;
    wire CLK;
    wire D__0;
    wire D__1;
    wire D__2;
    wire _0_;
    wire _1_;

    sky130_fd_sc_hd__or3b_2 _2_ (
        .A(IN__0),
        .B(IN__1),
        .C_N(IN__2),
        .X(_1_)
    );

    sky130_fd_sc_hd__buf_1 _3_ (
        .A(_1_),
        .X(D__0)
    );

    sky130_fd_sc_hd__or3b_2 _4_ (
        .A(IN__2),
        .B(IN__4),
        .C_N(IN__3),
        .X(_0_)
    );

    sky130_fd_sc_hd__buf_1 _5_ (
        .A(_0_),
        .X(D__2)
    );

    sky130_fd_sc_hd__nand2_2 _6_ (
        .A(IN__1),
        .B(IN__2),
        .Y(D__1)
    );

    sky130_fd_sc_hd__dfxtp_2 _7_ (
        .CLK(CLK),
        .D(D__2),
        .Q(OUT3)
    );

    sky130_fd_sc_hd__dfxtp_2 _8_ (
        .CLK(CLK),
        .D(D__1),
        .Q(OUT2)
    );

    sky130_fd_sc_hd__dfxtp_2 _9_ (
        .CLK(CLK),
        .D(D__0),
        .Q(OUT1)
    );
endmodule
    """),
    ("tests/test_readers/test2.v", """
    module AnotherModule(A, B, CLK, C, D);
    input A;
    input B;
    input CLK;
    output C;
    output D;
    wire CLK;
    wire D1;
    wire D2;

    sky130_fd_sc_hd__and2_2 _1_ (
        .A(A),
        .B(B),
        .X(D1)
    );

    sky130_fd_sc_hd__buf_1 _2_ (
        .A(D1),
        .X(D2)
    );

    sky130_fd_sc_hd__dfxtp_2 _3_ (
        .CLK(CLK),
        .D(D2),
        .Q(C)
    );

    sky130_fd_sc_hd__dfxtp_2 _4_ (
        .CLK(CLK),
        .D(D1),
        .Q(D)
    );
endmodule
    """)
])
def test_preprocess_verilog(verilog_file, expected_output):
    """
    Test case for preprocess_verilog function.

    Args:
        verilog_file (str): Path to the Verilog file to preprocess.
        expected_output (str): Expected output after preprocessing.

    Asserts:
        Compares the cleaned actual output with the cleaned expected output.
    """
    actual_output = preprocess_verilog(verilog_file)  # Preprocess the Verilog file
    actual_output_cleaned = remove_whitespace(actual_output)  # Remove whitespace for comparison
    expected_output_cleaned = remove_whitespace(expected_output)  # Clean expected output
    assert actual_output_cleaned == expected_output_cleaned  # Assert equal after cleaning


if __name__ == '__main__':
    pytest.main()
