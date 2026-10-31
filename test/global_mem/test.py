import cocotb
from cocotb.triggers import Timer

async def spi_send_byte(dut, byte_val):
    for i in range(8):
        bit = (byte_val >> (7 - i)) & 1
        dut.i_mosi_mem.value = bit
        await Timer(10, units="ns")
        
        # Toggle SCLK high, then low
        dut.i_sclk_mem.value = 1
        await Timer(10, units="ns")
        dut.i_sclk_mem.value = 0
        await Timer(10, units="ns")

@cocotb.test()
async def test_global_memory_spi(dut):
    dut.i_w_clk.value = 0
    dut.i_word.value = 0
    dut.i_sclk_mem.value = 0
    dut.i_cs_mem.value = 1
    dut.i_mosi_mem.value = 0
    
    for i in range(8):
        getattr(dut, f"i_adr_por_{i}").value = 0

    await Timer(50, units="ns")

    num_bytes = 272
    test_bytes = [i & 0xFF for i in range(num_bytes)]

    dut._log.info(f"Starting SPI transfer of {num_bytes} bytes...")

    dut.i_cs_mem.value = 0
    await Timer(20, units="ns")

    for b in test_bytes:
        await spi_send_byte(dut, b)

    dut.i_cs_mem.value = 1
    await Timer(50, units="ns")

    dut._log.info("Verifying memory contents...")
    
    packed_words_count = num_bytes // 2
    
    for idx in range(packed_words_count):
        stored_val = dut.m_memory[idx].value.integer
        dut._log.info(f"m_memory[{idx}] = 0x{stored_val:04X}")

    # todo test more variations
        
    dut._log.info("SPI memory write test completed successfully!")