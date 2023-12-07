library ieee;
library work;
use ieee.numeric_std.all;
use ieee.std_logic_1164.all;
use work.constants.all;

entity decoder is
    port ( i_clock : in  std_logic;
           i_data_instruction : in  std_logic_vector (31 downto 0);
           i_enable : in  std_logic;
           o_selecta : out  std_logic_vector (4 downto 0);
           o_selectb : out  std_logic_vector (4 downto 0);
           o_selectdest : out  std_logic_vector (4 downto 0);
           o_data_imm : out  std_logic_vector (31 downto 0);
           o_opcode : out  std_logic_vector (6 downto 0);
           o_fun3: out std_logic_vector (2 downto 0);
           o_fun7: out std_logic_vector (6 downto 0)
       );
end decoder;

architecture behavioral of decoder is

    constant ZERO : std_logic_vector(31 downto 0) := (others => '0');

begin
    process (i_clock)
    begin
        if rising_edge(i_clock) and i_enable = '1' then

            o_opcode <= i_data_instruction(OPCODE_START downto OPCODE_END);
            o_selectdest <= i_data_instruction(RD_START downto RD_END);
            o_selecta <= i_data_instruction(R1_START downto R1_END);
            o_selectb <= i_data_instruction(R2_START downto R2_END);
            o_fun3 <= i_data_instruction(FUNCT3_START downto FUNCT3_END);
			o_fun7 <= i_data_instruction(FUNCT7_START downto FUNCT7_END); 

            case i_data_instruction(OPCODE_START downto OPCODE_END) is
                when OP_LUI | OP_AUIPC => 
                    o_data_imm <= i_data_instruction(31 downto 12) &
                                  ZERO(11 downto 0);

                when OP_JAL => 
                    o_data_imm <= ZERO(31 downto 21) &
                                  i_data_instruction(31) &
                                  i_data_instruction(19 downto 12) &
                                  i_data_instruction(20) &
                                  i_data_instruction(30 downto 21) &
                                  ZERO(0);

                when OP_JALR | OP_LOAD => 
                    o_data_imm <= ZERO(31 downto 12) &
                                  i_data_instruction(31 downto 20);

                when OP_BRANCH =>
                    o_data_imm <= ZERO(31 downto 13) &
                                  i_data_instruction(31) &
                                  i_data_instruction(7) &
                                  i_data_instruction(30 downto 25) &
                                  i_data_instruction(11 downto 8) &
                                  ZERO(0);

                when OP_STORE =>
                    o_data_imm <= ZERO(31 downto 12) &
                                  i_data_instruction(31 downto 25) &
                                  i_data_instruction(11 downto 7);
                when OP_IMM =>
                    o_data_imm <= ZERO(31 downto 12) &
                                  i_data_instruction(31 downto 20);
		        when OP_FENCE =>
                when others =>
                    o_data_imm <= ZERO(31 downto 0);
            end case;
        end if;
    end process;

end behavioral;
