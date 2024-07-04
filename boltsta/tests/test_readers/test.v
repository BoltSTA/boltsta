module DigCt(IN, CLK, OUT1, OUT2, OUT3);
    input [4:0] IN;
    input CLK;
    output OUT1;
    output OUT2;
    output OUT3;
    wire CLK;
    wire \D[0];
    wire \D[1];
    wire \D[2];
    wire _0_;
    wire _1_;

    sky130_fd_sc_hd__or3b_2 _2_ (
        .A(IN[0]),
        .B(IN[1]),
        .C_N(IN[2]),
        .X(_1_)
    );

    sky130_fd_sc_hd__buf_1 _3_ (
        .A(_1_),
        .X(\D[0])
    );

    sky130_fd_sc_hd__or3b_2 _4_ (
        .A(IN[2]),
        .B(IN[4]),
        .C_N(IN[3]),
        .X(_0_)
    );

    sky130_fd_sc_hd__buf_1 _5_ (
        .A(_0_),
        .X(\D[2])
    );

    sky130_fd_sc_hd__nand2_2 _6_ (
        .A(IN[1]),
        .B(IN[2]),
        .Y(\D[1])
    );

    sky130_fd_sc_hd__dfxtp_2 _7_ (
        .CLK(CLK),
        .D(\D[2]),
        .Q(OUT3)
    );

    sky130_fd_sc_hd__dfxtp_2 _8_ (
        .CLK(CLK),
        .D(\D[1]),
        .Q(OUT2)
    );

    sky130_fd_sc_hd__dfxtp_2 _9_ (
        .CLK(CLK),
        .D(\D[0]),
        .Q(OUT1)
    );
endmodule
