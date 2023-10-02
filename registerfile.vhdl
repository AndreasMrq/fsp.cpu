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
begin
end;
