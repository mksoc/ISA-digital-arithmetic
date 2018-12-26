library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.multV2_pkg.all;

entity mult_daddaroorda is
    port (
            multiplier:     in std_logic_vector (WL-1 downto 0);
            multiplicand:   in std_logic_vector (WL-1 downto 0);
            product:        out std_logic_vector (WL-1 downto 0)
    );
end entity;

architecture struct of mult_daddaroorda is
	signal add0s,add1s	: signed (39 downto 0);
	signal add0,add1	: std_logic_vector(39 downto 0);
    signal sum  		: signed(40 downto 0);
	signal inv  		: std_logic_vector(11 downto 0);
	signal recode0		: std_logic_vector(2 downto 0);
    signal grid5,pps	: aidGrid5;
	signal grid4		: aidGrid4;
	signal grid3		: aidGrid3;
	signal grid2		: aidGrid2;
	signal grid1		: aidGrid1;
	signal grid0		: aidGrid0;
    begin
--Modified booth encoding partial product generation
--first and last particular case + generate for

    GEN_MBE_PROCESSING:
    for I in 1 to 11 generate
    --for sake of semplicity I'm not truncating here. I'M LOOSING POWER.
        mbeX : r4mbePP_processing
        generic map (
                    N             =>    multiplicand'length)
        port map    (
                    multiplicand  =>    multiplicand,
                    recode_bits   =>    multiplier(2*I+1 downto 2*I-1),
                    inv           =>    inv(I),
                    part_prod     =>    pps(I)((WL+I*2) downto I*2));
	end generate;
	recode0<=multiplier(1) & multiplier(0) & '0';
    mbe0 : r4mbePP_processing
        generic map (
                    N             =>    multiplicand'length)
        port map    (
                    multiplicand  =>    multiplicand,
                    recode_bits   =>    recode0,
                    inv           =>    inv(0),
                    part_prod     =>    pps(0)((WL) downto 0));
--Adjust for Dadda tree + Roorda aproach
    --Connecting inv to the matrix
    INV_CONNECTION:
    for I in 1 to 12 generate
        pps(I)((I-1)*2)<=inv(I-1);
    end generate;

    --Roorda correction
    pps(0)(24)<=pps(0)(23);
    pps(0)(25)<=not(pps(0)(24));
    ROORDA_CORRECTION:
    for I in 1 to 12 generate
        pps(I)(WL+2*I)<=not pps(I)(WL+2*I-1);
        pps(I)(WL+2*I+1)<='1';
    end generate;

    --Justifing
    --odd 39 to 21 cols
    C39_to_21_ODD:
    for J in 11 downto 2 generate
        grid5(J-1 downto 0)(40-(((J-2)*2)+1))<=pps(11 downto 11-J+1)(46-(((J-2)*2)+1));
    end generate;

    --even 39 to 21 cols
    C39_to_21_EVEN:
    for J in 10 downto 2 generate
        grid5(J-1 downto 0)(40-(((J-2)*2)+2))<=pps(11 downto 11-J+1)(46-(((J-2)*2)+2));
    end generate;

    --from 20 to 17 cols
    C20_to_17:
    for I in 20 downto 17 generate
        grid5(11 downto 0)(I)<=pps(11 downto 0)(I+6);
    end generate;

    --col 16
    grid5(12 downto 0)(16)<=pps(12 downto 0)(16+6);

    -- from 15 to 0 even
    C15_to_0_EVEN:
    for J in 11 downto 4 generate
        grid5(J downto 0)(2*(J-4))<=pps(J downto 0)(2*(J-4)+6);
    end generate;

    --from 15 to 0 odd
    C15_to_0_ODD:
    for J in 11 downto 4 generate
        grid5(J-1 downto 0)(2*(J-4)+1)<=pps(J-1 downto 0)(2*(J-4)+6+1);
    end generate;

-----------------------------
-- DADDA TREE LEVEL4
-----------------------------

-----------------------------
-- COLUMN 0
-----------------------------
-- move the other elements of the column
grid4(0)(0) <= grid5(0)(0);
grid4(1)(0) <= grid5(1)(0);
grid4(2)(0) <= grid5(2)(0);
grid4(3)(0) <= grid5(3)(0);
grid4(4)(0) <= grid5(4)(0);

-----------------------------
-- COLUMN 1
-----------------------------
-- move the other elements of the column
grid4(0)(1) <= grid5(0)(1);
grid4(1)(1) <= grid5(1)(1);
grid4(2)(1) <= grid5(2)(1);
grid4(3)(1) <= grid5(3)(1);

-----------------------------
-- COLUMN 2
-----------------------------
-- move the other elements of the column
grid4(0)(2) <= grid5(0)(2);
grid4(1)(2) <= grid5(1)(2);
grid4(2)(2) <= grid5(2)(2);
grid4(3)(2) <= grid5(3)(2);
grid4(4)(2) <= grid5(4)(2);
grid4(5)(2) <= grid5(5)(2);

-----------------------------
-- COLUMN 3
-----------------------------
-- move the other elements of the column
grid4(0)(3) <= grid5(0)(3);
grid4(1)(3) <= grid5(1)(3);
grid4(2)(3) <= grid5(2)(3);
grid4(3)(3) <= grid5(3)(3);
grid4(4)(3) <= grid5(4)(3);

-----------------------------
-- COLUMN 4
-----------------------------
-- move the other elements of the column
grid4(0)(4) <= grid5(0)(4);
grid4(1)(4) <= grid5(1)(4);
grid4(2)(4) <= grid5(2)(4);
grid4(3)(4) <= grid5(3)(4);
grid4(4)(4) <= grid5(4)(4);
grid4(5)(4) <= grid5(5)(4);
grid4(6)(4) <= grid5(6)(4);

-----------------------------
-- COLUMN 5
-----------------------------
-- move the other elements of the column
grid4(0)(5) <= grid5(0)(5);
grid4(1)(5) <= grid5(1)(5);
grid4(2)(5) <= grid5(2)(5);
grid4(3)(5) <= grid5(3)(5);
grid4(4)(5) <= grid5(4)(5);
grid4(5)(5) <= grid5(5)(5);

-----------------------------
-- COLUMN 6
-----------------------------
-- move the other elements of the column
grid4(0)(6) <= grid5(0)(6);
grid4(1)(6) <= grid5(1)(6);
grid4(2)(6) <= grid5(2)(6);
grid4(3)(6) <= grid5(3)(6);
grid4(4)(6) <= grid5(4)(6);
grid4(5)(6) <= grid5(5)(6);
grid4(6)(6) <= grid5(6)(6);
grid4(7)(6) <= grid5(7)(6);

-----------------------------
-- COLUMN 7
-----------------------------
-- move the other elements of the column
grid4(0)(7) <= grid5(0)(7);
grid4(1)(7) <= grid5(1)(7);
grid4(2)(7) <= grid5(2)(7);
grid4(3)(7) <= grid5(3)(7);
grid4(4)(7) <= grid5(4)(7);
grid4(5)(7) <= grid5(5)(7);
grid4(6)(7) <= grid5(6)(7);

-----------------------------
-- COLUMN 8
-----------------------------
-- move the other elements of the column
grid4(0)(8) <= grid5(0)(8);
grid4(1)(8) <= grid5(1)(8);
grid4(2)(8) <= grid5(2)(8);
grid4(3)(8) <= grid5(3)(8);
grid4(4)(8) <= grid5(4)(8);
grid4(5)(8) <= grid5(5)(8);
grid4(6)(8) <= grid5(6)(8);
grid4(7)(8) <= grid5(7)(8);
grid4(8)(8) <= grid5(8)(8);

-----------------------------
-- COLUMN 9
-----------------------------
-- move the other elements of the column
grid4(0)(9) <= grid5(0)(9);
grid4(1)(9) <= grid5(1)(9);
grid4(2)(9) <= grid5(2)(9);
grid4(3)(9) <= grid5(3)(9);
grid4(4)(9) <= grid5(4)(9);
grid4(5)(9) <= grid5(5)(9);
grid4(6)(9) <= grid5(6)(9);
grid4(7)(9) <= grid5(7)(9);

-----------------------------
-- COLUMN 10
-----------------------------
-- half adder c10, number 0
lv4_c10_HA_0: halfAdder
	port map (
		i0 => grid5(0)(10),
		i1 => grid5(1)(10),
		s => grid4(0)(10),
		co => grid4(0)(11) );

-- move the other elements of the column
grid4(1)(10) <= grid5(2)(10);
grid4(2)(10) <= grid5(3)(10);
grid4(3)(10) <= grid5(4)(10);
grid4(4)(10) <= grid5(5)(10);
grid4(5)(10) <= grid5(6)(10);
grid4(6)(10) <= grid5(7)(10);
grid4(7)(10) <= grid5(8)(10);
grid4(8)(10) <= grid5(9)(10);

-----------------------------
-- COLUMN 11
-----------------------------
-- half adder c11, number 0
lv4_c11_HA_0: halfAdder
	port map (
		i0 => grid5(0)(11),
		i1 => grid5(1)(11),
		s => grid4(1)(11),
		co => grid4(0)(12) );

-- move the other elements of the column
grid4(2)(11) <= grid5(2)(11);
grid4(3)(11) <= grid5(3)(11);
grid4(4)(11) <= grid5(4)(11);
grid4(5)(11) <= grid5(5)(11);
grid4(6)(11) <= grid5(6)(11);
grid4(7)(11) <= grid5(7)(11);
grid4(8)(11) <= grid5(8)(11);

-----------------------------
-- COLUMN 12
-----------------------------
-- full adder c12, number 0
lv4_c12_FA_0: fullAdder
	port map (
		i0 => grid5(0)(12),
		i1 => grid5(1)(12),
		ci => grid5(2)(12),
		s => grid4(1)(12),
		co => grid4(0)(13) );

-- half adder c12, number 0
lv4_c12_HA_0: halfAdder
	port map (
		i0 => grid5(3)(12),
		i1 => grid5(4)(12),
		s => grid4(2)(12),
		co => grid4(1)(13) );

-- move the other elements of the column
grid4(3)(12) <= grid5(5)(12);
grid4(4)(12) <= grid5(6)(12);
grid4(5)(12) <= grid5(7)(12);
grid4(6)(12) <= grid5(8)(12);
grid4(7)(12) <= grid5(9)(12);
grid4(8)(12) <= grid5(10)(12);

-----------------------------
-- COLUMN 13
-----------------------------
-- full adder c13, number 0
lv4_c13_FA_0: fullAdder
	port map (
		i0 => grid5(0)(13),
		i1 => grid5(1)(13),
		ci => grid5(2)(13),
		s => grid4(2)(13),
		co => grid4(0)(14) );

-- half adder c13, number 0
lv4_c13_HA_0: halfAdder
	port map (
		i0 => grid5(3)(13),
		i1 => grid5(4)(13),
		s => grid4(3)(13),
		co => grid4(1)(14) );

-- move the other elements of the column
grid4(4)(13) <= grid5(5)(13);
grid4(5)(13) <= grid5(6)(13);
grid4(6)(13) <= grid5(7)(13);
grid4(7)(13) <= grid5(8)(13);
grid4(8)(13) <= grid5(9)(13);

-----------------------------
-- COLUMN 14
-----------------------------
-- full adder c14, number 0
lv4_c14_FA_0: fullAdder
	port map (
		i0 => grid5(0)(14),
		i1 => grid5(1)(14),
		ci => grid5(2)(14),
		s => grid4(2)(14),
		co => grid4(0)(15) );

-- full adder c14, number 1
lv4_c14_FA_1: fullAdder
	port map (
		i0 => grid5(3)(14),
		i1 => grid5(4)(14),
		ci => grid5(5)(14),
		s => grid4(3)(14),
		co => grid4(1)(15) );

-- half adder c14, number 0
lv4_c14_HA_0: halfAdder
	port map (
		i0 => grid5(6)(14),
		i1 => grid5(7)(14),
		s => grid4(4)(14),
		co => grid4(2)(15) );

-- move the other elements of the column
grid4(5)(14) <= grid5(8)(14);
grid4(6)(14) <= grid5(9)(14);
grid4(7)(14) <= grid5(10)(14);
grid4(8)(14) <= grid5(11)(14);

-----------------------------
-- COLUMN 15
-----------------------------
-- full adder c15, number 0
lv4_c15_FA_0: fullAdder
	port map (
		i0 => grid5(0)(15),
		i1 => grid5(1)(15),
		ci => grid5(2)(15),
		s => grid4(3)(15),
		co => grid4(0)(16) );

-- full adder c15, number 1
lv4_c15_FA_1: fullAdder
	port map (
		i0 => grid5(3)(15),
		i1 => grid5(4)(15),
		ci => grid5(5)(15),
		s => grid4(4)(15),
		co => grid4(1)(16) );

-- half adder c15, number 0
lv4_c15_HA_0: halfAdder
	port map (
		i0 => grid5(6)(15),
		i1 => grid5(7)(15),
		s => grid4(5)(15),
		co => grid4(2)(16) );

-- move the other elements of the column
grid4(6)(15) <= grid5(8)(15);
grid4(7)(15) <= grid5(9)(15);
grid4(8)(15) <= grid5(10)(15);

-----------------------------
-- COLUMN 16
-----------------------------
-- full adder c16, number 0
lv4_c16_FA_0: fullAdder
	port map (
		i0 => grid5(0)(16),
		i1 => grid5(1)(16),
		ci => grid5(2)(16),
		s => grid4(3)(16),
		co => grid4(0)(17) );

-- full adder c16, number 1
lv4_c16_FA_1: fullAdder
	port map (
		i0 => grid5(3)(16),
		i1 => grid5(4)(16),
		ci => grid5(5)(16),
		s => grid4(4)(16),
		co => grid4(1)(17) );

-- full adder c16, number 2
lv4_c16_FA_2: fullAdder
	port map (
		i0 => grid5(6)(16),
		i1 => grid5(7)(16),
		ci => grid5(8)(16),
		s => grid4(5)(16),
		co => grid4(2)(17) );

-- half adder c16, number 0
lv4_c16_HA_0: halfAdder
	port map (
		i0 => grid5(9)(16),
		i1 => grid5(10)(16),
		s => grid4(6)(16),
		co => grid4(3)(17) );

-- move the other elements of the column
grid4(7)(16) <= grid5(11)(16);
grid4(8)(16) <= grid5(12)(16);

-----------------------------
-- COLUMN 17
-----------------------------
-- full adder c17, number 0
lv4_c17_FA_0: fullAdder
	port map (
		i0 => grid5(0)(17),
		i1 => grid5(1)(17),
		ci => grid5(2)(17),
		s => grid4(4)(17),
		co => grid4(0)(18) );

-- full adder c17, number 1
lv4_c17_FA_1: fullAdder
	port map (
		i0 => grid5(3)(17),
		i1 => grid5(4)(17),
		ci => grid5(5)(17),
		s => grid4(5)(17),
		co => grid4(1)(18) );

-- full adder c17, number 2
lv4_c17_FA_2: fullAdder
	port map (
		i0 => grid5(6)(17),
		i1 => grid5(7)(17),
		ci => grid5(8)(17),
		s => grid4(6)(17),
		co => grid4(2)(18) );

-- half adder c17, number 0
lv4_c17_HA_0: halfAdder
	port map (
		i0 => grid5(9)(17),
		i1 => grid5(10)(17),
		s => grid4(7)(17),
		co => grid4(3)(18) );

-- move the other elements of the column
grid4(8)(17) <= grid5(11)(17);

-----------------------------
-- COLUMN 18
-----------------------------
-- full adder c18, number 0
lv4_c18_FA_0: fullAdder
	port map (
		i0 => grid5(0)(18),
		i1 => grid5(1)(18),
		ci => grid5(2)(18),
		s => grid4(4)(18),
		co => grid4(0)(19) );

-- full adder c18, number 1
lv4_c18_FA_1: fullAdder
	port map (
		i0 => grid5(3)(18),
		i1 => grid5(4)(18),
		ci => grid5(5)(18),
		s => grid4(5)(18),
		co => grid4(1)(19) );

-- full adder c18, number 2
lv4_c18_FA_2: fullAdder
	port map (
		i0 => grid5(6)(18),
		i1 => grid5(7)(18),
		ci => grid5(8)(18),
		s => grid4(6)(18),
		co => grid4(2)(19) );

-- half adder c18, number 0
lv4_c18_HA_0: halfAdder
	port map (
		i0 => grid5(9)(18),
		i1 => grid5(10)(18),
		s => grid4(7)(18),
		co => grid4(3)(19) );

-- move the other elements of the column
grid4(8)(18) <= grid5(11)(18);

-----------------------------
-- COLUMN 19
-----------------------------
-- full adder c19, number 0
lv4_c19_FA_0: fullAdder
	port map (
		i0 => grid5(0)(19),
		i1 => grid5(1)(19),
		ci => grid5(2)(19),
		s => grid4(4)(19),
		co => grid4(0)(20) );

-- full adder c19, number 1
lv4_c19_FA_1: fullAdder
	port map (
		i0 => grid5(3)(19),
		i1 => grid5(4)(19),
		ci => grid5(5)(19),
		s => grid4(5)(19),
		co => grid4(1)(20) );

-- full adder c19, number 2
lv4_c19_FA_2: fullAdder
	port map (
		i0 => grid5(6)(19),
		i1 => grid5(7)(19),
		ci => grid5(8)(19),
		s => grid4(6)(19),
		co => grid4(2)(20) );

-- half adder c19, number 0
lv4_c19_HA_0: halfAdder
	port map (
		i0 => grid5(9)(19),
		i1 => grid5(10)(19),
		s => grid4(7)(19),
		co => grid4(3)(20) );

-- move the other elements of the column
grid4(8)(19) <= grid5(11)(19);

-----------------------------
-- COLUMN 20
-----------------------------
-- full adder c20, number 0
lv4_c20_FA_0: fullAdder
	port map (
		i0 => grid5(0)(20),
		i1 => grid5(1)(20),
		ci => grid5(2)(20),
		s => grid4(4)(20),
		co => grid4(0)(21) );

-- full adder c20, number 1
lv4_c20_FA_1: fullAdder
	port map (
		i0 => grid5(3)(20),
		i1 => grid5(4)(20),
		ci => grid5(5)(20),
		s => grid4(5)(20),
		co => grid4(1)(21) );

-- full adder c20, number 2
lv4_c20_FA_2: fullAdder
	port map (
		i0 => grid5(6)(20),
		i1 => grid5(7)(20),
		ci => grid5(8)(20),
		s => grid4(6)(20),
		co => grid4(2)(21) );

-- half adder c20, number 0
lv4_c20_HA_0: halfAdder
	port map (
		i0 => grid5(9)(20),
		i1 => grid5(10)(20),
		s => grid4(7)(20),
		co => grid4(3)(21) );

-- move the other elements of the column
grid4(8)(20) <= grid5(11)(20);

-----------------------------
-- COLUMN 21
-----------------------------
-- full adder c21, number 0
lv4_c21_FA_0: fullAdder
	port map (
		i0 => grid5(0)(21),
		i1 => grid5(1)(21),
		ci => grid5(2)(21),
		s => grid4(4)(21),
		co => grid4(0)(22) );

-- full adder c21, number 1
lv4_c21_FA_1: fullAdder
	port map (
		i0 => grid5(3)(21),
		i1 => grid5(4)(21),
		ci => grid5(5)(21),
		s => grid4(5)(21),
		co => grid4(1)(22) );

-- full adder c21, number 2
lv4_c21_FA_2: fullAdder
	port map (
		i0 => grid5(6)(21),
		i1 => grid5(7)(21),
		ci => grid5(8)(21),
		s => grid4(6)(21),
		co => grid4(2)(22) );

-- move the other elements of the column
grid4(7)(21) <= grid5(9)(21);
grid4(8)(21) <= grid5(10)(21);

-----------------------------
-- COLUMN 22
-----------------------------
-- full adder c22, number 0
lv4_c22_FA_0: fullAdder
	port map (
		i0 => grid5(0)(22),
		i1 => grid5(1)(22),
		ci => grid5(2)(22),
		s => grid4(3)(22),
		co => grid4(0)(23) );

-- full adder c22, number 1
lv4_c22_FA_1: fullAdder
	port map (
		i0 => grid5(3)(22),
		i1 => grid5(4)(22),
		ci => grid5(5)(22),
		s => grid4(4)(22),
		co => grid4(1)(23) );

-- move the other elements of the column
grid4(5)(22) <= grid5(6)(22);
grid4(6)(22) <= grid5(7)(22);
grid4(7)(22) <= grid5(8)(22);
grid4(8)(22) <= grid5(9)(22);

-----------------------------
-- COLUMN 23
-----------------------------
-- full adder c23, number 0
lv4_c23_FA_0: fullAdder
	port map (
		i0 => grid5(0)(23),
		i1 => grid5(1)(23),
		ci => grid5(2)(23),
		s => grid4(2)(23),
		co => grid4(0)(24) );

-- half adder c23, number 0
lv4_c23_HA_0: halfAdder
	port map (
		i0 => grid5(3)(23),
		i1 => grid5(4)(23),
		s => grid4(3)(23),
		co => grid4(1)(24) );

-- move the other elements of the column
grid4(4)(23) <= grid5(5)(23);
grid4(5)(23) <= grid5(6)(23);
grid4(6)(23) <= grid5(7)(23);
grid4(7)(23) <= grid5(8)(23);
grid4(8)(23) <= grid5(9)(23);

-----------------------------
-- COLUMN 24
-----------------------------
-- full adder c24, number 0
lv4_c24_FA_0: fullAdder
	port map (
		i0 => grid5(0)(24),
		i1 => grid5(1)(24),
		ci => grid5(2)(24),
		s => grid4(2)(24),
		co => grid4(0)(25) );

-- move the other elements of the column
grid4(3)(24) <= grid5(3)(24);
grid4(4)(24) <= grid5(4)(24);
grid4(5)(24) <= grid5(5)(24);
grid4(6)(24) <= grid5(6)(24);
grid4(7)(24) <= grid5(7)(24);
grid4(8)(24) <= grid5(8)(24);

-----------------------------
-- COLUMN 25
-----------------------------
-- half adder c25, number 0
lv4_c25_HA_0: halfAdder
	port map (
		i0 => grid5(0)(25),
		i1 => grid5(1)(25),
		s => grid4(1)(25),
		co => grid4(0)(26) );

-- move the other elements of the column
grid4(2)(25) <= grid5(2)(25);
grid4(3)(25) <= grid5(3)(25);
grid4(4)(25) <= grid5(4)(25);
grid4(5)(25) <= grid5(5)(25);
grid4(6)(25) <= grid5(6)(25);
grid4(7)(25) <= grid5(7)(25);
grid4(8)(25) <= grid5(8)(25);

-----------------------------
-- COLUMN 26
-----------------------------
-- move the other elements of the column
grid4(1)(26) <= grid5(0)(26);
grid4(2)(26) <= grid5(1)(26);
grid4(3)(26) <= grid5(2)(26);
grid4(4)(26) <= grid5(3)(26);
grid4(5)(26) <= grid5(4)(26);
grid4(6)(26) <= grid5(5)(26);
grid4(7)(26) <= grid5(6)(26);
grid4(8)(26) <= grid5(7)(26);

-----------------------------
-- COLUMN 27
-----------------------------
-- move the other elements of the column
grid4(0)(27) <= grid5(0)(27);
grid4(1)(27) <= grid5(1)(27);
grid4(2)(27) <= grid5(2)(27);
grid4(3)(27) <= grid5(3)(27);
grid4(4)(27) <= grid5(4)(27);
grid4(5)(27) <= grid5(5)(27);
grid4(6)(27) <= grid5(6)(27);
grid4(7)(27) <= grid5(7)(27);

-----------------------------
-- COLUMN 28
-----------------------------
-- move the other elements of the column
grid4(0)(28) <= grid5(0)(28);
grid4(1)(28) <= grid5(1)(28);
grid4(2)(28) <= grid5(2)(28);
grid4(3)(28) <= grid5(3)(28);
grid4(4)(28) <= grid5(4)(28);
grid4(5)(28) <= grid5(5)(28);
grid4(6)(28) <= grid5(6)(28);

-----------------------------
-- COLUMN 29
-----------------------------
-- move the other elements of the column
grid4(0)(29) <= grid5(0)(29);
grid4(1)(29) <= grid5(1)(29);
grid4(2)(29) <= grid5(2)(29);
grid4(3)(29) <= grid5(3)(29);
grid4(4)(29) <= grid5(4)(29);
grid4(5)(29) <= grid5(5)(29);
grid4(6)(29) <= grid5(6)(29);

-----------------------------
-- COLUMN 30
-----------------------------
-- move the other elements of the column
grid4(0)(30) <= grid5(0)(30);
grid4(1)(30) <= grid5(1)(30);
grid4(2)(30) <= grid5(2)(30);
grid4(3)(30) <= grid5(3)(30);
grid4(4)(30) <= grid5(4)(30);
grid4(5)(30) <= grid5(5)(30);

-----------------------------
-- COLUMN 31
-----------------------------
-- move the other elements of the column
grid4(0)(31) <= grid5(0)(31);
grid4(1)(31) <= grid5(1)(31);
grid4(2)(31) <= grid5(2)(31);
grid4(3)(31) <= grid5(3)(31);
grid4(4)(31) <= grid5(4)(31);
grid4(5)(31) <= grid5(5)(31);

-----------------------------
-- COLUMN 32
-----------------------------
-- move the other elements of the column
grid4(0)(32) <= grid5(0)(32);
grid4(1)(32) <= grid5(1)(32);
grid4(2)(32) <= grid5(2)(32);
grid4(3)(32) <= grid5(3)(32);
grid4(4)(32) <= grid5(4)(32);

-----------------------------
-- COLUMN 33
-----------------------------
-- move the other elements of the column
grid4(0)(33) <= grid5(0)(33);
grid4(1)(33) <= grid5(1)(33);
grid4(2)(33) <= grid5(2)(33);
grid4(3)(33) <= grid5(3)(33);
grid4(4)(33) <= grid5(4)(33);

-----------------------------
-- COLUMN 34
-----------------------------
-- move the other elements of the column
grid4(0)(34) <= grid5(0)(34);
grid4(1)(34) <= grid5(1)(34);
grid4(2)(34) <= grid5(2)(34);
grid4(3)(34) <= grid5(3)(34);

-----------------------------
-- COLUMN 35
-----------------------------
-- move the other elements of the column
grid4(0)(35) <= grid5(0)(35);
grid4(1)(35) <= grid5(1)(35);
grid4(2)(35) <= grid5(2)(35);
grid4(3)(35) <= grid5(3)(35);

-----------------------------
-- COLUMN 36
-----------------------------
-- move the other elements of the column
grid4(0)(36) <= grid5(0)(36);
grid4(1)(36) <= grid5(1)(36);
grid4(2)(36) <= grid5(2)(36);

-----------------------------
-- COLUMN 37
-----------------------------
-- move the other elements of the column
grid4(0)(37) <= grid5(0)(37);
grid4(1)(37) <= grid5(1)(37);
grid4(2)(37) <= grid5(2)(37);

-----------------------------
-- COLUMN 38
-----------------------------
-- move the other elements of the column
grid4(0)(38) <= grid5(0)(38);
grid4(1)(38) <= grid5(1)(38);

-----------------------------
-- COLUMN 39
-----------------------------
-- move the other elements of the column
grid4(0)(39) <= grid5(0)(39);
grid4(1)(39) <= grid5(1)(39);

-----------------------------
-- DADDA TREE LEVEL3
-----------------------------

-----------------------------
-- COLUMN 0
-----------------------------
-- move the other elements of the column
grid3(0)(0) <= grid4(0)(0);
grid3(1)(0) <= grid4(1)(0);
grid3(2)(0) <= grid4(2)(0);
grid3(3)(0) <= grid4(3)(0);
grid3(4)(0) <= grid4(4)(0);

-----------------------------
-- COLUMN 1
-----------------------------
-- move the other elements of the column
grid3(0)(1) <= grid4(0)(1);
grid3(1)(1) <= grid4(1)(1);
grid3(2)(1) <= grid4(2)(1);
grid3(3)(1) <= grid4(3)(1);

-----------------------------
-- COLUMN 2
-----------------------------
-- move the other elements of the column
grid3(0)(2) <= grid4(0)(2);
grid3(1)(2) <= grid4(1)(2);
grid3(2)(2) <= grid4(2)(2);
grid3(3)(2) <= grid4(3)(2);
grid3(4)(2) <= grid4(4)(2);
grid3(5)(2) <= grid4(5)(2);

-----------------------------
-- COLUMN 3
-----------------------------
-- move the other elements of the column
grid3(0)(3) <= grid4(0)(3);
grid3(1)(3) <= grid4(1)(3);
grid3(2)(3) <= grid4(2)(3);
grid3(3)(3) <= grid4(3)(3);
grid3(4)(3) <= grid4(4)(3);

-----------------------------
-- COLUMN 4
-----------------------------
-- half adder c4, number 0
lv3_c4_HA_0: halfAdder
	port map (
		i0 => grid4(0)(4),
		i1 => grid4(1)(4),
		s => grid3(0)(4),
		co => grid3(0)(5) );

-- move the other elements of the column
grid3(1)(4) <= grid4(2)(4);
grid3(2)(4) <= grid4(3)(4);
grid3(3)(4) <= grid4(4)(4);
grid3(4)(4) <= grid4(5)(4);
grid3(5)(4) <= grid4(6)(4);

-----------------------------
-- COLUMN 5
-----------------------------
-- half adder c5, number 0
lv3_c5_HA_0: halfAdder
	port map (
		i0 => grid4(0)(5),
		i1 => grid4(1)(5),
		s => grid3(1)(5),
		co => grid3(0)(6) );

-- move the other elements of the column
grid3(2)(5) <= grid4(2)(5);
grid3(3)(5) <= grid4(3)(5);
grid3(4)(5) <= grid4(4)(5);
grid3(5)(5) <= grid4(5)(5);

-----------------------------
-- COLUMN 6
-----------------------------
-- full adder c6, number 0
lv3_c6_FA_0: fullAdder
	port map (
		i0 => grid4(0)(6),
		i1 => grid4(1)(6),
		ci => grid4(2)(6),
		s => grid3(1)(6),
		co => grid3(0)(7) );

-- half adder c6, number 0
lv3_c6_HA_0: halfAdder
	port map (
		i0 => grid4(3)(6),
		i1 => grid4(4)(6),
		s => grid3(2)(6),
		co => grid3(1)(7) );

-- move the other elements of the column
grid3(3)(6) <= grid4(5)(6);
grid3(4)(6) <= grid4(6)(6);
grid3(5)(6) <= grid4(7)(6);

-----------------------------
-- COLUMN 7
-----------------------------
-- full adder c7, number 0
lv3_c7_FA_0: fullAdder
	port map (
		i0 => grid4(0)(7),
		i1 => grid4(1)(7),
		ci => grid4(2)(7),
		s => grid3(2)(7),
		co => grid3(0)(8) );

-- half adder c7, number 0
lv3_c7_HA_0: halfAdder
	port map (
		i0 => grid4(3)(7),
		i1 => grid4(4)(7),
		s => grid3(3)(7),
		co => grid3(1)(8) );

-- move the other elements of the column
grid3(4)(7) <= grid4(5)(7);
grid3(5)(7) <= grid4(6)(7);

-----------------------------
-- COLUMN 8
-----------------------------
-- full adder c8, number 0
lv3_c8_FA_0: fullAdder
	port map (
		i0 => grid4(0)(8),
		i1 => grid4(1)(8),
		ci => grid4(2)(8),
		s => grid3(2)(8),
		co => grid3(0)(9) );

-- full adder c8, number 1
lv3_c8_FA_1: fullAdder
	port map (
		i0 => grid4(3)(8),
		i1 => grid4(4)(8),
		ci => grid4(5)(8),
		s => grid3(3)(8),
		co => grid3(1)(9) );

-- half adder c8, number 0
lv3_c8_HA_0: halfAdder
	port map (
		i0 => grid4(6)(8),
		i1 => grid4(7)(8),
		s => grid3(4)(8),
		co => grid3(2)(9) );

-- move the other elements of the column
grid3(5)(8) <= grid4(8)(8);

-----------------------------
-- COLUMN 9
-----------------------------
-- full adder c9, number 0
lv3_c9_FA_0: fullAdder
	port map (
		i0 => grid4(0)(9),
		i1 => grid4(1)(9),
		ci => grid4(2)(9),
		s => grid3(3)(9),
		co => grid3(0)(10) );

-- full adder c9, number 1
lv3_c9_FA_1: fullAdder
	port map (
		i0 => grid4(3)(9),
		i1 => grid4(4)(9),
		ci => grid4(5)(9),
		s => grid3(4)(9),
		co => grid3(1)(10) );

-- half adder c9, number 0
lv3_c9_HA_0: halfAdder
	port map (
		i0 => grid4(6)(9),
		i1 => grid4(7)(9),
		s => grid3(5)(9),
		co => grid3(2)(10) );

-- move the other elements of the column

-----------------------------
-- COLUMN 10
-----------------------------
-- full adder c10, number 0
lv3_c10_FA_0: fullAdder
	port map (
		i0 => grid4(0)(10),
		i1 => grid4(1)(10),
		ci => grid4(2)(10),
		s => grid3(3)(10),
		co => grid3(0)(11) );

-- full adder c10, number 1
lv3_c10_FA_1: fullAdder
	port map (
		i0 => grid4(3)(10),
		i1 => grid4(4)(10),
		ci => grid4(5)(10),
		s => grid3(4)(10),
		co => grid3(1)(11) );

-- full adder c10, number 2
lv3_c10_FA_2: fullAdder
	port map (
		i0 => grid4(6)(10),
		i1 => grid4(7)(10),
		ci => grid4(8)(10),
		s => grid3(5)(10),
		co => grid3(2)(11) );

-- move the other elements of the column

-----------------------------
-- COLUMN 11
-----------------------------
-- full adder c11, number 0
lv3_c11_FA_0: fullAdder
	port map (
		i0 => grid4(0)(11),
		i1 => grid4(1)(11),
		ci => grid4(2)(11),
		s => grid3(3)(11),
		co => grid3(0)(12) );

-- full adder c11, number 1
lv3_c11_FA_1: fullAdder
	port map (
		i0 => grid4(3)(11),
		i1 => grid4(4)(11),
		ci => grid4(5)(11),
		s => grid3(4)(11),
		co => grid3(1)(12) );

-- full adder c11, number 2
lv3_c11_FA_2: fullAdder
	port map (
		i0 => grid4(6)(11),
		i1 => grid4(7)(11),
		ci => grid4(8)(11),
		s => grid3(5)(11),
		co => grid3(2)(12) );

-- move the other elements of the column

-----------------------------
-- COLUMN 12
-----------------------------
-- full adder c12, number 0
lv3_c12_FA_0: fullAdder
	port map (
		i0 => grid4(0)(12),
		i1 => grid4(1)(12),
		ci => grid4(2)(12),
		s => grid3(3)(12),
		co => grid3(0)(13) );

-- full adder c12, number 1
lv3_c12_FA_1: fullAdder
	port map (
		i0 => grid4(3)(12),
		i1 => grid4(4)(12),
		ci => grid4(5)(12),
		s => grid3(4)(12),
		co => grid3(1)(13) );

-- full adder c12, number 2
lv3_c12_FA_2: fullAdder
	port map (
		i0 => grid4(6)(12),
		i1 => grid4(7)(12),
		ci => grid4(8)(12),
		s => grid3(5)(12),
		co => grid3(2)(13) );

-- move the other elements of the column

-----------------------------
-- COLUMN 13
-----------------------------
-- full adder c13, number 0
lv3_c13_FA_0: fullAdder
	port map (
		i0 => grid4(0)(13),
		i1 => grid4(1)(13),
		ci => grid4(2)(13),
		s => grid3(3)(13),
		co => grid3(0)(14) );

-- full adder c13, number 1
lv3_c13_FA_1: fullAdder
	port map (
		i0 => grid4(3)(13),
		i1 => grid4(4)(13),
		ci => grid4(5)(13),
		s => grid3(4)(13),
		co => grid3(1)(14) );

-- full adder c13, number 2
lv3_c13_FA_2: fullAdder
	port map (
		i0 => grid4(6)(13),
		i1 => grid4(7)(13),
		ci => grid4(8)(13),
		s => grid3(5)(13),
		co => grid3(2)(14) );

-- move the other elements of the column

-----------------------------
-- COLUMN 14
-----------------------------
-- full adder c14, number 0
lv3_c14_FA_0: fullAdder
	port map (
		i0 => grid4(0)(14),
		i1 => grid4(1)(14),
		ci => grid4(2)(14),
		s => grid3(3)(14),
		co => grid3(0)(15) );

-- full adder c14, number 1
lv3_c14_FA_1: fullAdder
	port map (
		i0 => grid4(3)(14),
		i1 => grid4(4)(14),
		ci => grid4(5)(14),
		s => grid3(4)(14),
		co => grid3(1)(15) );

-- full adder c14, number 2
lv3_c14_FA_2: fullAdder
	port map (
		i0 => grid4(6)(14),
		i1 => grid4(7)(14),
		ci => grid4(8)(14),
		s => grid3(5)(14),
		co => grid3(2)(15) );

-- move the other elements of the column

-----------------------------
-- COLUMN 15
-----------------------------
-- full adder c15, number 0
lv3_c15_FA_0: fullAdder
	port map (
		i0 => grid4(0)(15),
		i1 => grid4(1)(15),
		ci => grid4(2)(15),
		s => grid3(3)(15),
		co => grid3(0)(16) );

-- full adder c15, number 1
lv3_c15_FA_1: fullAdder
	port map (
		i0 => grid4(3)(15),
		i1 => grid4(4)(15),
		ci => grid4(5)(15),
		s => grid3(4)(15),
		co => grid3(1)(16) );

-- full adder c15, number 2
lv3_c15_FA_2: fullAdder
	port map (
		i0 => grid4(6)(15),
		i1 => grid4(7)(15),
		ci => grid4(8)(15),
		s => grid3(5)(15),
		co => grid3(2)(16) );

-- move the other elements of the column

-----------------------------
-- COLUMN 16
-----------------------------
-- full adder c16, number 0
lv3_c16_FA_0: fullAdder
	port map (
		i0 => grid4(0)(16),
		i1 => grid4(1)(16),
		ci => grid4(2)(16),
		s => grid3(3)(16),
		co => grid3(0)(17) );

-- full adder c16, number 1
lv3_c16_FA_1: fullAdder
	port map (
		i0 => grid4(3)(16),
		i1 => grid4(4)(16),
		ci => grid4(5)(16),
		s => grid3(4)(16),
		co => grid3(1)(17) );

-- full adder c16, number 2
lv3_c16_FA_2: fullAdder
	port map (
		i0 => grid4(6)(16),
		i1 => grid4(7)(16),
		ci => grid4(8)(16),
		s => grid3(5)(16),
		co => grid3(2)(17) );

-- move the other elements of the column

-----------------------------
-- COLUMN 17
-----------------------------
-- full adder c17, number 0
lv3_c17_FA_0: fullAdder
	port map (
		i0 => grid4(0)(17),
		i1 => grid4(1)(17),
		ci => grid4(2)(17),
		s => grid3(3)(17),
		co => grid3(0)(18) );

-- full adder c17, number 1
lv3_c17_FA_1: fullAdder
	port map (
		i0 => grid4(3)(17),
		i1 => grid4(4)(17),
		ci => grid4(5)(17),
		s => grid3(4)(17),
		co => grid3(1)(18) );

-- full adder c17, number 2
lv3_c17_FA_2: fullAdder
	port map (
		i0 => grid4(6)(17),
		i1 => grid4(7)(17),
		ci => grid4(8)(17),
		s => grid3(5)(17),
		co => grid3(2)(18) );

-- move the other elements of the column

-----------------------------
-- COLUMN 18
-----------------------------
-- full adder c18, number 0
lv3_c18_FA_0: fullAdder
	port map (
		i0 => grid4(0)(18),
		i1 => grid4(1)(18),
		ci => grid4(2)(18),
		s => grid3(3)(18),
		co => grid3(0)(19) );

-- full adder c18, number 1
lv3_c18_FA_1: fullAdder
	port map (
		i0 => grid4(3)(18),
		i1 => grid4(4)(18),
		ci => grid4(5)(18),
		s => grid3(4)(18),
		co => grid3(1)(19) );

-- full adder c18, number 2
lv3_c18_FA_2: fullAdder
	port map (
		i0 => grid4(6)(18),
		i1 => grid4(7)(18),
		ci => grid4(8)(18),
		s => grid3(5)(18),
		co => grid3(2)(19) );

-- move the other elements of the column

-----------------------------
-- COLUMN 19
-----------------------------
-- full adder c19, number 0
lv3_c19_FA_0: fullAdder
	port map (
		i0 => grid4(0)(19),
		i1 => grid4(1)(19),
		ci => grid4(2)(19),
		s => grid3(3)(19),
		co => grid3(0)(20) );

-- full adder c19, number 1
lv3_c19_FA_1: fullAdder
	port map (
		i0 => grid4(3)(19),
		i1 => grid4(4)(19),
		ci => grid4(5)(19),
		s => grid3(4)(19),
		co => grid3(1)(20) );

-- full adder c19, number 2
lv3_c19_FA_2: fullAdder
	port map (
		i0 => grid4(6)(19),
		i1 => grid4(7)(19),
		ci => grid4(8)(19),
		s => grid3(5)(19),
		co => grid3(2)(20) );

-- move the other elements of the column

-----------------------------
-- COLUMN 20
-----------------------------
-- full adder c20, number 0
lv3_c20_FA_0: fullAdder
	port map (
		i0 => grid4(0)(20),
		i1 => grid4(1)(20),
		ci => grid4(2)(20),
		s => grid3(3)(20),
		co => grid3(0)(21) );

-- full adder c20, number 1
lv3_c20_FA_1: fullAdder
	port map (
		i0 => grid4(3)(20),
		i1 => grid4(4)(20),
		ci => grid4(5)(20),
		s => grid3(4)(20),
		co => grid3(1)(21) );

-- full adder c20, number 2
lv3_c20_FA_2: fullAdder
	port map (
		i0 => grid4(6)(20),
		i1 => grid4(7)(20),
		ci => grid4(8)(20),
		s => grid3(5)(20),
		co => grid3(2)(21) );

-- move the other elements of the column

-----------------------------
-- COLUMN 21
-----------------------------
-- full adder c21, number 0
lv3_c21_FA_0: fullAdder
	port map (
		i0 => grid4(0)(21),
		i1 => grid4(1)(21),
		ci => grid4(2)(21),
		s => grid3(3)(21),
		co => grid3(0)(22) );

-- full adder c21, number 1
lv3_c21_FA_1: fullAdder
	port map (
		i0 => grid4(3)(21),
		i1 => grid4(4)(21),
		ci => grid4(5)(21),
		s => grid3(4)(21),
		co => grid3(1)(22) );

-- full adder c21, number 2
lv3_c21_FA_2: fullAdder
	port map (
		i0 => grid4(6)(21),
		i1 => grid4(7)(21),
		ci => grid4(8)(21),
		s => grid3(5)(21),
		co => grid3(2)(22) );

-- move the other elements of the column

-----------------------------
-- COLUMN 22
-----------------------------
-- full adder c22, number 0
lv3_c22_FA_0: fullAdder
	port map (
		i0 => grid4(0)(22),
		i1 => grid4(1)(22),
		ci => grid4(2)(22),
		s => grid3(3)(22),
		co => grid3(0)(23) );

-- full adder c22, number 1
lv3_c22_FA_1: fullAdder
	port map (
		i0 => grid4(3)(22),
		i1 => grid4(4)(22),
		ci => grid4(5)(22),
		s => grid3(4)(22),
		co => grid3(1)(23) );

-- full adder c22, number 2
lv3_c22_FA_2: fullAdder
	port map (
		i0 => grid4(6)(22),
		i1 => grid4(7)(22),
		ci => grid4(8)(22),
		s => grid3(5)(22),
		co => grid3(2)(23) );

-- move the other elements of the column

-----------------------------
-- COLUMN 23
-----------------------------
-- full adder c23, number 0
lv3_c23_FA_0: fullAdder
	port map (
		i0 => grid4(0)(23),
		i1 => grid4(1)(23),
		ci => grid4(2)(23),
		s => grid3(3)(23),
		co => grid3(0)(24) );

-- full adder c23, number 1
lv3_c23_FA_1: fullAdder
	port map (
		i0 => grid4(3)(23),
		i1 => grid4(4)(23),
		ci => grid4(5)(23),
		s => grid3(4)(23),
		co => grid3(1)(24) );

-- full adder c23, number 2
lv3_c23_FA_2: fullAdder
	port map (
		i0 => grid4(6)(23),
		i1 => grid4(7)(23),
		ci => grid4(8)(23),
		s => grid3(5)(23),
		co => grid3(2)(24) );

-- move the other elements of the column

-----------------------------
-- COLUMN 24
-----------------------------
-- full adder c24, number 0
lv3_c24_FA_0: fullAdder
	port map (
		i0 => grid4(0)(24),
		i1 => grid4(1)(24),
		ci => grid4(2)(24),
		s => grid3(3)(24),
		co => grid3(0)(25) );

-- full adder c24, number 1
lv3_c24_FA_1: fullAdder
	port map (
		i0 => grid4(3)(24),
		i1 => grid4(4)(24),
		ci => grid4(5)(24),
		s => grid3(4)(24),
		co => grid3(1)(25) );

-- full adder c24, number 2
lv3_c24_FA_2: fullAdder
	port map (
		i0 => grid4(6)(24),
		i1 => grid4(7)(24),
		ci => grid4(8)(24),
		s => grid3(5)(24),
		co => grid3(2)(25) );

-- move the other elements of the column

-----------------------------
-- COLUMN 25
-----------------------------
-- full adder c25, number 0
lv3_c25_FA_0: fullAdder
	port map (
		i0 => grid4(0)(25),
		i1 => grid4(1)(25),
		ci => grid4(2)(25),
		s => grid3(3)(25),
		co => grid3(0)(26) );

-- full adder c25, number 1
lv3_c25_FA_1: fullAdder
	port map (
		i0 => grid4(3)(25),
		i1 => grid4(4)(25),
		ci => grid4(5)(25),
		s => grid3(4)(25),
		co => grid3(1)(26) );

-- full adder c25, number 2
lv3_c25_FA_2: fullAdder
	port map (
		i0 => grid4(6)(25),
		i1 => grid4(7)(25),
		ci => grid4(8)(25),
		s => grid3(5)(25),
		co => grid3(2)(26) );

-- move the other elements of the column

-----------------------------
-- COLUMN 26
-----------------------------
-- full adder c26, number 0
lv3_c26_FA_0: fullAdder
	port map (
		i0 => grid4(0)(26),
		i1 => grid4(1)(26),
		ci => grid4(2)(26),
		s => grid3(3)(26),
		co => grid3(0)(27) );

-- full adder c26, number 1
lv3_c26_FA_1: fullAdder
	port map (
		i0 => grid4(3)(26),
		i1 => grid4(4)(26),
		ci => grid4(5)(26),
		s => grid3(4)(26),
		co => grid3(1)(27) );

-- full adder c26, number 2
lv3_c26_FA_2: fullAdder
	port map (
		i0 => grid4(6)(26),
		i1 => grid4(7)(26),
		ci => grid4(8)(26),
		s => grid3(5)(26),
		co => grid3(2)(27) );

-- move the other elements of the column

-----------------------------
-- COLUMN 27
-----------------------------
-- full adder c27, number 0
lv3_c27_FA_0: fullAdder
	port map (
		i0 => grid4(0)(27),
		i1 => grid4(1)(27),
		ci => grid4(2)(27),
		s => grid3(3)(27),
		co => grid3(0)(28) );

-- full adder c27, number 1
lv3_c27_FA_1: fullAdder
	port map (
		i0 => grid4(3)(27),
		i1 => grid4(4)(27),
		ci => grid4(5)(27),
		s => grid3(4)(27),
		co => grid3(1)(28) );

-- half adder c27, number 0
lv3_c27_HA_0: halfAdder
	port map (
		i0 => grid4(6)(27),
		i1 => grid4(7)(27),
		s => grid3(5)(27),
		co => grid3(2)(28) );

-- move the other elements of the column

-----------------------------
-- COLUMN 28
-----------------------------
-- full adder c28, number 0
lv3_c28_FA_0: fullAdder
	port map (
		i0 => grid4(0)(28),
		i1 => grid4(1)(28),
		ci => grid4(2)(28),
		s => grid3(3)(28),
		co => grid3(0)(29) );

-- full adder c28, number 1
lv3_c28_FA_1: fullAdder
	port map (
		i0 => grid4(3)(28),
		i1 => grid4(4)(28),
		ci => grid4(5)(28),
		s => grid3(4)(28),
		co => grid3(1)(29) );

-- move the other elements of the column
grid3(5)(28) <= grid4(6)(28);

-----------------------------
-- COLUMN 29
-----------------------------
-- full adder c29, number 0
lv3_c29_FA_0: fullAdder
	port map (
		i0 => grid4(0)(29),
		i1 => grid4(1)(29),
		ci => grid4(2)(29),
		s => grid3(2)(29),
		co => grid3(0)(30) );

-- half adder c29, number 0
lv3_c29_HA_0: halfAdder
	port map (
		i0 => grid4(3)(29),
		i1 => grid4(4)(29),
		s => grid3(3)(29),
		co => grid3(1)(30) );

-- move the other elements of the column
grid3(4)(29) <= grid4(5)(29);
grid3(5)(29) <= grid4(6)(29);

-----------------------------
-- COLUMN 30
-----------------------------
-- full adder c30, number 0
lv3_c30_FA_0: fullAdder
	port map (
		i0 => grid4(0)(30),
		i1 => grid4(1)(30),
		ci => grid4(2)(30),
		s => grid3(2)(30),
		co => grid3(0)(31) );

-- move the other elements of the column
grid3(3)(30) <= grid4(3)(30);
grid3(4)(30) <= grid4(4)(30);
grid3(5)(30) <= grid4(5)(30);

-----------------------------
-- COLUMN 31
-----------------------------
-- half adder c31, number 0
lv3_c31_HA_0: halfAdder
	port map (
		i0 => grid4(0)(31),
		i1 => grid4(1)(31),
		s => grid3(1)(31),
		co => grid3(0)(32) );

-- move the other elements of the column
grid3(2)(31) <= grid4(2)(31);
grid3(3)(31) <= grid4(3)(31);
grid3(4)(31) <= grid4(4)(31);
grid3(5)(31) <= grid4(5)(31);

-----------------------------
-- COLUMN 32
-----------------------------
-- move the other elements of the column
grid3(1)(32) <= grid4(0)(32);
grid3(2)(32) <= grid4(1)(32);
grid3(3)(32) <= grid4(2)(32);
grid3(4)(32) <= grid4(3)(32);
grid3(5)(32) <= grid4(4)(32);

-----------------------------
-- COLUMN 33
-----------------------------
-- move the other elements of the column
grid3(0)(33) <= grid4(0)(33);
grid3(1)(33) <= grid4(1)(33);
grid3(2)(33) <= grid4(2)(33);
grid3(3)(33) <= grid4(3)(33);
grid3(4)(33) <= grid4(4)(33);

-----------------------------
-- COLUMN 34
-----------------------------
-- move the other elements of the column
grid3(0)(34) <= grid4(0)(34);
grid3(1)(34) <= grid4(1)(34);
grid3(2)(34) <= grid4(2)(34);
grid3(3)(34) <= grid4(3)(34);

-----------------------------
-- COLUMN 35
-----------------------------
-- move the other elements of the column
grid3(0)(35) <= grid4(0)(35);
grid3(1)(35) <= grid4(1)(35);
grid3(2)(35) <= grid4(2)(35);
grid3(3)(35) <= grid4(3)(35);

-----------------------------
-- COLUMN 36
-----------------------------
-- move the other elements of the column
grid3(0)(36) <= grid4(0)(36);
grid3(1)(36) <= grid4(1)(36);
grid3(2)(36) <= grid4(2)(36);

-----------------------------
-- COLUMN 37
-----------------------------
-- move the other elements of the column
grid3(0)(37) <= grid4(0)(37);
grid3(1)(37) <= grid4(1)(37);
grid3(2)(37) <= grid4(2)(37);

-----------------------------
-- COLUMN 38
-----------------------------
-- move the other elements of the column
grid3(0)(38) <= grid4(0)(38);
grid3(1)(38) <= grid4(1)(38);

-----------------------------
-- COLUMN 39
-----------------------------
-- move the other elements of the column
grid3(0)(39) <= grid4(0)(39);
grid3(1)(39) <= grid4(1)(39);

-----------------------------
-- DADDA TREE LEVEL2
-----------------------------

-----------------------------
-- COLUMN 0
-----------------------------
-- half adder c0, number 0
lv2_c0_HA_0: halfAdder
	port map (
		i0 => grid3(0)(0),
		i1 => grid3(1)(0),
		s => grid2(0)(0),
		co => grid2(0)(1) );

-- move the other elements of the column
grid2(1)(0) <= grid3(2)(0);
grid2(2)(0) <= grid3(3)(0);
grid2(3)(0) <= grid3(4)(0);

-----------------------------
-- COLUMN 1
-----------------------------
-- half adder c1, number 0
lv2_c1_HA_0: halfAdder
	port map (
		i0 => grid3(0)(1),
		i1 => grid3(1)(1),
		s => grid2(1)(1),
		co => grid2(0)(2) );

-- move the other elements of the column
grid2(2)(1) <= grid3(2)(1);
grid2(3)(1) <= grid3(3)(1);

-----------------------------
-- COLUMN 2
-----------------------------
-- full adder c2, number 0
lv2_c2_FA_0: fullAdder
	port map (
		i0 => grid3(0)(2),
		i1 => grid3(1)(2),
		ci => grid3(2)(2),
		s => grid2(1)(2),
		co => grid2(0)(3) );

-- half adder c2, number 0
lv2_c2_HA_0: halfAdder
	port map (
		i0 => grid3(3)(2),
		i1 => grid3(4)(2),
		s => grid2(2)(2),
		co => grid2(1)(3) );

-- move the other elements of the column
grid2(3)(2) <= grid3(5)(2);

-----------------------------
-- COLUMN 3
-----------------------------
-- full adder c3, number 0
lv2_c3_FA_0: fullAdder
	port map (
		i0 => grid3(0)(3),
		i1 => grid3(1)(3),
		ci => grid3(2)(3),
		s => grid2(2)(3),
		co => grid2(0)(4) );

-- half adder c3, number 0
lv2_c3_HA_0: halfAdder
	port map (
		i0 => grid3(3)(3),
		i1 => grid3(4)(3),
		s => grid2(3)(3),
		co => grid2(1)(4) );

-- move the other elements of the column

-----------------------------
-- COLUMN 4
-----------------------------
-- full adder c4, number 0
lv2_c4_FA_0: fullAdder
	port map (
		i0 => grid3(0)(4),
		i1 => grid3(1)(4),
		ci => grid3(2)(4),
		s => grid2(2)(4),
		co => grid2(0)(5) );

-- full adder c4, number 1
lv2_c4_FA_1: fullAdder
	port map (
		i0 => grid3(3)(4),
		i1 => grid3(4)(4),
		ci => grid3(5)(4),
		s => grid2(3)(4),
		co => grid2(1)(5) );

-- move the other elements of the column

-----------------------------
-- COLUMN 5
-----------------------------
-- full adder c5, number 0
lv2_c5_FA_0: fullAdder
	port map (
		i0 => grid3(0)(5),
		i1 => grid3(1)(5),
		ci => grid3(2)(5),
		s => grid2(2)(5),
		co => grid2(0)(6) );

-- full adder c5, number 1
lv2_c5_FA_1: fullAdder
	port map (
		i0 => grid3(3)(5),
		i1 => grid3(4)(5),
		ci => grid3(5)(5),
		s => grid2(3)(5),
		co => grid2(1)(6) );

-- move the other elements of the column

-----------------------------
-- COLUMN 6
-----------------------------
-- full adder c6, number 0
lv2_c6_FA_0: fullAdder
	port map (
		i0 => grid3(0)(6),
		i1 => grid3(1)(6),
		ci => grid3(2)(6),
		s => grid2(2)(6),
		co => grid2(0)(7) );

-- full adder c6, number 1
lv2_c6_FA_1: fullAdder
	port map (
		i0 => grid3(3)(6),
		i1 => grid3(4)(6),
		ci => grid3(5)(6),
		s => grid2(3)(6),
		co => grid2(1)(7) );

-- move the other elements of the column

-----------------------------
-- COLUMN 7
-----------------------------
-- full adder c7, number 0
lv2_c7_FA_0: fullAdder
	port map (
		i0 => grid3(0)(7),
		i1 => grid3(1)(7),
		ci => grid3(2)(7),
		s => grid2(2)(7),
		co => grid2(0)(8) );

-- full adder c7, number 1
lv2_c7_FA_1: fullAdder
	port map (
		i0 => grid3(3)(7),
		i1 => grid3(4)(7),
		ci => grid3(5)(7),
		s => grid2(3)(7),
		co => grid2(1)(8) );

-- move the other elements of the column

-----------------------------
-- COLUMN 8
-----------------------------
-- full adder c8, number 0
lv2_c8_FA_0: fullAdder
	port map (
		i0 => grid3(0)(8),
		i1 => grid3(1)(8),
		ci => grid3(2)(8),
		s => grid2(2)(8),
		co => grid2(0)(9) );

-- full adder c8, number 1
lv2_c8_FA_1: fullAdder
	port map (
		i0 => grid3(3)(8),
		i1 => grid3(4)(8),
		ci => grid3(5)(8),
		s => grid2(3)(8),
		co => grid2(1)(9) );

-- move the other elements of the column

-----------------------------
-- COLUMN 9
-----------------------------
-- full adder c9, number 0
lv2_c9_FA_0: fullAdder
	port map (
		i0 => grid3(0)(9),
		i1 => grid3(1)(9),
		ci => grid3(2)(9),
		s => grid2(2)(9),
		co => grid2(0)(10) );

-- full adder c9, number 1
lv2_c9_FA_1: fullAdder
	port map (
		i0 => grid3(3)(9),
		i1 => grid3(4)(9),
		ci => grid3(5)(9),
		s => grid2(3)(9),
		co => grid2(1)(10) );

-- move the other elements of the column

-----------------------------
-- COLUMN 10
-----------------------------
-- full adder c10, number 0
lv2_c10_FA_0: fullAdder
	port map (
		i0 => grid3(0)(10),
		i1 => grid3(1)(10),
		ci => grid3(2)(10),
		s => grid2(2)(10),
		co => grid2(0)(11) );

-- full adder c10, number 1
lv2_c10_FA_1: fullAdder
	port map (
		i0 => grid3(3)(10),
		i1 => grid3(4)(10),
		ci => grid3(5)(10),
		s => grid2(3)(10),
		co => grid2(1)(11) );

-- move the other elements of the column

-----------------------------
-- COLUMN 11
-----------------------------
-- full adder c11, number 0
lv2_c11_FA_0: fullAdder
	port map (
		i0 => grid3(0)(11),
		i1 => grid3(1)(11),
		ci => grid3(2)(11),
		s => grid2(2)(11),
		co => grid2(0)(12) );

-- full adder c11, number 1
lv2_c11_FA_1: fullAdder
	port map (
		i0 => grid3(3)(11),
		i1 => grid3(4)(11),
		ci => grid3(5)(11),
		s => grid2(3)(11),
		co => grid2(1)(12) );

-- move the other elements of the column

-----------------------------
-- COLUMN 12
-----------------------------
-- full adder c12, number 0
lv2_c12_FA_0: fullAdder
	port map (
		i0 => grid3(0)(12),
		i1 => grid3(1)(12),
		ci => grid3(2)(12),
		s => grid2(2)(12),
		co => grid2(0)(13) );

-- full adder c12, number 1
lv2_c12_FA_1: fullAdder
	port map (
		i0 => grid3(3)(12),
		i1 => grid3(4)(12),
		ci => grid3(5)(12),
		s => grid2(3)(12),
		co => grid2(1)(13) );

-- move the other elements of the column

-----------------------------
-- COLUMN 13
-----------------------------
-- full adder c13, number 0
lv2_c13_FA_0: fullAdder
	port map (
		i0 => grid3(0)(13),
		i1 => grid3(1)(13),
		ci => grid3(2)(13),
		s => grid2(2)(13),
		co => grid2(0)(14) );

-- full adder c13, number 1
lv2_c13_FA_1: fullAdder
	port map (
		i0 => grid3(3)(13),
		i1 => grid3(4)(13),
		ci => grid3(5)(13),
		s => grid2(3)(13),
		co => grid2(1)(14) );

-- move the other elements of the column

-----------------------------
-- COLUMN 14
-----------------------------
-- full adder c14, number 0
lv2_c14_FA_0: fullAdder
	port map (
		i0 => grid3(0)(14),
		i1 => grid3(1)(14),
		ci => grid3(2)(14),
		s => grid2(2)(14),
		co => grid2(0)(15) );

-- full adder c14, number 1
lv2_c14_FA_1: fullAdder
	port map (
		i0 => grid3(3)(14),
		i1 => grid3(4)(14),
		ci => grid3(5)(14),
		s => grid2(3)(14),
		co => grid2(1)(15) );

-- move the other elements of the column

-----------------------------
-- COLUMN 15
-----------------------------
-- full adder c15, number 0
lv2_c15_FA_0: fullAdder
	port map (
		i0 => grid3(0)(15),
		i1 => grid3(1)(15),
		ci => grid3(2)(15),
		s => grid2(2)(15),
		co => grid2(0)(16) );

-- full adder c15, number 1
lv2_c15_FA_1: fullAdder
	port map (
		i0 => grid3(3)(15),
		i1 => grid3(4)(15),
		ci => grid3(5)(15),
		s => grid2(3)(15),
		co => grid2(1)(16) );

-- move the other elements of the column

-----------------------------
-- COLUMN 16
-----------------------------
-- full adder c16, number 0
lv2_c16_FA_0: fullAdder
	port map (
		i0 => grid3(0)(16),
		i1 => grid3(1)(16),
		ci => grid3(2)(16),
		s => grid2(2)(16),
		co => grid2(0)(17) );

-- full adder c16, number 1
lv2_c16_FA_1: fullAdder
	port map (
		i0 => grid3(3)(16),
		i1 => grid3(4)(16),
		ci => grid3(5)(16),
		s => grid2(3)(16),
		co => grid2(1)(17) );

-- move the other elements of the column

-----------------------------
-- COLUMN 17
-----------------------------
-- full adder c17, number 0
lv2_c17_FA_0: fullAdder
	port map (
		i0 => grid3(0)(17),
		i1 => grid3(1)(17),
		ci => grid3(2)(17),
		s => grid2(2)(17),
		co => grid2(0)(18) );

-- full adder c17, number 1
lv2_c17_FA_1: fullAdder
	port map (
		i0 => grid3(3)(17),
		i1 => grid3(4)(17),
		ci => grid3(5)(17),
		s => grid2(3)(17),
		co => grid2(1)(18) );

-- move the other elements of the column

-----------------------------
-- COLUMN 18
-----------------------------
-- full adder c18, number 0
lv2_c18_FA_0: fullAdder
	port map (
		i0 => grid3(0)(18),
		i1 => grid3(1)(18),
		ci => grid3(2)(18),
		s => grid2(2)(18),
		co => grid2(0)(19) );

-- full adder c18, number 1
lv2_c18_FA_1: fullAdder
	port map (
		i0 => grid3(3)(18),
		i1 => grid3(4)(18),
		ci => grid3(5)(18),
		s => grid2(3)(18),
		co => grid2(1)(19) );

-- move the other elements of the column

-----------------------------
-- COLUMN 19
-----------------------------
-- full adder c19, number 0
lv2_c19_FA_0: fullAdder
	port map (
		i0 => grid3(0)(19),
		i1 => grid3(1)(19),
		ci => grid3(2)(19),
		s => grid2(2)(19),
		co => grid2(0)(20) );

-- full adder c19, number 1
lv2_c19_FA_1: fullAdder
	port map (
		i0 => grid3(3)(19),
		i1 => grid3(4)(19),
		ci => grid3(5)(19),
		s => grid2(3)(19),
		co => grid2(1)(20) );

-- move the other elements of the column

-----------------------------
-- COLUMN 20
-----------------------------
-- full adder c20, number 0
lv2_c20_FA_0: fullAdder
	port map (
		i0 => grid3(0)(20),
		i1 => grid3(1)(20),
		ci => grid3(2)(20),
		s => grid2(2)(20),
		co => grid2(0)(21) );

-- full adder c20, number 1
lv2_c20_FA_1: fullAdder
	port map (
		i0 => grid3(3)(20),
		i1 => grid3(4)(20),
		ci => grid3(5)(20),
		s => grid2(3)(20),
		co => grid2(1)(21) );

-- move the other elements of the column

-----------------------------
-- COLUMN 21
-----------------------------
-- full adder c21, number 0
lv2_c21_FA_0: fullAdder
	port map (
		i0 => grid3(0)(21),
		i1 => grid3(1)(21),
		ci => grid3(2)(21),
		s => grid2(2)(21),
		co => grid2(0)(22) );

-- full adder c21, number 1
lv2_c21_FA_1: fullAdder
	port map (
		i0 => grid3(3)(21),
		i1 => grid3(4)(21),
		ci => grid3(5)(21),
		s => grid2(3)(21),
		co => grid2(1)(22) );

-- move the other elements of the column

-----------------------------
-- COLUMN 22
-----------------------------
-- full adder c22, number 0
lv2_c22_FA_0: fullAdder
	port map (
		i0 => grid3(0)(22),
		i1 => grid3(1)(22),
		ci => grid3(2)(22),
		s => grid2(2)(22),
		co => grid2(0)(23) );

-- full adder c22, number 1
lv2_c22_FA_1: fullAdder
	port map (
		i0 => grid3(3)(22),
		i1 => grid3(4)(22),
		ci => grid3(5)(22),
		s => grid2(3)(22),
		co => grid2(1)(23) );

-- move the other elements of the column

-----------------------------
-- COLUMN 23
-----------------------------
-- full adder c23, number 0
lv2_c23_FA_0: fullAdder
	port map (
		i0 => grid3(0)(23),
		i1 => grid3(1)(23),
		ci => grid3(2)(23),
		s => grid2(2)(23),
		co => grid2(0)(24) );

-- full adder c23, number 1
lv2_c23_FA_1: fullAdder
	port map (
		i0 => grid3(3)(23),
		i1 => grid3(4)(23),
		ci => grid3(5)(23),
		s => grid2(3)(23),
		co => grid2(1)(24) );

-- move the other elements of the column

-----------------------------
-- COLUMN 24
-----------------------------
-- full adder c24, number 0
lv2_c24_FA_0: fullAdder
	port map (
		i0 => grid3(0)(24),
		i1 => grid3(1)(24),
		ci => grid3(2)(24),
		s => grid2(2)(24),
		co => grid2(0)(25) );

-- full adder c24, number 1
lv2_c24_FA_1: fullAdder
	port map (
		i0 => grid3(3)(24),
		i1 => grid3(4)(24),
		ci => grid3(5)(24),
		s => grid2(3)(24),
		co => grid2(1)(25) );

-- move the other elements of the column

-----------------------------
-- COLUMN 25
-----------------------------
-- full adder c25, number 0
lv2_c25_FA_0: fullAdder
	port map (
		i0 => grid3(0)(25),
		i1 => grid3(1)(25),
		ci => grid3(2)(25),
		s => grid2(2)(25),
		co => grid2(0)(26) );

-- full adder c25, number 1
lv2_c25_FA_1: fullAdder
	port map (
		i0 => grid3(3)(25),
		i1 => grid3(4)(25),
		ci => grid3(5)(25),
		s => grid2(3)(25),
		co => grid2(1)(26) );

-- move the other elements of the column

-----------------------------
-- COLUMN 26
-----------------------------
-- full adder c26, number 0
lv2_c26_FA_0: fullAdder
	port map (
		i0 => grid3(0)(26),
		i1 => grid3(1)(26),
		ci => grid3(2)(26),
		s => grid2(2)(26),
		co => grid2(0)(27) );

-- full adder c26, number 1
lv2_c26_FA_1: fullAdder
	port map (
		i0 => grid3(3)(26),
		i1 => grid3(4)(26),
		ci => grid3(5)(26),
		s => grid2(3)(26),
		co => grid2(1)(27) );

-- move the other elements of the column

-----------------------------
-- COLUMN 27
-----------------------------
-- full adder c27, number 0
lv2_c27_FA_0: fullAdder
	port map (
		i0 => grid3(0)(27),
		i1 => grid3(1)(27),
		ci => grid3(2)(27),
		s => grid2(2)(27),
		co => grid2(0)(28) );

-- full adder c27, number 1
lv2_c27_FA_1: fullAdder
	port map (
		i0 => grid3(3)(27),
		i1 => grid3(4)(27),
		ci => grid3(5)(27),
		s => grid2(3)(27),
		co => grid2(1)(28) );

-- move the other elements of the column

-----------------------------
-- COLUMN 28
-----------------------------
-- full adder c28, number 0
lv2_c28_FA_0: fullAdder
	port map (
		i0 => grid3(0)(28),
		i1 => grid3(1)(28),
		ci => grid3(2)(28),
		s => grid2(2)(28),
		co => grid2(0)(29) );

-- full adder c28, number 1
lv2_c28_FA_1: fullAdder
	port map (
		i0 => grid3(3)(28),
		i1 => grid3(4)(28),
		ci => grid3(5)(28),
		s => grid2(3)(28),
		co => grid2(1)(29) );

-- move the other elements of the column

-----------------------------
-- COLUMN 29
-----------------------------
-- full adder c29, number 0
lv2_c29_FA_0: fullAdder
	port map (
		i0 => grid3(0)(29),
		i1 => grid3(1)(29),
		ci => grid3(2)(29),
		s => grid2(2)(29),
		co => grid2(0)(30) );

-- full adder c29, number 1
lv2_c29_FA_1: fullAdder
	port map (
		i0 => grid3(3)(29),
		i1 => grid3(4)(29),
		ci => grid3(5)(29),
		s => grid2(3)(29),
		co => grid2(1)(30) );

-- move the other elements of the column

-----------------------------
-- COLUMN 30
-----------------------------
-- full adder c30, number 0
lv2_c30_FA_0: fullAdder
	port map (
		i0 => grid3(0)(30),
		i1 => grid3(1)(30),
		ci => grid3(2)(30),
		s => grid2(2)(30),
		co => grid2(0)(31) );

-- full adder c30, number 1
lv2_c30_FA_1: fullAdder
	port map (
		i0 => grid3(3)(30),
		i1 => grid3(4)(30),
		ci => grid3(5)(30),
		s => grid2(3)(30),
		co => grid2(1)(31) );

-- move the other elements of the column

-----------------------------
-- COLUMN 31
-----------------------------
-- full adder c31, number 0
lv2_c31_FA_0: fullAdder
	port map (
		i0 => grid3(0)(31),
		i1 => grid3(1)(31),
		ci => grid3(2)(31),
		s => grid2(2)(31),
		co => grid2(0)(32) );

-- full adder c31, number 1
lv2_c31_FA_1: fullAdder
	port map (
		i0 => grid3(3)(31),
		i1 => grid3(4)(31),
		ci => grid3(5)(31),
		s => grid2(3)(31),
		co => grid2(1)(32) );

-- move the other elements of the column

-----------------------------
-- COLUMN 32
-----------------------------
-- full adder c32, number 0
lv2_c32_FA_0: fullAdder
	port map (
		i0 => grid3(0)(32),
		i1 => grid3(1)(32),
		ci => grid3(2)(32),
		s => grid2(2)(32),
		co => grid2(0)(33) );

-- full adder c32, number 1
lv2_c32_FA_1: fullAdder
	port map (
		i0 => grid3(3)(32),
		i1 => grid3(4)(32),
		ci => grid3(5)(32),
		s => grid2(3)(32),
		co => grid2(1)(33) );

-- move the other elements of the column

-----------------------------
-- COLUMN 33
-----------------------------
-- full adder c33, number 0
lv2_c33_FA_0: fullAdder
	port map (
		i0 => grid3(0)(33),
		i1 => grid3(1)(33),
		ci => grid3(2)(33),
		s => grid2(2)(33),
		co => grid2(0)(34) );

-- half adder c33, number 0
lv2_c33_HA_0: halfAdder
	port map (
		i0 => grid3(3)(33),
		i1 => grid3(4)(33),
		s => grid2(3)(33),
		co => grid2(1)(34) );

-- move the other elements of the column

-----------------------------
-- COLUMN 34
-----------------------------
-- full adder c34, number 0
lv2_c34_FA_0: fullAdder
	port map (
		i0 => grid3(0)(34),
		i1 => grid3(1)(34),
		ci => grid3(2)(34),
		s => grid2(2)(34),
		co => grid2(0)(35) );

-- move the other elements of the column
grid2(3)(34) <= grid3(3)(34);

-----------------------------
-- COLUMN 35
-----------------------------
-- half adder c35, number 0
lv2_c35_HA_0: halfAdder
	port map (
		i0 => grid3(0)(35),
		i1 => grid3(1)(35),
		s => grid2(1)(35),
		co => grid2(0)(36) );

-- move the other elements of the column
grid2(2)(35) <= grid3(2)(35);
grid2(3)(35) <= grid3(3)(35);

-----------------------------
-- COLUMN 36
-----------------------------
-- move the other elements of the column
grid2(1)(36) <= grid3(0)(36);
grid2(2)(36) <= grid3(1)(36);
grid2(3)(36) <= grid3(2)(36);

-----------------------------
-- COLUMN 37
-----------------------------
-- move the other elements of the column
grid2(0)(37) <= grid3(0)(37);
grid2(1)(37) <= grid3(1)(37);
grid2(2)(37) <= grid3(2)(37);

-----------------------------
-- COLUMN 38
-----------------------------
-- move the other elements of the column
grid2(0)(38) <= grid3(0)(38);
grid2(1)(38) <= grid3(1)(38);

-----------------------------
-- COLUMN 39
-----------------------------
-- move the other elements of the column
grid2(0)(39) <= grid3(0)(39);
grid2(1)(39) <= grid3(1)(39);

-----------------------------
-- DADDA TREE LEVEL1
-----------------------------

-----------------------------
-- COLUMN 0
-----------------------------
-- half adder c0, number 0
lv1_c0_HA_0: halfAdder
	port map (
		i0 => grid2(0)(0),
		i1 => grid2(1)(0),
		s => grid1(0)(0),
		co => grid1(0)(1) );

-- move the other elements of the column
grid1(1)(0) <= grid2(2)(0);
grid1(2)(0) <= grid2(3)(0);

-----------------------------
-- COLUMN 1
-----------------------------
-- full adder c1, number 0
lv1_c1_FA_0: fullAdder
	port map (
		i0 => grid2(0)(1),
		i1 => grid2(1)(1),
		ci => grid2(2)(1),
		s => grid1(1)(1),
		co => grid1(0)(2) );

-- move the other elements of the column
grid1(2)(1) <= grid2(3)(1);

-----------------------------
-- COLUMN 2
-----------------------------
-- full adder c2, number 0
lv1_c2_FA_0: fullAdder
	port map (
		i0 => grid2(0)(2),
		i1 => grid2(1)(2),
		ci => grid2(2)(2),
		s => grid1(1)(2),
		co => grid1(0)(3) );

-- move the other elements of the column
grid1(2)(2) <= grid2(3)(2);

-----------------------------
-- COLUMN 3
-----------------------------
-- full adder c3, number 0
lv1_c3_FA_0: fullAdder
	port map (
		i0 => grid2(0)(3),
		i1 => grid2(1)(3),
		ci => grid2(2)(3),
		s => grid1(1)(3),
		co => grid1(0)(4) );

-- move the other elements of the column
grid1(2)(3) <= grid2(3)(3);

-----------------------------
-- COLUMN 4
-----------------------------
-- full adder c4, number 0
lv1_c4_FA_0: fullAdder
	port map (
		i0 => grid2(0)(4),
		i1 => grid2(1)(4),
		ci => grid2(2)(4),
		s => grid1(1)(4),
		co => grid1(0)(5) );

-- move the other elements of the column
grid1(2)(4) <= grid2(3)(4);

-----------------------------
-- COLUMN 5
-----------------------------
-- full adder c5, number 0
lv1_c5_FA_0: fullAdder
	port map (
		i0 => grid2(0)(5),
		i1 => grid2(1)(5),
		ci => grid2(2)(5),
		s => grid1(1)(5),
		co => grid1(0)(6) );

-- move the other elements of the column
grid1(2)(5) <= grid2(3)(5);

-----------------------------
-- COLUMN 6
-----------------------------
-- full adder c6, number 0
lv1_c6_FA_0: fullAdder
	port map (
		i0 => grid2(0)(6),
		i1 => grid2(1)(6),
		ci => grid2(2)(6),
		s => grid1(1)(6),
		co => grid1(0)(7) );

-- move the other elements of the column
grid1(2)(6) <= grid2(3)(6);

-----------------------------
-- COLUMN 7
-----------------------------
-- full adder c7, number 0
lv1_c7_FA_0: fullAdder
	port map (
		i0 => grid2(0)(7),
		i1 => grid2(1)(7),
		ci => grid2(2)(7),
		s => grid1(1)(7),
		co => grid1(0)(8) );

-- move the other elements of the column
grid1(2)(7) <= grid2(3)(7);

-----------------------------
-- COLUMN 8
-----------------------------
-- full adder c8, number 0
lv1_c8_FA_0: fullAdder
	port map (
		i0 => grid2(0)(8),
		i1 => grid2(1)(8),
		ci => grid2(2)(8),
		s => grid1(1)(8),
		co => grid1(0)(9) );

-- move the other elements of the column
grid1(2)(8) <= grid2(3)(8);

-----------------------------
-- COLUMN 9
-----------------------------
-- full adder c9, number 0
lv1_c9_FA_0: fullAdder
	port map (
		i0 => grid2(0)(9),
		i1 => grid2(1)(9),
		ci => grid2(2)(9),
		s => grid1(1)(9),
		co => grid1(0)(10) );

-- move the other elements of the column
grid1(2)(9) <= grid2(3)(9);

-----------------------------
-- COLUMN 10
-----------------------------
-- full adder c10, number 0
lv1_c10_FA_0: fullAdder
	port map (
		i0 => grid2(0)(10),
		i1 => grid2(1)(10),
		ci => grid2(2)(10),
		s => grid1(1)(10),
		co => grid1(0)(11) );

-- move the other elements of the column
grid1(2)(10) <= grid2(3)(10);

-----------------------------
-- COLUMN 11
-----------------------------
-- full adder c11, number 0
lv1_c11_FA_0: fullAdder
	port map (
		i0 => grid2(0)(11),
		i1 => grid2(1)(11),
		ci => grid2(2)(11),
		s => grid1(1)(11),
		co => grid1(0)(12) );

-- move the other elements of the column
grid1(2)(11) <= grid2(3)(11);

-----------------------------
-- COLUMN 12
-----------------------------
-- full adder c12, number 0
lv1_c12_FA_0: fullAdder
	port map (
		i0 => grid2(0)(12),
		i1 => grid2(1)(12),
		ci => grid2(2)(12),
		s => grid1(1)(12),
		co => grid1(0)(13) );

-- move the other elements of the column
grid1(2)(12) <= grid2(3)(12);

-----------------------------
-- COLUMN 13
-----------------------------
-- full adder c13, number 0
lv1_c13_FA_0: fullAdder
	port map (
		i0 => grid2(0)(13),
		i1 => grid2(1)(13),
		ci => grid2(2)(13),
		s => grid1(1)(13),
		co => grid1(0)(14) );

-- move the other elements of the column
grid1(2)(13) <= grid2(3)(13);

-----------------------------
-- COLUMN 14
-----------------------------
-- full adder c14, number 0
lv1_c14_FA_0: fullAdder
	port map (
		i0 => grid2(0)(14),
		i1 => grid2(1)(14),
		ci => grid2(2)(14),
		s => grid1(1)(14),
		co => grid1(0)(15) );

-- move the other elements of the column
grid1(2)(14) <= grid2(3)(14);

-----------------------------
-- COLUMN 15
-----------------------------
-- full adder c15, number 0
lv1_c15_FA_0: fullAdder
	port map (
		i0 => grid2(0)(15),
		i1 => grid2(1)(15),
		ci => grid2(2)(15),
		s => grid1(1)(15),
		co => grid1(0)(16) );

-- move the other elements of the column
grid1(2)(15) <= grid2(3)(15);

-----------------------------
-- COLUMN 16
-----------------------------
-- full adder c16, number 0
lv1_c16_FA_0: fullAdder
	port map (
		i0 => grid2(0)(16),
		i1 => grid2(1)(16),
		ci => grid2(2)(16),
		s => grid1(1)(16),
		co => grid1(0)(17) );

-- move the other elements of the column
grid1(2)(16) <= grid2(3)(16);

-----------------------------
-- COLUMN 17
-----------------------------
-- full adder c17, number 0
lv1_c17_FA_0: fullAdder
	port map (
		i0 => grid2(0)(17),
		i1 => grid2(1)(17),
		ci => grid2(2)(17),
		s => grid1(1)(17),
		co => grid1(0)(18) );

-- move the other elements of the column
grid1(2)(17) <= grid2(3)(17);

-----------------------------
-- COLUMN 18
-----------------------------
-- full adder c18, number 0
lv1_c18_FA_0: fullAdder
	port map (
		i0 => grid2(0)(18),
		i1 => grid2(1)(18),
		ci => grid2(2)(18),
		s => grid1(1)(18),
		co => grid1(0)(19) );

-- move the other elements of the column
grid1(2)(18) <= grid2(3)(18);

-----------------------------
-- COLUMN 19
-----------------------------
-- full adder c19, number 0
lv1_c19_FA_0: fullAdder
	port map (
		i0 => grid2(0)(19),
		i1 => grid2(1)(19),
		ci => grid2(2)(19),
		s => grid1(1)(19),
		co => grid1(0)(20) );

-- move the other elements of the column
grid1(2)(19) <= grid2(3)(19);

-----------------------------
-- COLUMN 20
-----------------------------
-- full adder c20, number 0
lv1_c20_FA_0: fullAdder
	port map (
		i0 => grid2(0)(20),
		i1 => grid2(1)(20),
		ci => grid2(2)(20),
		s => grid1(1)(20),
		co => grid1(0)(21) );

-- move the other elements of the column
grid1(2)(20) <= grid2(3)(20);

-----------------------------
-- COLUMN 21
-----------------------------
-- full adder c21, number 0
lv1_c21_FA_0: fullAdder
	port map (
		i0 => grid2(0)(21),
		i1 => grid2(1)(21),
		ci => grid2(2)(21),
		s => grid1(1)(21),
		co => grid1(0)(22) );

-- move the other elements of the column
grid1(2)(21) <= grid2(3)(21);

-----------------------------
-- COLUMN 22
-----------------------------
-- full adder c22, number 0
lv1_c22_FA_0: fullAdder
	port map (
		i0 => grid2(0)(22),
		i1 => grid2(1)(22),
		ci => grid2(2)(22),
		s => grid1(1)(22),
		co => grid1(0)(23) );

-- move the other elements of the column
grid1(2)(22) <= grid2(3)(22);

-----------------------------
-- COLUMN 23
-----------------------------
-- full adder c23, number 0
lv1_c23_FA_0: fullAdder
	port map (
		i0 => grid2(0)(23),
		i1 => grid2(1)(23),
		ci => grid2(2)(23),
		s => grid1(1)(23),
		co => grid1(0)(24) );

-- move the other elements of the column
grid1(2)(23) <= grid2(3)(23);

-----------------------------
-- COLUMN 24
-----------------------------
-- full adder c24, number 0
lv1_c24_FA_0: fullAdder
	port map (
		i0 => grid2(0)(24),
		i1 => grid2(1)(24),
		ci => grid2(2)(24),
		s => grid1(1)(24),
		co => grid1(0)(25) );

-- move the other elements of the column
grid1(2)(24) <= grid2(3)(24);

-----------------------------
-- COLUMN 25
-----------------------------
-- full adder c25, number 0
lv1_c25_FA_0: fullAdder
	port map (
		i0 => grid2(0)(25),
		i1 => grid2(1)(25),
		ci => grid2(2)(25),
		s => grid1(1)(25),
		co => grid1(0)(26) );

-- move the other elements of the column
grid1(2)(25) <= grid2(3)(25);

-----------------------------
-- COLUMN 26
-----------------------------
-- full adder c26, number 0
lv1_c26_FA_0: fullAdder
	port map (
		i0 => grid2(0)(26),
		i1 => grid2(1)(26),
		ci => grid2(2)(26),
		s => grid1(1)(26),
		co => grid1(0)(27) );

-- move the other elements of the column
grid1(2)(26) <= grid2(3)(26);

-----------------------------
-- COLUMN 27
-----------------------------
-- full adder c27, number 0
lv1_c27_FA_0: fullAdder
	port map (
		i0 => grid2(0)(27),
		i1 => grid2(1)(27),
		ci => grid2(2)(27),
		s => grid1(1)(27),
		co => grid1(0)(28) );

-- move the other elements of the column
grid1(2)(27) <= grid2(3)(27);

-----------------------------
-- COLUMN 28
-----------------------------
-- full adder c28, number 0
lv1_c28_FA_0: fullAdder
	port map (
		i0 => grid2(0)(28),
		i1 => grid2(1)(28),
		ci => grid2(2)(28),
		s => grid1(1)(28),
		co => grid1(0)(29) );

-- move the other elements of the column
grid1(2)(28) <= grid2(3)(28);

-----------------------------
-- COLUMN 29
-----------------------------
-- full adder c29, number 0
lv1_c29_FA_0: fullAdder
	port map (
		i0 => grid2(0)(29),
		i1 => grid2(1)(29),
		ci => grid2(2)(29),
		s => grid1(1)(29),
		co => grid1(0)(30) );

-- move the other elements of the column
grid1(2)(29) <= grid2(3)(29);

-----------------------------
-- COLUMN 30
-----------------------------
-- full adder c30, number 0
lv1_c30_FA_0: fullAdder
	port map (
		i0 => grid2(0)(30),
		i1 => grid2(1)(30),
		ci => grid2(2)(30),
		s => grid1(1)(30),
		co => grid1(0)(31) );

-- move the other elements of the column
grid1(2)(30) <= grid2(3)(30);

-----------------------------
-- COLUMN 31
-----------------------------
-- full adder c31, number 0
lv1_c31_FA_0: fullAdder
	port map (
		i0 => grid2(0)(31),
		i1 => grid2(1)(31),
		ci => grid2(2)(31),
		s => grid1(1)(31),
		co => grid1(0)(32) );

-- move the other elements of the column
grid1(2)(31) <= grid2(3)(31);

-----------------------------
-- COLUMN 32
-----------------------------
-- full adder c32, number 0
lv1_c32_FA_0: fullAdder
	port map (
		i0 => grid2(0)(32),
		i1 => grid2(1)(32),
		ci => grid2(2)(32),
		s => grid1(1)(32),
		co => grid1(0)(33) );

-- move the other elements of the column
grid1(2)(32) <= grid2(3)(32);

-----------------------------
-- COLUMN 33
-----------------------------
-- full adder c33, number 0
lv1_c33_FA_0: fullAdder
	port map (
		i0 => grid2(0)(33),
		i1 => grid2(1)(33),
		ci => grid2(2)(33),
		s => grid1(1)(33),
		co => grid1(0)(34) );

-- move the other elements of the column
grid1(2)(33) <= grid2(3)(33);

-----------------------------
-- COLUMN 34
-----------------------------
-- full adder c34, number 0
lv1_c34_FA_0: fullAdder
	port map (
		i0 => grid2(0)(34),
		i1 => grid2(1)(34),
		ci => grid2(2)(34),
		s => grid1(1)(34),
		co => grid1(0)(35) );

-- move the other elements of the column
grid1(2)(34) <= grid2(3)(34);

-----------------------------
-- COLUMN 35
-----------------------------
-- full adder c35, number 0
lv1_c35_FA_0: fullAdder
	port map (
		i0 => grid2(0)(35),
		i1 => grid2(1)(35),
		ci => grid2(2)(35),
		s => grid1(1)(35),
		co => grid1(0)(36) );

-- move the other elements of the column
grid1(2)(35) <= grid2(3)(35);

-----------------------------
-- COLUMN 36
-----------------------------
-- full adder c36, number 0
lv1_c36_FA_0: fullAdder
	port map (
		i0 => grid2(0)(36),
		i1 => grid2(1)(36),
		ci => grid2(2)(36),
		s => grid1(1)(36),
		co => grid1(0)(37) );

-- move the other elements of the column
grid1(2)(36) <= grid2(3)(36);

-----------------------------
-- COLUMN 37
-----------------------------
-- half adder c37, number 0
lv1_c37_HA_0: halfAdder
	port map (
		i0 => grid2(0)(37),
		i1 => grid2(1)(37),
		s => grid1(1)(37),
		co => grid1(0)(38) );

-- move the other elements of the column
grid1(2)(37) <= grid2(2)(37);

-----------------------------
-- COLUMN 38
-----------------------------
-- move the other elements of the column
grid1(1)(38) <= grid2(0)(38);
grid1(2)(38) <= grid2(1)(38);

-----------------------------
-- COLUMN 39
-----------------------------
-- move the other elements of the column
grid1(0)(39) <= grid2(0)(39);
grid1(1)(39) <= grid2(1)(39);

-----------------------------
-- DADDA TREE LEVEL0
-----------------------------

-----------------------------
-- COLUMN 0
-----------------------------
-- half adder c0, number 0
lv0_c0_HA_0: halfAdder
	port map (
		i0 => grid1(0)(0),
		i1 => grid1(1)(0),
		s => grid0(0)(0),
		co => grid0(0)(1) );

-- move the other elements of the column
grid0(1)(0) <= grid1(2)(0);

-----------------------------
-- COLUMN 1
-----------------------------
-- full adder c1, number 0
lv0_c1_FA_0: fullAdder
	port map (
		i0 => grid1(0)(1),
		i1 => grid1(1)(1),
		ci => grid1(2)(1),
		s => grid0(1)(1),
		co => grid0(0)(2) );

-- move the other elements of the column

-----------------------------
-- COLUMN 2
-----------------------------
-- full adder c2, number 0
lv0_c2_FA_0: fullAdder
	port map (
		i0 => grid1(0)(2),
		i1 => grid1(1)(2),
		ci => grid1(2)(2),
		s => grid0(1)(2),
		co => grid0(0)(3) );

-- move the other elements of the column

-----------------------------
-- COLUMN 3
-----------------------------
-- full adder c3, number 0
lv0_c3_FA_0: fullAdder
	port map (
		i0 => grid1(0)(3),
		i1 => grid1(1)(3),
		ci => grid1(2)(3),
		s => grid0(1)(3),
		co => grid0(0)(4) );

-- move the other elements of the column

-----------------------------
-- COLUMN 4
-----------------------------
-- full adder c4, number 0
lv0_c4_FA_0: fullAdder
	port map (
		i0 => grid1(0)(4),
		i1 => grid1(1)(4),
		ci => grid1(2)(4),
		s => grid0(1)(4),
		co => grid0(0)(5) );

-- move the other elements of the column

-----------------------------
-- COLUMN 5
-----------------------------
-- full adder c5, number 0
lv0_c5_FA_0: fullAdder
	port map (
		i0 => grid1(0)(5),
		i1 => grid1(1)(5),
		ci => grid1(2)(5),
		s => grid0(1)(5),
		co => grid0(0)(6) );

-- move the other elements of the column

-----------------------------
-- COLUMN 6
-----------------------------
-- full adder c6, number 0
lv0_c6_FA_0: fullAdder
	port map (
		i0 => grid1(0)(6),
		i1 => grid1(1)(6),
		ci => grid1(2)(6),
		s => grid0(1)(6),
		co => grid0(0)(7) );

-- move the other elements of the column

-----------------------------
-- COLUMN 7
-----------------------------
-- full adder c7, number 0
lv0_c7_FA_0: fullAdder
	port map (
		i0 => grid1(0)(7),
		i1 => grid1(1)(7),
		ci => grid1(2)(7),
		s => grid0(1)(7),
		co => grid0(0)(8) );

-- move the other elements of the column

-----------------------------
-- COLUMN 8
-----------------------------
-- full adder c8, number 0
lv0_c8_FA_0: fullAdder
	port map (
		i0 => grid1(0)(8),
		i1 => grid1(1)(8),
		ci => grid1(2)(8),
		s => grid0(1)(8),
		co => grid0(0)(9) );

-- move the other elements of the column

-----------------------------
-- COLUMN 9
-----------------------------
-- full adder c9, number 0
lv0_c9_FA_0: fullAdder
	port map (
		i0 => grid1(0)(9),
		i1 => grid1(1)(9),
		ci => grid1(2)(9),
		s => grid0(1)(9),
		co => grid0(0)(10) );

-- move the other elements of the column

-----------------------------
-- COLUMN 10
-----------------------------
-- full adder c10, number 0
lv0_c10_FA_0: fullAdder
	port map (
		i0 => grid1(0)(10),
		i1 => grid1(1)(10),
		ci => grid1(2)(10),
		s => grid0(1)(10),
		co => grid0(0)(11) );

-- move the other elements of the column

-----------------------------
-- COLUMN 11
-----------------------------
-- full adder c11, number 0
lv0_c11_FA_0: fullAdder
	port map (
		i0 => grid1(0)(11),
		i1 => grid1(1)(11),
		ci => grid1(2)(11),
		s => grid0(1)(11),
		co => grid0(0)(12) );

-- move the other elements of the column

-----------------------------
-- COLUMN 12
-----------------------------
-- full adder c12, number 0
lv0_c12_FA_0: fullAdder
	port map (
		i0 => grid1(0)(12),
		i1 => grid1(1)(12),
		ci => grid1(2)(12),
		s => grid0(1)(12),
		co => grid0(0)(13) );

-- move the other elements of the column

-----------------------------
-- COLUMN 13
-----------------------------
-- full adder c13, number 0
lv0_c13_FA_0: fullAdder
	port map (
		i0 => grid1(0)(13),
		i1 => grid1(1)(13),
		ci => grid1(2)(13),
		s => grid0(1)(13),
		co => grid0(0)(14) );

-- move the other elements of the column

-----------------------------
-- COLUMN 14
-----------------------------
-- full adder c14, number 0
lv0_c14_FA_0: fullAdder
	port map (
		i0 => grid1(0)(14),
		i1 => grid1(1)(14),
		ci => grid1(2)(14),
		s => grid0(1)(14),
		co => grid0(0)(15) );

-- move the other elements of the column

-----------------------------
-- COLUMN 15
-----------------------------
-- full adder c15, number 0
lv0_c15_FA_0: fullAdder
	port map (
		i0 => grid1(0)(15),
		i1 => grid1(1)(15),
		ci => grid1(2)(15),
		s => grid0(1)(15),
		co => grid0(0)(16) );

-- move the other elements of the column

-----------------------------
-- COLUMN 16
-----------------------------
-- full adder c16, number 0
lv0_c16_FA_0: fullAdder
	port map (
		i0 => grid1(0)(16),
		i1 => grid1(1)(16),
		ci => grid1(2)(16),
		s => grid0(1)(16),
		co => grid0(0)(17) );

-- move the other elements of the column

-----------------------------
-- COLUMN 17
-----------------------------
-- full adder c17, number 0
lv0_c17_FA_0: fullAdder
	port map (
		i0 => grid1(0)(17),
		i1 => grid1(1)(17),
		ci => grid1(2)(17),
		s => grid0(1)(17),
		co => grid0(0)(18) );

-- move the other elements of the column

-----------------------------
-- COLUMN 18
-----------------------------
-- full adder c18, number 0
lv0_c18_FA_0: fullAdder
	port map (
		i0 => grid1(0)(18),
		i1 => grid1(1)(18),
		ci => grid1(2)(18),
		s => grid0(1)(18),
		co => grid0(0)(19) );

-- move the other elements of the column

-----------------------------
-- COLUMN 19
-----------------------------
-- full adder c19, number 0
lv0_c19_FA_0: fullAdder
	port map (
		i0 => grid1(0)(19),
		i1 => grid1(1)(19),
		ci => grid1(2)(19),
		s => grid0(1)(19),
		co => grid0(0)(20) );

-- move the other elements of the column

-----------------------------
-- COLUMN 20
-----------------------------
-- full adder c20, number 0
lv0_c20_FA_0: fullAdder
	port map (
		i0 => grid1(0)(20),
		i1 => grid1(1)(20),
		ci => grid1(2)(20),
		s => grid0(1)(20),
		co => grid0(0)(21) );

-- move the other elements of the column

-----------------------------
-- COLUMN 21
-----------------------------
-- full adder c21, number 0
lv0_c21_FA_0: fullAdder
	port map (
		i0 => grid1(0)(21),
		i1 => grid1(1)(21),
		ci => grid1(2)(21),
		s => grid0(1)(21),
		co => grid0(0)(22) );

-- move the other elements of the column

-----------------------------
-- COLUMN 22
-----------------------------
-- full adder c22, number 0
lv0_c22_FA_0: fullAdder
	port map (
		i0 => grid1(0)(22),
		i1 => grid1(1)(22),
		ci => grid1(2)(22),
		s => grid0(1)(22),
		co => grid0(0)(23) );

-- move the other elements of the column

-----------------------------
-- COLUMN 23
-----------------------------
-- full adder c23, number 0
lv0_c23_FA_0: fullAdder
	port map (
		i0 => grid1(0)(23),
		i1 => grid1(1)(23),
		ci => grid1(2)(23),
		s => grid0(1)(23),
		co => grid0(0)(24) );

-- move the other elements of the column

-----------------------------
-- COLUMN 24
-----------------------------
-- full adder c24, number 0
lv0_c24_FA_0: fullAdder
	port map (
		i0 => grid1(0)(24),
		i1 => grid1(1)(24),
		ci => grid1(2)(24),
		s => grid0(1)(24),
		co => grid0(0)(25) );

-- move the other elements of the column

-----------------------------
-- COLUMN 25
-----------------------------
-- full adder c25, number 0
lv0_c25_FA_0: fullAdder
	port map (
		i0 => grid1(0)(25),
		i1 => grid1(1)(25),
		ci => grid1(2)(25),
		s => grid0(1)(25),
		co => grid0(0)(26) );

-- move the other elements of the column

-----------------------------
-- COLUMN 26
-----------------------------
-- full adder c26, number 0
lv0_c26_FA_0: fullAdder
	port map (
		i0 => grid1(0)(26),
		i1 => grid1(1)(26),
		ci => grid1(2)(26),
		s => grid0(1)(26),
		co => grid0(0)(27) );

-- move the other elements of the column

-----------------------------
-- COLUMN 27
-----------------------------
-- full adder c27, number 0
lv0_c27_FA_0: fullAdder
	port map (
		i0 => grid1(0)(27),
		i1 => grid1(1)(27),
		ci => grid1(2)(27),
		s => grid0(1)(27),
		co => grid0(0)(28) );

-- move the other elements of the column

-----------------------------
-- COLUMN 28
-----------------------------
-- full adder c28, number 0
lv0_c28_FA_0: fullAdder
	port map (
		i0 => grid1(0)(28),
		i1 => grid1(1)(28),
		ci => grid1(2)(28),
		s => grid0(1)(28),
		co => grid0(0)(29) );

-- move the other elements of the column

-----------------------------
-- COLUMN 29
-----------------------------
-- full adder c29, number 0
lv0_c29_FA_0: fullAdder
	port map (
		i0 => grid1(0)(29),
		i1 => grid1(1)(29),
		ci => grid1(2)(29),
		s => grid0(1)(29),
		co => grid0(0)(30) );

-- move the other elements of the column

-----------------------------
-- COLUMN 30
-----------------------------
-- full adder c30, number 0
lv0_c30_FA_0: fullAdder
	port map (
		i0 => grid1(0)(30),
		i1 => grid1(1)(30),
		ci => grid1(2)(30),
		s => grid0(1)(30),
		co => grid0(0)(31) );

-- move the other elements of the column

-----------------------------
-- COLUMN 31
-----------------------------
-- full adder c31, number 0
lv0_c31_FA_0: fullAdder
	port map (
		i0 => grid1(0)(31),
		i1 => grid1(1)(31),
		ci => grid1(2)(31),
		s => grid0(1)(31),
		co => grid0(0)(32) );

-- move the other elements of the column

-----------------------------
-- COLUMN 32
-----------------------------
-- full adder c32, number 0
lv0_c32_FA_0: fullAdder
	port map (
		i0 => grid1(0)(32),
		i1 => grid1(1)(32),
		ci => grid1(2)(32),
		s => grid0(1)(32),
		co => grid0(0)(33) );

-- move the other elements of the column

-----------------------------
-- COLUMN 33
-----------------------------
-- full adder c33, number 0
lv0_c33_FA_0: fullAdder
	port map (
		i0 => grid1(0)(33),
		i1 => grid1(1)(33),
		ci => grid1(2)(33),
		s => grid0(1)(33),
		co => grid0(0)(34) );

-- move the other elements of the column

-----------------------------
-- COLUMN 34
-----------------------------
-- full adder c34, number 0
lv0_c34_FA_0: fullAdder
	port map (
		i0 => grid1(0)(34),
		i1 => grid1(1)(34),
		ci => grid1(2)(34),
		s => grid0(1)(34),
		co => grid0(0)(35) );

-- move the other elements of the column

-----------------------------
-- COLUMN 35
-----------------------------
-- full adder c35, number 0
lv0_c35_FA_0: fullAdder
	port map (
		i0 => grid1(0)(35),
		i1 => grid1(1)(35),
		ci => grid1(2)(35),
		s => grid0(1)(35),
		co => grid0(0)(36) );

-- move the other elements of the column

-----------------------------
-- COLUMN 36
-----------------------------
-- full adder c36, number 0
lv0_c36_FA_0: fullAdder
	port map (
		i0 => grid1(0)(36),
		i1 => grid1(1)(36),
		ci => grid1(2)(36),
		s => grid0(1)(36),
		co => grid0(0)(37) );

-- move the other elements of the column

-----------------------------
-- COLUMN 37
-----------------------------
-- full adder c37, number 0
lv0_c37_FA_0: fullAdder
	port map (
		i0 => grid1(0)(37),
		i1 => grid1(1)(37),
		ci => grid1(2)(37),
		s => grid0(1)(37),
		co => grid0(0)(38) );

-- move the other elements of the column

-----------------------------
-- COLUMN 38
-----------------------------
-- full adder c38, number 0
lv0_c38_FA_0: fullAdder
	port map (
		i0 => grid1(0)(38),
		i1 => grid1(1)(38),
		ci => grid1(2)(38),
		s => grid0(1)(38),
		co => grid0(0)(39) );

-- move the other elements of the column

-----------------------------
-- COLUMN 39
-----------------------------
-- half adder c39, number 0
lv0_c39_HA_0: halfAdder
	port map (
		i0 => grid1(0)(39),
		i1 => grid1(1)(39),
		s => grid0(1)(39),
		co => open );

-- move the other elements of the column

--grid0(1)(1) <= '0';

-- last two levels
add0 <= grid0(0)(40-1 downto 0);
add1 <= grid0(1)(40-1 downto 0);

-- fast adder to be implemented
add0s<=signed(add0);
add1s<=signed(add1);
sum <= (add0s+add1s);

-- truncation step
product <= std_logic_vector(sum(40 downto (40-WL+1)));

end architecture;
