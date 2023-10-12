library ieee;
use ieee.numeric_std.all;
use ieee.std_logic_1164.all;

entity decoder is
    port ( i_clock : in  std_logic;
           i_data_instruction : in  std_logic_vector (31 downto 0);
           i_enable : in  std_logic;
           o_selecta : out  std_logic_vector (5 downto 0);
           o_selectb : out  std_logic_vector (5 downto 0);
           o_selectdest : out  std_logic_vector (5 downto 0);
           o_data_imm : out  std_logic_vector (31 downto 0);
           o_write_enable : out  std_logic;
           o_opcode : out  std_logic_vector (6 downto 0));
end decoder;

architecture behavioral of decoder is

begin

  process (i_clock)
  begin
    if rising_edge(i_clock) and i_enable = '1' then

      o_selecta <= i_data_instruction(7 downto 5);
      o_selectb <= i_data_instruction(4 downto 2);
      o_selectdest <= i_data_instruction(11 downto 9);
      o_data_imm <= i_data_instruction(7 downto 0) & i_data_instruction(7 downto 0);
      o_opcode <= i_data_instruction(15 downto 12) & i_data_instruction(8);

      case i_data_instruction(15 downto 12) is
        when "0111" => 	-- write
          o_write_enable <= '0';
        when "1100" => 	-- jump
          o_write_enable <= '0';
        when "1101" => 	-- jumpeq
          o_write_enable <= '0';
        when others =>
          o_write_enable <= '1';
      end case;
    end if;
  end process;

end behavioral;
