/*
 * Single clock divider unit, to clock one independent core. Each core receives clock from one of these.
 */

`default_nettype none

module CLOCK_DIVIDER_UNIT(
    input wire i_rst, // reset input signal
    input wire i_clk, // master clock signal routed through the CLK pin of the ASIC

    input wire [31:0] i_divisor, // master clock is divident

    output wire o_clk
);

reg [31:0] m_cnt;
reg m_clk;

wire [31:0] m_half_divisor;

always@(negedge i_clk or negedge i_rst) begin
    if(i_rst == 1'b0) begin
        m_cnt <= 32'd0;
        m_clk <= 1'b1;
    end else if(i_divisor <= 32'd1) begin
        m_clk <= i_clk;
        m_cnt <= 32'd0;
    end else begin
        if (m_cnt >= i_divisor - 1) begin
                m_cnt <= 32'd0;
                m_clk <= ~m_clk;
            end 
        else if (m_cnt == m_half_divisor - 1) begin
            m_cnt   <= m_cnt + 1'b1;
            m_clk <= ~m_clk;
        end 
        else begin
            m_cnt   <= m_cnt + 1'b1;
        end
    end
    // m_cnt <= m_cnt + 32'b1;
end

assign m_half_divisor = i_divisor >> 1;
assign o_clk = m_clk;

// remove later
initial begin
    $dumpfile("tb_div.fst");
    $dumpvars(0, CLOCK_DIVIDER_UNIT);
end

endmodule