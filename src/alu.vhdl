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
           i_data_a : in std_logic_vector(31 downto 0);
           i_data_b : in std_logic_vector(31 downto 0);
           i_data_immediate : in std_logic_vector(31 downto 0);
           o_data_result : out std_logic_vector(31 downto 0);
           o_should_branch: out std_logic;
		   o_rd_write_enable: out std_logic
       );
end alu;

architecture behavioral of alu is


function calculate_imm(
    data : std_logic_vector(31 downto 0);
    immediate : std_logic_vector(31 downto 0);
    fun3 : std_logic_vector(2 downto 0);
    fun7 : std_logic_vector(6 downto 0)
) 
return std_logic_vector is 
    variable result : std_logic_vector(31 downto 0);
    variable extended_immediate: signed(31 downto 0);
    begin
        case fun3(2 downto 0) is
            when F3_OPIMM_ADDI =>
                -- Add sign extended 12 bit immediate to data
                -- Ignore Overflow
                extended_immediate := resize(signed(immediate(11 downto 0)), 32);
                result := std_logic_vector(signed(data(31 downto 0)) + extended_immediate);
                return result(31 downto 0);
            when others =>
                return result;
        end case;
end function;


begin
    process (i_clock)
    begin
        if rising_edge(i_clock) and i_enable = '1' then
            case i_op_code(6 downto 0) is
                when OP_IMM => 
                    o_data_result <= calculate_imm(i_data_a, i_data_immediate, i_fun3, i_fun7);
                when others =>
                    o_data_result <= ZERO(31 downto 0);
		    end case;
		end if;
    end process;

end behavioral;
