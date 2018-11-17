library ieee;
library work;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.filter_pkg.all;

constant numPartProd: positive := 12;
constant daddaLev4: positive := 9;
constant daddaLev3: positive := 6;
constant daddaLev2: positive := 4;
constant daddaLev1: positive := 3;
constant daddaLev0: positive := 2;

-- fast multiplier with radix-4 modified Booth encoding, with Roorda's trick, CSA+fast adder Dadda tree
entity mbeDadda_mult is
	port ( 
		x,											-- multiplicand
		y: in std_logic_vector(WL-1 downto 0);		-- multiplier

		p: out std_logic_vector(WL-1 downto 0) );	-- product
end entity;

architecture structure of mbeDadda_mult is

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

component truncationBlock is
	generic (
		n_bit_in: positive := WL_INT+2*WL_FRAC;
		n_bit_out: positive := WL );
	port (
		data: in std_logic_vector(n_bit_in-1 downto 0);

		trunc_data: in std_logic_vector(n_bit_out-1 downto 0) );
end component;

-- aidGrid5: matrix to have each column ready to be used
-- numPartProd+1 rows and (WL_INT+2*WL_FRAC) columns (with fixed parallelism for integer part WL_INT there's
-- no need for saving also the other two MSBs)
type aidGridPreprocessedPP is array(numPartProd-1 downto 0) of std_logic_vector(WL downto 0);
type aidGrid5 is array(numPartProd downto 0) of std_logic_vector((WL_INT+2*WL_FRAC)-1 downto 0);
type aidGrid4 is array(daddaLev4-1 downto 0) of std_logic_vector((WL_INT+2*WL_FRAC)-1 downto 0);
type aidGrid3 is array(daddaLev3-1 downto 0) of std_logic_vector((WL_INT+2*WL_FRAC)-1 downto 0);
type aidGrid2 is array(daddaLev2-1 downto 0) of std_logic_vector((WL_INT+2*WL_FRAC)-1 downto 0);
type aidGrid1 is array(daddaLev1-1 downto 0) of std_logic_vector((WL_INT+2*WL_FRAC)-1 downto 0);
type aidGrid0 is array(daddaLev0-1 downto 0) of std_logic_vector((WL_INT+2*WL_FRAC)-1 downto 0);
signal gridPPP: gridPreprocessedPP;
signal negVector: std_logic_vector(numPartProd-1 downto 0);
signal grid5: aidGrid5;
signal grid4: aidGrid4;
signal grid3: aidGrid3;
signal grid2: aidGrid2;
signal grid1: aidGrid1;
signal grid0: aidGrid0;

signal y_zeroTail: std_logic_vector(WL downto 0);

begin

-- ready y to extract the triplets for MBE
y_zeroTail(WL downto 0) <= y(WL-1 downto 0) & '0';

-- generate the blocks for the encoding
MBE_encoding_and_preprocessing_generation: 
	for i in numPartProd-1 downto 0 generate
		r4mbePP_preprocessing
			generic map (
				n_bit => WL )
			port map (
				x => x,
				y_tri => y_zeroTail(2*i+2 downto 2*i),
				neg => negVector(i),
				x_absY => gridPPP(i)(WL downto 0) );
end generate;

-- generate the blocks for the conditional negation
conditional_negation_blocks_generation:
	for i in numPartProd-1 downto 0 generate
		bitwiseInv
			generic (
				n_bit => WL+1 );
			port (
				invEnable => negVector(i),
				dataIn => gridPPP(i)(WL downto 0),
				dataOut => grid5(i)();
end generate;

-- assign to the grid5 all the negation bits to be added to the LSBs of the PP
negation_bits_assignment:
	for i in numPartProd-1 downto 0 generate
		grid(i+1)(2*i) <= negVector(i);
	end generate;

-- partial products assignment to grid5
preprocessedPP_assignment:
	for i in numPartProd-1 downto 0 generate
		
	end generate;


end architecture;