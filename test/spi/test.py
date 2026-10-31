import random
import cocotb
from cocotb.triggers import Timer, RisingEdge, ReadOnly

SCLK_NS = 200

async def init(dut, cpol=0):
    dut.i_sclk.value = cpol
    dut.i_mosi.value = 0
    dut.i_cs_n.value = 0
    await Timer(SCLK_NS, "ns")
    dut.i_cs_n.value = 1 # rising edge of i_cs_n = reset
    await Timer(SCLK_NS, "ns")


async def spi_send_stream(dut, data, cpol=0, sclk_ns=SCLK_NS, gap_bits=0, nbits_last=8):
    half = sclk_ns // 2
    cpha = cpol
    dut.i_sclk.value = cpol
    dut.i_cs_n.value = 0
    await Timer(half, "ns")

    for idx, byte in enumerate(data):
        nbits = nbits_last if idx == len(data) - 1 else 8
        for i in range(7, 7 - nbits, -1):
            b = (byte >> i) & 1
            if cpha == 0: # mode 0: set data, rise (sample), fall
                dut.i_mosi.value = b
                await Timer(half, "ns")
                dut.i_sclk.value = 1
                await Timer(half, "ns")
                dut.i_sclk.value = 0
            else: # mode 3: fall + set data, rise (sample)
                dut.i_sclk.value = 0
                dut.i_mosi.value = b
                await Timer(half, "ns")
                dut.i_sclk.value = 1
                await Timer(half, "ns")
        if gap_bits:
            await Timer(sclk_ns * gap_bits, "ns")

    await Timer(half, "ns")
    dut.i_cs_n.value = 1
    await Timer(half, "ns")


async def collect(dut, received):
    while True:
        await RisingEdge(dut.o_data_valid)
        await ReadOnly() # let o_data_out settle in the same timestep
        received.append(int(dut.o_data_out.value))

########################################################################
#################### SPI TEST BENCH ####################################

@cocotb.test()
async def rx_stream_512(dut):
    for cpol in (0, 1):
        await init(dut, cpol)
        data = [random.getrandbits(8) for _ in range(512)]
        received = []
        mon = cocotb.start_soon(collect(dut, received))

        await spi_send_stream(dut, data, cpol)
        mon.cancel()

        mode = 0 if cpol == 0 else 3
        assert len(received) == 512, f"mode {mode}: got {len(received)} bytes, expected 512"
        for n, (exp, got) in enumerate(zip(data, received)):
            assert exp == got, f"mode {mode}, byte {n}: sent {exp:#04x}, got {got:#04x}"
        assert dut.o_data_valid.value == 0, "o_data_valid should be cleared after CS goes high"


@cocotb.test()
async def rx_aborted_frame(dut):
    await init(dut, 0)
    received = []
    mon = cocotb.start_soon(collect(dut, received))

    await spi_send_stream(dut, [0xFF], 0, nbits_last=5)   # partial byte
    assert received == [], "valid pulsed on a partial byte"

    await spi_send_stream(dut, [0xA5], 0)                 # fresh full byte
    mon.cancel()
    assert received == [0xA5], f"bit counter did not reset, got {received}"


@cocotb.test()
async def rx_gaps_between_bytes(dut):
    """SCLK idles between bytes while CS stays low."""
    for cpol in (0, 1):
        await init(dut, cpol)
        data = [random.getrandbits(8) for _ in range(32)]
        received = []
        mon = cocotb.start_soon(collect(dut, received))
        await spi_send_stream(dut, data, cpol, gap_bits=3)
        mon.cancel()
        assert received == data