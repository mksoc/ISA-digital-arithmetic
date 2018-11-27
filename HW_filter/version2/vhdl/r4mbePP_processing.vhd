library ieee;
use ieee.std_logic_1164.all;

entity r4mbePP_processing is
  generic (N: positive :=8);
  port(
    multiplicand : in std_logic_vector(N-1 downto 0);
    recode_bits  : in std_logic_vector(2 downto 0);
    inv          : out std_logic;
    part_prod    : out std_logic_vector(N downto 0)
  );
end entity;

architecture beha of r4mbePP_processing is
begin
  part_prod<= (others=>'0')                                       when recode_bits="000" or recode_bits="111" else
              multiplicand(N-1) & multiplicand(N-1 downto 0)      when recode_bits="001" or recode_bits="010" else
              multiplicand(N-1 downto 0) & '0'                    when recode_bits="011" else
              not(multiplicand(N-1) & multiplicand(N-1 downto 0)) when recode_bits="110" or recode_bits="101" else
              not(multiplicand(N-1 downto 0) & '0')               when recode_bits="100";
  inv<= '0' when recode_bits="000" or recode_bits="111" or recode_bits="001" or recode_bits="010" or recode_bits="011" else
        '1';
end architecture;