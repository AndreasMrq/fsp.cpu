from typing import List, Optional
from pathlib import Path
import cocotb
from utility import to_32_bit, to_32_bit_unsigned
from cocotb.runner import get_runner
from cocotb.triggers import FallingEdge, Timer, RisingEdge
from cocotb.clock import Clock
from hypothesis.strategies import integers, lists, data

def _generate_ints(min:Optional[int],
                           max:Optional[int], max_numbers=100) -> List[int]:
    integer_strat =integers(min_value=min, max_value=max)
    list_strat = lists(integer_strat,min_size=10,max_size=max_numbers)
    return list_strat.example()


async def _enable_and_wait(dut):
    cocotb.start_soon(Clock(dut.i_clock, 1, units="ns").start())
    await Timer(5, units="ns")  # wait a bit

    dut.i_enable.value=1
    await RisingEdge(dut.i_clock)



@cocotb.test()
async def test_IMM_ADDI(dut):
    await _enable_and_wait(dut)

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

            expected_result = to_32_bit(immediate + dat)
            assert bin(dut.o_data_result.value) == bin(expected_result)

@cocotb.test()
async def test_IMM_SLTI(dut):
    await _enable_and_wait(dut)

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
    await _enable_and_wait(dut)

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
    await _enable_and_wait(dut)

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

            extended_imm = to_32_bit_unsigned(immediate)
            expected_result = 1 if dat<extended_imm else 0
            assert dut.o_data_result.value == expected_result

@cocotb.test()
async def test_IMM_XORI(dut):
    await _enable_and_wait(dut)

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

            extended_imm = to_32_bit(immediate)
            dat32 = to_32_bit(dat)
            expected_result = extended_imm ^ dat32
            assert dut.o_data_result.value == expected_result

@cocotb.test()
async def test_IMM_ORI(dut):
    await _enable_and_wait(dut)

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

            extended_imm = to_32_bit(immediate)
            dat32 = to_32_bit(dat)
            expected_result = extended_imm | dat32
            assert dut.o_data_result.value == expected_result

@cocotb.test()
async def test_IMM_ANDI(dut):
    await _enable_and_wait(dut)

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

            extended_imm = to_32_bit(immediate)
            dat32 = to_32_bit(dat)
            expected_result = extended_imm & dat32
            assert dut.o_data_result.value == expected_result

@cocotb.test()
async def test_IMM_SLLI(dut):
    await _enable_and_wait(dut)

    # generate 12 bit signed immediates
    immediates = _generate_ints(0,(1<<5)-1)
    # generate 31 bit ints as data
    data = _generate_ints(-((1<<31)-1), ((1<<31)-1))

    for immediate in immediates:
        for dat in data:
            dut.i_op_code.value=0b0010011 #op imm
            dut.i_fun3.value=0b001 #SLLI
            dut.i_data_s1.value=dat
            dut.i_data_immediate.value=immediate

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            expected_result = to_32_bit(dat << immediate)
            assert dut.o_data_result.value == expected_result

@cocotb.test()
async def test_IMM_SRLI(dut):
    await _enable_and_wait(dut)

    # generate 12 bit signed immediates
    immediates = _generate_ints(0,(1<<5)-1)
    # generate 31 bit ints as data
    data = _generate_ints(-((1<<31)-1), ((1<<31)-1))

    for immediate in immediates:
        for dat in data:
            dut.i_op_code.value=0b0010011 #op imm
            dut.i_fun3.value=0b101 #SRLI
            dut.i_fun7.value=0b0
            dut.i_data_s1.value=dat
            dut.i_data_immediate.value=immediate

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            expected_result = to_32_bit(to_32_bit(dat) >> immediate)
            assert dut.o_data_result.value == expected_result

@cocotb.test()
async def test_IMM_SRAI_for_positive_data(dut):
    await _enable_and_wait(dut)

    # generate 12 bit signed immediates
    immediates = _generate_ints(0,(1<<5)-1)
    # generate 31 bit ints as data
    data = _generate_ints(0, ((1<<31)-1))

    for immediate in immediates:
        for dat in data:
            dut.i_op_code.value=0b0010011 #op imm
            dut.i_fun3.value=0b101 #SRLI
            dut.i_fun7.value= 1<<5
            dut.i_data_s1.value=dat
            dut.i_data_immediate.value=immediate

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            expected_result = to_32_bit(dat >> immediate)
            assert dut.o_data_result.value == expected_result

