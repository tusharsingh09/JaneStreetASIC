/*
 * Module to provide varying clocks to all standardc cores,
 * consists of 8 independent clock dividers with configuration registers and output mapping
 */

`default_nettype none

module CLOCK_GENERATION_UNIT(
    input wire i_rst, // negative edge reset signal
    input wire i_clk, // master clock to be divided

    output wire [7:0] o_clk // 8 different output clocks
    // each will be connected to its respective core
);

reg [31:0] m_divisor_config_reg [7:0];
reg [7:0] m_clk;

genvar i;
generate for (i=0; i < 8; i++) begin : dividers
    CLOCK_DIVIDER_UNIT divider_unit(
        .i_rst(i_rst),
        .i_clk(i_clk),

        .i_divisor(m_divisor_config_reg[i]), // for now
        .o_clk(o_clk[i])
    );
end
endgenerate

always@(negedge i_clk or negedge i_rst) begin
    if(i_rst == 1'b0) begin
        m_clk <= 8'd0;
    end
end

assign o_clk = m_clk;

endmodule