`timescale 1ns/1ps
`default_nettype none

module tb;
  reg [7:0] ui_in;
  wire [7:0] uo_out;
  reg [7:0] uio_in;
  wire [7:0] uio_out;
  wire [7:0] uio_oe;
  reg ena;
  reg clk;
  reg rst_n;

  // 1. Force the power nets globally
  initial begin
    force VPWR = 1'b1;
    force VGND = 1'b0;
    force VPB  = 1'b1;
    force VNB  = 1'b0;
  end

  // 2. Instantiate DUT
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

  initial begin
    $dumpfile("sim_build/gl/sim.fst");
    $dumpvars(0, tb);
  end
endmodule
