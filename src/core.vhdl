library ieee;
library work;
use ieee.numeric_std.all;
use ieee.std_logic_1164.all;
use work.constants.all;

entity core is
    port ( i_clock : in  std_logic;
           i_enable : in  std_logic;
           o_data_result : out std_logic_vector(31 downto 0)
       );
end core;

architecture behavioral of core is
    -- Registerfile and Data related
    signal address_s1 : std_logic_vector(4 downto 0) := (others => '0');
    signal address_s2 : std_logic_vector(4 downto 0) := (others => '0');
    signal address_dest : std_logic_vector(4 downto 0) := (others => '0');
    signal data_s1 : std_logic_vector(31 downto 0) := (others => '0');
    signal data_s2 : std_logic_vector(31 downto 0) := (others => '0');
    signal data_dest : std_logic_vector(31 downto 0) := (others => '0');
    signal data_immediate : std_logic_vector(31 downto 0) := (others => '0');

    -- OP Codes and ALU functions
    signal instruction : std_logic_vector(6 downto 0);
    signal alu_op : std_logic_vector(6 downto 0);
    signal function3 : std_logic_vector(2 downto 0);
    signal function7 : std_logic_vector(6 downto 0);
    signal pc_op : std_logic_vector(2 downto 0);
    
    -- Control Unit related
    signal pipeline_enable : std_logic_vector(PIPELINE_LENGTH downto 0)  := (others => '0');
    signal register_file_enable : std_logic := '0';
    signal register_file_write_enable : std_logic := '0';
    signal decoder_enable : std_logic := '0';
    signal memory_enable : std_logic := '0';
    signal alu_enable : std_logic := '0';
    signal pc_enable : std_logic := '0';
    signal control_unit_enable : std_logic := '0';

    -- Program Counter
    signal program_counter : std_logic_vector(31 downto 0) := (others => '0');
    signal should_branch: std_logic := '0';
    signal branch_target : std_logic_vector(31 downto 0) := (others => '0');

    begin
	register_file:	entity	work.register_file
	port map (
			 i_clock=>i_clock,
			 i_enable=>register_file_enable,
			 i_datadest=>data_dest,
			 o_dataa=>data_s1,
			 o_datab=>data_s2,
			 i_selecta=>address_s1,
			 i_selectb=>address_s2,
			 i_selectdest=>address_dest,
			 i_write_enable=>register_file_write_enable
		    );

    alu: entity work.alu
    port map ( 
           i_clock => i_clock,
           i_enable => register_file_write_enable,
           i_op_code => alu_op,
           i_fun3 => function3,
           i_fun7 => function7,
           i_data_s1 => data_s1,
           i_data_s2 => data_s2,
           i_data_immediate => data_immediate,
           i_program_counter => program_counter,
           o_data_result => data_result,
           o_should_branch => should_branch,
           o_branch_target => branch_target
       );

    decoder: entity work.decoder
    port map ( 
           i_clock => i_clock,
           i_data_instruction => instruction,
           i_enable => decoder_enable,
           o_selecta => address_s1,
           o_selectb => address_s2,
           o_selectdest => address_dest,
           o_data_imm => data_immediate,
           o_write_enable => o_write_enable,
           o_opcode => o_opcode,
           o_fun3 => o_fun3,
           o_fun7 => o_fun7
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
