library vunit_lib;
library IEEE;
context vunit_lib.vunit_context;
use IEEE.NUMERIC_STD.ALL;
use IEEE.std_logic_1164.All;

entity tb_registerfile is
  generic (runner_cfg : string := runner_cfg_default);
end entity;

architecture tb of tb_registerfile is

	signal i_clock : std_logic := '0';
	signal i_enable : std_logic := '0';
	signal i_datadest : std_logic_vector (31 downto 0) := (others => '0');
	signal i_selecta : std_logic_vector (5 downto 0) := (others => '0');
	signal i_selectb : std_logic_vector (5 downto 0) := (others => '0');
	signal i_selectdest : std_logic_vector (5 downto 0) := (others => '0');
	signal i_write_enable : std_logic := '0';

	signal o_dataa :  std_logic_vector (31 downto 0);
	signal o_datab :  std_logic_vector (31 downto 0);

	constant i_clk_period : time := 10 ns;

begin
	registerfile:	entity	work.register_file
	port map (
	i_clock=>i_clock,
	i_enable=>i_enable,
	i_datadest=>i_datadest,
	o_dataa=>o_dataa,
	o_datab=>o_datab,
	i_selecta=>i_selecta,
	i_selectb=>i_selectb,
	i_selectdest=>i_selectdest,
	i_write_enable=>i_write_enable
	);

  test_runner : process
  begin
    test_runner_setup(runner, runner_cfg);

    -- Put test suite setup code here

    while test_suite loop

      -- Put common test case setup code here

      if run("Test to_string for integer") then
        check_equal(to_string(17), "17");
      elsif run("Test to_string for boolean") then
        check_equal(to_string(true), "true");
      end if;

      -- Put common test case cleanup code here

    end loop;

    -- Put test suite cleanup code here

    test_runner_cleanup(runner);
  end process;
end architecture;
