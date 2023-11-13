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
           o_rd_write_enable: out std_logic
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
                -- Bitwise XOR with sign extended immediate
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


begin
    process (i_clock)
    begin
        if rising_edge(i_clock) and i_enable = '1' then
            case i_op_code(6 downto 0) is
                when OP_IMM => 
                    o_data_result <= execute_IMM(i_data_s1, i_data_immediate, i_fun3, i_fun7);
                when OP_LUI => 
                    o_data_result <= execute_LUI(i_data_immediate);
                when others =>
                    o_data_result <= ZERO(31 downto 0);
            end case;
        end if;
    end process;

end behavioral;
