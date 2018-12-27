library ieee;
use ieee.std_logic_1164.all;

entity r4mbePP_preprocessing is
	generic (
		n_bit: positive := 8 );
	port (
		x: in std_logic_vector(n_bit-1 downto 0);		-- multiplicand
		y_tri: in std_logic_vector(2 downto 0);			-- a triplet of the multiplier

		neg: out std_logic;								-- negation bit: '1' if Y is negative (Y=-1 or Y=-2)
		x_absY: out std_logic_vector(n_bit downto 0) );	-- partial product without informations about its sign
end entity;

architecture behaviour of r4mbePP_preprocessing is

	component mux2 is
generic (
	n_bit: positive := 8 );
port (
	i0: in std_logic_vector(n_bit-1 downto 0);		-- o <= i0 if sel = '0'
	i1: in std_logic_vector(n_bit-1 downto 0);		-- o <= i1 if sel = '1'	
	sel: in std_logic;		

	o: out std_logic_vector(n_bit-1 downto 0) );	
end component;

	signal 
		mux_sel_x,
		mux_enable: std_logic;

	signal
		zeroString,
		two_x,
		extended_x,
		mux_x_out: std_logic_vector(n_bit downto 0);

begin

neg <= y_tri(2) and not (y_tri(1) and y_tri(0));
mux_sel_x <= y_tri(1) xnor y_tri(0); 
mux_enable <= not(y_tri(2) or y_tri(1) or y_tri(0)) nor (y_tri(2) and y_tri(1) and y_tri(0));

zeroString <= (others => '0');
extended_x <= x(n_bit-1) & x;
two_x <= x & '0';

MUX_X: mux2
	generic map (
		n_bit => n_bit+1 )
	port map (
		i0 => extended_x,
		i1 => two_x,
		sel => mux_sel_x,
		o => mux_x_out );

MUX_0: mux2
	generic map (
		n_bit => n_bit+1 )
	port map (
		i0 => zeroString,
		i1 => mux_x_out,
		sel => mux_enable,
		o => x_absY );

end architecture ; -- behaviour