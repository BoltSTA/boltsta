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
