library ieee;
use ieee.std_logic_1164.all

entity halfAdder is
	port (
		i0,
		i1: in std_logic;

		s,
		co: out std_logic );
end entity;

architecture behaviour of halfAdder is
begin

	s <= i0 xor i1;
	co <= i0 and i1;

end architecture ; -- behaviour