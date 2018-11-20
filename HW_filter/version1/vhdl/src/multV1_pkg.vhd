library ieee;
use ieee.std_logic_1164.all;

package multV1_pkg is

constant numPartProd: positive := 12;
constant daddaLev4: positive := 9;
constant daddaLev3: positive := 6;
constant daddaLev2: positive := 4;
constant daddaLev1: positive := 3;
constant daddaLev0: positive := 2;

constant WL: positive := 24;
constant WL_INT: positive := 2;
constant WL_FRAC: positive := 22;

type aidGridPreprocessedPP is array(numPartProd-1 downto 0) of std_logic_vector(WL downto 0);
type aidGrid5 is array(numPartProd downto 0) of std_logic_vector((WL_INT+2*WL_FRAC)-1 downto 0);
type aidGrid4 is array(daddaLev4-1 downto 0) of std_logic_vector((WL_INT+2*WL_FRAC)-1 downto 0);
type aidGrid3 is array(daddaLev3-1 downto 0) of std_logic_vector((WL_INT+2*WL_FRAC)-1 downto 0);
type aidGrid2 is array(daddaLev2-1 downto 0) of std_logic_vector((WL_INT+2*WL_FRAC)-1 downto 0);
type aidGrid1 is array(daddaLev1-1 downto 0) of std_logic_vector((WL_INT+2*WL_FRAC)-1 downto 0);
type aidGrid0 is array(daddaLev0-1 downto 0) of std_logic_vector((WL_INT+2*WL_FRAC)-1 downto 0);

end package multV1_pkg;