@cocotb.test()
async def test_IMM_SRAI_for_negative_data(dut):
    await _enable_and_wait(dut)

    # generate 12 bit signed immediates
    immediates = _generate_ints(0,(1<<5)-1)
    # generate 31 bit ints as data
    data = _generate_ints(-(1<<31)+1, 0)

    for immediate in immediates:
        for dat in data:
            dut.i_op_code.value=0b0010011 #op imm
            dut.i_fun3.value=0b101 #SRLI
            dut.i_fun7.value= 1<<5
            dut.i_data_s1.value=dat
            dut.i_data_immediate.value=immediate

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            expected_result = to_32_bit(dat >> immediate)
            assert dut.o_data_result.value == expected_result

@cocotb.test()
async def test_LUI(dut):
    await _enable_and_wait(dut)

    # generate 20 bit immediates
    immediates = _generate_ints(0,(1<<20)-1)

    for immediate in immediates:
        dut.i_op_code.value=0b0110111 #op lui
        dut.i_data_immediate.value=immediate

        await RisingEdge(dut.i_clock)
        await RisingEdge(dut.i_clock)

        assert dut.o_data_result.value == (immediate << 12)

@cocotb.test()
async def test_AUIPC(dut):
    await _enable_and_wait(dut)

    # generate 20 bit immediates
    immediates = _generate_ints(0,(1<<20)-1)
    data = _generate_ints(0,(1<<31)-1)

    for immediate in immediates:
        for dat in data:
            dut.i_op_code.value=0b0010111 #op auipc
            dut.i_data_immediate.value=immediate
            dut.i_program_counter.value = dat
    
            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            expected_result = to_32_bit((immediate<<12) + dat)
            assert dut.o_data_result.value == expected_result


@cocotb.test()
async def test_REGREG_ADD(dut):
    await _enable_and_wait(dut)

    # generate 31 bit ints as data
    data_s1 = _generate_ints(-((1<<30)-1), ((1<<30)-1))
    data_s2 = _generate_ints(-((1<<30)-1), ((1<<30)-1))

    for s1 in data_s1:
        for s2 in data_s2:
            dut.i_op_code.value=0b0110011 #op regreg
            dut.i_fun3.value=0b000 #addi
            dut.i_fun7.value=0b0000000
            dut.i_data_s1.value=s1
            dut.i_data_s2.value=s2

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            expected_result = to_32_bit(s1+s2)
            assert bin(dut.o_data_result.value) == bin(expected_result)

@cocotb.test()
async def test_REGREG_SUB(dut):
    await _enable_and_wait(dut)

    # generate 31 bit ints as data
    data_s1 = _generate_ints(-((1<<30)-1), ((1<<30)-1))
    data_s2 = _generate_ints(-((1<<30)-1), ((1<<30)-1))

    for s1 in data_s1:
        for s2 in data_s2:
            dut.i_op_code.value=0b0110011 #op regreg
            dut.i_fun3.value=0b000 #addi
            dut.i_fun7.value=0b0100000
            dut.i_data_s1.value=s1
            dut.i_data_s2.value=s2

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            expected_result = to_32_bit(s1-s2)
            assert bin(dut.o_data_result.value) == bin(expected_result)
            
@cocotb.test()
async def test_REGREG_SLT(dut):
    await _enable_and_wait(dut)

    data_s1 = _generate_ints(-((1<<30)-1), ((1<<30)-1))
    data_s2 = _generate_ints(-((1<<30)-1), ((1<<30)-1))

    for s1 in data_s1:
        for s2 in data_s2:
            dut.i_op_code.value=0b0110011 #op regreg
            dut.i_fun3.value=0b010 #slt
            dut.i_fun7.value=0b0000000
            dut.i_data_s1.value=s1
            dut.i_data_s2.value=s2

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            expected_result = 1 if s1<s2 else 0
            assert bin(dut.o_data_result.value) == bin(expected_result)

@cocotb.test()
async def test_REGREG_SLTU(dut):
    await _enable_and_wait(dut)

    data_s1 = _generate_ints(0, ((1<<32)-1))
    data_s2 = _generate_ints(0, ((1<<32)-1))

    for s1 in data_s1:
        for s2 in data_s2:
            dut.i_op_code.value=0b0110011 #op regreg
            dut.i_fun3.value=0b011 #slt
            dut.i_fun7.value=0b0000000
            dut.i_data_s1.value=s1
            dut.i_data_s2.value=s2

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            expected_result = 1 if s1<s2 else 0
            assert bin(dut.o_data_result.value) == bin(expected_result)


