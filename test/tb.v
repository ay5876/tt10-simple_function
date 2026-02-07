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

  initial clk = 0;
  always #5 clk = ~clk;

  initial begin
    ena   = 1'b1;
    rst_n = 1'b1;
    ui_in = 8'h00;
    uio_in = 8'h00;
  end

`ifdef GL_TEST
  // Gate-level netlist has VPWR/VGND ports
  supply1 VPWR;
  supply0 VGND;

  tt_um_ay5876_simple dut (
    .clk(clk),
    .ena(ena),
    .rst_n(rst_n),
    .VPWR(VPWR),
    .VGND(VGND),
    .ui_in(ui_in),
    .uio_in(uio_in),
    .uio_oe(uio_oe),
    .uio_out(uio_out),
    .uo_out(uo_out)
  );
`else
  // RTL version has NO power pins
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
`endif

endmodule
