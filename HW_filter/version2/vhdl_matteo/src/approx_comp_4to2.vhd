-- approximate 4 to 2 compressor proposed by Yin
-- 1 positive error and 7 negative errors
-- out of 16 output combinations
library ieee;
use ieee.std_logic_1164.all;

entity approx_comp_4to2 is
    port (
        i0, i1, i2, i3: in std_logic;
        out0, out1: out std_logic ) ;
end approx_comp_4to2;

architecture structure of approx_comp_4to2 is
begin
    -- 'sum' bit
    out0 <= not(i3 xor i2);

    -- 'carry' bit
    out1 <= not(not(i0 or i1) or not(i2 or i3));
end structure ; -- structure