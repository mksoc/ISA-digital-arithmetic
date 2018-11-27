library ieee;
use ieee.std_logic_1164.all;

entity fullAdder is
	port (
		i0,
		i1,
		ci: in std_logic;

		s,
		co: out std_logic );
end entity;

architecture structure of fullAdder is

component halfAdder is
	port (
		i0,
		i1: in std_logic;

		s,
		co: out std_logic );
end component; 

	signal s0, s1, c0, c1: std_logic;

begin

	HA_0: halfAdder 
		port map (
			i0 => i0,
			i1 => i1,
			s => s0,
			co => c0 );

	HA_1: halfAdder 
		port map (
			i0 => ci,
			i1 => s0,
			s => s,
			co => c1 );

	co <= c0 or c1;

end architecture ; -- structure