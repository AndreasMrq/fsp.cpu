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

def _to_32_bit_unsigned(value:int):
    return (value & 0xffffffff) + (1<<32)

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
            dut.i_data_s1.value=dat
            dut.i_data_immediate.value=immediate

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            expected_result = _to_32_bit(immediate + dat)
            assert bin(dut.o_data_result.value) == bin(expected_result)

@cocotb.test()
async def test_IMM_SLTI(dut):
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
            dut.i_fun3.value=0b010 #slti
            dut.i_data_s1.value=dat
            dut.i_data_immediate.value=immediate

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            expected_result = 1 if dat<immediate else 0
            assert dut.o_data_result.value == expected_result

@cocotb.test()
async def test_IMM_SLTIU_positive_immediate(dut):
    cocotb.start_soon(Clock(dut.i_clock, 1, units="ns").start())
    await Timer(5, units="ns")  # wait a bit

    dut.i_enable.value=1
    await RisingEdge(dut.i_clock)

    # generate 12 bit signed immediates
    immediates = _generate_ints(0, ((1<<11)-1))
    # generate 31 bit ints as data
    data = _generate_ints(0, ((1<<31)-1))

    for immediate in immediates:
        for dat in data:
            dut.i_op_code.value=0b0010011 #op imm
            dut.i_fun3.value=0b011 #sltiu
            dut.i_data_s1.value=dat
            dut.i_data_immediate.value=immediate

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            expected_result = 1 if dat<immediate else 0
            assert dut.o_data_result.value == expected_result

@cocotb.test()
async def test_IMM_SLTIU_negative_immediate(dut):
    cocotb.start_soon(Clock(dut.i_clock, 1, units="ns").start())
    await Timer(5, units="ns")  # wait a bit

    dut.i_enable.value=1
    await RisingEdge(dut.i_clock)

    # generate 12 bit signed immediates
    immediates = _generate_ints(-((1<<11)-1),-1)
    # generate 31 bit ints as data
    data = _generate_ints(0, ((1<<31)-1))

    for immediate in immediates:
        for dat in data:
            dut.i_op_code.value=0b0010011 #op imm
            dut.i_fun3.value=0b011 #sltiu
            dut.i_data_s1.value=dat
            dut.i_data_immediate.value=immediate

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            extended_imm = _to_32_bit_unsigned(immediate)
            expected_result = 1 if dat<extended_imm else 0
            assert dut.o_data_result.value == expected_result

@cocotb.test()
async def test_IMM_XORI(dut):
    cocotb.start_soon(Clock(dut.i_clock, 1, units="ns").start())
    await Timer(5, units="ns")  # wait a bit

    dut.i_enable.value=1
    await RisingEdge(dut.i_clock)

    # generate 12 bit signed immediates
    immediates = _generate_ints(-((1<<11)-1),-1)
    # generate 31 bit ints as data
    data = _generate_ints(0, ((1<<31)-1))

    for immediate in immediates:
        for dat in data:
            dut.i_op_code.value=0b0010011 #op imm
            dut.i_fun3.value=0b100 #xori
            dut.i_data_s1.value=dat
            dut.i_data_immediate.value=immediate

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            extended_imm = _to_32_bit(immediate)
            dat32 = _to_32_bit(dat)
            expected_result = extended_imm ^ dat32
            assert dut.o_data_result.value == expected_result

@cocotb.test()
async def test_IMM_ORI(dut):
    cocotb.start_soon(Clock(dut.i_clock, 1, units="ns").start())
    await Timer(5, units="ns")  # wait a bit

    dut.i_enable.value=1
    await RisingEdge(dut.i_clock)

    # generate 12 bit signed immediates
    immediates = _generate_ints(-((1<<11)-1),-1)
    # generate 31 bit ints as data
    data = _generate_ints(0, ((1<<31)-1))

    for immediate in immediates:
        for dat in data:
            dut.i_op_code.value=0b0010011 #op imm
            dut.i_fun3.value=0b110 #ori
            dut.i_data_s1.value=dat
            dut.i_data_immediate.value=immediate

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            extended_imm = _to_32_bit(immediate)
            dat32 = _to_32_bit(dat)
            expected_result = extended_imm | dat32
            assert dut.o_data_result.value == expected_result

@cocotb.test()
async def test_IMM_ANDI(dut):
    cocotb.start_soon(Clock(dut.i_clock, 1, units="ns").start())
    await Timer(5, units="ns")  # wait a bit

    dut.i_enable.value=1
    await RisingEdge(dut.i_clock)

    # generate 12 bit signed immediates
    immediates = _generate_ints(-((1<<11)-1),-1)
    # generate 31 bit ints as data
    data = _generate_ints(0, ((1<<31)-1))

    for immediate in immediates:
        for dat in data:
            dut.i_op_code.value=0b0010011 #op imm
            dut.i_fun3.value=0b111 #andi
            dut.i_data_s1.value=dat
            dut.i_data_immediate.value=immediate

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            extended_imm = _to_32_bit(immediate)
            dat32 = _to_32_bit(dat)
            expected_result = extended_imm & dat32
            assert dut.o_data_result.value == expected_result

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
        build_args=["--std=08"]
    )

    runner.test(hdl_toplevel="alu",
                test_module="test_alu,",
                test_args=["--std=08"]
                )

if __name__ == "__main__":
    test_alu()
