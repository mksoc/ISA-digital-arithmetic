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
signal gridPPP: aidGridPreprocessedPP;
signal gridPPP_conditional_N: aidGridPreprocessedPP;
signal negVector: std_logic_vector(numPartProd-1 downto 0);
signal grid5_begin: aidGrid5;
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
	for i in (numPartProd-1 downto 0) generate
		recoding_block: r4mbePP_preprocessing
			generic map (
				n_bit => WL )
			port map (
				x => x,
				y_tri => y_zeroTail(2*i+2 downto 2*i),
				neg => negVector(i),
				x_absY => gridPPP(i)(WL downto 0) );
end generate;

-- generate the blocks for the conditional negation and partial products assignment to grid5.
-- the "MSB" (most significant block, ie the block related to the PP generated from the 
-- most significant triplet) has not to take the incoming MSB, because it will not be used
-- for the calculation.
conditional_negation_blocks_generation:
	for i in (numPartProd-1 downto 0) generate

		MSBlock: if (i = numPartProd-1) generate
			bitwiseInverter11: bitwiseInv
				generic map (
					n_bit => WL+1 )
				port map (
					invEnable => negVector(i),
					dataIn => gridPPP(i)(WL-1 downto 0),
					dataOut => gridPPP_conditional_N(i)(WL-1 downto 0) );
		end generate MSBlock;

		LSBlocks: if (i < numPartProd-1) generate
			bitwiseInverterX: bitwiseInv
				generic map (
					n_bit => WL+1 )
				port map (
					invEnable => negVector(i),
					dataIn => gridPPP(i)(WL downto 0),
					dataOut => gridPPP_conditional_N(i)(WL downto 0) );
		end generate LSBlocks;

end generate;

-- partial product assignment to grid5 (with the correct bit in sign position, ready for the Dadda tree)
PPP_assignment_to_grid5_begin:
	for i in (numPartProd-1 downto 0) generate

		PPP_MSBlock: if (i = numPartProd-1) generate
			grid5_begin(i)((WL+2*i)-1 downto (2*i)) <= gridPPP_conditional_N(i)(WL-1 downto 0);
		end generate PPP_MSBlock;

		PPP_intermediateBlocks: if (i > 0 and i < numPartProd-1) generate 
			grid5_begin(i)((WL+2*i) downto (2*i)) <= not(gridPPP_conditional_N(i)(WL)) & gridPPP_conditional_N(i)(WL-1 downto 0);
		end generate PPP_intermediateBlocks;

		PPP_LSBlock: if (i = 0) generate 
			grid5_begin(i)((WL+2*i) downto (2*i)) <= gridPPP_conditional_N(i)(WL downto 0);
		end generate PPP_LSBlock;

end generate;

-- assign to the grid5 all the negation bits to be added to the LSBs of the PP
negation_bits_assignment:
	for i in (numPartProd-1 downto 0) generate
		grid5_begin(i+1)(2*i) <= negVector(i);
	end generate;

-- PP's MSBs assignment
PP_MSB_assignment:
	for i in (numPartProd-2 downto 0) generate

		otherPPs: if (i = 0) generate
			grid5_begin(i)(WL+2 downto WL+1) <= not(gridPPP_conditional_N(i)(WL)) & gridPPP_conditional_N(i)(WL);
		end generate otherPPs;

		firstPP: if (i > 0) generate
			grid5_begin(i)(WL+1 downto WL) <= '1' & not(gridPPP_conditional_N(i)(WL));
		end generate firstPP;

end generate;

-- flattening to ceiling
LSBs_passive_assignments:
	for i in (26 downto 0) generate
		grid5(daddaLev4-1 downto 0)(i) <= grid5_begin(daddaLev4-1 downto 0)(i);
end generate;

