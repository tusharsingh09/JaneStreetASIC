`default_nettype none

// single write port at reset
// octa port output for each core
module GLOBAL_MEMORY(
    input wire i_w_clk, // clock to write configs and instructions,
    input wire [15:0] i_word, // data to be written,

    input wire i_sclk_mem, // input clock routes to spi receiver
    input wire i_cs_mem, // spi rx cs line
    input wire i_mosi_mem, // spi rx line

    input wire [4:0] i_adr_por_0, // input port 0 (0x0000 - 0x001f) pad with 00 MSB to access instr for PI core 0
    input wire [4:0] i_adr_por_1, // input port 0 (0x0020 - 0x003f) pad with 00 MSB to access instr for PI core 1
    input wire [4:0] i_adr_por_2, // input port 0 (0x0040 - 0x005f) pad with 00 MSB to access instr for PI core 2
    input wire [4:0] i_adr_por_3, // input port 0 (0x0060 - 0x007f) pad with 00 MSB to access instr for PI core 3
    input wire [4:0] i_adr_por_4, // input port 0 (0x0080 - 0x009f) pad with 00 MSB to access instr for PO core 0
    input wire [4:0] i_adr_por_5, // input port 0 (0x00a0 - 0x00bf) pad with 00 MSB to access instr for PO core 1
    input wire [4:0] i_adr_por_6, // input port 0 (0x00c0 - 0x00df) pad with 00 MSB to access instr for PO core 2
    input wire [4:0] i_adr_por_7, // input port 0 (0x00e0 - 0x00ff) pad with 00 MSB to access instr for PO core 3

    output wire [15:0] o_data_por_0, // instructions output for PI0 core
    output wire [15:0] o_data_por_1, // instructions output for PI1 core
    output wire [15:0] o_data_por_2, // instructions output for PI2 core
    output wire [15:0] o_data_por_3, // instructions output for PI3 core
    output wire [15:0] o_data_por_4, // instructions output for PO0 core
    output wire [15:0] o_data_por_5, // instructions output for PO1 core
    output wire [15:0] o_data_por_6, // instructions output for PO2 core
    output wire [15:0] o_data_por_7 // instructions output for PO3 core
);

local parameter INSTRUCTION_WORD_SIZE = 16;
local parameter INSTRUCTION_MEM_SIZE_PER_CORE = 32;
local parameter CLOCK_CONFIG_DIVISOR_SIZE = 32;

// spi vars
wire [7:0] m_spi_rx_output;
wire m_spi_output_valid;

// packer vars
wire m_packer_o_clk;
wire [15:0] m_packer_o_data;

SPI_RX m_spi_rx(
    .i_sclk(i_sclk_mem),
    .i_cs_n(i_cs_mem),
    .i_mosi(i_mosi_mem),
    
    .o_data_out(m_spi_rx_output),
    .o_data_valid(m_spi_output_valid)
);

SPI_PACKER m_spi_packer(
    .i_data(m_spi_rx_output),
    .i_valid(m_spi_output_valid),
    .i_cs(i_cs_mem),

    .o_clk(m_packer_o_clk), // sample into memory every positive edge of this clock
    .o_data(m_packer_o_data)
);



reg [INSTRUCTION_WORD_SIZE - 1:0] m_memory [8*(CLOCK_CONFIG_DIVISOR_SIZE + INSTRUCTION_MEM_SIZE_PER_CORE)-1:0];

endmodule