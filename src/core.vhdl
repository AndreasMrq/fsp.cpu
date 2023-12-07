library ieee;
library work;
use ieee.numeric_std.all;
use ieee.std_logic_1164.all;
use work.constants.all;

entity core is
    port ( i_clock : in  std_logic;
           i_enable : in  std_logic;
           i_op_code : in  std_logic_vector (6 downto 0);
           i_fun3 : in std_logic_vector(2 downto 0);
           i_fun7 : in std_logic_vector(6 downto 0);
           i_data_s1 : in std_logic_vector(31 downto 0);
           i_data_s2 : in std_logic_vector(31 downto 0);
           i_data_immediate : in std_logic_vector(31 downto 0);
           i_program_counter : in std_logic_vector(31 downto 0);
           o_data_result : out std_logic_vector(31 downto 0);
           o_should_branch: out std_logic;
           o_rd_write_enable: out std_logic;
           o_branch_target: out std_logic_vector(31 downto 0)
       );
end core;

architecture behavioral of core is
    -- Data related
    signal select_s1 : std_logic_vector(4 downto 0) := (others => '0');
    signal select_s2 : std_logic_vector(4 downto 0) := (others => '0');
    signal select_dest : std_logic_vector(4 downto 0) := (others => '0');
    signal data_s1 : std_logic_vector(31 downto 0) := (others => '0');
    signal data_s2 : std_logic_vector(31 downto 0) := (others => '0');
    signal data_dest : std_logic_vector(31 downto 0) := (others => '0');

    -- OP Codes and functions
    signal alu_op : std_logic_vector(6 downto 0);
    signal i_fun3 : std_logic_vector(2 downto 0);
    signal i_fun7 : std_logic_vector(6 downto 0);
    
    -- Control Unit related
    signal pipeline_enable : std_logic_vector(PIPELINE_LENGTH downto 0)  := (others => '0');


    begin
	register_file:	entity	work.register_file
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

    alu: entity work.alu
    port map ( 
           i_clock => i_clock,
           i_enable => i_enable,
           i_op_code => i_op_code,
           i_fun3 => i_fun3,
           i_fun7 => i_fun7,
           i_data_s1 => i_data_s1,
           i_data_s2 => i_data_s2,
           i_data_immediate => i_data_immediate,
           i_program_counter => i_program_counter,
           o_data_result => o_data_result,
           o_should_branch => o_should_branch,
           o_rd_write_enable => o_rd_write_enable,
           o_branch_target => o_branch_target
       );

    decoder: entity work.decoder
    port map ( 
           i_clock => i_clock,
           i_data_instruction => i_data_instruction,
           i_enable => i_enable,
           o_selecta => o_selecta,
           o_selectb => o_selectb,
           o_selectdest => o_selectdest,
           o_data_imm => o_data_imm,
           o_write_enable => o_write_enable,
           o_opcode => o_opcode,
           o_fun3 => o_fun3,
           o_fun7 => o_fun7,
       );

    pc: entity work.pc
    port map ( 
           i_clock => i_clock,
           i_enable => i_enable,
           i_op_code => i_op_code,
           i_data => i_data,
           o_pc => o_pc
        );

    control_unit: entity work.control_unit
    port map (
           i_clock => i_clock,
           i_reset => i_reset,
           o_active_phase => o_active_phase,
        );

        process (i_clock)
            begin
        end process;
end behavioral;
