from typing import List, Optional
from pathlib import Path
import cocotb
from utility import to_32_bit, to_32_bit_unsigned
from cocotb.runner import get_runner
from cocotb.triggers import FallingEdge, Timer, RisingEdge
from cocotb.clock import Clock
from hypothesis.strategies import integers, lists, data

async def _enable_and_wait(dut):
    cocotb.start_soon(Clock(dut.i_clock, 1, units="ns").start())
    await Timer(5, units="ns")  # wait a bit

    dut.i_enable.value=1
    await RisingEdge(dut.i_clock)

@cocotb.test()
async def test_NOP_does_nothing(dut):
    await _enable_and_wait(dut)

    dut.i_op_code.value=0
    for _ in range(0,10):
        await RisingEdge(dut.i_clock)
        assert dut.o_pc.value == 0

@cocotb.test()
async def test_INC_increments_correctly(dut):
    await _enable_and_wait(dut)

    dut.i_op_code.value=0b01
    await RisingEdge(dut.i_clock)
    await RisingEdge(dut.i_clock)

    for i in range(0,10):
        assert dut.o_pc.value == i
        await RisingEdge(dut.i_clock)

def test_pc():
    proj_path = Path(__file__).resolve().parent
    src_path = proj_path.parent.parent / "src"

    vhdl_sources = [src_path / "pc.vhdl", 
                    src_path / "constants.vhdl"]

    runner = get_runner("ghdl")
    runner.build(
        vhdl_sources=vhdl_sources,
        hdl_toplevel="pc",
        always=True,
        build_args=["--std=08"]
    )

    runner.test(hdl_toplevel="pc",
                test_module="test_pc,",
                test_args=["--std=08"]
                )

if __name__ == "__main__":
    test_pc()
