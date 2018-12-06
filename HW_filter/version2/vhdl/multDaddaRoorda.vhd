library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.multV2_pkg.all;

constant approximate_bits: positive :=6;

entity multDaddaRoorda is
  generic (N: positive :=WL)
  port (
    multiplier:     in std_logic_vector (N-1 downto 0);
    multiplicand:   in std_logic_vector (N-1 downto 0);
    product:        out std_logic_vector (N-1 downto 0)
  );
end entity;

architecture struct of multDaddaRoorda is

--Signals for MBE block
  recode_bits0: std_logic_vector (2 downto 0);
  inv         : std_logic_vector (numPartProd-1 downto 0);
  last_pp     : std_logic_vector (N downto 0);
  signal grid5,pps,pps1	  : aidGrid5;
  signal grid4		        : aidGrid4;
  signal grid3		        : aidGrid3;
  signal grid2		        : aidGrid2;
  signal grid1		        : aidGrid1;
  signal grid0		        : aidGrid0;

begin
--MBE partial product generation
  --Partial Product 0
  recode_bits0<=multiplier(1 downto 0) & '0';
  mbe0 : r4mbePP_processing
  generic map (
              N             =>    multiplicand'length)
  port map    (
              multiplicand  =>    multiplicand,
              recode_bits   =>    recode_bits0,
              inv           =>    inv(0),
              part_prod     =>    pps(0)(N downto 0));
  --Partial Product 11
  mbe11 : r4mbePP_processing
  generic map (
              N             =>    multiplicand'length)
  port map    (
              multiplicand  =>    multiplicand,
              recode_bits   =>    multiplier((multiplier'length-1) downto (multiplier'length-1)-3),
              inv           =>    inv(inv'length),
              part_prod     =>    last_pp;
  --Manual assignment in order to drop the MSbit
  pps(11)((WL_INT+2*WL_FRAC)-1 downto (WL_INT+2*WL_FRAC)-1-last_pp'length-1)<=last_pp(last_pp'length-2 downto 0);
  --Generate all the other Partial Products
  GEN_MBE_PROCESSING:
  for I in 1 to 10 generate
      mbeX : r4mbePP_processing
      generic map (
                  N             =>    multiplicand'length)
      port map    (
                  multiplicand  =>    multiplicand,
                  recode_bits   =>    multiplier(2*I+1 downto 2*I-1),
                  inv           =>    inv(I),
                  part_prod     =>    pps(I)((WL+I*2) downto I*2));
  end generate;

-- Roorda's approach correction + adjust for Dadda tree automathic generated VHDL

  --Roorda corrections. Sign bit will be inverted after justification
  --First line
  pps(0)(25)<=pps(0)(24);
  pps(0)(26)<=not(pps(0)(25));
  --Connecting '1' at the end of each partial product form 1 to 10
  ROORDA_CORRECTION:
  for I in 1 to 10 generate
      pps(I)(WL+2*I+1)<='1';
  end generate;

  --Justifing
  --odd 39 to 21 cols
  C39_to_21_ODD:
  for J in 11 downto 2 generate
      pps1(J-1 downto 0)(40-(((J-2)*2)+1))<=pps(11 downto 11-J+1)(46-(((J-2)*2)+1));
  end generate;

  --even 39 to 21 cols
  C39_to_21_EVEN:
  for J in 10 downto 2 generate
      pps1(J-1 downto 0)(40-(((J-2)*2)+2))<=pps(11 downto 11-J+1)(46-(((J-2)*2)+2));
  end generate;

  --from 20 to 17 cols
  C20_to_17:
  for I in 20 downto 17 generate
      pps1(11 downto 0)(I)<=pps(11 downto 0)(I+6);
  end generate;

  --col 16
  pps1(12 downto 0)(16)<=pps(12 downto 0)(16+6);

  -- from 15 to 0 even
  C15_to_0_EVEN:
  for J in 11 downto 4 generate
      pps1(J downto 0)(2*(J-4))<=pps(J downto 0)(2*(J-4)+6);
  end generate;

  --from 15 to 0 odd
  C15_to_0_ODD:
  for J in 11 downto 4 generate
      pps1(J-1 downto 0)(2*(J-4)+1)<=pps(J-1 downto 0)(2*(J-4)+6+1);
  end generate

  --Roorda correction of sign bits
  --Connecting inv to the matrix
  INV_CONNECTION:
  for I in 4 to 12 generate
      grid5(I)((I-4)*2)<=inv(I-1);
  end generate;

  --move form 15 downto 0 even
  M
