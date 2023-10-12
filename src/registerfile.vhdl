library ieee;
use ieee.numeric_std.all;
use ieee.std_logic_1164.all;

entity register_file is
port ( i_clock : in  std_logic;
       i_enable : in  std_logic;
       i_datadest : in  std_logic_vector (31 downto 0);
       o_dataa : out  std_logic_vector (31 downto 0);
       o_datab : out  std_logic_vector (31 downto 0);
       i_selecta : in  std_logic_vector (4 downto 0);
       i_selectb : in  std_logic_vector (4 downto 0);
       i_selectdest : in  std_logic_vector (4 downto 0);
       i_write_enable : in  std_logic);
end register_file;

architecture behavioral of register_file is
	type store_t is array (0 to 31) of std_logic_vector(31 downto 0);
	signal registers: store_t := (others => x"00000000");
begin
	process(i_clock)
	begin
		if rising_edge(i_clock) and i_enable = '1' then
			o_dataa <= registers(to_integer(unsigned(i_selecta)));
			o_datab <= registers(to_integer(unsigned(i_selectb)));
			if (i_write_enable = '1') and (unsigned(i_selectdest) > 0) then
				registers(to_integer(unsigned(i_selectdest))) <= i_datadest;
			end if;
		end if;
	end process;
end;
