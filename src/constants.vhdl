library ieee;
use ieee.numeric_std.all;
use ieee.std_logic_1164.all;
package constants is
	-- Instruction Form Offsets
	constant OPCODE_START: integer := 6;
	constant OPCODE_END: integer := 0;
	constant OPCODE_END_2: integer := 2;

	constant RD_START: integer := 11;
	constant RD_END: integer := 7;

	constant FUNCT3_START: integer := 14;
	constant FUNCT3_END: integer := 12;

	constant R1_START: integer := 19;
	constant R1_END: integer := 15;

	constant R2_START: integer := 24;
	constant R2_END: integer := 20;

	constant FUNCT7_START: integer := 31;
	constant FUNCT7_END: integer := 25;

	constant IMM_I_START: integer := 31;
	constant IMM_I_END: integer := 20;

	constant IMM_U_START: integer := 31;
	constant IMM_U_END: integer := 12;

	constant IMM_S_A_START: integer := 31;
	constant IMM_S_A_END: integer := 25;

	constant IMM_S_B_START: integer := 11;
	constant IMM_S_B_END: integer := 7;


	-- OP Codes
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


	-- Flags
	constant F3_BRANCH_BEQ: std_logic_vector(2 downto 0) := "000";
	constant F3_BRANCH_BNE: std_logic_vector(2 downto 0) := "001";
	constant F3_BRANCH_BLT: std_logic_vector(2 downto 0) := "100";
	constant F3_BRANCH_BGE: std_logic_vector(2 downto 0) := "101";
	constant F3_BRANCH_BLTU: std_logic_vector(2 downto 0) := "110";
	constant F3_BRANCH_BGEU: std_logic_vector(2 downto 0) := "111";

	constant F3_JALR: std_logic_vector(2 downto 0) := "000";

	constant F3_LOAD_LB: std_logic_vector(2 downto 0) := "000";
	constant F3_LOAD_LH: std_logic_vector(2 downto 0) := "001";
	constant F3_LOAD_LW: std_logic_vector(2 downto 0) := "010";
	constant F3_LOAD_LBU: std_logic_vector(2 downto 0) := "100";
	constant F3_LOAD_LHU: std_logic_vector(2 downto 0) := "101";

	constant F2_MEM_LS_SIZE_B: std_logic_vector(1 downto 0) := "00";
	constant F2_MEM_LS_SIZE_H: std_logic_vector(1 downto 0) := "01";
	constant F2_MEM_LS_SIZE_W: std_logic_vector(1 downto 0) := "10";

	constant F3_STORE_SB: std_logic_vector(2 downto 0) := "000";
	constant F3_STORE_SH: std_logic_vector(2 downto 0) := "001";
	constant F3_STORE_SW: std_logic_vector(2 downto 0) := "010";

	constant F3_OPIMM_ADDI: std_logic_vector(2 downto 0) := "000";
	constant F3_OPIMM_SLTI: std_logic_vector(2 downto 0) := "010";
	constant F3_OPIMM_SLTIU: std_logic_vector(2 downto 0) := "011";
	constant F3_OPIMM_XORI: std_logic_vector(2 downto 0) := "100";
	constant F3_OPIMM_ORI: std_logic_vector(2 downto 0) := "110";
	constant F3_OPIMM_ANDI: std_logic_vector(2 downto 0) := "111";

	constant F3_OPIMM_SLLI: std_logic_vector(2 downto 0) := "001";
	constant F7_OPIMM_SLLI: std_logic_vector(6 downto 0) := "0000000";
	constant F3_OPIMM_SRLI: std_logic_vector(2 downto 0) := "101";
	constant F7_OPIMM_SRLI: std_logic_vector(6 downto 0) := "0000000";
	constant F3_OPIMM_SRAI: std_logic_vector(2 downto 0) := "101";
	constant F7_OPIMM_SRAI: std_logic_vector(6 downto 0) := "0100000";

	constant F3_OP_ADD: std_logic_vector(2 downto 0) := "000";
	constant F7_OP_ADD: std_logic_vector(6 downto 0) := "0000000";
	constant F3_OP_SUB: std_logic_vector(2 downto 0) := "000";
	constant F7_OP_SUB: std_logic_vector(6 downto 0) := "0100000";
	constant F3_OP_SLL: std_logic_vector(2 downto 0) := "001";
	constant F7_OP_SLL: std_logic_vector(6 downto 0) := "0000000";
	constant F3_OP_SLT: std_logic_vector(2 downto 0) := "010";
	constant F7_OP_SLT: std_logic_vector(6 downto 0) := "0000000";
	constant F3_OP_SLTU: std_logic_vector(2 downto 0) := "011";
	constant F7_OP_SLTU: std_logic_vector(6 downto 0) := "0000000";
	constant F3_OP_XOR: std_logic_vector(2 downto 0) := "100";
	constant F7_OP_XOR: std_logic_vector(6 downto 0) := "0000000";
	constant F3_OP_SRL: std_logic_vector(2 downto 0) := "101";
	constant F7_OP_SRL: std_logic_vector(6 downto 0) := "0000000";
	constant F3_OP_SRA: std_logic_vector(2 downto 0) := "101";
	constant F7_OP_SRA: std_logic_vector(6 downto 0) := "0100000";
	constant F3_OP_OR: std_logic_vector(2 downto 0) := "110";
	constant F7_OP_OR: std_logic_vector(6 downto 0) := "0000000";
	constant F3_OP_AND: std_logic_vector(2 downto 0) := "111";
	constant F7_OP_AND: std_logic_vector(6 downto 0) := "0000000";
end constants;

package body constants is
 
end constants;