@cocotb.test()
async def test_REGREG_OR(dut):
    await _enable_and_wait(dut)

    data_s1 = _generate_ints(0, ((1<<32)-1))
    data_s2 = _generate_ints(0, ((1<<32)-1))

    for s1 in data_s1:
        for s2 in data_s2:
            dut.i_op_code.value=0b0110011 #op regreg
            dut.i_fun3.value=0b110 #or
            dut.i_fun7.value=0b0000000
            dut.i_data_s1.value=s1
            dut.i_data_s2.value=s2

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            expected_result = s1 | s2
            assert bin(dut.o_data_result.value) == bin(expected_result)

@cocotb.test()
async def test_REGREG_AND(dut):
    await _enable_and_wait(dut)

    data_s1 = _generate_ints(0, ((1<<32)-1))
    data_s2 = _generate_ints(0, ((1<<32)-1))

    for s1 in data_s1:
        for s2 in data_s2:
            dut.i_op_code.value=0b0110011 #op regreg
            dut.i_fun3.value=0b111 #and
            dut.i_fun7.value=0b0000000
            dut.i_data_s1.value=s1
            dut.i_data_s2.value=s2

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            expected_result = s1 & s2
            assert bin(dut.o_data_result.value) == bin(expected_result)


@cocotb.test()
async def test_REGREG_XOR(dut):
    await _enable_and_wait(dut)

    data_s1 = _generate_ints(0, ((1<<32)-1))
    data_s2 = _generate_ints(0, ((1<<32)-1))

    for s1 in data_s1:
        for s2 in data_s2:
            dut.i_op_code.value=0b0110011 #op regreg
            dut.i_fun3.value=0b100 #xor
            dut.i_fun7.value=0b0000000
            dut.i_data_s1.value=s1
            dut.i_data_s2.value=s2

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            expected_result = s1 ^ s2
            assert bin(dut.o_data_result.value) == bin(expected_result)

@cocotb.test()
async def test_REGREG_SLL(dut):
    await _enable_and_wait(dut)

    # generate 31 bit ints as data
    data_s1 = _generate_ints(-((1<<30)-1), ((1<<30)-1))
    data_s2 = _generate_ints(0, ((1<<5)-1))

    for s1 in data_s1:
        for s2 in data_s2:
            dut.i_op_code.value=0b0110011 #op regreg
            dut.i_fun3.value=0b001 #sll
            dut.i_fun7.value=0b0000000
            dut.i_data_s1.value=s1
            dut.i_data_s2.value=s2

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            expected_result = to_32_bit(s1<<s2)
            assert dut.o_data_result.value == expected_result

@cocotb.test()
async def test_REGREG_SRL(dut):
    await _enable_and_wait(dut)

    # generate 31 bit ints as data
    data_s1 = _generate_ints(-((1<<30)-1), ((1<<30)-1))
    data_s2 = _generate_ints(0, ((1<<5)-1))

    for s1 in data_s1:
        for s2 in data_s2:
            dut.i_op_code.value=0b0110011 #op regreg
            dut.i_fun3.value=0b101 #srl
            dut.i_fun7.value=0b0000000
            dut.i_data_s1.value=s1
            dut.i_data_s2.value=s2

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            expected_result = to_32_bit((to_32_bit(s1))>>s2)
            assert bin(dut.o_data_result.value) == bin(expected_result)

@cocotb.test()
async def test_REGREG_SRA(dut):
    await _enable_and_wait(dut)

    # generate 31 bit ints as data
    data_s1 = _generate_ints(-((1<<30)-1), ((1<<30)-1))
    data_s2 = _generate_ints(0, ((1<<5)-1))

    for s1 in data_s1:
        for s2 in data_s2:
            dut.i_op_code.value=0b0110011 #op regreg
            dut.i_fun3.value=0b101 #srl
            dut.i_fun7.value=0b0100000
            dut.i_data_s1.value=s1
            dut.i_data_s2.value=s2

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            expected_result = to_32_bit(s1>>s2)
            assert bin(dut.o_data_result.value) == bin(expected_result)

