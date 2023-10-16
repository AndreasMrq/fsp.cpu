library ieee;
use ieee.numeric_std.all;
use ieee.std_logic_1164.all;
entity constants is
	constant OP_LUI : std_logic_vector (6 downto 0) := "0110111";
	constant OP_AUIPC : std_logic_vector (6 downto 0) := "0010111";
	constant OP_JAL : std_logic_vector (6 downto 0) := "1101111";
	constant OP_JALR : std_logic_vector (6 downto 0) := "1100111";
	constant OP_BRANCH : std_logic_vector (6 downto 0) := "1100011";
	constant OP_LOAD : std_logic_vector (6 downto 0) := "0000011";
	constant OP_STORE : std_logic_vector (6 downto 0) := "0100011";
	constant OP_IMM : std_logic_vector (6 downto 0) := "0010011";
	constant OP_REGREG : std_logic_vector (6 downto 0) := "0110011";
	constant OP_FENCE : std_logic_vector (6 downto 0) := "0001111";
	constant OP_ENV : std_logic_vector (6 downto 0) := "1110011";

	constant FUN_BEQ : std_logic_vector (2 downto 0) := "000";
	constant FUN_BNE : std_logic_vector (2 downto 0) := "001";
	constant FUN_BLT : std_logic_vector (2 downto 0) := "100";
	constant FUN_BGE : std_logic_vector (2 downto 0) := "101";
	constant FUN_BLTU : std_logic_vector (2 downto 0) := "110";
	constant FUN_BGEU : std_logic_vector (2 downto 0) := "111";
	constant FUN_LB : std_logic_vector (2 downto 0) := "000";
	constant FUN_LH : std_logic_vector (2 downto 0) := "001";
	constant FUN_LW : std_logic_vector (2 downto 0) := "010";
	constant FUN_LBU : std_logic_vector (2 downto 0) := "100";
	constant FUN_LHU : std_logic_vector (2 downto 0) := "101";
	constant FUN_SB : std_logic_vector (2 downto 0) := "000";
	constant FUN_SH : std_logic_vector (2 downto 0) := "001";
	constant FUN_SW : std_logic_vector (2 downto 0) := "010";
end constants;