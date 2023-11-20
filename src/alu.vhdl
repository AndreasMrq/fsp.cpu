library ieee;
library work;
use ieee.numeric_std.all;
use ieee.std_logic_1164.all;
use work.constants.all;

entity alu is
    port ( i_clock : in  std_logic;
           i_enable : in  std_logic;
           i_op_code : in  std_logic_vector (6 downto 0);
           i_fun3 : in std_logic_vector(2 downto 0);
           i_fun7 : in std_logic_vector(6 downto 0);
           i_data_s1 : in std_logic_vector(31 downto 0);
           i_data_s2 : in std_logic_vector(31 downto 0);
           i_data_immediate : in std_logic_vector(31 downto 0);
           i_program_counter : in std_logic_vector(31 downto 0);
           o_data_result : out std_logic_vector(31 downto 0);
           o_should_branch: out std_logic;
           o_rd_write_enable: out std_logic;
           o_branch_target: out std_logic_vector(31 downto 0)
       );
end alu;

architecture behavioral of alu is


    function execute_IMM(
    data : std_logic_vector(31 downto 0);
    immediate : std_logic_vector(31 downto 0);
    fun3 : std_logic_vector(2 downto 0);
    fun7 : std_logic_vector(6 downto 0)
) 
return std_logic_vector is 
    variable result : std_logic_vector(31 downto 0);
    variable ext_imm: signed(31 downto 0);
    variable shift: integer;
    begin
        case fun3(2 downto 0) is
            when F3_OPIMM_ADDI =>
                -- Add sign extended 12 bit immediate to data
                -- Ignore Overflow
                ext_imm := resize(signed(immediate(11 downto 0)), 32);
                result := std_logic_vector(signed(data(31 downto 0)) + ext_imm);
                return result(31 downto 0);

            when F3_OPIMM_SLTI =>
                -- Set less than immediate
                -- result is 1 if is less than sign ext imm, else 0
                ext_imm := resize(signed(immediate(11 downto 0)), 32);
                result(31 downto 1) := ZERO(31 downto 1);
                result(0) := '1' when signed(data(31 downto 0))<ext_imm else '0';
                return result;

            when F3_OPIMM_SLTIU =>
                -- Set less than immediate unsigned
                -- result is 1 if is less than sign ext imm as unsigned, else 0
                ext_imm := resize(signed(immediate(11 downto 0)), 32);
                result(31 downto 1) := ZERO(31 downto 1);
                result(0) := '1' when unsigned(data(31 downto 0))<unsigned(ext_imm)
            else '0';
                return result;

            when F3_OPIMM_XORI =>
                -- Bitwise XOR with sign extended immediate
                ext_imm := resize(signed(immediate(11 downto 0)), 32);
                return data xor std_logic_vector(ext_imm);

            when F3_OPIMM_ORI =>
                -- Bitwise OR with sign extended immediate
                ext_imm := resize(signed(immediate(11 downto 0)), 32);
                return data or std_logic_vector(ext_imm);

            when F3_OPIMM_ANDI =>
                -- Bitwise AND with sign extended immediate
                ext_imm := resize(signed(immediate(11 downto 0)), 32);
                return data and std_logic_vector(ext_imm);

            when F3_OPIMM_SLLI =>
                -- Logical Left Shift (zeros shifted into lsbs)
                shift := to_integer(unsigned(immediate(4 downto 0)));
                result := std_logic_vector(shift_left(unsigned(data), shift));
                return result(31 downto 0);

            when F3_OPIMM_SRLI =>
                case fun7 is
                    when F7_OPIMM_SRLI=>
                        -- Logical Right Shift (zeros shifted into msbs)
                        shift := to_integer(unsigned(immediate(4 downto 0)));
                        result := std_logic_vector(shift_right(unsigned(data),shift));
                        return result(31 downto 0);

                    when others =>
                        -- Arithmetic Right Shift (sign shifted into msbs)
                        shift := to_integer(unsigned(immediate(4 downto 0)));
                        result := std_logic_vector(shift_right(signed(data),shift));
                        return result(31 downto 0);
                end case;
            when others =>
                return ZERO;
        end case;
    end function;

function execute_LUI(
    immediate : std_logic_vector(31 downto 0)
) 
return std_logic_vector is 
    begin
        -- place immediate in top 20 bits and fill with 0
        return immediate(19 downto 0) & ZERO(11 downto 0);
end function;

