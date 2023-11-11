library ieee;
library work;
use ieee.numeric_std.all;
use ieee.std_logic_1164.all;
use work.constants.all;

entity alu is
    port ( i_clock : in  std_logic;
           i_enable : in  std_logic;
           i_op_code : in  std_logic_vector (6 downto 0);
		   i_fun3 : in std_logic_vector(3 downto 0);
		   i_fun7 : in std_logic_vector(7 downto 0);
		   i_data_a : in std_logic_vector(31 downto 0);
		   i_data_b : in std_logic_vector(31 downto 0);
		   i_data_immediate : in std_logic_vector(31 downto 0);
		   o_data_result : out std_logic_vector(31 downto 0);
		   o_should_branch: out std_logic;
		   o_rd_write_enable: out std_logic
       );
end alu;

architecture behavioral of alu is

		function calculate_imm(data_a : std_logic_vector(31 downto 0)) return std_logic_vector(31 downto 0) is 
				variable result : std_logic_vector(31 downto 0);
		begin
				return result;
		end function;

begin
    process (i_clock)
    begin
        if rising_edge(i_clock) and i_enable = '1' then
            case i_op_code(6 downto 0) is
                when OP_IMM => 
		    end case;
		end if;
    end process;

end behavioral;
