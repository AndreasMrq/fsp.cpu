from typing import List, Tuple
from pathlib import Path
import cocotb
from cocotb.runner import get_runner
from cocotb.triggers import FallingEdge, Timer, RisingEdge
from cocotb.clock import Clock
from hypothesis.strategies import integers, lists, data
import pytest

rd_lsb=7
r1_lsb=15
r2_lsb=20

def _generate_sized_ints(bits: int) -> List[int]:
    integer_strat =integers(min_value=0, max_value=(1<<bits)-1)
    list_strat = lists(integer_strat,min_size=10,max_size=100)
    return list_strat.example()

def _map_to_instruction(immediate: int, mapping: List[Tuple[int,int]]):
    result = 0
    for initial,to in mapping:
        result = result + (((immediate>>initial) & 1)<<to)
    return result

@cocotb.test()
async def test_op_code_forwarded_correctly(dut):
    cocotb.start_soon(Clock(dut.i_clock, 1, units="ns").start())
    await Timer(5, units="ns")  # wait a bit

    dut.i_enable.value=1
    await RisingEdge(dut.i_clock)

    for op_code in range(0, (1<<7)-1):
        dut.i_data_instruction.value=op_code

        await RisingEdge(dut.i_clock)
        await RisingEdge(dut.i_clock)

        assert dut.o_opcode.value == op_code

@cocotb.test()
async def test_rd_decoded_correctyl(dut):
    cocotb.start_soon(Clock(dut.i_clock, 1, units="ns").start())
    await Timer(5, units="ns")  # wait a bit

    dut.i_enable.value=1
    await RisingEdge(dut.i_clock)
    
    for selectdest in range(0,(1<<5)-1):
        dut.i_data_instruction.value=selectdest<<rd_lsb

        await RisingEdge(dut.i_clock)
        await RisingEdge(dut.i_clock)

        assert dut.o_selectdest.value == selectdest

@cocotb.test()
async def test_r1_decoded_correctly(dut):
    cocotb.start_soon(Clock(dut.i_clock, 1, units="ns").start())
    await Timer(5, units="ns")  # wait a bit

    dut.i_enable.value=1
    await RisingEdge(dut.i_clock)

    for selecta in range(0,(1<<5)-1):
        dut.i_data_instruction.value=selecta<<r1_lsb

        await RisingEdge(dut.i_clock)
        await RisingEdge(dut.i_clock)

        assert dut.o_selecta.value == selecta

@cocotb.test()
async def test_r2_decoded_correctly(dut):
    cocotb.start_soon(Clock(dut.i_clock, 1, units="ns").start())
    await Timer(5, units="ns")  # wait a bit

    dut.i_enable.value=1
    await RisingEdge(dut.i_clock)

    for selectb in range(0,(1<<5)-1):
        dut.i_data_instruction.value=selectb<<r2_lsb

        await RisingEdge(dut.i_clock)
        await RisingEdge(dut.i_clock)

        assert dut.o_selectb.value == selectb

@cocotb.test()
async def test_immediate_correct_for_lui_and_auipc(dut):
    cocotb.start_soon(Clock(dut.i_clock, 1, units="ns").start())
    await Timer(5, units="ns")  # wait a bit

    dut.i_enable.value=1
    await RisingEdge(dut.i_clock)

    immediates = _generate_sized_ints(20)

    for immediate in immediates:
        for op_code in [0b0110111,0b0010111]:   
            instr = op_code + (immediate<<12)
            dut.i_data_instruction.value=instr

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            assert dut.o_data_imm.value == immediate<<12

@cocotb.test()
async def test_immediate_correct_for_JALR_and_LOAD(dut):
    cocotb.start_soon(Clock(dut.i_clock, 1, units="ns").start())
    await Timer(5, units="ns")  # wait a bit

    dut.i_enable.value=1
    await RisingEdge(dut.i_clock)

    immediates = _generate_sized_ints(12)

    for immediate in immediates:
        for op_code in [0b1100111,0b0000011]:   
            instr = op_code + (immediate<<20)
            dut.i_data_instruction.value=instr

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            assert dut.o_data_imm.value == immediate

