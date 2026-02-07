`default_nettype none

module top_basys3(
    input  wire [15:0] sw,
    output wire [15:0] led
);
    // Switch mapping: SW0=A, SW1=B, SW2=C
    wire A = sw[0];
    wire B = sw[1];
    wire C = sw[2];

    // Logic: F = AB + C', Y = C'
    wire Cn = ~C;
    wire F  = (A & B) | Cn;
    wire Y  = Cn;

    // LED mapping: LED0=F, LED1=Y
    assign led[0] = F;
    assign led[1] = Y;
    assign led[15:2] = 14'b0;

endmodule
