library ieee;
library work;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.filter_pkg.all;

-- fast multiplier with radix-4 modified Booth encoding, with Roorda's trick, CSA+fast adder Dadda tree
entity mbeDadda_mult is
	port ( 
		x,											-- multiplicand
		y: in std_logic_vector(WL-1 downto 0);		-- multiplier

		p: out std_logic_vector(WL-1 downto 0) );	-- product
end entity;

architecture structure of mbeDadda_mult is

component r4mbePP_preprocessing is
	port (
		x: in std_logic_vector(WL-1 downto 0);			-- multiplicand
		y_tri: in std_logic_vector(2 downto 0);			-- a triplet of the multiplier

		neg: out std_logic;								-- negation bit: '1' if Y is negative (Y=-1 or Y=-2)
		x_absY: out std_logic_vector(WL+1 downto 0) );	-- partial product without informations about its sign
end component;

component bitwiseInv is
	port (
		dataIn: in MBEcodedWord;
		);
end component;

begin
end architecture;