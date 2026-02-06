`default_nettype none

module tt_um_ay5876_d_flip_flop (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    wire din = ui_in[0];
    reg  q;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) q <= 1'b0;
        else        q <= din;
    end

    assign uo_out[0] = q;
    assign uo_out[7:1] = 7'b0;

    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

    wire _unused = &{ena, ui_in[7:1], uio_in, 1'b0};

endmodule