@cocotb.test()
async def test_JAL(dut):
    await _enable_and_wait(dut)

    # generate 31 bit ints as data
    program_counter = _generate_ints(0, (1<<31)-1)
    immediates = _generate_ints(-(1<<19)+1, (1<<19)-1)

    for pc in program_counter:
        for immediate in immediates:
            dut.i_op_code.value=0b1101111 #op JAL
            dut.i_program_counter.value=pc
            dut.i_data_immediate.value=immediate

            await RisingEdge(dut.i_clock)
            await RisingEdge(dut.i_clock)

            assert dut.o_data_result.value == pc + 4
            assert dut.o_should_branch.value == 1
            assert dut.o_branch_target.value == to_32_bit(pc+immediate)

@cocotb.test()
async def test_JALR(dut):
    await _enable_and_wait(dut)

    # generate 31 bit ints as data and pc
    program_counter = _generate_ints(0, (1<<31)-1)
    data_s1 = _generate_ints(0, (1<<31)-1)
    immediates = _generate_ints(-(1<<11)+1, (1<<11)-1)

    for pc in program_counter:
        for immediate in immediates:
            for data in data_s1:
                dut.i_op_code.value=0b1100111 #op JALR
                dut.i_program_counter.value=pc
                dut.i_data_s1.value=data
                dut.i_data_immediate.value=immediate
    
                await RisingEdge(dut.i_clock)
                await RisingEdge(dut.i_clock)
    
                assert dut.o_data_result.value == pc + 4
                assert dut.o_should_branch.value == 1
                expected_result = to_32_bit(data+immediate) & 0xFFFFFFFE
                assert dut.o_branch_target.value == expected_result

@cocotb.test()
async def test_BRANCH_BEQ(dut):
    await _enable_and_wait(dut)

    # generate 31 bit ints as data and pc
    program_counter = _generate_ints(0, (1<<31)-1, max_numbers=10 )
    data = _generate_ints(-(1<<31)+1, (1<<31)-1, max_numbers=10)
    immediates = _generate_ints(-(1<<11)+1, (1<<11)-1, max_numbers=10)

    for pc in program_counter:
        for immediate in immediates:
            for data1 in data:
                for data2 in data:
                    dut.i_op_code.value=0b1100011 #op BRANCH
                    dut.i_fun3.value=0b000 #op BEQ
                    dut.i_program_counter.value=pc
                    dut.i_data_s1.value=data1
                    dut.i_data_s2.value=data2
                    dut.i_data_immediate.value=immediate
        
                    await RisingEdge(dut.i_clock)
                    await RisingEdge(dut.i_clock)
        
                    should_branch = data1 == data2
                    target = to_32_bit(pc + immediate)
                    assert dut.o_should_branch.value == should_branch
                    if should_branch:
                        assert dut.o_branch_target.value == target

@cocotb.test()
async def test_BRANCH_BNE(dut):
    await _enable_and_wait(dut)

    # generate 31 bit ints as data and pc
    program_counter = _generate_ints(0, (1<<31)-1, max_numbers=10 )
    data = _generate_ints(-(1<<31)+1, (1<<31)-1, max_numbers=10)
    immediates = _generate_ints(-(1<<11)+1, (1<<11)-1, max_numbers=10)

    for pc in program_counter:
        for immediate in immediates:
            for data1 in data:
                for data2 in data:
                    dut.i_op_code.value=0b1100011 #op BRANCH
                    dut.i_fun3.value=0b001 #op BNE
                    dut.i_program_counter.value=pc
                    dut.i_data_s1.value=data1
                    dut.i_data_s2.value=data2
                    dut.i_data_immediate.value=immediate
        
                    await RisingEdge(dut.i_clock)
                    await RisingEdge(dut.i_clock)
        
                    should_branch = data1 != data2
                    target = to_32_bit(pc + immediate)
                    assert dut.o_should_branch.value == should_branch
                    if should_branch:
                        assert dut.o_branch_target.value == target

