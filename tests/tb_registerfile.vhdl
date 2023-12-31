library vunit_lib;
library ieee;
use vunit_lib.log_levels_pkg.all;
use vunit_lib.logger_pkg.all;
use vunit_lib.run_pkg.all;

use std.textio.all;
context vunit_lib.vunit_context;
use ieee.numeric_std.all;
use ieee.std_logic_1164.all;

entity tb_registerfile is
  generic (runner_cfg : string := runner_cfg_default);
end entity;

architecture tb of tb_registerfile is

	signal i_clock : std_logic := '0';
	signal i_enable : std_logic := '0';
	signal i_datadest : std_logic_vector (31 downto 0) := (others => '0');
	signal i_selecta : std_logic_vector (4 downto 0) := (others => '0');
	signal i_selectb : std_logic_vector (4 downto 0) := (others => '0');
	signal i_selectdest : std_logic_vector (4 downto 0) := (others => '0');
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
	I_clk_process : process
	begin
		i_clock <= '0';
		wait for I_clk_period/2;
		i_clock <= '1';
		wait for I_clk_period/2;
	end process;

	test_runner : process
	begin
		test_runner_setup(runner, runner_cfg);

		-- Put test suite setup code here

		while test_suite loop

			-- Put common test case setup code here

			if run("Registers are initialized to 0x0") then
				i_enable <= '1';
				for i in 0 to 31 loop
					i_selecta <= std_logic_vector(to_unsigned(i, i_selecta'length));
					wait for i_clk_period;
					check_equal(unsigned(o_dataa),0);
				end loop;
			elsif run("Read Write on same cycle") then
				i_enable <= '1';
				i_selectdest <= "00001";
				i_datadest <= x"aaaaaaaa";
				i_write_enable <= '1';
				wait for i_clk_period;
				i_datadest <= x"bbbbbbbb";
				i_selecta <= "00001";
				wait for i_clk_period;
				check_equal(to_string(o_dataa),x"aaaaaaaa");
			elsif run("Read Write test select A") then
				i_enable <= '1';
				i_write_enable<='1';

				for i in 1 to 31 loop
					i_selectdest <= std_logic_vector(to_unsigned(i, i_selectdest'length));
					info("dest:" & to_string(i_selectdest));
					i_datadest <= x"aaaaaaaa";
					wait for i_clk_period;

					i_selecta <= std_logic_vector(to_unsigned(i, i_selecta'length));
					wait for i_clk_period;

					check_equal(to_string(o_dataa),x"aaaaaaaa");
					wait for i_clk_period;
				end loop;
			elsif run("Read Write test select B") then
				i_enable <= '1';
				i_write_enable<='1';

				for i in 1 to 31 loop
					i_selectdest <= std_logic_vector(to_unsigned(i, i_selectdest'length));
					info("dest:" & to_string(i_selectdest));
					i_datadest <= x"aaaaaaaa";
					wait for i_clk_period;

					i_selectb <= std_logic_vector(to_unsigned(i, i_selectb'length));
					wait for i_clk_period;

					check_equal(to_string(o_datab),x"aaaaaaaa");
					wait for i_clk_period;
				end loop;
			elsif run("Both selects for same register") then
				i_enable <= '1';

				i_selectdest <= "00001";
				i_datadest <= x"aaaaaaaa";
				i_write_enable<='1';
				wait for i_clk_period;

				i_selecta <= "00001";
				i_selectb <= "00001";
				wait for i_clk_period;

				check_equal(to_string(o_dataa),x"aaaaaaaa");
				check_equal(to_string(o_datab),x"aaaaaaaa");
			elsif run("No Write when enable not asserted") then
				i_enable <= '0';
				i_selectdest <= "00001";
				i_datadest <= x"aaaaaaaa";
				i_write_enable<='1';
				i_selecta <= "00001";
				wait for i_clk_period;
				i_enable <= '1';
				i_selectdest <= "00000";
				i_write_enable<='1';
				wait for i_clk_period;

				check_equal(to_string(o_dataa),x"00000000");
			elsif run("No Write when write_enable not asserted") then
				i_enable <= '1';

				i_selectdest <= "00001";
				i_datadest <= x"aaaaaaaa";
				i_write_enable<='0';
				wait for i_clk_period;

				i_selectdest <= "00000";
				i_datadest <= (others => '0');
				i_write_enable<='0';
				i_selecta <= "00001";
				wait for i_clk_period;

				check_equal(to_string(o_dataa),x"00000000");
			elsif run("Register 0 cannot be overriden") then
				i_enable <= '1';

				i_selectdest <= "00000";
				i_datadest <= x"aaaaaaaa";
				i_write_enable<='1';
				wait for i_clk_period;

				i_datadest <= (others => '0');
				i_write_enable<='0';
				i_selecta <= "00000";
				wait for i_clk_period;

				check_equal(to_string(o_dataa),x"00000000");
			end if;

    -- Put common test case cleanup code here

		end loop;

    -- Put test suite cleanup code here

		test_runner_cleanup(runner);
	end process;
end architecture;
