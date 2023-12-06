library ieee;
library work;
use ieee.numeric_std.all;
use ieee.std_logic_1164.all;
use work.constants.all;

entity pc is
    port ( i_clock : in  std_logic;
           i_enable : in  std_logic;
           i_op_code : in  std_logic_vector (1 downto 0);
           i_data : in std_logic_vector(31 downto 0);
           o_pc : out std_logic_vector(31 downto 0)
        );
end pc;

architecture behavioral of pc is
    signal current_pc: std_logic_vector(31 downto 0) := (others => '0');
begin 
    process(i_clock)
    begin
        if rising_edge(i_clock) and i_enable = '1' then
            case i_op_code is
            when PCU_OP_NOP => -- Do Nothing --
            when PCU_OP_INC =>
                current_pc <= std_logic_vector(unsigned(current_pc)+1);
            when PCU_OP_ASSIGN=>
                current_pc <= i_data;
            when PCU_OP_RESET=>
                current_pc <= (others => '0');
            when others =>
            end case;
            o_pc <= current_pc;
        end if;
    end process;
end behavioral;