MSBs_reorganization:
	for i in (45 downto 27) generate

		odd_case: if (i mod 2 != 0 and i != 27) generate
			for j in (11-(1+(45-i)/2) to 11) generate
				grid5(j-(9+(i-27)/2)(i) <= grid5_begin(j)(i);
				grid5(j-(11-(1+(45-i)/2)))(i-1) <= grid5_begin(j)(i-1);
		end generate;

		odd_special_case: if (i = 27) generate
			for j in (9+(i-27)/2 to 11) generate
				grid5(j-(9+(i-27)/2)(i) <= grid5_begin(j)(i);
		end generate;
	
end generate;













-- DADDA tree level 4

-- columns from 0 to 15
LSBs_passive_assignments:
	for i in (15 downto 0) generate
		grid4(daddaLev4-1 downto 0)(i) <= grid5(daddaLev4-1 downto 0)(i);
end generate;

-- column 16
c16_HA: halfAdder 
	port map (
		i0 => grid5(0)(16),
		i1 => grid5(1)(16),
		s => grid4(0)(16),
		co => grid4(0)(17) );

c16_fallingUp:
	for i in (numPartProd-1 downto 2) generate
		grid4(i-1)(16) <= grid5(i)(16);
	end generate;

-- column 17 -- 1 cin
c17_HA: halfAdder 
	port map (
		i0 => grid5(0)(17),
		i1 => grid5(1)(17),
		s => grid4(1)(17),
		co => grid4(0)(18) );

c17_copying:
	for i in (numPartProd-1 downto 2) generate
		grid4(i)(17) <= grid5(i)(17);
	end generate;

-- column 18 -- 1 cin
c18_FA: fullAdder 
	port map (
		i0 => grid5(0)(18),
		i1 => grid5(1)(18),
		ci => grid5(2)(18),
		s => grid4(1)(18),
		co => grid4(0)(19) );
c18_HA: halfAdder 
	port map (
		i0 => grid5(3)(18),
		i1 => grid5(4)(18),
		s => grid4(2)(18),
		co => grid4(1)(19) );

c18_fallingUp:
	for i in (numPartProd-1 downto 5) generate
		grid4(i-2)(17) <= grid5(i)(17);
	end generate;

-- column 19 -- 2 cin
c19_FA: fullAdder 
	port map (
		i0 => grid5(0)(19),
		i1 => grid5(1)(19),
		ci => grid5(2)(19),
		s => grid4(3)(19),
		co => grid4(0)(20) );
c19_HA: halfAdder 
	port map (
		i0 => grid5(3)(19),
		i1 => grid5(4)(19),
		s => grid4(4)(19),
		co => grid4(1)(20) );

-- column 20 -- 2 cin

-- column 21

-- column 22

-- column 23

-- column 24

-- column 25

-- column 26

-- column 27

-- column 28

-- column 29

-- column 30

-- column 31

-- column 32

-- columns from 45 to 33
MSBs_reorganization:
	for i in (45 downto 35) generate

		odd_case: if (i mod 2 != 0 and i != 33) generate
			for j in (5+(i-35)/2 to 11) generate
				grid4(j-(5+(i-35)/2)(i) <= grid5(j)(i);
				grid4(j-(5+(i-35)/2)(i-1) <= grid5(j)(i-1);
		end generate;

		odd_special_case: if (i = 33) generate
			for j in (5+(i-35)/2 to 11) generate
				grid4(j-(5+(i-35)/2)(i) <= grid5(j)(i); 
		end generate;
	
end generate;



-- regular middle level
fourth_daddaLevel_13to9_0:
	for i in (26 downto 18) generate
		firstBlocksFA: fullAdder
			port map (
				i0 => grid5(0)(i),
				i1 => grid5(1)(i),
				ci => grid5(2)(i),
				s => ,
				co => );
	end generate;

fourth_daddaLevel_13to9_1:
	for i in (26 downto 20) generate
		secondBlocksFA: fullAdder
			port map (
				i0 => grid5(3)(i),
				i1 => grid5(4)(i),
				ci => grid5(5)(i),
				s => ,
				co => );
	end generate;

fourth_daddaLevel_13to9_2:
	for i in (26 downto 22) generate
		thirdBlocksFA: fullAdder
			port map (
				i0 => grid5(6)(i),
				i1 => grid5(7)(i),
				ci => grid5(8)(i),
				s => ,
				co => );
	end generate;

fourth_daddaLevel_13to9_3:
	for i in (26 downto 22) generate
		thirdBlocksHA: halfAdder
			port map (
				i0 => grid5(9)(i),
				i1 => grid5(10)(i),
				s => ,
				co => );
	end generate;



-- DADDA tree level 3

-- DADDA tree level 2

-- DADDA tree level 1

-- DADDA tree level 0

-- fast adder

-- truncation step

end architecture;

