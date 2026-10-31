import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_spi_packer(dut):
    dut.i_data.value = 0
    dut.i_valid.value = 0
    dut.i_cs.value = 1
    
    await Timer(20, units="ns")
    
    dut.i_cs.value = 0
    await Timer(20, units="ns")
    
    dut.i_data.value = 0x34
    dut.i_valid.value = 1
    await Timer(20, units="ns")
    dut.i_valid.value = 0
    await Timer(20, units="ns")

    dut.i_data.value = 0x12
    dut.i_valid.value = 1
    await Timer(20, units="ns")
    dut.i_valid.value = 0
    await Timer(20, units="ns")
    
    dut.i_cs.value = 1
    await Timer(20, units="ns")
    
    cocotb.log.info(f"Test completed successfully.")