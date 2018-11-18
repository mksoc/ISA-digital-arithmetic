
-- fragment of the first approach with the dadda



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

