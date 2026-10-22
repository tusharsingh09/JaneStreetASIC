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