@cocotb.test()
async def test_immediate_correct_for_JAL(dut):
    cocotb.start_soon(Clock(dut.i_clock, 1, units="ns").start())
    await Timer(5, units="ns")  # wait a bit

    dut.i_enable.value=1
    await RisingEdge(dut.i_clock)

    immediates = _generate_sized_ints(20)

    immediate_mapping = []
    for i in range(0,10):
        immediate_mapping.append((i, 21+i))
    for i in range(0,8):
        immediate_mapping.append((11 + i, 12 +i))
    immediate_mapping.append((10,20))
    immediate_mapping.append((19,31))


    for immediate in immediates:
        op_code = 0b1101111
        instr = op_code + _map_to_instruction(immediate,immediate_mapping)
        dut.i_data_instruction.value=instr

        await RisingEdge(dut.i_clock)
        await RisingEdge(dut.i_clock)

        assert dut.o_data_imm.value == (immediate<<1)

@cocotb.test()
async def test_immediate_correct_for_BRANCH(dut):
    cocotb.start_soon(Clock(dut.i_clock, 1, units="ns").start())
    await Timer(5, units="ns")  # wait a bit

    dut.i_enable.value=1
    await RisingEdge(dut.i_clock)

    immediates = _generate_sized_ints(12)

    immediate_mapping = []
    for i in range(0,4):
        immediate_mapping.append((i, 8+i))
    for i in range(0,6):
        immediate_mapping.append((4 + i, 25 +i))
    immediate_mapping.append((10,7))
    immediate_mapping.append((11,31))


    for immediate in immediates:
        op_code = 0b1100011
        instr = op_code + _map_to_instruction(immediate,immediate_mapping)
        dut.i_data_instruction.value=instr

        await RisingEdge(dut.i_clock)
        await RisingEdge(dut.i_clock)

        assert dut.o_data_imm.value == (immediate<<1)

@cocotb.test()
async def test_immediate_correct_for_STORE(dut):
    cocotb.start_soon(Clock(dut.i_clock, 1, units="ns").start())
    await Timer(5, units="ns")  # wait a bit

    dut.i_enable.value=1
    await RisingEdge(dut.i_clock)

    immediates = _generate_sized_ints(12)

    immediate_mapping = []
    for i in range(0,5):
        immediate_mapping.append((i, 7+i))
    for i in range(0,7):
        immediate_mapping.append((5 + i, 25 +i))

    for immediate in immediates:
        op_code = 0b0100011
        instr = op_code + _map_to_instruction(immediate,immediate_mapping)

        dut.i_data_instruction.value=instr

        await RisingEdge(dut.i_clock)
        await RisingEdge(dut.i_clock)

        assert dut.o_data_imm.value == immediate

@cocotb.test()
async def test_immediate_correct_for_IMM(dut):
    cocotb.start_soon(Clock(dut.i_clock, 1, units="ns").start())
    await Timer(5, units="ns")  # wait a bit

    dut.i_enable.value=1
    await RisingEdge(dut.i_clock)

    immediates = _generate_sized_ints(12)

    for immediate in immediates:
        op_code = 0b0010011
        instr = op_code + (immediate << 20) 

        dut.i_data_instruction.value=instr

        await RisingEdge(dut.i_clock)
        await RisingEdge(dut.i_clock)

        assert dut.o_data_imm.value == immediate

@cocotb.test()
async def test_function3_correct(dut):
    cocotb.start_soon(Clock(dut.i_clock, 1, units="ns").start())
    await Timer(5, units="ns")  # wait a bit

    dut.i_enable.value=1
    await RisingEdge(dut.i_clock)

    op_codes=[0b1100011, # BRANCH
              0b0000011, # LOAD
              0b0100011, # STORE
              0b0010011, # IMM
              0b0110011] # REGREG
    function3_codes = _generate_sized_ints(3)

    for fun3 in function3_codes:
        for op in op_codes:
            instr = op + (fun3 << 12) 

            dut.i_data_instruction.value=instr

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            assert dut.o_function.value == fun3

@cocotb.test()
async def test_function7_correct(dut):
    cocotb.start_soon(Clock(dut.i_clock, 1, units="ns").start())
    await Timer(5, units="ns")  # wait a bit

    dut.i_enable.value=1
    await RisingEdge(dut.i_clock)

    op_codes=[0b0010011, # IMM
              0b0110011] # REGREG
    function7_codes = _generate_sized_ints(7)

    for fun7 in function7_codes:
        for op in op_codes:
            instr = op + (fun7 << 25) 

            dut.i_data_instruction.value=instr

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            assert dut.o_function.value == (fun7<<3)

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