@cocotb.test()
async def test_BRANCH_BLT(dut):
    await _enable_and_wait(dut)

    # generate 31 bit ints as data and pc
    program_counter = _generate_ints(0, (1<<31)-1, max_numbers=10 )
    data = _generate_ints(-(1<<31)+1, (1<<31)-1, max_numbers=10)
    immediates = _generate_ints(-(1<<11)+1, (1<<11)-1, max_numbers=10)

    for pc in program_counter:
        for immediate in immediates:
            for data1 in data:
                for data2 in data:
                    dut.i_op_code.value=0b1100011 #op BRANCH
                    dut.i_fun3.value=0b100 #op BLT
                    dut.i_program_counter.value=pc
                    dut.i_data_s1.value=data1
                    dut.i_data_s2.value=data2
                    dut.i_data_immediate.value=immediate
        
                    await RisingEdge(dut.i_clock)
                    await RisingEdge(dut.i_clock)
        
                    should_branch = data1 < data2
                    target = to_32_bit(pc + immediate)
                    assert dut.o_should_branch.value == should_branch
                    if should_branch:
                        assert dut.o_branch_target.value == target

@cocotb.test()
async def test_BRANCH_BGE(dut):
    await _enable_and_wait(dut)

    # generate 31 bit ints as data and pc
    program_counter = _generate_ints(0, (1<<31)-1, max_numbers=10 )
    data = _generate_ints(-(1<<31)+1, (1<<31)-1, max_numbers=10)
    immediates = _generate_ints(-(1<<11)+1, (1<<11)-1, max_numbers=10)

    for pc in program_counter:
        for immediate in immediates:
            for data1 in data:
                for data2 in data:
                    dut.i_op_code.value=0b1100011 #op BRANCH
                    dut.i_fun3.value=0b101 #op BLT
                    dut.i_program_counter.value=pc
                    dut.i_data_s1.value=data1
                    dut.i_data_s2.value=data2
                    dut.i_data_immediate.value=immediate
        
                    await RisingEdge(dut.i_clock)
                    await RisingEdge(dut.i_clock)
        
                    should_branch = data1 >= data2
                    target = to_32_bit(pc + immediate)
                    assert dut.o_should_branch.value == should_branch
                    if should_branch:
                        assert dut.o_branch_target.value == target

@cocotb.test()
async def test_BRANCH_BLTU(dut):
    await _enable_and_wait(dut)

    # generate 31 bit ints as data and pc
    program_counter = _generate_ints(0, (1<<31)-1, max_numbers=10 )
    data = _generate_ints(-(1<<31)+1, (1<<31)-1, max_numbers=10)
    immediates = _generate_ints(-(1<<11)+1, (1<<11)-1, max_numbers=10)

    for pc in program_counter:
        for immediate in immediates:
            for data1 in data:
                for data2 in data:
                    dut.i_op_code.value=0b1100011 #op BRANCH
                    dut.i_fun3.value=0b110 #op BLT
                    dut.i_program_counter.value=pc
                    dut.i_data_s1.value=data1
                    dut.i_data_s2.value=data2
                    dut.i_data_immediate.value=immediate
        
                    await RisingEdge(dut.i_clock)
                    await RisingEdge(dut.i_clock)
        
                    should_branch = to_32_bit_unsigned(data1) < to_32_bit_unsigned(data2)
                    target = to_32_bit(pc + immediate)
                    assert dut.o_should_branch.value == should_branch
                    if should_branch:
                        assert dut.o_branch_target.value == target

@cocotb.test()
async def test_BRANCH_BGEU(dut):
    await _enable_and_wait(dut)

    # generate 31 bit ints as data and pc
    program_counter = _generate_ints(0, (1<<31)-1, max_numbers=10 )
    data = _generate_ints(-(1<<31)+1, (1<<31)-1, max_numbers=10)
    immediates = _generate_ints(-(1<<11)+1, (1<<11)-1, max_numbers=10)

    for pc in program_counter:
        for immediate in immediates:
            for data1 in data:
                for data2 in data:
                    dut.i_op_code.value=0b1100011 #op BRANCH
                    dut.i_fun3.value=0b111 #op BLT
                    dut.i_program_counter.value=pc
                    dut.i_data_s1.value=data1
                    dut.i_data_s2.value=data2
                    dut.i_data_immediate.value=immediate
        
                    await RisingEdge(dut.i_clock)
                    await RisingEdge(dut.i_clock)
        
                    should_branch = to_32_bit_unsigned(data1) >= to_32_bit_unsigned(data2)
                    target = to_32_bit(pc + immediate)
                    assert dut.o_should_branch.value == should_branch
                    if should_branch:
                        assert dut.o_branch_target.value == target

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
