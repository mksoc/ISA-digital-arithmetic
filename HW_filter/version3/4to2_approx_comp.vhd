-- file '4to2_approx_comp.vhd'
-- approximate 4 to 2 compressor proposed by Yin
-- 1 positive error and 7 negative errors
-- out of 16 output combinations
library ieee;
use ieee.std_logic_1164.all;

entity 4to2_approx_comp is
  port (
    input: in std_logic_vector(3 downto 0);
    output: out std_logic_vector(1 downto 0)
  ) ;
end 4to2_approx_comp;

architecture structure of 4to2_approx_comp is
begin
    -- 'sum' bit
    output(0) <= not(input(3) xor input(2));

    -- 'carry' bit
    output(1) <= not(not(input(0) or input(1)) or not(input(2) or input(3)));
end structure ; -- structure