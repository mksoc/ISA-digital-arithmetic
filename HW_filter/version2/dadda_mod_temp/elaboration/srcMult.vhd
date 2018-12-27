library ieee;
library work;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.multV1_pkg.all;

-- fast multiplier with radix-4 modified Booth encoding, with Roorda's trick, CSA+fast adder Dadda tree
entity mbeDadda_mult is
	port (
		x,											-- multiplicand
		y: in std_logic_vector(WL-1 downto 0);		-- multiplier

		p: out std_logic_vector(46 downto 0) );	-- product
end entity;

architecture structure of mbeDadda_mult is

	-- aidGrid5: matrix to have each column ready to be used
	-- numPartProd+1 rows and (WL_INT+2*WL_FRAC) columns (with fixed parallelism for integer part WL_INT there's
	-- no need for saving also the other two MSBs)
	signal gridPPP: aidGridPreprocessedPP;
	signal gridPPP_conditional_N: aidGridPreprocessedPP;
	signal grid5_begin: aidGrid5;
	signal grid5: aidGrid5;
	signal grid4: aidGrid4;
	signal grid3: aidGrid3;
	signal grid2: aidGrid2;
	signal grid1: aidGrid1;
	signal grid0: aidGrid0;

	signal add0, add1: std_logic_vector((WL_INT+2*WL_FRAC)-1 -{nBit} downto 0);
	signal sum: std_logic_vector((WL_INT+2*WL_FRAC)-1 -{nBit} downto 0);

	signal y_zeroTail: std_logic_vector(WL downto 0);
	signal negVector: std_logic_vector(numPartProd-1 downto 0);

begin

	-- ready y to extract the triplets for MBE
	y_zeroTail(WL downto 0) <= y(WL-1 downto 0) & '0';

	-- generate the blocks for the encoding
	MBE_encoding_and_preprocessing_generation:
		for i in numPartProd-1 downto 0 generate
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
		for i in numPartProd-1 downto 0 generate

			MSBlock: if (i = numPartProd-1) generate
				bitwiseInverter11: bitwiseInv
					generic map (
						n_bit => WL )
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
		for i in numPartProd-1 downto 0 generate

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
		for i in numPartProd-1 downto 0 generate
			grid5_begin(i+1)(2*i) <= negVector(i);
		end generate;

	-- PP's MSBs assignment (the real MSB has already been assigned (already assigned bits: (WL downto 0)). This assignment is from WL+1 bit to the left)
	PP_MSB_assignment:
		for i in numPartProd-2 downto 0 generate

			firstPP: if (i = 0) generate
				grid5_begin(i)((WL+2)+2*i downto (WL+1)+2*i) <= not(gridPPP_conditional_N(i)(WL)) & gridPPP_conditional_N(i)(WL);
			end generate firstPP;

			otherPPs: if (i > 0) generate
				grid5_begin(i)((WL+1)+2*i) <= '1';
			end generate otherPPs;

	end generate;

	-- flattening to ceiling
	LSBs_passive_assignments:
		for i in numPartProd downto 0 generate
			grid5(i)(26 downto 0) <= grid5_begin(i)(26 downto 0);
	end generate;


	MSBs_reorganization:
		for i in 45 downto 27 generate

			odd_case: if ((i mod 2 /= 0) and (i /= 27)) generate
				MSBs_odd_assignment:
					for j in (11-(1+(45-i)/2)) to 11 generate
						grid5(j-(11-(1+(45-i)/2)))(i) <= grid5_begin(j)(i);
						grid5(j-(11-(1+(45-i)/2)))(i-1) <= grid5_begin(j)(i-1);
					end generate;
			end generate odd_case;

			odd_special_case: if (i = 27) generate
				MSBs_odd_spec_assignment:
					for j in (11-(1+(45-i)/2)) to 11 generate
						grid5(j-(11-(1+(45-i)/2)))(i) <= grid5_begin(j)(i);
					end generate;
			end generate odd_special_case;

		end generate;

---DELIMITER---

	-- last two levels
	add0 <= grid0(0)((WL_INT+2*WL_FRAC)-1 downto {nBit});
	add1 <= grid0(1)((WL_INT+2*WL_FRAC)-1 downto {nBit});

	-- fast adder (to be implemented)
	sum <= std_logic_vector(signed(add0) + signed(add1));

	-- truncation step
	p <= sum(sum'length-1) & sum & ({nBit}-1 downto 0=>'0');

end architecture;
