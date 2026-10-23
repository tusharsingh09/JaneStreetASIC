/*
 * SPI receiver to get instructions and configuration from host MCU.
 * Received bytes will be packed into 16 bits and written to memory.
 */

 `default_nettype none

module SPI_RX (
    input  wire i_sclk,       
    input  wire i_cs_n,
    input  wire i_mosi,
    output reg [7:0] o_data_out,
    output reg  o_data_valid
);

reg [2:0] m_bit_count;
reg [7:0] m_shift_reg;

always @(posedge i_sclk or posedge i_cs_n) begin
    if (i_cs_n) begin
        m_bit_count  <= 3'd0;
        m_shift_reg  <= 8'd0;
        o_data_valid <= 1'b0;
    end else begin
        o_data_valid <= 1'b0;
            
        m_shift_reg <= {m_shift_reg[6:0], i_mosi}; 

        if (m_bit_count == 3'd7) begin
            m_bit_count  <= 3'd0;
            o_data_out   <= {m_shift_reg[6:0], i_mosi};
            o_data_valid <= 1'b1;
        end else begin
            m_bit_count  <= m_bit_count + 3'd1;
        end
    end
end

// `define DEBUG
`ifdef DEBUG

initial begin
    $dumpfile("tb_spi_rx.fst");
    $dumpvars(0, SPI_RX);
end

`endif

endmodule