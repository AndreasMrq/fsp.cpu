from pathlib import Path
import cocotb
from cocotb.runner import get_runner
from cocotb.triggers import FallingEdge, Timer, RisingEdge
from cocotb.clock import Clock
from hypothesis import given
from hypothesis.strategies import integers
import pytest

rd_lsb=7
r1_lsb=15
r2_lsb=20

@cocotb.test()
async def test_op_code_forwarded_correctly(dut):
    cocotb.start_soon(Clock(dut.i_clock, 1, units="ns").start())
    await Timer(5, units="ns")  # wait a bit

    dut.i_enable.value=1
    await RisingEdge(dut.i_clock)

    dut.i_data_instruction.value=1

    await RisingEdge(dut.i_clock)
    await RisingEdge(dut.i_clock)

    assert dut.o_opcode.value == 1

@cocotb.test()
async def test_rd_decoded_correctyl(dut):
    cocotb.start_soon(Clock(dut.i_clock, 1, units="ns").start())
    await Timer(5, units="ns")  # wait a bit

    dut.i_enable.value=1
    await RisingEdge(dut.i_clock)

    dut.i_data_instruction.value=1<<rd_lsb

    await RisingEdge(dut.i_clock)
    await RisingEdge(dut.i_clock)

    assert dut.o_selectdest.value == 1

@cocotb.test()
async def test_r1_decoded_correctly(dut):
    cocotb.start_soon(Clock(dut.i_clock, 1, units="ns").start())
    await Timer(5, units="ns")  # wait a bit

    dut.i_enable.value=1
    await RisingEdge(dut.i_clock)

    dut.i_data_instruction.value=1<<r1_lsb

    await RisingEdge(dut.i_clock)
    await RisingEdge(dut.i_clock)

    assert dut.o_selecta.value == 1

@cocotb.test()
async def test_r2_decoded_correctly(dut):
    cocotb.start_soon(Clock(dut.i_clock, 1, units="ns").start())
    await Timer(5, units="ns")  # wait a bit

    dut.i_enable.value=1
    await RisingEdge(dut.i_clock)

    dut.i_data_instruction.value=1<<r2_lsb

    await RisingEdge(dut.i_clock)
    await RisingEdge(dut.i_clock)

    assert dut.o_selectb.value == 1

def test_decoder():
    proj_path = Path(__file__).resolve().parent
    src_path = proj_path.parent.parent / "src"

    vhdl_sources = [src_path / "decoder.vhdl", 
                    src_path / "constants.vhdl"]

    runner = get_runner("ghdl")
    runner.build(
        vhdl_sources=vhdl_sources,
        hdl_toplevel="decoder",
        always=True,
    )

    runner.test(hdl_toplevel="decoder", test_module="test_decoder,")

if __name__ == "__main__":
    test_decoder()
