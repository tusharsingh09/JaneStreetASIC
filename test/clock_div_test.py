import cocotb 
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

from cocotb.triggers import RisingEdge
from cocotb.utils import get_sim_time

async def measure_frequency(signal, time_unit="ns"):
    await RisingEdge(signal)
    t1 = get_sim_time(units=time_unit)
    
    await RisingEdge(signal)
    t2 = get_sim_time(units=time_unit)
    
    period = t2 - t1
    
    if period == 0:
        raise ValueError("Measured period is 0. Cannot calculate frequency.")
        
    scale = {"fs": 1e15, "ps": 1e12, "ns": 1e9, "us": 1e6, "ms": 1e3, "sec": 1.0}
    frequency_hz = scale[time_unit] / period
    
    return frequency_hz, period

@cocotb.test()
async def test_divider(dut):
    dut._log.info("Start")

    clock = Clock(dut.i_clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    dut._log.info("Reset")
    dut.i_rst.value = 1

    await ClockCycles(dut.i_clk, 1)
    dut.i_rst.value = 0

    await ClockCycles(dut.i_clk, 1)
    dut.i_rst.value = 1

    dut._log.info("Test project behaviour")
    dut.i_divisor.value = 7

    await ClockCycles(dut.i_clk, 20)

    dut._log.info("Measurnig frequency")
    fo, fp = await measure_frequency(dut.i_clk, "us")
    f, p = await measure_frequency(dut.o_clk, "us")

    dut._log.info(f"Frequency Original: {fo}")
    dut._log.info(f"Frequency: {f}")