library ieee;
use ieee.std_logic_1164.all

-- 2 to 1 n_bit mux

entity mux2 is
	generic (
		n_bit: positive := 8 );
	port (
		i0: in std_logic_vector(n_bit-1 downto 0);		-- o <= i0 if sel = '0'
		i1: in std_logic_vector(n_bit-1 downto 0);		-- o <= i1 if sel = '1'	
		sel: in std_logic;	
									
		o: out std_logic_vector(n_bit-1 downto 0) );	
end entity;

architecture behaviour of mux2 is
begin

	o <= 	
		i0 when (sel = '0') else
		i1;
		
end architecture ; -- behaviour