function execute_AUIPC(
    pc: std_logic_vector(31 downto 0);
    immediate : std_logic_vector(31 downto 0)
) 
return std_logic_vector is 
    variable offset : unsigned(31 downto 0) ;
    begin
        -- place immediate in top 20 bits and fill with 0
        -- add this offset to address of AUIPC instruction
        offset := unsigned(immediate(19 downto 0) & ZERO(11 downto 0));
        return std_logic_vector(unsigned(pc) + offset);
end function;

function execute_REGREG(
    data_s1 : std_logic_vector(31 downto 0);
    data_s2 : std_logic_vector(31 downto 0);
    fun : std_logic_vector(9 downto 0)
) 
return std_logic_vector is 
    variable result : std_logic_vector(31 downto 0);
    variable shift : integer;
    begin
        case fun(9 downto 0) is
            when F7_OP_ADD & F3_OP_ADD =>
                -- performs add, ignores overflow
                return std_logic_vector(unsigned(data_s1) + unsigned(data_s2));
            when F7_OP_SUB & F3_OP_SUB =>
                -- performs add, ignores overflow
                return std_logic_vector(signed(data_s1) - signed(data_s2));
            when F7_OP_SLT & F3_OP_SLT =>
                -- Signed compare if rs1<rs2 then 1, else 0
                result(31 downto 1) := ZERO(31 downto 1);
                result(0) := '1' when signed(data_s1) < signed(data_s2) else '0';
                return result;

            when F7_OP_SLTU & F3_OP_SLTU =>
                -- unsigned compare if rs1<rs2 then 1, else 0
                result(31 downto 1) := ZERO(31 downto 1);
                result(0) := '1' when unsigned(data_s1) < unsigned(data_s2) else '0';
                return result;

            when F7_OP_OR & F3_OP_OR =>
                -- bitwise or
                return data_s1 or data_s2;

            when F7_OP_AND & F3_OP_AND =>
                -- bitwise and
                return data_s1 and data_s2;

            when F7_OP_XOR & F3_OP_XOR =>
                -- bitwise xor
                return data_s1 xor data_s2;

            when F7_OP_SLL & F3_OP_SLL =>
                -- leftshift of rs1 by value in lower 5 bits of rs2
                shift := to_integer(unsigned(data_s2(4 downto 0)));
                result := std_logic_vector(shift_left(unsigned(data_s1), shift));
                return result;

            when F7_OP_SRL & F3_OP_SRL =>
                -- right shift of rs1 by value in lower 5 bits of rs2
                shift := to_integer(unsigned(data_s2(4 downto 0)));
                result := std_logic_vector(shift_right(unsigned(data_s1), shift));
                return result;

            when F7_OP_SRA & F3_OP_SRA =>
                -- arithmetic right shift of rs1 by value in lower 5 bits of rs2
                shift := to_integer(unsigned(data_s2(4 downto 0)));
                result := std_logic_vector(shift_right(signed(data_s1), shift));
                return result;

            when others =>
                return ZERO(31 downto 0);
        end case;
end function;

function execute_JAL(
    pc: std_logic_vector(31 downto 0);
    immediate : std_logic_vector(31 downto 0)
) 
return std_logic_vector is 
    variable offset : signed(31 downto 0) ;
    begin
        -- Sign extend 20 bit immediate, add to address of jump
        -- instruction
        -- This returns the branch target
        offset := signed(immediate(19 downto 0));
        return std_logic_vector(signed(pc) + offset);
end function;

begin
    process (i_clock)
    begin
        if rising_edge(i_clock) and i_enable = '1' then
            case i_op_code(6 downto 0) is
                when OP_IMM => 
                    o_data_result <= execute_IMM(i_data_s1, i_data_immediate, i_fun3, i_fun7);
                when OP_LUI => 
                    o_data_result <= execute_LUI(i_data_immediate);
                when OP_AUIPC =>
                    o_data_result <= execute_AUIPC(i_program_counter, i_data_immediate);
                when OP_REGREG =>
                    o_data_result <= execute_REGREG(i_data_s1, i_data_s2, i_fun7 & i_fun3);
                when OP_JAL =>
                    o_branch_target <= execute_JAL(i_program_counter, i_data_immediate);
                    o_data_result <= std_logic_vector(signed(i_program_counter) + 4);
                    o_should_branch <= '1';
                when others =>
                    o_data_result <= ZERO(31 downto 0);
            end case;
        end if;
    end process;

end behavioral;
