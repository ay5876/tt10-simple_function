`default_nettype none

module tt_um_ay5876_simple (
    input  wire [7:0] ui_in,     // Dedicated inputs
    output wire [7:0] uo_out,    // Dedicated outputs
    input  wire [7:0] uio_in,    // IOs: Input path
    output wire [7:0] uio_out,   // IOs: Output path
    output wire [7:0] uio_oe,    // IOs: Enable path (0=input, 1=output)
    input  wire       ena,       // Always 1 when design is powered
    input  wire       clk,       // Clock (not used here)
    input  wire       rst_n       // Reset (not used here)
);

    // Inputs
    wire A = ui_in[0];
    wire B = ui_in[1];
    wire C = ui_in[2];

    // Required outputs:
    // F = AB + C'
    // Y = C'
    wire Cn = ~C;
    wire F  = (A & B) | Cn;
    wire Y  = Cn;

    // Map to TinyTapeout outputs
    assign uo_out[0] = F;
    assign uo_out[1] = Y;
    assign uo_out[7:2] = 6'b0;

    // Unused bidirectional pins
    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

    // Prevent unused warnings
    wire _unused = &{ena, clk, rst_n, ui_in[7:3], uio_in, 1'b0};

endmodule
