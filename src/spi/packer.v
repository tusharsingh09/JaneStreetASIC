`default_nettype none

module SPI_PACKER(
    input wire [7:0] i_data,
    input wire i_valid,

    input wire i_cs, // active low when spi is active
    // when this is high spi no active
    // whenever cs is high, m_cnt will reset to 0 so as to allow following 16 bytes to be written
    // acts as divider for i_valid signal

    output wire o_clk, // clock for writing 16 bit o_data
    output wire [15:0] o_data
);

reg m_cnt;
reg [15:0] m_data;

always@(posedge i_cs or posedge i_valid) begin
    if(i_cs == 1'b1) begin
        m_cnt <= 1'b0;    
    end else begin
        m_cnt <= ~m_cnt;
    end
end

always@(posedge i_valid) begin
    if(m_cnt == 1'b0) begin // least significant byte (little endian used)
        m_data[7:0] <= i_data;
    end else begin
        m_data[15:0] <= i_data;
    end
end

assign o_clk = ~m_cnt;

endmodule