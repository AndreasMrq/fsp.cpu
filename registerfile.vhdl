library IEEE;
use IEEE.NUMERIC_STD.ALL;
use IEEE.std_logic_1164.All;

entity register_file is
Port ( I_clock : in  STD_LOGIC;
       I_enable : in  STD_LOGIC;
       I_dataDest : in  STD_LOGIC_VECTOR (31 downto 0);
       O_dataA : out  STD_LOGIC_VECTOR (31 downto 0);
       O_dataB : out  STD_LOGIC_VECTOR (31 downto 0);
       I_selectA : in  STD_LOGIC_VECTOR (5 downto 0);
       I_selectB : in  STD_LOGIC_VECTOR (5 downto 0);
       I_selectDest : in  STD_LOGIC_VECTOR (5 downto 0);
       I_write_enable : in  STD_LOGIC);
end register_file;

architecture Behavioral of register_file is
	type store_t is array (0 to 31) of std_logic_vector(31 downto 0);
	signal registers: store_t := (others => X"00000000");
begin
	process(I_clock)
	begin
		if rising_edge(I_clock) and I_enable = '1' then
			O_dataA <= registers(to_integer(unsigned(I_selectA)));
			O_dataB <= registers(to_integer(unsigned(I_selectB)));
			if (I_write_enable = '1') and (unsigned(I_selectDest) > 0) then
				registers(to_integer(unsigned(I_selectDest))) <= I_dataDest;
			end if;
		end if;
	end process;
end;
