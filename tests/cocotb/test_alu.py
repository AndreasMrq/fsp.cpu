from typing import List, Optional
from pathlib import Path
import cocotb
from cocotb.runner import get_runner
from cocotb.triggers import FallingEdge, Timer, RisingEdge
from cocotb.clock import Clock
from hypothesis.strategies import integers, lists, data

def _generate_ints(min:Optional[int],
                           max:Optional[int]) -> List[int]:
    integer_strat =integers(min_value=min, max_value=max)
    list_strat = lists(integer_strat,min_size=10,max_size=100)
    return list_strat.example()

def _to_32_bit(value:int):
    return value & 0xffffffff

@cocotb.test()
async def test_IMM_ADDI(dut):
    cocotb.start_soon(Clock(dut.i_clock, 1, units="ns").start())
    await Timer(5, units="ns")  # wait a bit

    dut.i_enable.value=1
    await RisingEdge(dut.i_clock)

    # generate 12 bit signed immediates
    immediates = _generate_ints(-((1<<11)-1), ((1<<11)-1))
    # generate 31 bit ints as data
    data = _generate_ints(-((1<<30)-1), ((1<<30)-1))

    for immediate in immediates:
        for dat in data:
            dut.i_op_code.value=0b0010011 #op imm
            dut.i_fun3.value=0b000 #addi
            dut.i_data_a.value=dat
            dut.i_data_immediate.value=immediate

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            expected_result = _to_32_bit(immediate + dat)
            assert bin(dut.o_data_result.value) == bin(expected_result)

def test_alu():
    proj_path = Path(__file__).resolve().parent
    src_path = proj_path.parent.parent / "src"

    vhdl_sources = [src_path / "alu.vhdl", 
                    src_path / "constants.vhdl"]

    runner = get_runner("ghdl")
    runner.build(
        vhdl_sources=vhdl_sources,
        hdl_toplevel="alu",
        always=True,
    )

    runner.test(hdl_toplevel="alu", test_module="test_alu,")

if __name__ == "__main__":
    test_alu()
