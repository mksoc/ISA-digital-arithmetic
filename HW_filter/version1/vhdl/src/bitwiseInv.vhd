library ieee;
use ieee.std_logic_1164.all;

entity bitwiseInv is
	generic (
		n_bit: positive := WL+1 );
	port (
		invEnable: in std_logic;
		dataIn: in std_logic_vector(n_bit-1 downto 0);

		dataOut: out std_logic_vector(n_bit-1 downto 0) );
end entity;

architecture behaviour of bitwiseInv is
begin

controlled_negation:
	for i in n_bit-1 downto 0 generate
		dataOut(i) <= dataIn(i) xor invEnable;
	end generate;

end architecture; -- behaviour