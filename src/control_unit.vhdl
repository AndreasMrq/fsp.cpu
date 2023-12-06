
library ieee;
library work;
use ieee.numeric_std.all;
use ieee.std_logic_1164.all;
use work.constants.all;

entity control_unit is
    port ( i_clock : in  std_logic;
           i_reset : in  std_logic;
           o_active_phase : out std_logic_vector(5 downto 0)
        );
end control_unit;

architecture behavioral of control_unit is
    signal active_phase: std_logic_vector(5 downto 0) := CU_RESET;
begin 
    process(i_clock)
    begin
        if rising_edge(i_clock) and i_reset = '0' then
            case active_phase is
            when CU_RESET =>
                active_phase <= CU_FETCH;
            when CU_FETCH =>
                active_phase <= CU_DECODE;
            when CU_DECODE =>
                active_phase <= CU_EXECUTE;
            when CU_EXECUTE =>
                active_phase <= CU_PC;
            when CU_PC =>
                active_phase <= CU_FETCH;
            when others => -- do nothing
            end case;
            o_active_phase <= active_phase;
        end if;
        if rising_edge(i_clock) and i_reset = '1' then
            active_phase <= CU_RESET;
            o_active_phase <=active_phase;
        end if;
    end process;
end behavioral;
