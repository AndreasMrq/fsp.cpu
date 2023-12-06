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
    dut.i_reset.value = 1
    await Timer(5, units="ns")  # wait a bit

    dut.i_reset.value=0
    await RisingEdge(dut.i_clock)

@cocotb.test()
async def test_pipeline_execution(dut):
    await _enable_and_wait(dut)

    await RisingEdge(dut.i_clock)
    assert dut.o_active_phase.value == 0 # reset

    for _ in range(0,10):
        await RisingEdge(dut.i_clock)
        assert dut.o_active_phase.value == 1 # fetch
    
        await RisingEdge(dut.i_clock)
        assert dut.o_active_phase.value == 0b100 #decode
    
        await RisingEdge(dut.i_clock)
        assert dut.o_active_phase.value == 0b1000 #execute
    
        await RisingEdge(dut.i_clock)
        assert dut.o_active_phase.value == 0b10000 # pc

@cocotb.test()
async def test_reset(dut):
    await _enable_and_wait(dut)

    await RisingEdge(dut.i_clock)
    assert dut.o_active_phase.value == 0 # reset 1
    await RisingEdge(dut.i_clock)
    assert dut.o_active_phase.value == 1 # fetch 1

    dut.i_reset.value = 1
    await RisingEdge(dut.i_clock)
    await RisingEdge(dut.i_clock)

    dut.i_reset.value = 0
    await RisingEdge(dut.i_clock)
    await RisingEdge(dut.i_clock)

    assert dut.o_active_phase.value == 0 # reset 2
    await RisingEdge(dut.i_clock)
    assert dut.o_active_phase.value == 1 # fetch 2

def test_control_unit():
    proj_path = Path(__file__).resolve().parent
    src_path = proj_path.parent.parent / "src"

    vhdl_sources = [src_path / "control_unit.vhdl", 
                    src_path / "constants.vhdl"]

    runner = get_runner("ghdl")
    runner.build(
        vhdl_sources=vhdl_sources,
        hdl_toplevel="control_unit",
        always=True,
        build_args=["--std=08"]
    )

    runner.test(hdl_toplevel="control_unit",
                test_module="test_control_unit,",
                test_args=["--std=08"]
                )

if __name__ == "__main__":
    test_control_unit()
