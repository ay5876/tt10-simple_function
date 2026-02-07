`timescale 1ns/1ps
`default_nettype none

module tb;
  reg  [7:0] ui_in;
  wire [7:0] uo_out;
  reg  [7:0] uio_in;
  wire [7:0] uio_out;
  wire [7:0] uio_oe;
  reg  ena;
  reg  clk;
  reg  rst_n;

  // Provide global supplies for gate-level sims (sky130 cells use these nets)
`ifdef USE_POWER_PINS
  supply1 VPWR;
  supply0 VGND;
  // Some libraries may reference these; define them globally even if not used by DUT
  supply1 VPB;
  supply0 VNB;
`endif

  // Instantiate DUT (NO power pins on RTL module)
  tt_um_ay5876_simple dut (
    .ui_in(ui_in),
    .uo_out(uo_out),
    .uio_in(uio_in),
    .uio_out(uio_out),
    .uio_oe(uio_oe),
    .ena(ena),
    .clk(clk),
    .rst_n(rst_n)
  );

  initial clk = 0;
  always #5 clk = ~clk;

endmodule
