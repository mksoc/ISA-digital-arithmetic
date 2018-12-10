library ieee;
use ieee.std_logic_1164.all;

package multV3_pkg is

-- constants
constant numPartProd: positive := 12;
constant daddaLev4: positive := 9;
constant daddaLev3: positive := 6;
constant daddaLev2: positive := 4;
constant daddaLev1: positive := 3;
constant daddaLev0: positive := 2;

constant WL: positive := 24;
constant WL_INT: positive := 2;
constant WL_FRAC: positive := 22;

-- types
type aidGridPreprocessedPP is array(numPartProd-1 downto 0) of std_logic_vector(WL downto 0);
type aidGrid5 is array(numPartProd downto 0) of std_logic_vector((WL_INT+2*WL_FRAC)-1 downto 0);
type aidGrid4 is array(daddaLev4-1 downto 0) of std_logic_vector((WL_INT+2*WL_FRAC)-1 downto 0);
type aidGrid3 is array(daddaLev3-1 downto 0) of std_logic_vector((WL_INT+2*WL_FRAC)-1 downto 0);
type aidGrid2 is array(daddaLev2-1 downto 0) of std_logic_vector((WL_INT+2*WL_FRAC)-1 downto 0);
type aidGrid1 is array(daddaLev1-1 downto 0) of std_logic_vector((WL_INT+2*WL_FRAC)-1 downto 0);
type aidGrid0 is array(daddaLev0-1 downto 0) of std_logic_vector((WL_INT+2*WL_FRAC)-1 downto 0);

-- components

component approx_comp_4to2 is
    port (
        i0, 
        i1, 
        i2, 
        i3: in std_logic;

        out0, 
        out1: out std_logic ) ;
end component;

component r4mbePP_preprocessing is
	generic (
		n_bit: positive := WL );
	port (
		x: in std_logic_vector(n_bit-1 downto 0);		-- multiplicand
		y_tri: in std_logic_vector(2 downto 0);			-- a triplet of the multiplier

		neg: out std_logic;								-- negation bit: '1' if Y is negative (Y=-1 or Y=-2)
		x_absY: out std_logic_vector(n_bit downto 0) );	-- partial product without informations about its sign
end component;

component bitwiseInv is
	generic (
		n_bit: positive := WL+1 );
	port (
		invEnable: in std_logic;
		dataIn: in std_logic_vector(n_bit-1 downto 0);

		dataOut: out std_logic_vector(n_bit-1 downto 0) );
end component;

component halfAdder is
	port (
		i0,
		i1: in std_logic;

		s,
		co: out std_logic );
end component;

component fullAdder is
	port (
		i0,
		i1,
		ci: in std_logic;

		s,
		co: out std_logic );
end component;

end package multV3_pkg;