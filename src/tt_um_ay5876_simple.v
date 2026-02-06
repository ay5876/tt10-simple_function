`default_nettype none

module tt_um_ay5876_simple (
    input  wire [7:0] ui_in,     // inputs
    output wire [7:0] uo_out,     // outputs
    input  wire [7:0] uio_in,     // bidir input
    output wire [7:0] uio_out,    // bidir output
    output wire [7:0] uio_oe,     // bidir output enable
    input  wire       ena,        // enable
    input  wire       clk,        // clock
    input  wire       rst_n        // reset (active low)
);

    // Map inputs
    wire A = ui_in[0];
    wire B = ui_in[1];
    wire C = ui_in[2];

    // Logic: F = AB + C', Y = C'
    wire Cn = ~C;
    wire F  = (A & B) | Cn;
    wire Y  = Cn;

    // Map outputs
    assign uo_out[0] = F;
    assign uo_out[1] = Y;
    assign uo_out[7:2] = 6'b0;

    // Disable bidirectional pins
    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

    // Prevent unused warnings
    wire _unused = &{uio_in, ena, clk, rst_n, ui_in[7:3], 1'b0};

endmodule
